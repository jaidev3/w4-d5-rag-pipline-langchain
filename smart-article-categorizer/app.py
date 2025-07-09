import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Smart Article Categorizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# Categories and their colors
CATEGORIES = {
    'Tech': '#1976d2',
    'Finance': '#388e3c',
    'Healthcare': '#c2185b',
    'Sports': '#f57c00',
    'Politics': '#7b1fa2',
    'Entertainment': '#d32f2f'
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

# Mock prediction functions (will be replaced with actual API calls)
def mock_predict_word2vec(text):
    """Mock Word2Vec prediction"""
    np.random.seed(len(text))
    scores = np.random.dirichlet(np.ones(6))
    categories = list(CATEGORIES.keys())
    return dict(zip(categories, scores))

def mock_predict_bert(text):
    """Mock BERT prediction"""
    np.random.seed(len(text) * 2)
    scores = np.random.dirichlet(np.ones(6))
    categories = list(CATEGORIES.keys())
    return dict(zip(categories, scores))

def mock_predict_sentence_bert(text):
    """Mock Sentence-BERT prediction"""
    np.random.seed(len(text) * 3)
    scores = np.random.dirichlet(np.ones(6))
    categories = list(CATEGORIES.keys())
    return dict(zip(categories, scores))

def mock_predict_openai(text):
    """Mock OpenAI prediction"""
    np.random.seed(len(text) * 4)
    scores = np.random.dirichlet(np.ones(6))
    categories = list(CATEGORIES.keys())
    return dict(zip(categories, scores))

def get_category_class(category):
    """Get CSS class for category"""
    return category.lower()

def create_confidence_chart(predictions, model_name):
    """Create a horizontal bar chart for confidence scores"""
    categories = list(predictions.keys())
    scores = list(predictions.values())
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker_color=[CATEGORIES[cat] for cat in categories],
        text=[f'{score:.2%}' for score in scores],
        textposition='auto',
    ))
    
    fig.update_layout(
        title=f'{model_name} Confidence Scores',
        xaxis_title='Confidence Score',
        yaxis_title='Categories',
        height=300,
        showlegend=False
    )
    
    return fig

def create_comparison_chart(all_predictions):
    """Create a comparison chart for all models"""
    df_data = []
    for model, predictions in all_predictions.items():
        for category, score in predictions.items():
            df_data.append({
                'Model': model,
                'Category': category,
                'Score': score
            })
    
    df = pd.DataFrame(df_data)
    
    fig = px.bar(
        df, 
        x='Category', 
        y='Score', 
        color='Model',
        barmode='group',
        title='Model Comparison Across Categories'
    )
    
    fig.update_layout(height=400)
    return fig

