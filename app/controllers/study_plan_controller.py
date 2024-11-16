import os
import openai
from flask import Blueprint, request, jsonify
from ..utils import transform_study_plan, search_resources

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
    Please generate a study plan for "{name}" with the following structure.
    For each prerequisites and main topic, provide a brief explanation and generate 3-5 keywords that represent the core ideas of the topic. These keywords should help identify relevant resources later. You can also include advanced topics for further exploration. 

1. **Introduction**:
   - Briefly explain what "{name}" is and why it’s important. Provide a high-level overview of the key concepts and applications.
   - Provide 3-5 keywords related to the introduction.

2. **Prerequisites**:
   - List important topics that should be understood before studying "{name}".
   - For each topic, provide a brief explanation and 3-5 keywords.

3. **Main Topics**:
   - Break down key "{name}" topics into smaller, focused topics.
    - For each topic, provide a brief explanation and 3-5 keywords.

4. **Advanced Topics**:
    - Include advanced topics for further exploration.
    - For each topic, provide a brief explanation and 3-5 keywords.
   
Example:

   # Quantum Mechanics

## Introduction:
   Quantum Mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles.
   Keywords: Quantum Mechanics, Subatomic Particles, Physical Properties, Atoms, Theory.

## Prerequisites:
     - **Classical Mechanics**: Understand Newton’s laws, concepts of force and motion, energy conservation, and basic oscillations.
     Keywords: Newton's Laws, Force, Energy Conservation, Oscillations.
     - **Linear Algebra**: Familiarity with vectors, matrices, and basic linear transformations.
     keywords: Vectors, Matrices, Linear Transformations.

## Main Topics:
   - **Introduction to Quantum Mechanics**: Historical background, key experiments, and the need for a new theory.
     keywords: Quantum Mechanics, Historical Background, Key Experiments, New Theory.
   - **Wave-particle Duality**: Understanding the dual nature of matter and radiation. De Broglie hypothesis, Heisenberg's uncertainty principle.
     keywords: Wave-particle Duality, De Broglie Hypothesis, Uncertainty Principle.
   - **Quantum States and Wave Functions**: Representing quantum states, probability amplitudes, and the Schrödinger equation.
     keywords: Quantum States, Wave Functions, Probability Amplitudes, Schrödinger Equation.
   - **Operators and Observables**: Mathematical operators, commutators, and measurement in quantum mechanics.
     keywords: Quantum Operators, Observables, Commutators, Measurement.
   - **Schrodinger Equation**: Solving the time-dependent and time-independent Schrödinger equations for simple systems.
     Keywords: Schrodinger Equation, Time-dependent, Time-independent, Simple Systems.
   - **Quantum Harmonic Oscillator**: Analyzing the quantum harmonic oscillator and its energy levels.
     Keywords: Harmonic Oscillator, Energy Levels, Quantum Analysis.
   - **Quantum Mechanics in Three Dimensions**: Extending quantum mechanics to three-dimensional systems.
     Keywords: Three Dimensions, Quantum Mechanics, Extended Systems.
   - **Quantum Statistics and Entanglement**: Understanding quantum statistics like Bose-Einstein and Fermi-Dirac statistics, entanglement, and Bell's theorem.
     Keywords: Quantum Statistics, Entanglement, Bell's Theorem.
   - **Quantum Mechanics Applications**: Applications in atomic, molecular, condensed matter physics, and quantum information theory.
     Keywords: Applications, Atomic Physics, Condensed Matter, Quantum Information.

## Advanced Topics:
   - **Quantum Field Theory**: Introduction to relativistic quantum mechanics and quantum field theory.
     Keywords: Quantum Field Theory, Relativistic Quantum Mechanics.
   - **Quantum Computing**: Basics of quantum computing, qubits, quantum gates, and quantum algorithms.
     Keywords: Quantum Computing, Qubits, Quantum Gates, Algorithms.
   - **Relativistic Quantum Mechanics**: Combining quantum mechanics with special relativity.
     Keywords: Relativistic Quantum Mechanics, Special Relativity.
    """

    try:
        # Call the GPT-4 API (use GPT-4 or another model as needed)
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Make sure your OpenAI account has access to GPT-4
            messages=[
                {"role": "system", "content": "You are an AI tutor providing personalized study plans. You may use the following prompt to generate a study plan for a specific topic. You can use whichever language the user's request is in to generate the study plan, but please keep following the same structure and format (i.e. '## Introduction:', '## Prerequisites:', '## Main Topics:', '## Advanced Topics:' and 'Resource:' should always be in english)."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the study plan from the response
        gpt_output = completion.choices[0].message['content'].strip()

        # Transform the GPT output into the desired JSON format
        study_plan_json = transform_study_plan(gpt_output)

        # Return the study plan in the response
        return jsonify({"StudyPlan": study_plan_json})

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500

@bp.route('/test_search_resources', methods=['POST'])
def test_search_resources():
    """Test API for searching resources."""
    try:
        # Parse the request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON request body"}), 400

        topic_name = data.get("topic_name")
        keywords = data.get("keywords")
        # max_results = data.get("max_results", 10)

        # Validate inputs
        if not topic_name or not isinstance(keywords, list):
            return jsonify({"error": "Invalid input: 'topic_name' must be a string and 'keywords' must be a list"}), 400

        # Perform the search
        resources = search_resources(topic_name, keywords)
        return jsonify({"topic_name": topic_name, "keywords": keywords, "resources": resources})

    except Exception as e:
        return jsonify({"error": str(e)}), 500