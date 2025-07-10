from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os
import PyPDF2
import docx
from io import BytesIO
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = FastAPI(title="Indian Legal Document Search System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
model = SentenceTransformer('all-MiniLM-L6-v2')
tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

# Legal entities for hybrid similarity
LEGAL_ENTITIES = {
    'income_tax': ['income tax', 'tax deduction', 'section 80c', 'section 80d', 'tds', 'tax exemption'],
    'gst': ['gst', 'goods and services tax', 'cgst', 'sgst', 'igst', 'tax rate', 'hsn code'],
    'property': ['property registration', 'stamp duty', 'registration fee', 'title deed', 'property tax'],
    'court': ['court fee', 'filing fee', 'judicial', 'litigation', 'judgment', 'decree']
}

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    document_id: str
    title: str
    content: str
    score: float
    method: str

class ComparisonResult(BaseModel):
    query: str
    cosine_results: List[SearchResult]
    euclidean_results: List[SearchResult]
    mmr_results: List[SearchResult]
    hybrid_results: List[SearchResult]
    metrics: Dict[str, float]

# Sample legal documents dataset
SAMPLE_DOCUMENTS = [
    {
        "id": "doc_1",
        "title": "Income Tax Act - Section 80C Deductions",
        "content": "Under Section 80C of the Income Tax Act, deductions are allowed for investments in specified financial instruments including life insurance premiums, provident fund contributions, equity linked saving schemes (ELSS), and education loan principal repayment. The maximum deduction allowed is Rs. 1,50,000 per financial year.",
        "category": "income_tax"
    },
    {
        "id": "doc_2", 
        "title": "GST Rates for Textile Products",
        "content": "Goods and Services Tax (GST) rates for textile products vary based on the type of fabric and processing. Cotton fabrics attract 5% GST, while synthetic textiles are taxed at 12%. Readymade garments above Rs. 1000 are subject to 12% GST, while those below Rs. 1000 attract 5% GST.",
        "category": "gst"
    },
    {
        "id": "doc_3",
        "title": "Property Registration Process in India",
        "content": "Property registration in India involves several steps including verification of title documents, payment of stamp duty and registration fees, execution of sale deed, and registration with the sub-registrar office. The stamp duty varies from 3% to 10% depending on the state, and registration fee is typically 1% of the property value.",
        "category": "property"
    },
    {
        "id": "doc_4",
        "title": "Court Fee Structure for Civil Cases",
        "content": "Court fees for civil cases in India are governed by the Court Fees Act. The fee structure includes filing fees, process fees, and hearing fees. For suits involving monetary claims, the court fee is calculated as a percentage of the claim amount, typically ranging from 1% to 7.5% with a minimum and maximum limit.",
        "category": "court"
    },
    {
        "id": "doc_5",
        "title": "Income Tax Deduction for Education Expenses",
        "content": "Section 80E of the Income Tax Act allows deduction of interest paid on education loans for higher education. The deduction is available for 8 years or until the interest is fully paid, whichever is earlier. There is no upper limit on the deduction amount for interest on education loans.",
        "category": "income_tax"
    },
    {
        "id": "doc_6",
        "title": "GST Input Tax Credit Rules",
        "content": "Input Tax Credit (ITC) under GST allows businesses to claim credit for GST paid on inputs used in the course of business. The credit can be claimed only if the supplier has filed their GST returns and the goods/services are used for business purposes. Certain items like motor vehicles for personal use are not eligible for ITC.",
        "category": "gst"
    },
    {
        "id": "doc_7",
        "title": "Property Tax Assessment and Payment",
        "content": "Property tax is levied by municipal corporations on immovable property within their jurisdiction. The tax is calculated based on the annual rental value or capital value of the property. Property owners must pay this tax annually, and failure to pay can result in penalties and legal action.",
        "category": "property"
    },
    {
        "id": "doc_8",
        "title": "Supreme Court Judgment on Tax Evasion",
        "content": "The Supreme Court has held that tax evasion is a serious offense that undermines the fiscal policy of the government. The court emphasized that willful tax evasion with intent to defraud the revenue constitutes a criminal offense punishable under the Income Tax Act and can result in prosecution and imprisonment.",
        "category": "court"
    }
]

# Initialize document embeddings
document_embeddings = None
document_tfidf = None

def initialize_embeddings():
    global document_embeddings, document_tfidf
    
    # Create embeddings for all documents
    texts = [doc['content'] for doc in SAMPLE_DOCUMENTS]
    document_embeddings = model.encode(texts)
    
    # Create TF-IDF vectors
    document_tfidf = tfidf_vectorizer.fit_transform(texts)

# Initialize on startup
initialize_embeddings()

def preprocess_text(text: str) -> str:
    """Preprocess text by removing special characters and converting to lowercase"""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    return text

def extract_legal_entities(text: str) -> Dict[str, int]:
    """Extract legal entities from text for hybrid similarity"""
    text_lower = text.lower()
    entity_counts = {}
    
    for category, entities in LEGAL_ENTITIES.items():
        count = 0
        for entity in entities:
            count += len(re.findall(r'\b' + re.escape(entity) + r'\b', text_lower))
        entity_counts[category] = count
    
    return entity_counts

def cosine_similarity_search(query: str, top_k: int = 5) -> List[SearchResult]:
    """Perform cosine similarity search"""
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)[0]
    
    # Get top k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        doc = SAMPLE_DOCUMENTS[idx]
        results.append(SearchResult(
            document_id=doc['id'],
            title=doc['title'],
            content=doc['content'],
            score=float(similarities[idx]),
            method="cosine"
        ))
    
    return results

