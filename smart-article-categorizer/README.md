# Smart Article Categorizer

A comprehensive system that automatically classifies articles into 6 categories (Tech, Finance, Healthcare, Sports, Politics, Entertainment) using different embedding approaches with a beautiful Streamlit web interface.

## Features

- **4 Embedding Models**: Word2Vec/GloVe, BERT, Sentence-BERT, OpenAI
- **Interactive Web UI**: Built with Streamlit
- **Real-time Predictions**: Classify articles instantly
- **Model Comparison**: Compare performance across different models
- **Visualizations**: Embedding clusters, performance metrics, category distributions
- **FastAPI Backend**: RESTful API for model predictions
- **Batch Processing**: Handle multiple articles at once

## Project Structure

```
smart-article-categorizer/
├── app.py                 # Main Streamlit application
├── utils/
│   └── api_client.py     # API client for backend communication
├── requirements.txt      # Python dependencies
├── project_plan.md      # Detailed project plan
└── README.md           # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd smart-article-categorizer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Phase 1: Frontend Only (Current)

The UI is fully functional with mock data for testing and development.

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Test the interface**:
   - Try different input methods (text input, sample articles, file upload)
   - Select different models in the sidebar
   - Explore the visualizations
   - Test the prediction interface

### Phase 2: Full System (Backend + Frontend)

Once the FastAPI backend is implemented:

1. **Start the FastAPI backend**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Start the Streamlit frontend**:
   ```bash
   streamlit run app.py
   ```

3. **Configure the backend URL** in the Streamlit sidebar (default: `http://localhost:8000`)

## Features Overview

### Article Input Methods
- **Text Input**: Direct text entry
- **Sample Articles**: Pre-loaded examples for each category
- **File Upload**: Upload `.txt` or `.md` files

### Model Selection
- **Word2Vec/GloVe**: Average word vectors for document representation
- **BERT**: Uses [CLS] token embeddings
- **Sentence-BERT**: Direct sentence embeddings (all-MiniLM-L6-v2)
- **OpenAI**: text-embedding-ada-002 API (requires API key)

### Predictions & Analysis
- **Individual Model Results**: See predictions from each selected model
- **Confidence Scores**: Visual progress bars for each category
- **Model Comparison**: Side-by-side comparison table and charts
- **Consensus Prediction**: Average prediction across all models

### Visualizations
- **Embedding Clusters**: 2D visualization of article embeddings
- **Model Performance**: Accuracy, precision, recall, F1-score comparison
- **Category Distribution**: Pie chart of article categories

### Configuration Options
- **Model Selection**: Enable/disable specific models
- **API Configuration**: Set backend URL and OpenAI API key
- **Advanced Settings**: Confidence threshold, text length limits

## Categories

The system classifies articles into these 6 categories:

1. **Tech** 🔵 - Technology, software, hardware, innovation
2. **Finance** 🟢 - Markets, economy, business, investments
3. **Healthcare** 🔴 - Medicine, health, research, treatments
4. **Sports** 🟠 - Games, athletes, competitions, scores
5. **Politics** 🟣 - Government, elections, policies, legislation
6. **Entertainment** 🔴 - Movies, music, celebrities, shows

## API Endpoints (Future Implementation)

The FastAPI backend will provide these endpoints:

- `GET /health` - Health check
- `POST /predict/word2vec` - Word2Vec predictions
- `POST /predict/bert` - BERT predictions
- `POST /predict/sentence-bert` - Sentence-BERT predictions
- `POST /predict/openai` - OpenAI predictions
- `POST /predict/batch` - Batch predictions
- `GET /models/performance` - Model performance metrics
- `POST /embeddings/{model}` - Get embeddings for visualization

## Development

### Current Status: Phase 1 Complete ✅

- [x] Project setup and structure
- [x] Streamlit UI with full functionality
- [x] Mock data integration for testing
- [x] Interactive visualizations
- [x] Model selection and configuration
- [x] Article input methods
- [x] Prediction display interface
- [x] API client utility for future backend integration

### Next Steps: Phase 2 (Backend Development)

- [ ] Data collection and preprocessing
- [ ] Implement Word2Vec/GloVe model
- [ ] Implement BERT model
- [ ] Implement Sentence-BERT model
- [ ] Implement OpenAI API integration
- [ ] Train classification models
- [ ] Create FastAPI backend
- [ ] Connect frontend to backend
- [ ] Performance optimization

## Configuration

### OpenAI API Key
To use OpenAI embeddings, you'll need an API key:
1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Enter it in the sidebar under "API Configuration"

### Backend URL
The default backend URL is `http://localhost:8000`. Change this in the sidebar if your backend runs on a different port or host.

## Troubleshooting

### Common Issues

1. **Dependencies not installing**:
   - Make sure you're using Python 3.8+
   - Try upgrading pip: `pip install --upgrade pip`

2. **Streamlit not starting**:
   - Check if port 8501 is available
   - Try: `streamlit run app.py --server.port 8502`

3. **Mock predictions not working**:
   - This is expected in Phase 1 - they're placeholder functions
   - Real predictions will work once the backend is implemented

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please respect the terms of use for any third-party APIs or models used.

## Support

For issues or questions, please check the project plan document or create an issue in the repository.

---

**Built with ❤️ using Streamlit and FastAPI** 