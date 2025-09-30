#!/usr/bin/env python3
"""
Sentiment Analysis API with Modal
"""

import modal
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Create Modal app
app_name = os.getenv("SENTIMENT_APP_NAME", "sentiment-analyzer")
app = modal.App(app_name)

# Define the container image with required packages
image = modal.Image.debian_slim(python_version="3.11").pip_install([
    "transformers==4.36.0",
    "torch==2.1.0", 
    "fastapi==0.104.1",
    "pydantic==2.5.0"
])

@app.function(
    image=image,
    timeout=300,  # 5 minute timeout
    concurrency_limit=int(os.getenv("MAX_CONCURRENT_REQUESTS", 10)),
    # No GPU needed for this simple model
)
def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of input text
    Returns: {"label": "POSITIVE/NEGATIVE", "score": float, "emoji": str}
    """
    from transformers import pipeline
    
    # Load model (cached after first run)
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        return_all_scores=True
    )
    
    try:
        # Get sentiment scores
        results = sentiment_pipeline(text)[0]
        
        # Find the top result
        top_result = max(results, key=lambda x: x['score'])
        label = top_result['label']
        score = top_result['score']
        
        # Map to readable labels with emojis
        label_map = {
            'LABEL_0': {'label': 'Negative', 'emoji': '😞'},
            'LABEL_1': {'label': 'Neutral', 'emoji': '😐'},
            'LABEL_2': {'label': 'Positive', 'emoji': '😊'},
            'negative': {'label': 'Negative', 'emoji': '😞'},
            'neutral': {'label': 'Neutral', 'emoji': '😐'},
            'positive': {'label': 'Positive', 'emoji': '😊'}
        }
        
        mapped = label_map.get(label.lower(), {'label': label, 'emoji': '🤔'})
        
        return {
            "text": text,
            "label": mapped['label'],
            "score": round(score, 3),
            "confidence": f"{round(score * 100, 1)}%",
            "emoji": mapped['emoji'],
            "status": "success"
        }
        
    except Exception as e:
        return {
            "text": text,
            "error": str(e),
            "status": "error"
        }

# Create web endpoint
@app.function(image=image)
@modal.web_endpoint(method="POST")
def sentiment_endpoint(data: dict) -> Dict[str, Any]:
    """
    Web endpoint for sentiment analysis
    Send POST request with: {"text": "your text here"}
    """
    text = data.get("text", "")
    
    if not text or text.strip() == "":
        return {
            "error": "Please provide text to analyze",
            "status": "error"
        }
    
    # Call the sentiment analysis function
    result = analyze_sentiment.remote(text)
    return result

# Create a simple GET endpoint for health checks
@app.function(image=image)
@modal.web_endpoint(method="GET")
def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "sentiment-analyzer",
        "message": "Ready to analyze sentiment! Send POST requests to /sentiment_endpoint"
    }

# Batch processing function (optional - for processing multiple texts)
@app.function(image=image, timeout=600)
def batch_sentiment_analysis(texts: list) -> list:
    """
    Analyze sentiment for multiple texts at once
    More efficient for bulk processing
    """
    from transformers import pipeline
    
    sentiment_pipeline = pipeline("sentiment-analysis")
    results = []
    
    for text in texts:
        try:
            result = sentiment_pipeline(text)[0]
            results.append({
                "text": text,
                "label": result['label'],
                "score": round(result['score'], 3),
                "status": "success"
            })
        except Exception as e:
            results.append({
                "text": text,
                "error": str(e),
                "status": "error"
            })
    
    return results

# Local testing function
@app.local_entrypoint()
def test_local():
    """Test the function locally before deployment"""
    test_texts = [
        "I love this workshop!",
        "This is terrible",
        "It's an okay day",
        "Machine learning is amazing!"
    ]
    
    print("🧪 Testing sentiment analysis locally...")
    for text in test_texts:
        result = analyze_sentiment.remote(text)
        print(f"Text: '{text}'")
        print(f"Result: {result['label']} {result['emoji']} ({result['confidence']})")
        print("-" * 50)

if __name__ == "__main__":
    print("Sentiment Analysis API")
    print("To deploy: modal deploy sentiment_api.py")
    print("To test locally: modal run sentiment_api.py")
    
    # Show deployment info
    print(f"\nApp name: {app_name}")
    print("Endpoints after deployment:")
    print("- POST /sentiment_endpoint (for analysis)")  
    print("- GET /health_check (for health check)")
    
    # Run local test
    print("\n" + "="*50)
    test_local()