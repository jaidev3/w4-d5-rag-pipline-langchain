import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Indian Legal Document Search System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .method-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .result-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .score-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .metrics-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">⚖️ Indian Legal Document Search System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Configuration")
        
        # Query input
        query = st.text_input(
            "Enter your legal query:",
            placeholder="e.g., Income tax deduction for education"
        )
        
        # Number of results
        top_k = st.slider("Number of results per method:", 1, 10, 5)
        
        # Predefined test queries
        st.subheader("📝 Test Queries")
        test_queries = [
            "Income tax deduction for education",
            "GST rate for textile products", 
            "Property registration process",
            "Court fee structure"
        ]
        
        selected_test_query = st.selectbox(
            "Select a test query:",
            [""] + test_queries
        )
        
        if selected_test_query:
            query = selected_test_query
        
        # Document upload
        st.subheader("📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Upload a legal document",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, Word, or text files"
        )
        
        if uploaded_file and st.button("Upload Document"):
            upload_document(uploaded_file)
    
    # Main content area
    if query:
        # Search button
        if st.button("🔍 Search & Compare Methods", type="primary"):
            search_and_compare(query, top_k)
    else:
        # Welcome message
        st.info("👆 Enter a query in the sidebar to start searching!")
        
        # Show sample documents
        show_sample_documents()

def upload_document(uploaded_file):
    """Upload document to the backend"""
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
        else:
            st.error(f"❌ Error uploading document: {response.text}")
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {str(e)}")

def search_and_compare(query, top_k):
    """Search using all methods and display comparison"""
    try:
        # Make API request
        with st.spinner("🔍 Searching with all methods..."):
            response = requests.post(
                f"{API_BASE_URL}/search/compare",
                json={"query": query, "top_k": top_k}
            )
        
        if response.status_code == 200:
            results = response.json()
            display_comparison_results(results)
        else:
            st.error(f"❌ Search failed: {response.text}")
            
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {str(e)}")

def display_comparison_results(results):
    """Display search results in 4-column comparison format"""
    
    st.subheader(f"🔍 Search Results for: '{results['query']}'")
    
    # Create 4 columns for comparison
    col1, col2, col3, col4 = st.columns(4)
    
    methods = [
        ("Cosine Similarity", "cosine_results", col1, "#1f77b4"),
        ("Euclidean Distance", "euclidean_results", col2, "#ff7f0e"), 
        ("MMR (Diversity)", "mmr_results", col3, "#2ca02c"),
        ("Hybrid (0.6×Cosine + 0.4×Entity)", "hybrid_results", col4, "#d62728")
    ]
    
    # Display results for each method
    for method_name, result_key, column, color in methods:
        with column:
            st.markdown(f'<div class="method-header" style="color: {color};">{method_name}</div>', 
                       unsafe_allow_html=True)
            
            method_results = results[result_key]
            
            for i, result in enumerate(method_results, 1):
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>#{i}</strong>
                        <span class="score-badge">Score: {result['score']:.3f}</span>
                    </div>
                    <h4 style="margin: 0.5rem 0; color: {color};">{result['title']}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">{result['content'][:200]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Display metrics
    st.subheader("📊 Performance Metrics")
    display_metrics(results['metrics'])
    
    # Display detailed analysis
    st.subheader("📈 Detailed Analysis")
    display_detailed_analysis(results)

