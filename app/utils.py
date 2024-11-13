import requests
from neo4j import GraphDatabase
from flask import current_app as app

# URL validation
def is_valid_url(url):
    """Check if a URL is valid and accessible."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# GPT resource validation
def validate_gpt_resources(gpt_resources):
    """Validate each resource from GPT."""
    valid_resources = []
    for resource in gpt_resources:
        if is_valid_url(resource["link"]):
            valid_resources.append(resource)
    return valid_resources

# Main study plan transformation
def transform_study_plan(gpt_output):
    # Split the output into sections based on headers
    sections = gpt_output.split('##')
    
    # Extract the title (first line of the output)
    title = sections[0].strip().replace("#", "").strip() if sections[0].strip().startswith("#") else "Untitled Study Plan"

    # Initialize dictionaries for each section
    introduction = ""
    prerequisites = []
    main_curriculum = []
    advanced_topics = []

    # Process each section of the output
    for section in sections:
        section = section.strip()
        
        if section.startswith("Introduction"):
            introduction = section.replace("Introduction:", "").strip()
        
        elif section.startswith("Prerequisites") or section.startswith("Main Topics") or section.startswith("Advanced Topics"):
            lines = section.split("\n")[1:]
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("- **"):  # This line contains the topic and description
                    parts = line.split("**")
                    if len(parts) > 2:
                        topic_name = parts[1].strip()
                        
                        # Ensure the description does not include a leading colon
                        description_part = parts[2].strip()
                        if description_part.startswith(":") | description_part.startswith("："):
                            description = description_part[1:].strip()  # Remove the leading colon
                        else:
                            description = description_part.strip()

                        # Query Neo4j for relevant resources
                        existing_resources = app.neo4j_db.query_resources(topic_name)
                        
                        # Collect GPT resources for this topic
                        gpt_resources = []
                        i += 1  # Move to the potential resource line
                        while i < len(lines) and "Resource: " in lines[i]:
                            resource_line = lines[i].strip()

                            # Safer splitting of the URL
                            if "https://" in resource_line:
                                try:
                                    resource_link = resource_line.split("https://")[1].split(")")[0].strip()
                                    resource_link = "https://" + resource_link
                                except IndexError:
                                    resource_link = None  # Handle error gracefully

                            # Optionally parse resource name if provided (e.g., in square brackets)
                            if "[" in resource_line and "]" in resource_line:
                                resource_name = resource_line.split("[")[1].split("]")[0].strip()
                            else:
                                resource_name = "Unnamed resource"

                            # Only add the resource if the link is valid
                            if resource_link:
                                gpt_resources.append({
                                    "name": resource_name,
                                    "link": resource_link
                                })
                            i += 1  # Move to the next line
                        
                        # Validate GPT resources
                        valid_gpt_resources = validate_gpt_resources(gpt_resources)

                        # Merge Neo4j resources with valid GPT resources
                        all_resources = existing_resources + valid_gpt_resources

                        # If no resources are found, skip adding an empty resource list
                        if all_resources:
                            entry = {
                                "name": topic_name,
                                "description": description,
                                "resources": all_resources
                            }
                        else:
                            entry = {
                                "name": topic_name,
                                "description": description,
                                "resources": []
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

    # Return the JSON as a dictionary (to be converted later if needed)
    return study_plan_json