def euclidean_distance_search(query: str, top_k: int = 5) -> List[SearchResult]:
    """Perform Euclidean distance search"""
    query_embedding = model.encode([query])
    distances = euclidean_distances(query_embedding, document_embeddings)[0]
    
    # Convert distances to similarity scores (lower distance = higher similarity)
    max_distance = np.max(distances)
    similarities = 1 - (distances / max_distance)
    
    # Get top k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        doc = SAMPLE_DOCUMENTS[idx]
        results.append(SearchResult(
            document_id=doc['id'],
            title=doc['title'],
            content=doc['content'],
            score=float(similarities[idx]),
            method="euclidean"
        ))
    
    return results

def mmr_search(query: str, top_k: int = 5, lambda_param: float = 0.7) -> List[SearchResult]:
    """Perform Maximum Marginal Relevance (MMR) search"""
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)[0]
    
    selected_indices = []
    remaining_indices = list(range(len(SAMPLE_DOCUMENTS)))
    
    for _ in range(min(top_k, len(SAMPLE_DOCUMENTS))):
        mmr_scores = []
        
        for idx in remaining_indices:
            relevance_score = similarities[idx]
            
            if not selected_indices:
                diversity_score = 0
            else:
                # Calculate maximum similarity with already selected documents
                selected_embeddings = document_embeddings[selected_indices]
                current_embedding = document_embeddings[idx].reshape(1, -1)
                max_similarity = np.max(cosine_similarity(current_embedding, selected_embeddings))
                diversity_score = max_similarity
            
            mmr_score = lambda_param * relevance_score - (1 - lambda_param) * diversity_score
            mmr_scores.append((idx, mmr_score))
        
        # Select document with highest MMR score
        best_idx = max(mmr_scores, key=lambda x: x[1])[0]
        selected_indices.append(best_idx)
        remaining_indices.remove(best_idx)
    
    results = []
    for idx in selected_indices:
        doc = SAMPLE_DOCUMENTS[idx]
        results.append(SearchResult(
            document_id=doc['id'],
            title=doc['title'],
            content=doc['content'],
            score=float(similarities[idx]),
            method="mmr"
        ))
    
    return results

def hybrid_similarity_search(query: str, top_k: int = 5) -> List[SearchResult]:
    """Perform hybrid similarity search (0.6 * cosine + 0.4 * legal entity match)"""
    query_embedding = model.encode([query])
    cosine_similarities = cosine_similarity(query_embedding, document_embeddings)[0]
    
    # Extract legal entities from query
    query_entities = extract_legal_entities(query)
    
    # Calculate entity match scores
    entity_scores = []
    for doc in SAMPLE_DOCUMENTS:
        doc_entities = extract_legal_entities(doc['content'])
        
        # Calculate entity overlap score
        total_query_entities = sum(query_entities.values())
        if total_query_entities == 0:
            entity_score = 0
        else:
            overlap_score = 0
            for category, count in query_entities.items():
                if count > 0 and doc_entities.get(category, 0) > 0:
                    overlap_score += min(count, doc_entities[category])
            entity_score = overlap_score / total_query_entities
        
        entity_scores.append(entity_score)
    
    # Normalize entity scores
    max_entity_score = max(entity_scores) if max(entity_scores) > 0 else 1
    normalized_entity_scores = [score / max_entity_score for score in entity_scores]
    
    # Calculate hybrid scores
    hybrid_scores = []
    for i in range(len(SAMPLE_DOCUMENTS)):
        hybrid_score = 0.6 * cosine_similarities[i] + 0.4 * normalized_entity_scores[i]
        hybrid_scores.append(hybrid_score)
    
    # Get top k results
    top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        doc = SAMPLE_DOCUMENTS[idx]
        results.append(SearchResult(
            document_id=doc['id'],
            title=doc['title'],
            content=doc['content'],
            score=float(hybrid_scores[idx]),
            method="hybrid"
        ))
    
    return results