def display_metrics(metrics):
    """Display performance metrics with visualizations"""
    
    # Create metrics dataframe
    methods = ['cosine', 'euclidean', 'mmr', 'hybrid']
    metric_types = ['precision', 'recall', 'diversity']
    
    metrics_data = []
    for method in methods:
        row = {'Method': method.title()}
        for metric in metric_types:
            key = f"{method}_{metric}"
            row[metric.title()] = metrics.get(key, 0)
        metrics_data.append(row)
    
    df_metrics = pd.DataFrame(metrics_data)
    
    # Display metrics table
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="metrics-card">', unsafe_allow_html=True)
        st.dataframe(df_metrics, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create radar chart
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        for i, method in enumerate(methods):
            values = [metrics.get(f"{method}_{metric}", 0) for metric in metric_types]
            values.append(values[0])  # Close the radar chart
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metric_types + [metric_types[0]],
                fill='toself',
                name=method.title(),
                line_color=colors[i]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Performance Comparison Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_detailed_analysis(results):
    """Display detailed analysis with charts"""
    
    # Score comparison chart
    methods = ['cosine', 'euclidean', 'mmr', 'hybrid']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Score Distribution', 'Top Document Overlap', 'Method Performance', 'Score Trends'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Score distribution
    for i, method in enumerate(methods):
        result_key = f"{method}_results"
        scores = [result['score'] for result in results[result_key]]
        
        fig.add_trace(
            go.Bar(
                x=[f"Doc {j+1}" for j in range(len(scores))],
                y=scores,
                name=method.title(),
                marker_color=colors[i],
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Document overlap analysis
    all_docs = set()
    method_docs = {}
    
    for method in methods:
        result_key = f"{method}_results"
        doc_ids = [result['document_id'] for result in results[result_key]]
        method_docs[method] = set(doc_ids)
        all_docs.update(doc_ids)
    
    overlap_data = []
    for doc_id in all_docs:
        count = sum(1 for method_set in method_docs.values() if doc_id in method_set)
        overlap_data.append(count)
    
    fig.add_trace(
        go.Histogram(
            x=overlap_data,
            name="Document Overlap",
            marker_color='lightblue',
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Method performance (precision vs recall)
    precision_scores = [results['metrics'].get(f"{method}_precision", 0) for method in methods]
    recall_scores = [results['metrics'].get(f"{method}_recall", 0) for method in methods]
    
    fig.add_trace(
        go.Scatter(
            x=precision_scores,
            y=recall_scores,
            mode='markers+text',
            text=[method.title() for method in methods],
            textposition="top center",
            marker=dict(size=15, color=colors),
            name="Performance",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Score trends (top 3 documents)
    for i, method in enumerate(methods):
        result_key = f"{method}_results"
        scores = [result['score'] for result in results[result_key][:3]]
        
        fig.add_trace(
            go.Scatter(
                x=[1, 2, 3],
                y=scores,
                mode='lines+markers',
                name=method.title(),
                line=dict(color=colors[i]),
                showlegend=False
            ),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=True)
    fig.update_xaxes(title_text="Documents", row=1, col=1)
    fig.update_yaxes(title_text="Score", row=1, col=1)
    fig.update_xaxes(title_text="Methods in Top Results", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_xaxes(title_text="Precision", row=2, col=1)
    fig.update_yaxes(title_text="Recall", row=2, col=1)
    fig.update_xaxes(title_text="Rank", row=2, col=2)
    fig.update_yaxes(title_text="Score", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Method recommendations
    st.subheader("💡 Method Recommendations")
    
    # Calculate best method for each metric
    best_precision = max(methods, key=lambda m: results['metrics'].get(f"{m}_precision", 0))
    best_recall = max(methods, key=lambda m: results['metrics'].get(f"{m}_recall", 0))
    best_diversity = max(methods, key=lambda m: results['metrics'].get(f"{m}_diversity", 0))
    
    recommendations = f"""
    **Best for Precision**: {best_precision.title()} - Most relevant results in top 5
    
    **Best for Recall**: {best_recall.title()} - Best coverage of all relevant documents
    
    **Best for Diversity**: {best_diversity.title()} - Most varied results (good for exploration)
    
    **Overall Recommendation**: 
    - Use **Cosine Similarity** for general semantic matching
    - Use **Hybrid Method** for legal-specific queries with entity matching
    - Use **MMR** when you need diverse results to avoid redundancy
    - Use **Euclidean Distance** for geometric similarity in embedding space
    """
    
    st.markdown(recommendations)

def show_sample_documents():
    """Show available sample documents"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents")
        if response.status_code == 200:
            documents = response.json()
            
            st.subheader("📚 Available Sample Documents")
            
            # Group documents by category
            categories = {}
            for doc in documents:
                category = doc.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(doc)
            
            # Display documents by category
            for category, docs in categories.items():
                st.write(f"**{category.replace('_', ' ').title()}**")
                for doc in docs:
                    st.write(f"- {doc['title']}")
                st.write("")
                
        else:
            st.error("❌ Could not load sample documents")
            
    except Exception as e:
        st.error(f"❌ Error connecting to backend: {str(e)}")

if __name__ == "__main__":
    main() 