import os
import openai
from flask import Blueprint, request, jsonify

bp = Blueprint('study_plan_controller', __name__, url_prefix='/api')

@bp.route('/studyplan', methods=['POST'])
def generate_study_plan():
    study_plan_request = request.get_json()
    name = study_plan_request.get('Name')
    description = study_plan_request.get('Description')

    prompt = f"Generate a study plan based on the topic \"{name}\" and its description \"{description}\"."

    openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have the OPENAI_API_KEY environment variable set

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant tasked with generating study plans."},
                {"role": "user", "content": prompt}
            ]
        )
        study_plan = completion.choices[0].message['content'].strip()
        return jsonify({"StudyPlan": study_plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

