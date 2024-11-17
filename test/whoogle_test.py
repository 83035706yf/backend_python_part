import requests
from bs4 import BeautifulSoup
import io
import sys

# Configure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def search_whoogle(query, whoogle_url):
    """
    Search Whoogle and return a list of results.
    
    :param query: Search query string
    :param whoogle_url: URL of the Whoogle instance
    :return: List of results in the format {title: xxx, link: xxx}
    """
    try:
        # Prepare search URL
        search_url = f"{whoogle_url}/search"
        params = {"q": query}
        
        # Send the search request
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debugging: Extract and print potential result sections
        print("HTML Content Debugging:")
        sections = soup.find_all(['div', 'a', 'h3'])
        for idx, section in enumerate(sections[:10], start=1):
            print(f"Section {idx}: {section}")
        
        # Extract search results
        results = []
        for result in soup.find_all('div', class_='result'):  # Adjust class as needed
            title_tag = result.find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag.get('href')
                results.append({"title": title, "link": link})
        
        return results
    
    except requests.RequestException as e:
        print(f"Error during Whoogle search: {e}")
        return []

# Example usage
if __name__ == "__main__":
    whoogle_url = "http://localhost:5000"  # Replace with your Whoogle instance URL
    query = "test search using Whoogle"
    results = search_whoogle(query, whoogle_url)
    
    # Print the results
    if results:
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Title: {result['title']}, Link: {result['link']}")
    else:
        print("No results found.")
