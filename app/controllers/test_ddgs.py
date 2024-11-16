import sys
import io
import time
from duckduckgo_search import DDGS

# Configure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def search_resources_with_backoff(topic_name, keywords, max_results=3, retries=0, delay=5):
    query = f"{topic_name} {' '.join(keywords)}"
    print(f"Constructed Query: {query}")
    for attempt in range(retries):
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, region="wt-wt", safesearch="moderate", timelimit="y")
                filtered_results = [
                    {"name": result["title"], "link": result["href"]}
                    for result in results[:max_results]
                    if "title" in result and "href" in result
                ]
                return {"topic_name": topic_name, "keywords": keywords, "resources": filtered_results}
        except Exception as e:
            if "Ratelimit" in str(e):
                print(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error fetching resources: {e}")
                break
    print("Exhausted retries.")
    return {"topic_name": topic_name, "keywords": keywords, "resources": []}


# Test the function
result = search_resources_with_backoff("线性代数", ["向量", "矩阵", "线性变换"], max_results=5)

# Safely print the results
resources = result.get("resources", [])
if resources:
    print("\nFetched Resources:")
    for idx, resource in enumerate(resources, start=1):
        print(f"{idx}. Name: {resource['name']}")
        print(f"   Link: {resource['link']}")
else:
    print("No resources found.")