# Smart Article Categorizer - Project Plan

## Project Overview
Build a system that automatically classifies articles into 6 categories (Tech, Finance, Healthcare, Sports, Politics, Entertainment) using different embedding approaches with a Streamlit web interface.

## Categories
1. Tech
2. Finance
3. Healthcare
4. Sports
5. Politics
6. Entertainment

## Technical Architecture

### Embedding Models (4 Types)
1. **Word2Vec/GloVe**: Average word vectors for document representation
2. **BERT**: Use [CLS] token embeddings
3. **Sentence-BERT**: Direct sentence embeddings (all-MiniLM-L6-v2)
4. **OpenAI**: text-embedding-ada-002 API

### Classification Pipeline
- Train Logistic Regression classifier on each embedding type
- Compare accuracy, precision, recall, and F1-score
- Analyze which embedding works best for news classification

---

## Phase 1: Frontend/UI Development (Streamlit)

### Task 1.1: Project Setup
- [ ] Create project structure and directories
- [ ] Set up virtual environment
- [ ] Install required dependencies (streamlit, plotly, pandas, numpy, etc.)
- [ ] Create requirements.txt file

### Task 1.2: Main UI Layout
- [ ] Create main Streamlit app structure
- [ ] Design header and navigation
- [ ] Create sidebar for model selection and settings
- [ ] Implement responsive layout

### Task 1.3: Article Input Interface
- [ ] Create text area for article input
- [ ] Add file upload functionality for batch processing
- [ ] Implement input validation and preprocessing
- [ ] Add example articles for testing

### Task 1.4: Prediction Display Interface
- [ ] Create sections for each model's predictions
- [ ] Display confidence scores with progress bars
- [ ] Show predicted category with color coding
- [ ] Add comparison table for all models

### Task 1.5: Visualization Components
- [ ] Create embedding cluster visualization (2D/3D scatter plots)
- [ ] Add model performance comparison charts
- [ ] Implement confidence score distributions
- [ ] Create category distribution visualizations

### Task 1.6: Mock Data Integration
- [ ] Create mock prediction functions for testing UI
- [ ] Generate sample embedding data for visualizations
- [ ] Implement placeholder model performance metrics
- [ ] Add sample articles for each category

### Task 1.7: UI Enhancement
- [ ] Add loading states and progress indicators
- [ ] Implement error handling and user feedback
- [ ] Add tooltips and help text
- [ ] Style with custom CSS for better UX

---

## Phase 2: Backend Development

### Task 2.1: Data Collection & Preprocessing
- [ ] Collect/curate article dataset for 6 categories
- [ ] Implement text preprocessing pipeline
- [ ] Create data validation and cleaning functions
- [ ] Split data into train/validation/test sets

### Task 2.2: Word2Vec/GloVe Implementation
- [ ] Download pre-trained Word2Vec/GloVe models
- [ ] Implement document embedding by averaging word vectors
- [ ] Handle out-of-vocabulary words
- [ ] Create embedding caching mechanism

### Task 2.3: BERT Implementation
- [ ] Set up BERT model (bert-base-uncased)
- [ ] Implement [CLS] token extraction
- [ ] Create batch processing for efficiency
- [ ] Add GPU support if available

### Task 2.4: Sentence-BERT Implementation
- [ ] Install and configure sentence-transformers
- [ ] Implement all-MiniLM-L6-v2 model
- [ ] Create sentence embedding pipeline
- [ ] Optimize for inference speed

### Task 2.5: OpenAI API Integration
- [ ] Set up OpenAI API client
- [ ] Implement text-embedding-ada-002 integration
- [ ] Add rate limiting and error handling
- [ ] Create API key management

### Task 2.6: Classification Models
- [ ] Train Logistic Regression for each embedding type
- [ ] Implement cross-validation
- [ ] Create model evaluation metrics
- [ ] Save/load trained models

### Task 2.7: Model Evaluation & Comparison
- [ ] Calculate accuracy, precision, recall, F1-score
- [ ] Create confusion matrices
- [ ] Generate performance comparison reports
- [ ] Implement statistical significance tests

### Task 2.8: FastAPI Backend Development
- [ ] Set up FastAPI application structure
- [ ] Create prediction endpoints for each model
- [ ] Implement batch processing capabilities
- [ ] Add CORS middleware for Streamlit integration
- [ ] Create health check endpoints
- [ ] Add request/response models with Pydantic

### Task 2.9: Integration & Testing
- [ ] Connect Streamlit frontend to FastAPI backend
- [ ] Implement real-time predictions via HTTP requests
- [ ] Add comprehensive error handling
- [ ] Create unit and integration tests
- [ ] Test API endpoints with different payloads

### Task 2.10: Performance Optimization
- [ ] Optimize model loading and inference
- [ ] Implement async processing where possible
- [ ] Add monitoring and logging
- [ ] Create deployment configuration

---

## Technical Stack

### Frontend
- **Streamlit**: Main web framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

### Backend
- **FastAPI**: Main backend API framework
- **scikit-learn**: Machine learning models
- **transformers**: BERT implementation
- **sentence-transformers**: Sentence-BERT
- **gensim**: Word2Vec/GloVe
- **openai**: OpenAI API client
- **uvicorn**: ASGI server for FastAPI

### Development Tools
- **Python 3.8+**: Programming language
- **pip**: Package management
- **pytest**: Testing framework
- **black**: Code formatting

---

## Success Metrics
- All 4 embedding models successfully implemented
- Accurate classification across 6 categories
- Responsive and intuitive web interface
- Performance comparison and analysis complete
- System runs locally without external dependencies (except OpenAI API)

---

## Timeline Estimate
- **Phase 1 (UI)**: 3-4 days
- **Phase 2 (Backend)**: 5-7 days
- **Total**: 8-11 days

---

## Notes
- System will run locally only
- OpenAI API requires internet connection and API key
- Other models can work offline after initial setup
- Focus on modularity for easy model swapping
- Prioritize user experience and clear visualizations 