import streamlit as st
import requests
import json
import time
from typing import Dict, Any

# Configure the page
st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://backend:8000"  # Docker service name
# For local development, use: API_BASE_URL = "http://localhost:8000"

def check_api_health() -> bool:
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def predict_sentiment(text: str) -> Dict[str, Any]:
    """Send text to API for sentiment prediction"""
    try:
        payload = {"text": text}
        response = requests.post(
            f"{API_BASE_URL}/predict", 
            json=payload, 
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def batch_predict_sentiment(texts: list) -> Dict[str, Any]:
    """Send multiple texts to API for batch prediction"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch_predict", 
            json=texts, 
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def display_sentiment_result(result: Dict[str, Any]):
    """Display sentiment prediction result with styling"""
    if not result:
        return
    
    label = result['label']
    score = result['score']
    confidence = result['confidence_percentage']
    
    # Color coding based on sentiment
    if label == 'Positive':
        color = "#28a745"  # Green
        emoji = "😊"
    else:
        color = "#dc3545"  # Red
        emoji = "😞"
    
    # Display result in columns
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### {emoji} Sentiment: **{label}**")
    
    with col2:
        st.metric("Confidence", f"{confidence}%")
    
    with col3:
        st.metric("Raw Score", f"{score:.4f}")
    
    # Progress bar for confidence
    st.progress(confidence / 100)
    
    # Confidence interpretation
    if confidence >= 80:
        st.success("🎯 High confidence prediction!")
    elif confidence >= 60:
        st.info("📊 Moderate confidence prediction")
    else:
        st.warning("⚠️ Low confidence prediction")

def main():
    # Title and description
    st.title("🎭 Sentiment Analysis with BERT")
    st.markdown("---")
    
    # Sidebar for API status
    with st.sidebar:
        st.header("API Status")
        
        # Check API health
        if check_api_health():
            st.success("✅ API is healthy")
        else:
            st.error("❌ API is not responding")
            st.info("Make sure the FastAPI backend is running")
        
        st.markdown("---")
        st.header("About")
        st.info("""
        This app uses a fine-tuned BERT model for sentiment analysis.
        
        **Features:**
        - Single text prediction
        - Batch text prediction
        - Confidence scores
        - Real-time analysis
        """)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Single Prediction", "📊 Batch Analysis", "🧪 Examples"])
    
    with tab1:
        st.header("Analyze Single Text")
        
        # Text input
        user_text = st.text_area(
            "Enter text to analyze:",
            placeholder="Type or paste your text here...",
            height=150
        )
        
        # Prediction button
        if st.button("🚀 Analyze Sentiment", type="primary"):
            if user_text.strip():
                with st.spinner("Analyzing sentiment..."):
                    result = predict_sentiment(user_text.strip())
                
                if result:
                    st.markdown("---")
                    st.subheader("Results")
                    
                    # Display the input text
                    st.markdown("**Input Text:**")
                    st.info(user_text)
                    
                    # Display results
                    display_sentiment_result(result)
            else:
                st.warning("Please enter some text to analyze!")
    
    with tab2:
        st.header("Batch Text Analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload a text file (one text per line):",
            type=['txt']
        )
        
        # Manual text input for batch
        batch_text = st.text_area(
            "Or enter multiple texts (one per line):",
            placeholder="Enter multiple texts, one per line...",
            height=200
        )
        
        if st.button("🔍 Analyze All", type="primary"):
            texts_to_analyze = []
            
            # Process uploaded file
            if uploaded_file:
                content = uploaded_file.read().decode('utf-8')
                file_texts = [line.strip() for line in content.split('\n') if line.strip()]
                texts_to_analyze.extend(file_texts)
            
            # Process manual input
            if batch_text.strip():
                manual_texts = [line.strip() for line in batch_text.split('\n') if line.strip()]
                texts_to_analyze.extend(manual_texts)
            
            if texts_to_analyze:
                with st.spinner(f"Analyzing {len(texts_to_analyze)} texts..."):
                    results = batch_predict_sentiment(texts_to_analyze)
                
                if results and 'predictions' in results:
                    st.markdown("---")
                    st.subheader(f"Results for {len(results['predictions'])} texts")
                    
                    # Summary statistics
                    predictions = results['predictions']
                    positive_count = sum(1 for p in predictions if p['label'] == 'Positive')
                    negative_count = len(predictions) - positive_count
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Analyzed", len(predictions))
                    with col2:
                        st.metric("Positive", positive_count)
                    with col3:
                        st.metric("Negative", negative_count)
                    
                    # Detailed results
                    st.markdown("### Detailed Results")
                    for i, pred in enumerate(predictions, 1):
                        with st.expander(f"Text {i}: {pred['label']} ({pred['confidence_percentage']:.1f}%)"):
                            st.write(f"**Text:** {pred['text']}")
                            display_sentiment_result(pred)
            else:
                st.warning("Please provide texts to analyze!")
    
    with tab3:
        st.header("Try These Examples")
        
        examples = [
            "I absolutely love this movie! It's fantastic!",
            "This was the worst experience ever. Completely disappointed.",
            "The weather is okay today, nothing special.",
            "Amazing product! Highly recommend to everyone!",
            "Not sure how I feel about this...",
            "This restaurant has great food and excellent service!",
            "The movie was boring and too long.",
            "I'm feeling neutral about this decision."
        ]
        
        for i, example in enumerate(examples):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Example {i+1}:** {example}")
            
            with col2:
                if st.button(f"Analyze", key=f"example_{i}"):
                    with st.spinner("Analyzing..."):
                        result = predict_sentiment(example)
                    
                    if result:
                        st.write(f"**{result['label']}** ({result['confidence_percentage']}%)")

if __name__ == "__main__":
    main()
