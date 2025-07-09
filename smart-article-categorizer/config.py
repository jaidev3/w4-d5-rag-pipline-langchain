"""
Configuration file for Smart Article Categorizer
"""

# Application settings
APP_TITLE = "Smart Article Categorizer"
APP_ICON = "📰"
VERSION = "1.0.0"

# Server configuration
STREAMLIT_PORT = 8501
FASTAPI_PORT = 8000
BACKEND_URL = f"http://localhost:{FASTAPI_PORT}"

# Categories and their display colors
CATEGORIES = {
    'Tech': '#1976d2',
    'Finance': '#388e3c',
    'Healthcare': '#c2185b',
    'Sports': '#f57c00',
    'Politics': '#7b1fa2',
    'Entertainment': '#d32f2f'
}

# Model configuration
MODELS = {
    'word2vec': {
        'name': 'Word2Vec/GloVe',
        'description': 'Average word vectors for document representation',
        'enabled': True
    },
    'bert': {
        'name': 'BERT',
        'description': 'Uses [CLS] token embeddings',
        'enabled': True
    },
    'sentence_bert': {
        'name': 'Sentence-BERT',
        'description': 'Direct sentence embeddings (all-MiniLM-L6-v2)',
        'enabled': True
    },
    'openai': {
        'name': 'OpenAI',
        'description': 'text-embedding-ada-002 API',
        'enabled': True,
        'requires_api_key': True
    }
}

# UI configuration
UI_CONFIG = {
    'max_text_length': 10000,
    'default_confidence_threshold': 0.5,
    'chart_height': 400,
    'embedding_viz_height': 500,
    'model_card_height': 300
}

# API endpoints (for future backend)
API_ENDPOINTS = {
    'health': '/health',
    'predict': {
        'word2vec': '/predict/word2vec',
        'bert': '/predict/bert',
        'sentence_bert': '/predict/sentence-bert',
        'openai': '/predict/openai',
        'batch': '/predict/batch'
    },
    'models': {
        'performance': '/models/performance'
    },
    'embeddings': '/embeddings/{model}'
}

# Sample articles for testing
SAMPLE_ARTICLES = {
    'Tech': """
    Apple has announced its latest iPhone 15 Pro with groundbreaking features including a titanium design, 
    advanced camera system with 5x optical zoom, and the powerful A17 Pro chip built on 3-nanometer technology. 
    The device also features USB-C connectivity and enhanced battery life, marking a significant upgrade 
    in the smartphone industry.
    """,
    'Finance': """
    The Federal Reserve announced a 0.25% interest rate hike today, bringing the federal funds rate to 5.5%, 
    its highest level in 22 years. The decision comes amid persistent inflation concerns and a robust job market. 
    Stock markets reacted positively to the news, with the S&P 500 gaining 1.2% in afternoon trading.
    """,
    'Healthcare': """
    Researchers at Johns Hopkins University have developed a new gene therapy treatment for sickle cell disease 
    that shows promising results in clinical trials. The treatment uses CRISPR technology to edit patients' 
    bone marrow cells, potentially offering a cure for this inherited blood disorder that affects millions worldwide.
    """,
    'Sports': """
    The Los Angeles Lakers defeated the Boston Celtics 118-114 in a thrilling overtime game last night. 
    LeBron James led the Lakers with 35 points and 12 assists, while Jayson Tatum scored 42 points for the Celtics. 
    The victory puts the Lakers in second place in the Western Conference standings.
    """,
    'Politics': """
    The Senate passed a bipartisan infrastructure bill with a 69-30 vote, allocating $1.2 trillion for roads, 
    bridges, broadband, and clean energy projects over the next decade. The legislation now heads to the House 
    for final approval before reaching the President's desk for signature.
    """,
    'Entertainment': """
    The highly anticipated Marvel movie "Guardians of the Galaxy Vol. 3" has broken box office records, 
    earning $118 million in its opening weekend. Director James Gunn's final installment in the trilogy 
    has received critical acclaim for its emotional depth and spectacular visual effects.
    """
}

# Mock performance data (will be replaced with real data from backend)
MOCK_PERFORMANCE_DATA = {
    'Word2Vec/GloVe': {
        'accuracy': 0.78,
        'precision': 0.76,
        'recall': 0.75,
        'f1_score': 0.75
    },
    'BERT': {
        'accuracy': 0.85,
        'precision': 0.84,
        'recall': 0.83,
        'f1_score': 0.83
    },
    'Sentence-BERT': {
        'accuracy': 0.82,
        'precision': 0.81,
        'recall': 0.80,
        'f1_score': 0.80
    },
    'OpenAI': {
        'accuracy': 0.87,
        'precision': 0.86,
        'recall': 0.85,
        'f1_score': 0.85
    }
}

# CSS styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .model-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .prediction-result {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .tech { background-color: #e3f2fd; color: #1976d2; }
    .finance { background-color: #e8f5e8; color: #388e3c; }
    .healthcare { background-color: #fce4ec; color: #c2185b; }
    .sports { background-color: #fff3e0; color: #f57c00; }
    .politics { background-color: #f3e5f5; color: #7b1fa2; }
    .entertainment { background-color: #ffebee; color: #d32f2f; }
    .stProgress .st-bo {
        background-color: #e0e0e0;
    }
    .footer {
        text-align: center;
        color: #666;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""" 