def calculate_metrics(results_dict: Dict[str, List[SearchResult]], query: str) -> Dict[str, float]:
    """Calculate precision, recall, and diversity metrics"""
    
    # For demonstration, we'll use a simple relevance judgment
    # In practice, this would be based on human annotations
    relevant_docs = set()
    query_lower = query.lower()
    
    # Simple relevance judgment based on query terms
    for doc in SAMPLE_DOCUMENTS:
        doc_content_lower = doc['content'].lower()
        doc_title_lower = doc['title'].lower()
        
        # Check if query terms appear in document
        query_terms = query_lower.split()
        matches = sum(1 for term in query_terms if term in doc_content_lower or term in doc_title_lower)
        
        if matches >= len(query_terms) * 0.5:  # At least 50% of query terms match
            relevant_docs.add(doc['id'])
    
    metrics = {}
    
    for method, results in results_dict.items():
        retrieved_docs = set(result.document_id for result in results)
        
        # Precision: relevant docs in top 5 results
        precision = len(relevant_docs.intersection(retrieved_docs)) / len(retrieved_docs) if retrieved_docs else 0
        
        # Recall: coverage of relevant documents
        recall = len(relevant_docs.intersection(retrieved_docs)) / len(relevant_docs) if relevant_docs else 0
        
        # Diversity score: average pairwise distance between results
        if len(results) > 1:
            result_embeddings = []
            for result in results:
                doc_idx = next(i for i, doc in enumerate(SAMPLE_DOCUMENTS) if doc['id'] == result.document_id)
                result_embeddings.append(document_embeddings[doc_idx])
            
            pairwise_distances = []
            for i in range(len(result_embeddings)):
                for j in range(i + 1, len(result_embeddings)):
                    distance = euclidean_distances([result_embeddings[i]], [result_embeddings[j]])[0][0]
                    pairwise_distances.append(distance)
            
            diversity = np.mean(pairwise_distances) if pairwise_distances else 0
        else:
            diversity = 0
        
        metrics[f"{method}_precision"] = precision
        metrics[f"{method}_recall"] = recall
        metrics[f"{method}_diversity"] = diversity
    
    return metrics

@app.get("/")
async def root():
    return {"message": "Indian Legal Document Search System API"}

@app.post("/search/compare", response_model=ComparisonResult)
async def compare_search_methods(request: SearchRequest):
    """Compare all 4 similarity methods for a given query"""
    
    try:
        # Perform searches with all methods
        cosine_results = cosine_similarity_search(request.query, request.top_k)
        euclidean_results = euclidean_distance_search(request.query, request.top_k)
        mmr_results = mmr_search(request.query, request.top_k)
        hybrid_results = hybrid_similarity_search(request.query, request.top_k)
        
        # Calculate metrics
        results_dict = {
            "cosine": cosine_results,
            "euclidean": euclidean_results,
            "mmr": mmr_results,
            "hybrid": hybrid_results
        }
        
        metrics = calculate_metrics(results_dict, request.query)
        
        return ComparisonResult(
            query=request.query,
            cosine_results=cosine_results,
            euclidean_results=euclidean_results,
            mmr_results=mmr_results,
            hybrid_results=hybrid_results,
            metrics=metrics
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a legal document"""
    
    try:
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file.filename.endswith('.docx'):
            doc = docx.Document(BytesIO(content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:
            # Assume text file
            text = content.decode('utf-8')
        
        # Add to document collection (in practice, this would be stored in a database)
        new_doc = {
            "id": f"uploaded_{len(SAMPLE_DOCUMENTS)}",
            "title": file.filename,
            "content": text,
            "category": "uploaded"
        }
        
        SAMPLE_DOCUMENTS.append(new_doc)
        
        # Reinitialize embeddings
        initialize_embeddings()
        
        return {"message": f"Document {file.filename} uploaded successfully", "document_id": new_doc["id"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    """Get all available documents"""
    return [{"id": doc["id"], "title": doc["title"], "category": doc["category"]} for doc in SAMPLE_DOCUMENTS]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 