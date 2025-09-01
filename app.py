from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from llama_integration import LlamaIntegration

app = Flask(__name__)
CORS(app)

# Initialize Llama integration
llama = LlamaIntegration()

# In-memory storage for demo purposes
learners = {}
interactions = {}

@app.route('/api/sage/chat', methods=['POST'])
def chat():
    """Main chat endpoint for SAGE multi-agent interaction."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['learner_id', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        learner_id = data['learner_id']
        user_message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # Get learner info (for demo, use default values)
        learner_info = {
            'proficiency_level': 'intermediate',
            'course_type': 'IRW'
        }
        
        # Ensure model availability
        if not llama.check_model_availability():
            return jsonify({'error': 'Model not available'}), 503

        # Generate response using Llama model
        response_data = llama.generate_educational_response(
            user_input=user_message,
            proficiency_level=learner_info['proficiency_level'],
            course_type=learner_info['course_type']
        )
        
        # Create interaction record
        interaction_id = str(uuid.uuid4())
        interactions[interaction_id] = {
            'id': interaction_id,
            'learner_id': learner_id,
            'session_id': session_id,
            'user_message': user_message,
            'assistant_response': response_data['content'],
            'intent': response_data.get('intent', 'Answer'),
            'confidence': response_data.get('confidence', 0.9),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Prepare response
        response_data = {
            'session_id': session_id,
            'interaction_id': interaction_id,
            'intent': interactions[interaction_id]['intent'],
            'confidence': interactions[interaction_id]['confidence'],
            'response': interactions[interaction_id]['assistant_response'],
            'response_type': 'educational',
            'srl_suggestion': response_data.get('srl_suggestion', 'Continue practicing!'),
            'validation': {
                'approved': True,
                'overall_score': 0.9,
                'issues': []
            },
            'suggestions': response_data.get('suggestions', [])
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sage/learners', methods=['POST'])
def create_learner():
    """Create a new learner profile."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'course_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new learner profile
        learner = {
            'id': data['user_id'],
            'user_id': data['user_id'],
            'name': data.get('name'),
            'course_type': data['course_type'],
            'proficiency_level': data.get('proficiency_level', 'intermediate'),
            'preferred_language': data.get('preferred_language', 'en'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        learners[data['user_id']] = learner
        
        return jsonify({
            'message': 'Learner profile created successfully',
            'learner': learner
        }), 201
        
    except Exception as e:
        print(f"Error creating learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sage/learners/<learner_id>', methods=['GET'])
def get_learner(learner_id):
    """Get learner profile by ID."""
    try:
        learner = learners.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        return jsonify({'learner': learner}), 200
        
    except Exception as e:
        print(f"Error getting learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/sage/learners/<learner_id>', methods=['PUT'])
def update_learner(learner_id):
    """Update learner profile."""
    try:
        learner = learners.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['name', 'course_type', 'proficiency_level', 'preferred_language', 'learning_goals']
        for field in allowed_fields:
            if field in data:
                learner[field] = data[field]
        
        learner['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'message': 'Learner profile updated successfully',
            'learner': learner
        }), 200
        
    except Exception as e:
        print(f"Error updating learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting SAGE API server with Meta-Llama integration...")
    print("Chat endpoint: http://localhost:5000/api/sage/chat")
    app.run(host='0.0.0.0', port=5000, debug=True)
