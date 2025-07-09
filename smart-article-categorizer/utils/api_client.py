import requests
import json
from typing import Dict, List, Optional
import streamlit as st

class APIClient:
    """Client for communicating with the FastAPI backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def health_check(self) -> bool:
        """Check if the backend is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def predict_word2vec(self, text: str) -> Dict[str, float]:
        """Get Word2Vec/GloVe predictions"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict/word2vec",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()["predictions"]
        except requests.RequestException as e:
            st.error(f"Word2Vec prediction failed: {e}")
            return {}
    
    def predict_bert(self, text: str) -> Dict[str, float]:
        """Get BERT predictions"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict/bert",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()["predictions"]
        except requests.RequestException as e:
            st.error(f"BERT prediction failed: {e}")
            return {}
    
    def predict_sentence_bert(self, text: str) -> Dict[str, float]:
        """Get Sentence-BERT predictions"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict/sentence-bert",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()["predictions"]
        except requests.RequestException as e:
            st.error(f"Sentence-BERT prediction failed: {e}")
            return {}
    
    def predict_openai(self, text: str, api_key: str) -> Dict[str, float]:
        """Get OpenAI predictions"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict/openai",
                json={"text": text, "api_key": api_key}
            )
            response.raise_for_status()
            return response.json()["predictions"]
        except requests.RequestException as e:
            st.error(f"OpenAI prediction failed: {e}")
            return {}
    
    def predict_all(self, text: str, api_key: Optional[str] = None) -> Dict[str, Dict[str, float]]:
        """Get predictions from all models"""
        results = {}
        
        # Word2Vec/GloVe
        word2vec_result = self.predict_word2vec(text)
        if word2vec_result:
            results["Word2Vec/GloVe"] = word2vec_result
        
        # BERT
        bert_result = self.predict_bert(text)
        if bert_result:
            results["BERT"] = bert_result
        
        # Sentence-BERT
        sentence_bert_result = self.predict_sentence_bert(text)
        if sentence_bert_result:
            results["Sentence-BERT"] = sentence_bert_result
        
        # OpenAI (if API key provided)
        if api_key:
            openai_result = self.predict_openai(text, api_key)
            if openai_result:
                results["OpenAI"] = openai_result
        
        return results
    
    def get_model_performance(self) -> Dict[str, Dict[str, float]]:
        """Get model performance metrics"""
        try:
            response = self.session.get(f"{self.base_url}/models/performance")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Failed to get model performance: {e}")
            return {}
    
    def get_embeddings(self, text: str, model: str) -> List[float]:
        """Get embeddings for visualization"""
        try:
            response = self.session.post(
                f"{self.base_url}/embeddings/{model}",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()["embeddings"]
        except requests.RequestException as e:
            st.error(f"Failed to get embeddings: {e}")
            return []
    
    def batch_predict(self, texts: List[str], models: List[str]) -> Dict[str, List[Dict[str, float]]]:
        """Batch prediction for multiple texts"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict/batch",
                json={"texts": texts, "models": models}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Batch prediction failed: {e}")
            return {} 