import streamlit as st
import requests
import plotly.graph_objects as go
from typing import List, Dict, Any

API_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="Financial News Sentiment Analyzer",
    page_icon="📊",
    layout="wide"
)

# ------------------- UI Components -------------------

def render_header():
    st.title("Financial News Sentiment Analyzer")
    st.markdown("""
    This application analyzes financial news articles and determines their sentiment impact on the market.
    Enter a topic to search for relevant news articles and get their sentiment analysis.
    """)

def render_sidebar():
    with st.sidebar:
        st.header("Search Parameters")
        topic = st.text_input("Topic", value="Finance")
        num_articles = st.slider("Number of Articles", min_value=1, max_value=10, value=5)
        
        analyze_button = st.button("Analyze", type="primary")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app uses:
        - Brave Search API for fetching relevant news
        - Google's Gemini AI for sentiment analysis
        - Streamlit for the UI
        """)
        
        return topic, num_articles, analyze_button

def render_sentiment_indicator(sentiment: str, confidence: int):
    sentiment_values = {
        "Very Bearish": -2,
        "Bearish": -1,
        "Neutral": 0,
        "Bullish": 1,
        "Very Bullish": 2
    }
    
    value = sentiment_values.get(sentiment, 0)
    
    # Apply confidence as a modifier to position
    position = value * (confidence / 10)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=position,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{sentiment} (Confidence: {confidence}/10)"},
        gauge={
            'axis': {'range': [-2, 2], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-2, -1], 'color': "red"},
                {'range': [-1, -0.2], 'color': "lightcoral"},
                {'range': [-0.2, 0.2], 'color': "lightgray"},
                {'range': [0.2, 1], 'color': "lightgreen"},
                {'range': [1, 2], 'color': "green"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': position
            }
        }
    ))
    
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def render_article_card(result: Dict[str, Any], index: int = 0):
    with st.container():
        st.subheader(result["title"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### Summary")
            st.write(result["summary"])
            
            st.markdown("#### Key Insights")
            for insight in result["insights"]:
                st.markdown(f"- {insight}")
            
            st.markdown(f"[Read Full Article]({result['url']})")
        
        with col2:
            sentiment_fig = render_sentiment_indicator(
                result["sentiment"], 
                result["confidence"]
            )
            st.plotly_chart(sentiment_fig, use_container_width=True, key=f"chart_{index}_{result['url'][-8:]}")
        
        st.markdown("---")

def fetch_and_analyze(topic: str, num_articles: int):
    try:
        with st.spinner("Analyzing news articles..."):
            response = requests.post(
                API_URL, 
                json={"topic": topic, "num_articles": num_articles}
            )
            response.raise_for_status()
            return response.json()["results"]
    except requests.RequestException as e:
        st.error(f"Error fetching results: {str(e)}")
        return []

# ------------------- Main App -------------------

def main():
    render_header()
    topic, num_articles, analyze_button = render_sidebar()
    
    if analyze_button or 'results' in st.session_state:
        if analyze_button:
            results = fetch_and_analyze(topic, num_articles)
            st.session_state.results = results
        else:
            results = st.session_state.results
        
        if results:
            # Calculate overall sentiment stats
            sentiment_counts = {
                "Very Bullish": 0, 
                "Bullish": 0,
                "Neutral": 0,
                "Bearish": 0,
                "Very Bearish": 0
            }
            
            for result in results:
                if result["sentiment"] in sentiment_counts:
                    sentiment_counts[result["sentiment"]] += 1
            
            # Display results
            st.header(f"Analysis Results for '{topic}'")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Articles", len(results))
            
            bullish_count = sentiment_counts["Very Bullish"] + sentiment_counts["Bullish"]
            bearish_count = sentiment_counts["Very Bearish"] + sentiment_counts["Bearish"]
            
            col2.metric("Bullish Articles", bullish_count)
            col3.metric("Bearish Articles", bearish_count)
            
            # Render each article
            for i, result in enumerate(results):
                render_article_card(result, i)
        else:
            st.info("No results found. Try a different topic.")
    else:
        st.info("Enter a topic and click 'Analyze' to get started.")

if __name__ == "__main__":
    main()
