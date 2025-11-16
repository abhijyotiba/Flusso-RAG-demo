# Flusso Knowledge Base RAG Demo

A professional RAG (Retrieval-Augmented Generation) demonstration application for querying the Flusso product knowledge base using Google Gemini AI with File Search capabilities.

## 🚀 Features

- **Advanced RAG System**: Leverages Google Gemini 2.0 Flash with File Search for accurate product information retrieval
- **Professional UI**: Clean, modern, responsive frontend with excellent UX
- **Comprehensive API**: RESTful API with multiple endpoints for different query types
- **Smart Formatting**: Automatic markdown formatting and structured response display
- **Source Citations**: Displays grounding sources for transparency and verification
- **Error Handling**: Robust error handling throughout the application
- **Real-time Status**: Health check and system status monitoring

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Access to Flusso File Search store

## 🛠️ Installation

### 1. Clone or Navigate to the Project

```bash
cd rag_demo
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

The `.env` file is already configured with:
- Gemini API Key: `AIzaSyAvSB3HkGc7gN0nT4EbJU6NZzvL7FMxg_I`
- Store ID: `fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh`

You can modify these values in the `.env` file if needed.

## 🎯 Usage

### Start the Server

#### Using the Startup Script (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### Manual Start

```bash
cd backend
python app.py
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📡 API Endpoints

### Health Check
```
GET /api/health
```
Returns system status and configuration.

### Query
```
POST /api/query
Content-Type: application/json

{
    "query": "Your question here",
    "temperature": 0.3,  // optional
    "top_p": 0.9        // optional
}
```

### Product Information
```
GET /api/product/<product_code>
```
Get comprehensive information about a specific product.

### Compare Products
```
POST /api/compare
Content-Type: application/json

{
    "products": ["100.1000", "160.1000"]
}
```

### Search by Features
```
POST /api/search
Content-Type: application/json

{
    "category": "kitchen faucet",
    "features": ["pull-down", "matte black"]
}
```

### Installation Guide
```
GET /api/installation/<product_code>
```

### Parts Information
```
GET /api/parts/<product_code>
```

## 🎨 Frontend Features

- **Clean Design**: Modern, professional interface with gradient backgrounds
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Example Queries**: Pre-built example queries for quick testing
- **Smart Formatting**: Automatic markdown rendering for better readability
- **Source Display**: Clear visualization of grounding sources
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during query processing

## 🏗️ Architecture

```
rag_demo/
├── backend/
│   ├── app.py              # Flask application and API endpoints
│   └── query_engine.py     # Gemini AI integration and query processing
├── frontend/
│   └── index.html          # Single-page application UI
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── start.bat              # Windows startup script
└── start.sh               # Linux/Mac startup script
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | (required) |
| `STORE_ID` | File Search store ID | (required) |
| `PORT` | Server port | 5000 |
| `DEBUG` | Debug mode | False |

### Query Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `temperature` | float | 0.0-1.0 | Controls randomness (lower = more focused) |
| `top_p` | float | 0.0-1.0 | Nucleus sampling parameter |
| `max_tokens` | int | - | Maximum response length |

## 📝 Example Queries

1. **Product Specifications**
   - "Show me specifications for product 100.1000"
   - "What are the features of TVH.2691?"

2. **Product Search**
   - "What kitchen faucets are available in matte black finish?"
   - "Find all shower systems with thermostatic valves"

3. **Comparison**
   - "Compare products 100.1000 and 160.1000"
   - "What's the difference between Kingston and Victoria series?"

4. **Installation & Parts**
   - "Installation guide for product 240.4420"
   - "Show me parts diagram for product 100.1000"

5. **General Questions**
   - "What finishes does Flusso offer?"
   - "Tell me about the warranty policy"

## 🐛 Troubleshooting

### Server Won't Start

1. Check if Python is installed: `python --version`
2. Verify virtual environment is activated
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check if port 5000 is available

### API Errors

1. Verify API key in `.env` file
2. Check store ID is correct
3. Review server logs for detailed error messages
4. Ensure internet connectivity for Gemini API

### No Results Returned

1. Check if the store has indexed documents
2. Verify query is clear and specific
3. Try different query formulations
4. Check server logs for errors

## 🔒 Security Notes

- API key is stored in `.env` file (never commit to version control)
- Add `.env` to `.gitignore` if using git
- Consider using environment variables for production
- Implement rate limiting for production use

## 📄 License

This is a demonstration application for Flusso product knowledge base.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs in the terminal
3. Verify API and store configuration

## 🎯 System Prompt

The AI assistant is configured with a comprehensive system prompt that:
- Specializes in Flusso product information
- Provides accurate specifications and details
- Cites sources and product codes
- Formats responses for readability
- Maintains professional tone
- Only uses knowledge base information

## 🚀 Performance

- Average query response time: 2-5 seconds
- Supports concurrent requests
- Efficient source retrieval with File Search
- Cached responses (optional)

## 📊 Future Enhancements

Potential improvements:
- User authentication
- Query history
- Advanced filtering options
- Export functionality
- Multi-language support
- Analytics dashboard

---

**Built with Google Gemini AI** | **Powered by File Search RAG**
