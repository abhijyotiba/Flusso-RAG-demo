"""
Flask API Server for Flusso RAG Demo
Provides REST API endpoints for querying the knowledge base
"""
import os
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from query_engine import FlussoQueryEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAvSB3HkGc7gN0nT4EbJU6NZzvL7FMxg_I')
STORE_ID = os.getenv('STORE_ID', 'fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh')
FRONTEND_PATH = Path(__file__).parent.parent / 'frontend'

# Initialize query engine
query_engine = None
try:
    query_engine = FlussoQueryEngine(api_key=API_KEY, store_id=STORE_ID)
    logger.info("✓ Flask app initialized with query engine")
except Exception as e:
    logger.error(f"Failed to initialize query engine: {e}")
    logger.error("API will return errors until this is fixed")


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory(FRONTEND_PATH, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory(FRONTEND_PATH, filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'query_engine_ready': query_engine is not None,
        'store_id': STORE_ID,
        'model': query_engine.model_name if query_engine else None
    })


@app.route('/api/query', methods=['POST'])
def api_query():
    """
    Process a user query
    
    Request body:
    {
        "query": "user question",
        "temperature": 0.3 (optional),
        "top_p": 0.9 (optional)
    }
    
    Response:
    {
        "success": true/false,
        "query": "original query",
        "answer": "AI response",
        "sources": [...],
        "source_count": N,
        "metadata": {...}
    }
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized. Check server logs.'
        }), 500
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract query
        user_query = data.get('query', '').strip()
        if not user_query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        # Extract optional parameters
        temperature = data.get('temperature')
        top_p = data.get('top_p')
        
        # Validate parameters if provided
        if temperature is not None:
            try:
                temperature = float(temperature)
                if not 0.0 <= temperature <= 1.0:
                    raise ValueError()
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'error': 'Temperature must be a number between 0.0 and 1.0'
                }), 400
        
        if top_p is not None:
            try:
                top_p = float(top_p)
                if not 0.0 <= top_p <= 1.0:
                    raise ValueError()
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'error': 'Top_p must be a number between 0.0 and 1.0'
                }), 400
        
        # Process query
        logger.info(f"API Query received: {user_query[:100]}...")
        result = query_engine.query(
            user_query=user_query,
            temperature=temperature,
            top_p=top_p
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing API query: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/product/<product_code>', methods=['GET'])
def api_product_info(product_code):
    """
    Get information for a specific product
    
    Parameters:
        product_code: Product code (e.g., "100.1000")
    
    Response: Same as /api/query
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized'
        }), 500
    
    try:
        logger.info(f"API Product info request: {product_code}")
        result = query_engine.get_product_info(product_code)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting product info: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/compare', methods=['POST'])
def api_compare_products():
    """
    Compare multiple products
    
    Request body:
    {
        "products": ["100.1000", "160.1000", ...]
    }
    
    Response: Same as /api/query
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized'
        }), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        product_codes = data.get('products', [])
        
        if not isinstance(product_codes, list):
            return jsonify({
                'success': False,
                'error': 'Products must be a list'
            }), 400
        
        if len(product_codes) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 products required for comparison'
            }), 400
        
        logger.info(f"API Compare request: {', '.join(product_codes)}")
        result = query_engine.compare_products(product_codes)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error comparing products: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/search', methods=['POST'])
def api_search_by_features():
    """
    Search for products by features
    
    Request body:
    {
        "category": "kitchen faucet",
        "features": ["pull-down", "matte black", ...]
    }
    
    Response: Same as /api/query
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized'
        }), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        category = data.get('category', '').strip()
        features = data.get('features', [])
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'Category is required'
            }), 400
        
        if not features or not isinstance(features, list):
            return jsonify({
                'success': False,
                'error': 'Features must be a non-empty list'
            }), 400
        
        logger.info(f"API Search request: {category} - {', '.join(features)}")
        result = query_engine.search_by_features(category, features)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error searching by features: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/installation/<product_code>', methods=['GET'])
def api_installation_guide(product_code):
    """
    Get installation guide for a product
    
    Parameters:
        product_code: Product code
    
    Response: Same as /api/query
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized'
        }), 500
    
    try:
        logger.info(f"API Installation guide request: {product_code}")
        result = query_engine.get_installation_guide(product_code)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting installation guide: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/parts/<product_code>', methods=['GET'])
def api_parts_info(product_code):
    """
    Get parts information for a product
    
    Parameters:
        product_code: Product code
    
    Response: Same as /api/query
    """
    if not query_engine:
        return jsonify({
            'success': False,
            'error': 'Query engine not initialized'
        }), 500
    
    try:
        logger.info(f"API Parts info request: {product_code}")
        result = query_engine.get_parts_info(product_code)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting parts info: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# Main
# ============================================================================

def main():
    """Start the Flask application"""
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info("=" * 70)
    logger.info("Flusso RAG Demo - Starting Server")
    logger.info("=" * 70)
    logger.info(f"Server URL: http://localhost:{port}")
    logger.info(f"Frontend: {FRONTEND_PATH}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Store ID: {STORE_ID}")
    logger.info("=" * 70)
    
    # For production (Render), gunicorn will handle the server
    # This is only for local development
    if os.getenv('RENDER'):
        logger.info("Running in production mode with gunicorn")
    else:
        app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()
