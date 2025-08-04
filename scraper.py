import trafilatura
import requests

def scrape_article(url):
    """
    Scrapes the main text content from a given URL using trafilatura.

    Args:
        url (str): The URL to scrape.

    Returns:
        str or None: Cleaned article text, or None if it fails.
    """
    print(f"Attempting to scrape URL: {url}")
    try:
        # Download the page first
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is None:
            print(f"Failed to download content from {url}")
            return None

        # Extract the main content
        # include_comments=False and include_tables=False make it cleaner
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=True # Use only the main content extractor
        )
        
        if text and len(text) > 100:
            print("✅ Successfully scraped content.")
            return text
        else:
            print("Scraped content was too short or empty.")
            return None

    except (requests.exceptions.RequestException, Exception) as e:
        print(f"❌ An error occurred during scraping: {e}")
        return None
