# AI-Powered Text Summarizer 📝

A lightweight, powerful web application built with **Streamlit** that automatically generates concise summaries from long articles, documents, or text blocks. This project is optimized for low-memory deployment on cloud platforms.

## Features

- **URL Scraping**: Paste any article URL and get an instant summary.
- **Direct Text Input**: Copy and paste text directly for summarization.
- **Memory-Efficient AI**: Uses a lightweight, pre-trained transformer model (`t5-small`) to ensure it runs smoothly on free hosting plans.
- **Interactive UI**: Clean, modern, and responsive web interface built with Streamlit.
- **Production Ready**: Includes instructions for easy deployment to Streamlit Community Cloud.

## Technology Stack

- **Web Framework**: Streamlit
- **AI/ML**: Hugging Face Transformers, PyTorch
- **Web Scraping**: `trafilatura`, Requests
- **Deployment**: Streamlit Community Cloud
- **Default Model**: `t5-small`

## Project Structure

The `Dockerfile` is optional and only needed if you choose to deploy using Docker instead of Streamlit Community Cloud.

```
AI-TEXT-SUMMARIZER/
├── app.py              # Main Streamlit application
├── scraper.py          # Web scraping functionality
├── summarizer.py       # AI summarization logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Optional: For Docker-based deployments
└── README.md           # Project documentation
```

---

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1.  **Clone the repository**
2.  **Create and activate a virtual environment**
3.  **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application**
    ```bash
    streamlit run app.py
    ```
5.  **Open your browser**
    Navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

---

## Deployment (Production)

This project is configured for easy deployment directly to **Streamlit Community Cloud**.

### Prerequisites

- Your app code must be in a **public** GitHub repository.
- Your repository must contain a `requirements.txt` file.

### Deployment Steps

1.  **Sign up** or log in to [share.streamlit.io](https://share.streamlit.io).
2.  Click the **"New app"** button on the top right of your workspace.
3.  **Configure the deployment:**
    - **Repository**: Choose the GitHub repository for this project.
    - **Branch**: Select the branch you want to deploy (e.g., `main`).
    - **Main file path**: Enter the name of your main script (e.g., `app.py`).
4.  Click the **"Deploy!"** button.

Streamlit will now build the environment from your `requirements.txt` file and deploy your application. Once complete, you will get a public URL to access your live summarizer app.
