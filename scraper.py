import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def scrape_article(url):
    """
    Scrape text content from a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        str or None: Cleaned article text, or None if failed.
    """
    try:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove <script> and <style> elements
        for tag in soup(['script', 'style']):
            tag.decompose()

        content_selectors = [
            'article',
            '[role="main"]',
            '.content',
            '.article-content',
            '.post-content',
            '.entry-content',
            'main',
            '.main-content'
        ]

        text_content = ""

        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                text_content = ' '.join(elem.get_text(separator=' ', strip=True) for elem in elements)
                break

        if not text_content.strip():
            body = soup.find('body')
            if body:
                text_content = body.get_text(separator=' ', strip=True)

        text_content = clean_text(text_content)

        return text_content if len(text_content) >= 100 else None

    except requests.RequestException as e:
        print(f"[Request Error] {e}")
        return None
    except Exception as e:
        print(f"[Parsing Error] {e}")
        return None

def clean_text(text):
    """
    Clean and normalize text content.

    Args:
        text (str): Raw text.

    Returns:
        str: Cleaned text.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?;:()\-"\']', ' ', text)
    text = re.sub(r'[.,!?;:]{2,}', '.', text)
    return text.strip()

def is_valid_url(url):
    """
    Validate URL format.

    Args:
        url (str): URL to check.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
