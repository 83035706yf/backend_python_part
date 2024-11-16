import requests
from flask import current_app as app
from duckduckgo_search import DDGS
import urllib.parse
import time
import io
import sys

# Configure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# URL validation
def is_valid_url(url):
    """Check if a URL is valid and accessible."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Search for relevant resources using topic name and keywords
def search_resources(topic_name, keywords, max_results=3, retries=0, delay=5):
    query = f"{topic_name} {' '.join(keywords)}"
    for attempt in range(retries):
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, region="wt-wt", safesearch="moderate", timelimit="y")
                filtered_results = [
                    {"name": result["title"], "link": result["href"]}
                    for result in results[:max_results]
                    if "title" in result and "href" in result
                ]
                return filtered_results
        except Exception as e:
            if "Ratelimit" in str(e):
                print(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error fetching resources: {e}")
                break
    return []

# Main study plan transformation
def transform_study_plan(gpt_output):
    """Transform GPT output into structured JSON with resources."""
    sections = gpt_output.split('##')
    
    # Extract the title (first line of the output)
    title = sections[0].strip().replace("#", "").strip() if sections[0].strip().startswith("#") else "Untitled Study Plan"

    # Initialize dictionaries for each section
    introduction = {"description": "", "keywords": []}
    prerequisites = []
    main_curriculum = []
    advanced_topics = []

    # Process each section of the output
    for section in sections:
        section = section.strip()
        
        if section.startswith("Introduction"):
            lines = section.split("\n")
            introduction["description"] = lines[1].strip()
            for line in lines:
                if line.startswith("Keywords:"):
                    introduction["keywords"] = [kw.strip() for kw in line.replace("Keywords:", "").split(",")]

        elif section.startswith("Prerequisites") or section.startswith("Main Topics") or section.startswith("Advanced Topics"):
            lines = section.split("\n")[1:]
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("- **"):  # This line contains the topic and description
                    parts = line.split("**")
                    if len(parts) > 2:
                        topic_name = parts[1].strip()
                        description = parts[2].strip(":：").strip()

                        # Collect keywords for the topic
                        keywords = []
                        i += 1
                        while i < len(lines) and "Keywords:" in lines[i]:
                            keyword_line = lines[i].strip()
                            if "Keywords:" in keyword_line:
                                keywords = [kw.strip() for kw in keyword_line.replace("Keywords:", "").split(",")]
                            i += 1

                        # Search for relevant resources
                        resources = search_resources(topic_name, keywords)

                        # Create the entry
                        entry = {
                            "name": topic_name,
                            "description": description,
                            "keywords": keywords,
                            "resources": resources
                        }

                        if section.startswith("Prerequisites"):
                            prerequisites.append(entry)
                        elif section.startswith("Main Topics"):
                            main_curriculum.append(entry)
                        elif section.startswith("Advanced Topics"):
                            advanced_topics.append(entry)
                else:
                    i += 1  # Move to the next line if not a topic

    # Construct the final JSON format
    study_plan_json = {
        "title": title,
        "introduction": introduction,
        "prerequisite": prerequisites,
        "mainCurriculum": main_curriculum,
        "advancedTopics": advanced_topics
    }

    return study_plan_json
