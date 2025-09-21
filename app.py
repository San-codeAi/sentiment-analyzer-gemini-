import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# This is the new function that gets text from a URL
def get_article_text_from_url(url):
    """Fetches and extracts text from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return article_text
    except Exception as e:
        st.error(f"Error fetching URL: {e}")
        return None

# --- YOUR EXISTING CODE (IT'S PERFECT) ---

# Configure Gemini API key
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("GEMINI API key not found. Please check your .streamlit/secrets.toml file with your key.")
    st.stop()

# Your Gemini function - NO CHANGES NEEDED
def get_gemini_sentiment(text):
    """Gets a simple, one-word sentiment from the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = (
        "What is the overall sentiment of the following text? "
        "Please respond with only a single word: Positive, Negative, or Neutral.\n\n"
        f'Text: """{text}"""'
    )
    try:
        response = model.generate_content(prompt)
        # We just return the simple text response now, no more JSON!
        return response.text.strip()
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None


# --- NEW USER INTERFACE CODE ---
st.title("✨ Sentiment Analyzer powered by Gemini")

user_input = st.text_input("Enter a URL or text to analyze sentiment:", placeholder="https://example.com/article or I feel great today!")

if st.button("Analyze Sentiment"):
    if user_input:
        content_to_analyze = ""
        
        # Smartly decide if the input is a URL or plain text
        if user_input.strip().startswith('http'):
            with st.spinner("Fetching article from URL... 🌐"):
                content_to_analyze = get_article_text_from_url(user_input)
        else:
            content_to_analyze = user_input
        
        # If we have content, call your Gemini function
        if content_to_analyze:
            with st.spinner("Gemini is thinking... 🤔"):
                sentiment = get_gemini_sentiment(content_to_analyze)
                if sentiment:
                    st.success(f"### Sentiment: *{sentiment}*")
    else:
        st.warning("Please enter a URL or some text.")