from flask import Flask, render_template, request, jsonify
from summarizer import TextSummarizer
from scraper import scrape_article
import os

app = Flask(__name__)

# --- Model Loading ---
# Load the model when the application starts.
# Gunicorn's `preload_app = True` ensures this runs once before workers are forked.
summarizer_instance = None
try:
    summarizer_instance = TextSummarizer()
except Exception as e:
    print(f"FATAL: Could not initialize TextSummarizer. The app will run but summarization will fail. Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_route():
    if not summarizer_instance or not summarizer_instance.summarizer:
        return jsonify({'error': 'The summarization model is not available. Please contact support or check server logs.'}), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request format. Expected JSON.'}), 400

        text_to_summarize = ""
        source_type = ""

        if 'url' in data and data['url']:
            source_type = "url"
            url = data['url']
            print(f"🔗 Received URL for summarization: {url}")
            scraped_text = scrape_article(url)
            if not scraped_text or len(scraped_text.strip()) < 100:
                return jsonify({'error': 'Failed to scrape sufficient content from the URL. Please try another article or paste the text directly.'}), 400
            text_to_summarize = scraped_text
        elif 'text' in data and data['text']:
            source_type = "text"
            text = data['text']
            print("📝 Received text for summarization.")
            if len(text.strip()) < 100:
                return jsonify({'error': 'Text is too short to summarize. Please provide at least 100 characters.'}), 400
            text_to_summarize = text
        else:
            return jsonify({'error': 'Request must include either a "url" or "text" field.'}), 400

        summary = summarizer_instance.summarize(text_to_summarize)

        # Return character lengths to match the frontend JavaScript calculation
        response_data = {
            'summary': summary,
            'original_length': len(text_to_summarize),
            'summary_length': len(summary)
        }
        
        print("✅ Summarization complete.")
        return jsonify(response_data)

    except Exception as e:
        print(f"⚠️ An unexpected error occurred during summarization: {e}")
        return jsonify({'error': 'An internal server error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    # This block is mainly for local development.
    # For production, Gunicorn is used.
    print("🚀 Starting Flask server for local development...")
    app.run(host='0.0.0.0', port=5000, debug=True)
