# Main application file
import streamlit as st
from summarizer import TextSummarizer
from scraper import scrape_article

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Caching the Model ---
# Use st.cache_resource to load the model only once
@st.cache_resource
def load_summarizer():
    """Loads the summarization model."""
    print("--- Loading summarization model ---")
    return TextSummarizer()

# --- Main Application UI ---
def main():
    st.title("🤖 AI Text Summarizer")
    st.markdown("Transform long articles and documents into concise, intelligent summaries. Powered by Streamlit and Hugging Face Transformers.")

    # Load the model from cache
    summarizer_instance = load_summarizer()

    # Check if the model loaded successfully
    if not summarizer_instance or not summarizer_instance.summarizer:
        st.error("🚨 The summarization model failed to load. Please check the server logs or contact support.")
        return

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📄 Summarize from URL", "📝 Summarize Text"])

    with tab1:
        st.header("Summarize from an Article URL")
        url_input = st.text_input("Enter the article URL:", placeholder="https://example.com/article")

        if st.button("🚀 Summarize from URL", key="url_button"):
            if not url_input or not url_input.startswith("http"):
                st.warning("Please enter a valid URL.")
            else:
                with st.spinner("🧠 Scraping article and summarizing... This may take a moment."):
                    try:
                        scraped_text = scrape_article(url_input)
                        if not scraped_text or len(scraped_text.strip()) < 100:
                            st.error("Failed to scrape sufficient content. The website might be blocking scrapers. Please try another URL or paste the text directly.")
                        else:
                            summary = summarizer_instance.summarize(scraped_text)
                            display_summary(summary, scraped_text)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    with tab2:
        st.header("Summarize from Pasted Text")
        text_input = st.text_area("Paste your text here (at least 100 characters):", height=250, placeholder="Paste your article, document, or any long text here...")

        if st.button("🚀 Summarize Text", key="text_button"):
            if len(text_input.strip()) < 100:
                st.warning("Text is too short. Please provide at least 100 characters.")
            else:
                with st.spinner("🧠 AI is processing your content..."):
                    try:
                        summary = summarizer_instance.summarize(text_input)
                        display_summary(summary, text_input)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

def display_summary(summary, original_text):
    """Helper function to display the summarization results."""
    st.subheader("📋 Summary")
    
    original_len = len(original_text)
    summary_len = len(summary)
    compression_ratio = f"{((1 - summary_len / original_len) * 100):.1f}%" if original_len > 0 else "N/A"

    # Display stats in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Original Length", f"{original_len:,} chars")
    col2.metric("Summary Length", f"{summary_len:,} chars")
    col3.metric("Compression", compression_ratio)

    st.success(summary)

    with st.expander("Show Original Text"):
        st.text(original_text)

if __name__ == '__main__':
    main()
