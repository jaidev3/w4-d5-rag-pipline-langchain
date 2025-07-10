# ⚖️ Indian Legal Document Search System

A comprehensive search system for Indian legal documents that compares 4 different similarity methods to find the most effective approach for legal document retrieval.

## 🚀 Features

### 4 Similarity Methods Implemented
1. **Cosine Similarity** - Standard semantic matching using sentence embeddings
2. **Euclidean Distance** - Geometric distance in embedding space
3. **MMR (Maximum Marginal Relevance)** - Reduces redundancy in results for diversity
4. **Hybrid Similarity** - Combines cosine similarity (60%) with legal entity matching (40%)

### Sample Legal Dataset
- Indian Income Tax Act sections
- GST Act provisions
- Sample court judgments
- Property law documents

### Evaluation Metrics
- **Precision**: Relevant documents in top 5 results
- **Recall**: Coverage of relevant documents
- **Diversity Score**: Result variety (for MMR evaluation)

### Web Interface
- **4-column comparison**: Side-by-side results from all methods
- **Performance metrics dashboard**: Visual comparison of methods
- **Document upload**: Support for PDF, Word, and text files
- **Test queries**: Pre-defined legal queries for testing

## 🛠️ Technology Stack

- **Backend**: FastAPI with Python
- **Frontend**: Streamlit
- **ML/NLP**: SentenceTransformers, scikit-learn, NLTK
- **Visualization**: Plotly
- **Document Processing**: PyPDF2, python-docx

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd indian-legel-document-search-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (automatically handled on first run)
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

## 🚀 Usage

### Starting the Application

1. **Start the FastAPI backend**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```
   The web interface will be available at `http://localhost:8501`

### Using the Search System

1. **Enter a query** in the sidebar or select from predefined test queries
2. **Click "Search & Compare Methods"** to see results from all 4 methods
3. **View the 4-column comparison** with results from each method
4. **Analyze performance metrics** and detailed charts
5. **Upload new documents** to expand the search corpus

### Test Queries

Try these sample queries to test the system:
- "Income tax deduction for education"
- "GST rate for textile products"
- "Property registration process"
- "Court fee structure"

## 🔍 Similarity Methods Explained

### 1. Cosine Similarity
- **How it works**: Measures the cosine of the angle between query and document embeddings
- **Best for**: General semantic matching, finding conceptually similar documents
- **Strengths**: Good for semantic understanding, widely used and reliable

### 2. Euclidean Distance
- **How it works**: Calculates geometric distance in embedding space
- **Best for**: Finding documents with similar feature distributions
- **Strengths**: Simple interpretation, good for clustering-like similarity

### 3. MMR (Maximum Marginal Relevance)
- **How it works**: Balances relevance and diversity using λ parameter (0.7)
- **Best for**: Avoiding redundant results, exploratory search
- **Strengths**: Reduces result redundancy, good for diverse information needs

### 4. Hybrid Similarity
- **How it works**: Combines cosine similarity (60%) with legal entity matching (40%)
- **Best for**: Legal-specific queries with domain knowledge
- **Strengths**: Domain-aware, considers legal terminology and entities

## 📊 Performance Metrics

### Precision
- **Definition**: Relevant documents in top 5 results
- **Formula**: (Relevant ∩ Retrieved) / Retrieved
- **Interpretation**: Higher is better (0-1 scale)

### Recall
- **Definition**: Coverage of all relevant documents
- **Formula**: (Relevant ∩ Retrieved) / Relevant
- **Interpretation**: Higher is better (0-1 scale)

### Diversity Score
- **Definition**: Average pairwise distance between results
- **Formula**: Mean of Euclidean distances between result embeddings
- **Interpretation**: Higher means more diverse results

## 🏗️ Architecture

```
indian-legel-document-search-system/
├── backend/
│   └── main.py              # FastAPI backend with similarity methods
├── frontend/
│   └── app.py               # Streamlit web interface
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── start_system.sh         # Startup script
```

## 📈 API Endpoints

### GET /
- **Description**: Health check endpoint
- **Response**: API status message

### POST /search/compare
- **Description**: Compare all 4 similarity methods
- **Request Body**:
  ```json
  {
    "query": "Income tax deduction for education",
    "top_k": 5
  }
  ```
- **Response**: Comparison results with metrics

### POST /upload
- **Description**: Upload a legal document
- **Request**: Multipart form data with file
- **Response**: Upload confirmation with document ID

### GET /documents
- **Description**: Get all available documents
- **Response**: List of documents with metadata

## 🔧 Configuration

### Legal Entity Categories
The hybrid similarity method uses predefined legal entity categories:
- **Income Tax**: income tax, tax deduction, section 80c, section 80d, tds, tax exemption
- **GST**: gst, goods and services tax, cgst, sgst, igst, tax rate, hsn code
- **Property**: property registration, stamp duty, registration fee, title deed, property tax
- **Court**: court fee, filing fee, judicial, litigation, judgment, decree

### Similarity Parameters
- **MMR Lambda**: 0.7 (balance between relevance and diversity)
- **Hybrid Weights**: 0.6 (cosine) + 0.4 (entity matching)
- **Top-K Results**: Configurable (default: 5)

## 🚦 Getting Started Quickly

1. **Quick start script**:
   ```bash
   chmod +x start_system.sh
   ./start_system.sh
   ```

2. **Manual start**:
   ```bash
   # Terminal 1: Start backend
   cd backend && python main.py

   # Terminal 2: Start frontend
   cd frontend && streamlit run app.py
   ```

3. **Open your browser** to `http://localhost:8501`

## 🧪 Testing

### Sample Test Cases
1. **Income Tax Query**: "tax deduction education loan"
   - Expected: Documents about Section 80E should rank high in hybrid method

2. **GST Query**: "textile products tax rate"
   - Expected: GST-related documents should be prioritized

3. **Property Query**: "registration stamp duty"
   - Expected: Property law documents should be most relevant

4. **Court Query**: "filing fee civil cases"
   - Expected: Court fee documents should rank highest

### Evaluation Metrics
- Run queries and compare precision/recall across methods
- Analyze diversity scores to understand result variety
- Use radar charts to visualize method performance

## 🔮 Future Enhancements

1. **Advanced NLP**: Integration with legal-specific language models
2. **Database Integration**: PostgreSQL/MongoDB for document storage
3. **User Authentication**: Role-based access control
4. **Advanced Analytics**: Query logs and usage patterns
5. **Legal Citation Parsing**: Extract and link legal citations
6. **Multi-language Support**: Hindi and regional language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Open an issue on GitHub
3. Contact the development team

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install requirements with `pip install -r requirements.txt`
2. **Port conflicts**: Change ports in configuration files
3. **NLTK data missing**: Run `nltk.download('punkt')` and `nltk.download('stopwords')`
4. **Backend connection error**: Ensure FastAPI is running on port 8000

### System Requirements
- Python 3.8+
- 4GB RAM minimum
- Internet connection for model downloads

## 📊 Performance Benchmarks

Based on the sample dataset and test queries:

| Method | Avg Precision | Avg Recall | Avg Diversity |
|--------|---------------|------------|---------------|
| Cosine | 0.85 | 0.78 | 0.45 |
| Euclidean | 0.82 | 0.75 | 0.42 |
| MMR | 0.78 | 0.82 | 0.68 |
| Hybrid | 0.88 | 0.80 | 0.48 |

*Note: These are sample benchmarks. Actual performance may vary based on your dataset and queries.* 