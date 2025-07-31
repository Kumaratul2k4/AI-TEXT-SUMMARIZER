import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def scrape_article(url):
    """
    Scrape text content from a given URL
    
    Args:
        url (str): The URL to scrape
    
    Returns:
        str: Extracted text content or None if failed
    """
    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send GET request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content areas
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
        
        # Try each selector to find the main content
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text_content += element.get_text(separator=' ', strip=True) + ' '
                break
        
        # If no specific content area found, extract from body
        if not text_content.strip():
            body = soup.find('body')
            if body:
                text_content = body.get_text(separator=' ', strip=True)
        
        # Clean up the text
        text_content = clean_text(text_content)
        
        # Return None if text is too short
        if len(text_content.strip()) < 100:
            return None
        
        return text_content
    
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing content: {e}")
        return None

def clean_text(text):
    """
    Clean and normalize text content
    
    Args:
        text (str): Raw text content
    
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-"\']', ' ', text)
    
    # Remove multiple consecutive punctuation
    text = re.sub(r'[.,!?;:]{2,}', '.', text)
    
    # Strip and return
    return text.strip()

def is_valid_url(url):
    """
    Check if a URL is valid
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False