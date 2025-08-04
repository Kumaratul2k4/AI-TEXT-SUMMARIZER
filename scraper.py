import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def scrape_article(url):
    """
    Scrape text content from a given URL.
    Returns cleaned article text or None if failed.
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

        soup = BeautifulSoup(response.content, 'lxml')  # Use lxml: faster & lower memory

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()

        content_selectors = [
            'article', '[role="main"]', '.content',
            '.article-content', '.post-content',
            '.entry-content', 'main', '.main-content'
        ]

        text_content = ""
        for selector in content_selectors:
            for element in soup.select(selector):
                text_content += element.get_text(separator=' ', strip=True) + ' '
            if text_content.strip():
                break

        if not text_content.strip():
            body = soup.find('body')
            if body:
                text_content = body.get_text(separator=' ', strip=True)

        cleaned = clean_text(text_content)
        return cleaned if len(cleaned) >= 100 else None

    except requests.RequestException as e:
        print(f"[URL Error] {e}")
        return None
    except Exception as e:
        print(f"[Parsing Error] {e}")
        return None

def clean_text(text):
    """
    Normalize and clean the raw text.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?;:()\'"-]', '', text)
    text = re.sub(r'([.,!?;:]){2,}', r'\1', text)
    return text.strip()

def is_valid_url(url):
    """
    Basic URL format validation.
    """
    try:
        result = urlparse(url)
        return bool(result.scheme and result.netloc)
    except:
        return False
