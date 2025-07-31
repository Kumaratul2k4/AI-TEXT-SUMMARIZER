# AI-Powered Text Summarizer 📝

A powerful web application that automatically generates concise summaries from long articles, documents, or text blocks using state-of-the-art Natural Language Processing (NLP) models. This project is designed for both local development and easy deployment to a cloud platform.

## Features

- **URL Scraping**: Paste any article URL and get an instant summary.
- **Direct Text Input**: Copy and paste text directly for summarization.
- **AI-Powered**: Uses pre-trained transformer models (`sshleifer/distilbart-cnn-12-6`).
- **Web Interface**: Clean, modern web interface built with Flask.
- **Smart Text Processing**: Handles long documents by chunking and combining summaries.
- **Production Ready**: Includes `Dockerfile` and `Gunicorn` configuration for easy deployment.

## Technology Stack

- **Backend**: Python, Flask
- **AI/ML**: Hugging Face Transformers, PyTorch
- **Web Scraping**: `trafilatura`, BeautifulSoup, Requests
- **Deployment**: Docker, Gunicorn
- **Default Model**: `sshleifer/distilbart-cnn-12-6`

## Project Structure

```
AI-TEXT-SUMMARIZER/
├── app.py              # Main Flask application
├── scraper.py          # Web scraping functionality
├── summarizer.py       # AI summarization logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration for deployment
├── gunicorn_config.py  # Gunicorn server configuration
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

---

## Local Development Setup

Follow these steps to run the application on your local machine.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- At least 4GB RAM (for AI models)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/AI-TEXT-SUMMARIZER.git](https://github.com/Kumaratul2k4/AI-TEXT-SUMMARIZER.git)
   cd AI-TEXT-SUMMARIZER
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # Create the environment
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   The first time you run this, it will download the AI model (~1-2GB), which may take a few minutes.

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`.

---

## Deployment (Production)

This project is configured for easy deployment using Docker. The following instructions are for deploying to **Render**, a cloud platform with a user-friendly interface and a free tier.

### Step 1: Push to GitHub

Push your complete project, including the `Dockerfile` and `gunicorn_config.py`, to a GitHub repository.

### Step 2: Deploy on Render

1. **Sign up** or log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** and select **Web Service**.
3. **Connect your GitHub account** and select your project repository.
4. On the configuration screen, set the following:
   - **Name**: Give your service a unique name (e.g., `text-summarizer-app`).
   - **Environment**: Select **`Docker`**. Render will automatically find your `Dockerfile`.
   - **Instance Type**: Choose the **Free** plan.
     - **Note**: The free plan has limited RAM. If the app crashes, you may need to upgrade to a paid plan.
5. Click **Create Web Service**.

Render will now build the Docker image from your `Dockerfile` and deploy your application. Once complete, you will get a public URL to access your live summarizer app.

## Usage

### Web Interface

- **URL Summarization**: Paste an article URL into the input field and click "Summarize".
- **Direct Text Summarization**: Paste your text into the text area and click "Summarize".

### API Endpoint

- `POST /summarize`
  - **Headers**: `Content-Type: application/json`
  - **Body for URL**: `{"url": "https://example.com/article"}`
  - **Body for Text**: `{"text": "Your long text here..."}`
  - **Success Response**: `{"summary": "...", "original_length": 1000, "summary_length": 200}`

## Troubleshooting

- **Model Download Fails**: Ensure a stable internet connection and sufficient disk space.
- **Out of Memory Error**: This can happen on machines with low RAM or on free hosting tiers. Close other applications or upgrade your hosting plan.
- **Web Scraping Fails**: Some websites block scraping. Try copying the text directly.
- **Slow First Run**: The initial model download and loading takes 2-5 minutes. Subsequent runs are much faster as models are cached.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Hugging Face** for their incredible `transformers` library and pre-trained models.
- **The Flask and Gunicorn teams** for the powerful web framework and server.
- **The developers of `trafilatura` and BeautifulSoup** for making web scraping accessible.

---

**Happy Summarizing! 🚀**
