# AI-Powered Text Summarizer 📝

A lightweight, powerful web application built with **Streamlit** that automatically generates concise summaries from long articles, documents, or text blocks. This project is optimized for low-memory deployment on cloud platforms like Render.

## Features

- **URL Scraping**: Paste any article URL and get an instant summary.
- **Direct Text Input**: Copy and paste text directly for summarization.
- **Memory-Efficient AI**: Uses a lightweight, pre-trained transformer model (`t5-small`) to ensure it runs smoothly on free hosting plans.
- **Interactive UI**: Clean, modern, and responsive web interface built with Streamlit.
- **Production Ready**: Includes a `Dockerfile` for easy, robust deployment.

## Technology Stack

- **Web Framework**: Streamlit
- **AI/ML**: Hugging Face Transformers, PyTorch
- **Web Scraping**: `trafilatura`, Requests
- **Deployment**: Docker, Render
- **Default Model**: `t5-small`

## Project Structure

```
AI-TEXT-SUMMARIZER/
├── app.py              # Main Streamlit application
├── scraper.py          # Web scraping functionality
├── summarizer.py       # AI summarization logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration for deployment
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

## Deployment (Production on Render)

This project is configured for easy deployment using Docker on the **Render** cloud platform.

### Step 1: Push to GitHub

Push your complete project, including the `Dockerfile`, to a GitHub repository.

### Step 2: Deploy on Render

1.  **Sign up** or log in to [dashboard.render.com](https://dashboard.render.com).
2.  Click **New +** and select **Web Service**.
3.  **Connect your GitHub account** and select your project repository.
4.  On the configuration screen, set the following:
    - **Environment**: Select **`Docker`**. Render will automatically find and use your `Dockerfile`.
    - **Instance Type**: Choose the **Free** plan.
5.  Click **Create Web Service**.

Render will now build the Docker image and deploy your Streamlit application. Once complete, you will get a public URL to access your live summarizer app.
