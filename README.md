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
