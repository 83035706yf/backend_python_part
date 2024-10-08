import os
import openai
from flask import Blueprint, request, jsonify

bp = Blueprint('study_plan_controller', __name__, url_prefix='/api')

# Load your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the route for generating study plans
@bp.route('/studyplan', methods=['POST'])
def generate_study_plan():
    # Extract the request data
    study_plan_request = request.get_json()
    name = study_plan_request.get('Name')

    # Mr. Ranedeer prompt - Customize this prompt based on the model instructions
    prompt = f"""
    Please generate a study plan for "{name}" with the following structure:

1. **Introduction**:
   - Briefly explain what "{name}" is and why it’s important.

2. **Prerequisites**:
   - List important topics that should be understood before studying "{name}".

3. **Main Topics**:
   - Break down key "{name}" topics.
   - For each topic, provide a list of recommended resources (books, websites, etc.) to aid learning.
    """

    try:
        # Call the GPT-4 API (use GPT-4 or another model as needed)
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Make sure your OpenAI account has access to GPT-4
            messages=[
                {"role": "system", "content": "You are an AI tutor providing personalized study plans."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the study plan from the response
        study_plan = completion.choices[0].message['content'].strip()

        # Return the study plan in the response
        return jsonify({"StudyPlan": study_plan})

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500
