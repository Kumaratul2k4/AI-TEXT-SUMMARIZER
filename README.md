# AI-Powered Text Summarizer 📝

A lightweight, powerful web application that automatically generates concise summaries from long articles, documents, or text blocks. This project uses state-of-the-art Natural Language Processing (NLP) and is **optimized for low-memory deployment** on cloud platforms like Render's free tier.

## Features

- **URL Scraping**: Paste any article URL and get an instant summary.
- **Direct Text Input**: Copy and paste text directly for summarization.
- **Memory-Efficient AI**: Uses a lightweight, pre-trained transformer model (`t5-small`) to ensure it runs smoothly on free hosting plans.
- **Web Interface**: Clean, modern, and responsive web interface built with Flask.
- **Smart Text Processing**: Handles long documents by intelligently chunking text and summarizing each part.
- **Production Ready**: Includes a `Dockerfile` and `Gunicorn` configuration for easy, robust deployment.

## Technology Stack

- **Backend**: Python, Flask
- **AI/ML**: Hugging Face Transformers, PyTorch
- **Web Scraping**: `trafilatura`, Requests
- **Deployment**: Docker, Gunicorn
- **Default Model**: `t5-small` (a lightweight and efficient model)

## Project Structure
AI-TEXT-SUMMARIZER/
├── app.py              # Main Flask application
├── scraper.py          # Web scraping functionality (using trafilatura)
├── summarizer.py       # AI summarization logic (optimized for t5-small)
├── requirements.txt    # Lean Python dependencies
├── Dockerfile          # Container configuration for deployment
├── gunicorn_config.py  # Gunicorn server configuration
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation 
---

## Local Development Setup

Follow these steps to run the application on your local machine.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- At least 2GB RAM recommended

### Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/AI-TEXT-SUMMARIZER.git](https://github.com/your-username/AI-TEXT-SUMMARIZER.git)
    cd AI-TEXT-SUMMARIZER
    ```

2.  **Create and activate a virtual environment** (recommended)
    ```bash
    # Create the environment
    python -m venv venv
    
    # On Windows
    venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the optimized dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    python app.py
    ```
    The first time you run this, it will download the lightweight AI model (~240MB), which should only take a minute or two.

5.  **Open your browser**
    Navigate to `http://127.0.0.1:5000`.

---

## Deployment (Production)

This project is configured for easy deployment using Docker. The following instructions are for deploying to **Render**, a cloud platform with a user-friendly interface and a free tier.

### Step 1: Push to GitHub

Push your complete project, including the `Dockerfile` and `gunicorn_config.py`, to a GitHub repository.

### Step 2: Deploy on Render

1.  **Sign up** or log in to [dashboard.render.com](https://dashboard.render.com).
2.  Click **New +** and select **Web Service**.
3.  **Connect your GitHub account** and select your project repository.
4.  On the configuration screen, set the following:
    - **Name**: Give your service a unique name (e.g., `text-summarizer-app`).
    - **Environment**: Select **`Docker`**. Render will automatically find your `Dockerfile`.
    - **Instance Type**: Choose the **Free** plan.
      - **Note**: This project has been specifically optimized to run reliably on Render's free tier (512MB RAM).
5.  Click **Create Web Service**.

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
  - **Success Response**: `{"summary": "...", "original_length": 1000, "summary_length": 200}` (lengths are in characters)

## Troubleshooting

- **Model Download Fails**: Ensure a stable internet connection and sufficient disk space (~500MB).
- **Out of Memory Error**: Unlikely with the new optimizations, but if it occurs on other platforms, it indicates the hosting environment has very low RAM. This code is optimized for 512MB.
- **Web Scraping Fails**: Some websites use advanced techniques to block scraping. If a URL fails, try copying the text directly.
- **Slow First Run**: The initial model download and loading takes a minute or two. Subsequent runs are much faster as models are cached.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Hugging Face** for their incredible `transformers` library and community models.
- **The Flask and Gunicorn teams** for the powerful web framework and server.
- **The developers of `trafilatura`** for making robust web scraping so accessible.

---

**Happy Summarizing! 🚀**