def create_embedding_visualization():
    """Create mock embedding visualization"""
    np.random.seed(42)
    n_points = 200
    
    # Generate mock embedding data
    data = []
    for i, category in enumerate(CATEGORIES.keys()):
        # Create clusters for each category
        x = np.random.normal(i * 3, 1, n_points // 6)
        y = np.random.normal(i * 2, 1, n_points // 6)
        
        for j in range(len(x)):
            data.append({
                'x': x[j],
                'y': y[j],
                'category': category,
                'text': f'Article {j+1}'
            })
    
    df = pd.DataFrame(data)
    
    fig = px.scatter(
        df, 
        x='x', 
        y='y', 
        color='category',
        color_discrete_map=CATEGORIES,
        title='Article Embeddings Visualization (2D Projection)',
        hover_data=['text']
    )
    
    fig.update_layout(
        xaxis_title='Embedding Dimension 1',
        yaxis_title='Embedding Dimension 2',
        height=500
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">📰 Smart Article Categorizer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This system automatically classifies articles into 6 categories using different embedding approaches:
    **Tech**, **Finance**, **Healthcare**, **Sports**, **Politics**, and **Entertainment**.
    """)
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    st.sidebar.subheader("Model Selection")
    use_word2vec = st.sidebar.checkbox("Word2Vec/GloVe", value=True)
    use_bert = st.sidebar.checkbox("BERT", value=True)
    use_sentence_bert = st.sidebar.checkbox("Sentence-BERT", value=True)
    use_openai = st.sidebar.checkbox("OpenAI", value=True)
    
    # API Configuration
    st.sidebar.subheader("API Configuration")
    backend_url = st.sidebar.text_input("Backend URL", value="http://localhost:8000")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", 
                                         help="Required for OpenAI embeddings")
    
    # Advanced settings
    st.sidebar.subheader("Advanced Settings")
    show_confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5)
    max_text_length = st.sidebar.number_input("Max Text Length", min_value=100, max_value=10000, value=5000)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Article Input")
        
        # Input method selection
        input_method = st.radio("Choose input method:", ["Text Input", "Sample Articles", "File Upload"])
        
        article_text = ""
        
        if input_method == "Text Input":
            article_text = st.text_area(
                "Enter article text:",
                height=200,
                max_chars=max_text_length,
                placeholder="Paste your article text here..."
            )
        
        elif input_method == "Sample Articles":
            selected_sample = st.selectbox("Choose a sample article:", list(SAMPLE_ARTICLES.keys()))
            if st.button("Load Sample Article"):
                article_text = SAMPLE_ARTICLES[selected_sample]
                st.text_area("Sample Article:", value=article_text, height=200, disabled=True)
        
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader("Choose a text file", type=['txt', 'md'])
            if uploaded_file is not None:
                article_text = str(uploaded_file.read(), "utf-8")
                st.text_area("Uploaded Article:", value=article_text[:1000] + "..." if len(article_text) > 1000 else article_text, 
                           height=200, disabled=True)
    
    with col2:
        st.header("📊 Quick Stats")
        if article_text:
            word_count = len(article_text.split())
            char_count = len(article_text)
            
            st.metric("Word Count", word_count)
            st.metric("Character Count", char_count)
            st.metric("Estimated Reading Time", f"{word_count // 200} min")
    
    # Prediction section
    if article_text and len(article_text.strip()) > 10:
        st.header("🔮 Predictions")
        
        # Predict button
        if st.button("🚀 Classify Article", type="primary"):
            with st.spinner("Analyzing article..."):
                # Simulate processing time
                time.sleep(1)
                
                # Get predictions from selected models
                all_predictions = {}
                
                if use_word2vec:
                    all_predictions["Word2Vec/GloVe"] = mock_predict_word2vec(article_text)
                
                if use_bert:
                    all_predictions["BERT"] = mock_predict_bert(article_text)
                
                if use_sentence_bert:
                    all_predictions["Sentence-BERT"] = mock_predict_sentence_bert(article_text)
                
                if use_openai and openai_api_key:
                    all_predictions["OpenAI"] = mock_predict_openai(article_text)
                
                # Display results
                if all_predictions:
                    # Individual model results
                    st.subheader("Individual Model Results")
                    
                    cols = st.columns(len(all_predictions))
                    for i, (model_name, predictions) in enumerate(all_predictions.items()):
                        with cols[i]:
                            st.markdown(f'<div class="model-card">', unsafe_allow_html=True)
                            st.markdown(f"**{model_name}**")
                            
                            # Get top prediction
                            top_category = max(predictions, key=predictions.get)
                            top_score = predictions[top_category]
                            
                            # Display prediction with color coding
                            st.markdown(f'''
                            <div class="prediction-result {get_category_class(top_category)}">
                                {top_category} ({top_score:.1%})
                            </div>
                            ''', unsafe_allow_html=True)
                            
                            # Confidence scores
                            for category, score in sorted(predictions.items(), key=lambda x: x[1], reverse=True):
                                st.progress(score, text=f"{category}: {score:.1%}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Comparison section
                    st.subheader("Model Comparison")
                    
                    # Comparison table
                    comparison_df = pd.DataFrame(all_predictions).T
                    comparison_df = comparison_df.round(3)
                    st.dataframe(comparison_df, use_container_width=True)
                    
                    # Comparison chart
                    comparison_chart = create_comparison_chart(all_predictions)
                    st.plotly_chart(comparison_chart, use_container_width=True)
                    
                    # Consensus prediction
                    st.subheader("Consensus Prediction")
                    
                    # Calculate average scores
                    avg_predictions = {}
                    for category in CATEGORIES.keys():
                        scores = [predictions[category] for predictions in all_predictions.values()]
                        avg_predictions[category] = np.mean(scores)
                    
                    consensus_category = max(avg_predictions, key=avg_predictions.get)
                    consensus_score = avg_predictions[consensus_category]
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f'''
                        <div class="prediction-result {get_category_class(consensus_category)}" style="text-align: center; font-size: 1.5rem;">
                            Consensus: {consensus_category} ({consensus_score:.1%})
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.warning("No models selected or API key missing for OpenAI.")
    
    # Visualization section
    st.header("📈 Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Embedding Clusters", "Model Performance", "Category Distribution"])
    
    with tab1:
        st.subheader("Article Embeddings in 2D Space")
        embedding_viz = create_embedding_visualization()
        st.plotly_chart(embedding_viz, use_container_width=True)
        
        st.info("This visualization shows how articles are clustered in the embedding space. Points of the same color represent articles from the same category.")
    
    with tab2:
        st.subheader("Model Performance Metrics")
        
        # Mock performance data
        performance_data = {
            'Model': ['Word2Vec/GloVe', 'BERT', 'Sentence-BERT', 'OpenAI'],
            'Accuracy': [0.78, 0.85, 0.82, 0.87],
            'Precision': [0.76, 0.84, 0.81, 0.86],
            'Recall': [0.75, 0.83, 0.80, 0.85],
            'F1-Score': [0.75, 0.83, 0.80, 0.85]
        }
        
        perf_df = pd.DataFrame(performance_data)
        
        # Performance metrics chart
        fig = px.bar(
            perf_df.melt(id_vars=['Model'], var_name='Metric', value_name='Score'),
            x='Model',
            y='Score',
            color='Metric',
            barmode='group',
            title='Model Performance Comparison'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance table
        st.dataframe(perf_df.set_index('Model'), use_container_width=True)
    
    with tab3:
        st.subheader("Category Distribution")
        
        # Mock category distribution data
        category_counts = {
            'Tech': 45,
            'Finance': 38,
            'Healthcare': 32,
            'Sports': 41,
            'Politics': 35,
            'Entertainment': 39
        }
        
        fig = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title='Distribution of Articles by Category',
            color_discrete_map=CATEGORIES
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        Smart Article Categorizer v1.0 | Built with Streamlit & FastAPI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 