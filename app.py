from flask import Flask, render_template, request, jsonify
import os
import socket
from summarizer import TextSummarizer
from scraper import scrape_article

app = Flask(__name__)

# Use a lightweight model (or switch to a lighter alternative if needed)
summarizer_instance = None

@app.before_first_request
def load_model():
    """Load the summarization model once before first request."""
    global summarizer_instance
    print("⏳ Loading summarization model...")
    try:
        summarizer_instance = TextSummarizer()
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        summarizer_instance = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    global summarizer_instance
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request. Expected JSON.'}), 400

        url = data.get('url')
        text = data.get('text')

        if not summarizer_instance:
            return jsonify({'error': 'Model not loaded. Please retry later.'}), 500

        if url:
            print(f"🔗 Scraping and summarizing from URL: {url}")
            scraped_text = scrape_article(url)
            if not scraped_text or len(scraped_text.strip()) < 50:
                return jsonify({'error': 'Failed to scrape sufficient content from the URL.'}), 400
            text_to_summarize = scraped_text
        elif text:
            print("📝 Summarizing provided text.")
            if len(text.strip()) < 50:
                return jsonify({'error': 'Text too short to summarize.'}), 400
            text_to_summarize = text
        else:
            return jsonify({'error': 'Provide either "url" or "text".'}), 400

        summary = summarizer_instance.summarize(text_to_summarize)

        return jsonify({
            'summary': summary,
            'original_text': text_to_summarize,
            'original_length': len(text_to_summarize.split()),
            'summary_length': len(summary.split())
        })

    except Exception as e:
        print(f"⚠️ Summarization error: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

def get_local_ip():
    """Get the machine's local IP."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write('<h1>Summarizer API is running</h1>')

    port = 5000
    local_ip = get_local_ip()

    print("\n" + "="*50)
    print("🚀 Flask server started")
    print(f"🔗 Local:   http://127.0.0.1:{port}")
    print(f"🌐 Network: http://{local_ip}:{port}")
    print("="*50 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port)
