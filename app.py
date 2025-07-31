from flask import Flask, render_template, request, jsonify
from scraper import scrape_article
from summarizer import TextSummarizer # Import the new TextSummarizer class
import os
import socket

app = Flask(__name__)

# --- Key Change 1: Load the model once on startup ---
# This creates a global instance of the summarizer that all requests can use.
# This is crucial for performance as model loading is slow.
print("Loading summarization model. This may take a moment...")
try:
    # Default model is "sshleifer/distilbart-cnn-12-6" (fast and good quality)
    # For higher quality (but slower), you could use:
    # summarizer_instance = TextSummarizer(model_name="facebook/bart-large-cnn")
    summarizer_instance = TextSummarizer()
    print("✅ Model loaded successfully and is ready to use.")
except Exception as e:
    print(f"❌ Critical Error: Failed to load the summarizer model: {e}")
    # If the model fails to load, we create a placeholder to avoid crashing the app
    # but it will return an error message on API calls.
    class FailedSummarizer:
        def summarize(self, text, **kwargs):
            return "Error: The summarization model failed to load. Please check the server logs."
    summarizer_instance = FailedSummarizer()


@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint to handle summarization of text or a URL."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request. Expected JSON.'}), 400

        url = data.get('url')
        text = data.get('text')
        
        text_to_summarize = ""
        
        if url:
            print(f"Received request to scrape and summarize URL: {url}")
            scraped_text = scrape_article(url)
            if not scraped_text or len(scraped_text) < 50:
                return jsonify({'error': 'Failed to scrape sufficient content from the URL.'}), 400
            text_to_summarize = scraped_text
        elif text:
            print("Received request to summarize provided text.")
            text_to_summarize = text
        else:
            return jsonify({'error': 'Please provide either a "url" or "text" field.'}), 400
        
        # --- Key Change 2: Use the summarize method from our instance ---
        summary = summarizer_instance.summarize(text_to_summarize)
        
        original_word_count = len(text_to_summarize.split())
        summary_word_count = len(summary.split())
        
        print(f"Successfully summarized text from {original_word_count} words to {summary_word_count} words.")
        
        return jsonify({
            'summary': summary,
            'original_text': text_to_summarize,
            'original_length': original_word_count,
            'summary_length': summary_word_count
        })
    
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

def get_local_ip():
    """Utility function to find the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    # Ensure the templates directory exists for Flask
    if not os.path.exists('templates'):
        os.makedirs('templates')
        # Create a basic index.html if it doesn't exist
        if not os.path.exists('templates/index.html'):
            with open('templates/index.html', 'w') as f:
                f.write('<h1>Summarizer API is running</h1>')
    
    # --- Key Change 3: Print server addresses ---
    port = 5000
    local_ip = get_local_ip()
    
    print("\n" + "="*50)
    print("Flask server is running and ready.")
    print(f"Access the application at:")
    print(f"-> Local:   http://127.0.0.1:{port}")
    print(f"-> Network: http://{local_ip}:{port}")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)