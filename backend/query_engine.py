"""
RAG Query Engine for Flusso Knowledge Base
Handles queries to Gemini API using File Search with the knowledge base store
"""
import os
import logging
from typing import Dict, List, Optional
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FlussoQueryEngine:
    """
    Query engine for Flusso product knowledge base using Gemini API with File Search
    """
    
    def __init__(self, api_key: str, store_id: str):
        """
        Initialize the query engine
        
        Args:
            api_key: Google Gemini API key
            store_id: File Search store ID (e.g., fileSearchStores/...)
        """
        if not api_key:
            raise ValueError("API key is required")
        if not store_id:
            raise ValueError("Store ID is required")
        
        self.api_key = api_key
        self.store_id = store_id
        
        # Initialize Gemini client
        try:
            self.client = genai.Client(api_key=api_key)
            logger.info("✓ Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
        
        # Model configuration
        self.model_name = 'gemini-2.5-flash'
        self.default_temperature = 0.2
        self.default_top_p = 0.8
        
        logger.info(f"✓ Query engine initialized")
        logger.info(f"  Model: {self.model_name}")
        logger.info(f"  Store ID: {self.store_id}")
    
    def _build_system_instruction(self) -> str:
        """Build comprehensive system instruction for the AI"""
        return """You are an expert assistant for Flusso Faucets, a premium plumbing fixtures company. Your role is to help users find information about Flusso products, including specifications, installation instructions, parts diagrams, and product details.

**Your Responsibilities:**
1. Provide accurate, detailed information about Flusso products
2. Help users find specific product specifications and features
3. Explain installation procedures and requirements
4. Identify parts and their functions from diagrams
5. Compare products when requested
6. Recommend products based on user requirements

**Guidelines:**
- Always cite specific product codes when referring to products
- Provide exact specifications from the knowledge base
- If information is not available, clearly state that
- For installation questions, reference official installation guides
- For parts questions, refer to parts diagrams when available
- Be professional, clear, and concise
- Format responses for easy readability
- When comparing products, create clear comparison tables

**Response Format:**
- Use markdown formatting for better readability
- Use bullet points for lists
- Use tables for comparisons
- Bold important product codes and specifications
- Include relevant measurements with units

**Important:**
- Only provide information from the knowledge base
- Don't make assumptions about products not in the database
- If unsure, ask for clarification rather than guessing"""
    
    def query(
        self,
        user_query: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Process a user query and return results
        
        Args:
            user_query: The user's question
            temperature: Model temperature (0.0-1.0), default 0.3
            top_p: Top-p sampling parameter, default 0.9
            max_tokens: Maximum tokens in response, default None (model default)
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        if not user_query or not user_query.strip():
            raise ValueError("Query cannot be empty")
        
        logger.info(f"Processing query: {user_query[:100]}...")
        
        # Use provided parameters or defaults
        temp = temperature if temperature is not None else self.default_temperature
        top_p_val = top_p if top_p is not None else self.default_top_p
        
        try:
            # Build the prompt with system instruction embedded
            full_prompt = f"""{self._build_system_instruction()}

User Query: {user_query}"""
            
            # Generate response using File Search (following official documentation pattern)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[self.store_id]
                        )
                    )],
                    temperature=temp,
                    top_p=top_p_val,
                )
            )
            
            # Extract answer text
            answer = response.text if response.text else "No response generated"
            
            # Extract sources from grounding metadata
            sources = []
            grounding_metadata = None
            
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                grounding_metadata = candidate.grounding_metadata
                
                if grounding_metadata and grounding_metadata.grounding_chunks:
                    # Extract unique source titles
                    seen_sources = set()
                    for chunk in grounding_metadata.grounding_chunks:
                        if hasattr(chunk, 'retrieved_context'):
                            source_title = chunk.retrieved_context.title
                            if source_title and source_title not in seen_sources:
                                sources.append({
                                    'title': source_title,
                                    'uri': getattr(chunk.retrieved_context, 'uri', None)
                                })
                                seen_sources.add(source_title)
            
            logger.info(f"✓ Query processed successfully, {len(sources)} sources found")
            
            return {
                'success': True,
                'query': user_query,
                'answer': answer,
                'sources': sources,
                'source_count': len(sources),
                'metadata': {
                    'model': self.model_name,
                    'temperature': temp,
                    'top_p': top_p_val,
                    'has_grounding': grounding_metadata is not None
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            return {
                'success': False,
                'query': user_query,
                'answer': None,
                'error': str(e),
                'sources': [],
                'source_count': 0
            }
    
    def get_product_info(self, product_code: str) -> Dict:
        """
        Get comprehensive information about a specific product
        
        Args:
            product_code: Product code (e.g., "100.1000", "TVH.2691")
            
        Returns:
            Query result dictionary
        """
        query = f"Provide comprehensive information about product {product_code}, including specifications, features, available finishes, and any installation requirements."
        return self.query(query)
    
    def compare_products(self, product_codes: List[str]) -> Dict:
        """
        Compare multiple products
        
        Args:
            product_codes: List of product codes to compare
            
        Returns:
            Query result dictionary
        """
        if len(product_codes) < 2:
            raise ValueError("At least 2 products required for comparison")
        
        codes_str = ", ".join(product_codes)
        query = f"Create a detailed comparison of these products: {codes_str}. Include specifications, features, finishes, dimensions, and key differences. Present the information in a table format."
        return self.query(query)
    
    def search_by_features(self, category: str, features: List[str]) -> Dict:
        """
        Search for products by category and features
        
        Args:
            category: Product category (e.g., "kitchen faucet", "shower system")
            features: List of desired features
            
        Returns:
            Query result dictionary
        """
        features_str = ", ".join(features)
        query = f"Find all {category} products that have these features: {features_str}. List the products with their codes and brief descriptions."
        return self.query(query)
    
    def get_installation_guide(self, product_code: str) -> Dict:
        """
        Get installation instructions for a product
        
        Args:
            product_code: Product code
            
        Returns:
            Query result dictionary
        """
        query = f"Provide detailed installation instructions for product {product_code}, including required tools, steps, and any important warnings."
        return self.query(query)
    
    def get_parts_info(self, product_code: str) -> Dict:
        """
        Get parts and assembly information for a product
        
        Args:
            product_code: Product code
            
        Returns:
            Query result dictionary
        """
        query = f"Show the parts list and assembly diagram information for product {product_code}. List all parts with their numbers and descriptions."
        return self.query(query)


def main():
    """Test the query engine"""
    import sys
    
    # Get API key and store ID from environment or command line
    api_key = os.getenv('GEMINI_API_KEY')
    store_id = os.getenv('STORE_ID', 'fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh')
    
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize engine
    engine = FlussoQueryEngine(api_key=api_key, store_id=store_id)
    
    # Test queries
    test_queries = [
        "What products does Flusso offer?",
        "Tell me about product 100.1000",
        "What finishes are available for kitchen faucets?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print('='*70)
        
        result = engine.query(query)
        
        if result['success']:
            print(f"\nAnswer:\n{result['answer']}\n")
            if result['sources']:
                print(f"Sources ({result['source_count']}):")
                for i, source in enumerate(result['sources'][:5], 1):
                    print(f"  {i}. {source['title']}")
        else:
            print(f"\nError: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
