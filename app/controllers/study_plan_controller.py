import os
import openai
from flask import Blueprint, request, jsonify
from ..utils import transform_study_plan

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
    For each prerequisites and main topic, provide a brief explanation and suggest at least one relevant resource, including web links to reliable articles, books, web pages, or papers. You can also include advanced topics for further exploration. The resources should be freely accessible to the user. Better to provide resources that are expressed in the language the user requested the study plan in (i.e. Prioritize the provision of Chinese language sites if user's request is in Chinese).

1. **Introduction**:
   - Briefly explain what "{name}" is and why it’s important.

2. **Prerequisites**:
   - List important topics that should be understood before studying "{name}".

3. **Main Topics**:
   - Break down key "{name}" topics.

4. **Advanced Topics**:
    - Include advanced topics for further exploration.
   
Example:

   # Quantum Mechanics

## Introduction:
   Quantum Mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles.

## Prerequisites:
   - **Classical Mechanics**: Understand Newton’s laws, concepts of force and motion, energy conservation, and basic oscillations.
     - Resource: [Classical Mechanics (MIT)](https://ocw.mit.edu/courses/physics/8-01-classical-mechanics-fall-1999/)
   - **Linear Algebra**: Familiarity with vectors, matrices, and basic linear transformations.
     - Resource: [Linear Algebra (Khan Academy)](https://www.khanacademy.org/math/linear-algebra)

## Main Topics:
   - **Introduction to Quantum Mechanics**: Historical background, key experiments, and the need for a new theory.
     - Resource: [Quantum Mechanics Overview (Wikipedia)](https://en.wikipedia.org/wiki/Quantum_mechanics)
   - **Wave-particle Duality**: Understanding the dual nature of matter and radiation. De Broglie hypothesis, Heisenberg's uncertainty principle.
     - Resource: [Wave-Particle Duality (Khan Academy)](https://www.khanacademy.org/science/physics/quantum-physics/quantum-physics-101/a/wave-particle-duality)
   - **Quantum States and Wave Functions**: Representing quantum states, probability amplitudes, and the Schrödinger equation.
     - Resource: [Quantum States (Coursera)](https://www.coursera.org/lecture/quantum-mechanics/quantum-states-YtTYv)
   - **Operators and Observables**: Mathematical operators, commutators, and measurement in quantum mechanics.
     - Resource: [Quantum Operators (University of Toronto)](https://www.physics.utoronto.ca/~phy293/QM/quantum_operators.pdf)
   - **Schrodinger Equation**: Solving the time-dependent and time-independent Schrödinger equations for simple systems.
     - Resource: [Schrodinger Equation (Physics LibreTexts)](https://phys.libretexts.org/Bookshelves/Quantum_Mechanics/Quantum_Mechanics_(A_Konar)/Schrodinger_Equation)
   - **Quantum Harmonic Oscillator**: Analyzing the quantum harmonic oscillator and its energy levels.
     - Resource: [Quantum Harmonic Oscillator (Harvard)](https://scholar.harvard.edu/files/quantum-harmonic-oscillator.pdf)
   - **Quantum Mechanics in Three Dimensions**: Extending quantum mechanics to three-dimensional systems.
     - Resource: [Quantum Mechanics in 3D (University of Cambridge)](https://www.damtp.cam.ac.uk/user/hs402/teaching/quantum-mechanics-3D.pdf)
   - **Quantum Statistics and Entanglement**: Understanding quantum statistics like Bose-Einstein and Fermi-Dirac statistics, entanglement, and Bell's theorem.
     - Resource: [Quantum Entanglement (Physics World)](https://physicsworld.com/a/what-is-quantum-entanglement/)
   - **Quantum Mechanics Applications**: Applications in atomic, molecular, condensed matter physics, and quantum information theory.
     - Resource: [Quantum Mechanics Applications (ScienceDirect)](https://www.sciencedirect.com/topics/physics-and-astronomy/quantum-mechanics)

## Advanced Topics:
   - **Quantum Field Theory**: Introduction to relativistic quantum mechanics and quantum field theory.
     - Resource: [Quantum Field Theory (MIT OpenCourseWare)](https://ocw.mit.edu/courses/physics/8-323-relativistic-quantum-field-theory-i-fall-2009/)
   - **Quantum Computing**: Basics of quantum computing, qubits, quantum gates, and quantum algorithms.
     - Resource: [Quantum Computing (IBM)](https://www.ibm.com/quantum-computing/learn/what-is-quantum-computing/)
   - **Relativistic Quantum Mechanics**: Combining quantum mechanics with special relativity.
     - Resource: [Relativistic Quantum Mechanics (Harvard)](https://scholar.harvard.edu/files/relativistic-quantum-mechanics.pdf)
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
