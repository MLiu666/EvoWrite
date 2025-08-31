"""
SAGE API Routes
Flask blueprint for handling SAGE multi-agent system API endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid
import json

from src.models.sage_agents import (
    db, LearnerProfile, Interaction, WritingSession, 
    LearningAnalytics, AgentMemory, IntentType
)
from src.agents.user_agent import UserAgent
from src.agents.assistant_agent import AssistantAgent
from src.agents.checker_agent import CheckerAgent

sage_bp = Blueprint('sage', __name__)

# Initialize agents
user_agent = UserAgent()
assistant_agent = AssistantAgent()
checker_agent = CheckerAgent()

@sage_bp.route('/learners', methods=['POST'])
def create_learner():
    """Create a new learner profile."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'course_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if learner already exists
        existing_learner = LearnerProfile.query.filter_by(user_id=data['user_id']).first()
        if existing_learner:
            return jsonify({'error': 'Learner already exists'}), 409
        
        # Create new learner profile
        learner = LearnerProfile(
            user_id=data['user_id'],
            name=data.get('name'),
            course_type=data['course_type'],
            proficiency_level=data.get('proficiency_level', 'intermediate'),
            preferred_language=data.get('preferred_language', 'en'),
            learning_goals=data.get('learning_goals')
        )
        
        db.session.add(learner)
        db.session.commit()
        
        return jsonify({
            'message': 'Learner profile created successfully',
            'learner': learner.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error creating learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/learners/<int:learner_id>', methods=['GET'])
def get_learner(learner_id):
    """Get learner profile by ID."""
    try:
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        return jsonify({'learner': learner.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/learners/<int:learner_id>', methods=['PUT'])
def update_learner(learner_id):
    """Update learner profile."""
    try:
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['name', 'course_type', 'proficiency_level', 'preferred_language', 'learning_goals']
        for field in allowed_fields:
            if field in data:
                setattr(learner, field, data[field])
        
        learner.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Learner profile updated successfully',
            'learner': learner.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error updating learner: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/chat', methods=['POST'])
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
        
        # Verify learner exists
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        # Step 1: User Agent processes input
        processed_input = user_agent.process_user_input(
            user_input=user_message,
            learner_id=learner_id,
            session_id=session_id
        )
        
        # Step 2: Assistant Agent generates response
        assistant_response = assistant_agent.generate_response(processed_input)
        
        # Step 3: Checker Agent validates response
        validation_results = checker_agent.validate_response(
            assistant_response=assistant_response,
            processed_input=processed_input,
            interaction_id=processed_input['interaction_id']
        )
        
        # Step 4: Update interaction with assistant response
        interaction = Interaction.query.get(processed_input['interaction_id'])
        if interaction:
            interaction.assistant_response = assistant_response['content']
            db.session.commit()
        
        # Step 5: Prepare response
        response_data = {
            'session_id': session_id,
            'interaction_id': processed_input['interaction_id'],
            'intent': processed_input['intent'],
            'confidence': processed_input['confidence'],
            'response': assistant_response['content'],
            'response_type': assistant_response.get('type', 'general'),
            'srl_suggestion': assistant_response.get('srl_suggestion'),
            'validation': {
                'approved': validation_results['approved'],
                'overall_score': validation_results['overall_score'],
                'issues': validation_results['issues']
            },
            'suggestions': assistant_response.get('suggestions', [])
        }
        
        # Add warnings if response not approved
        if not validation_results['approved']:
            response_data['warnings'] = validation_results['recommendations']
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback on an interaction."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['interaction_id', 'rating']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        interaction_id = data['interaction_id']
        rating = data['rating']
        feedback_text = data.get('feedback_text')
        
        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        # Submit feedback through User Agent
        user_agent.handle_feedback(
            interaction_id=interaction_id,
            rating=rating,
            feedback_text=feedback_text
        )
        
        return jsonify({'message': 'Feedback submitted successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error submitting feedback: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/sessions', methods=['POST'])
def create_writing_session():
    """Create a new writing session."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['learner_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        learner_id = data['learner_id']
        
        # Verify learner exists
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        # Create new writing session
        session = WritingSession(
            learner_id=learner_id,
            session_id=str(uuid.uuid4()),
            essay_title=data.get('essay_title'),
            writing_goal=data.get('writing_goal')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Writing session created successfully',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error creating writing session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/sessions/<int:session_id>', methods=['PUT'])
def update_writing_session(session_id):
    """Update a writing session."""
    try:
        session = WritingSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Writing session not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['essay_title', 'essay_content', 'writing_goal', 'status']
        for field in allowed_fields:
            if field in data:
                setattr(session, field, data[field])
        
        # Update word count if essay content is provided
        if 'essay_content' in data and data['essay_content']:
            session.word_count = len(data['essay_content'].split())
        
        # Mark as completed if status is set to completed
        if data.get('status') == 'completed':
            session.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Writing session updated successfully',
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error updating writing session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/learners/<int:learner_id>/analytics', methods=['GET'])
def get_learning_analytics(learner_id):
    """Get learning analytics for a learner."""
    try:
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        # Get or create analytics record
        analytics = LearningAnalytics.query.filter_by(learner_id=learner_id).first()
        if not analytics:
            analytics = LearningAnalytics(learner_id=learner_id)
            db.session.add(analytics)
            db.session.commit()
        
        # Get recent interactions for analysis
        interactions = Interaction.query.filter_by(learner_id=learner_id).all()
        
        # Calculate updated metrics
        if interactions:
            ratings = [i.user_rating for i in interactions if i.user_rating]
            analytics.total_interactions = len(interactions)
            analytics.avg_satisfaction_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Get writing sessions
        sessions = WritingSession.query.filter_by(learner_id=learner_id).all()
        completed_sessions = [s for s in sessions if s.status == 'completed']
        analytics.essays_completed = len(completed_sessions)
        
        # Get validation summary from Checker Agent
        validation_summary = checker_agent.get_validation_summary(learner_id, days=30)
        
        # Get personalization data from User Agent
        personalization_data = user_agent.get_personalization_data(learner_id)
        
        db.session.commit()
        
        return jsonify({
            'analytics': analytics.to_dict(),
            'validation_summary': validation_summary,
            'personalization_data': personalization_data,
            'recent_activity': {
                'total_interactions': len(interactions),
                'recent_sessions': len(sessions),
                'completed_essays': len(completed_sessions)
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting learning analytics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/learners/<int:learner_id>/interactions', methods=['GET'])
def get_learner_interactions(learner_id):
    """Get interaction history for a learner."""
    try:
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        session_id = request.args.get('session_id')
        
        # Build query
        query = Interaction.query.filter_by(learner_id=learner_id)
        
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        interactions = query.order_by(
            Interaction.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'interactions': [interaction.to_dict() for interaction in interactions],
            'total_count': len(interactions)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting learner interactions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/learners/<int:learner_id>/memory', methods=['GET'])
def get_learner_memory(learner_id):
    """Get memory records for a learner."""
    try:
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return jsonify({'error': 'Learner not found'}), 404
        
        # Get query parameters
        memory_type = request.args.get('memory_type')
        limit = request.args.get('limit', 20, type=int)
        
        # Retrieve memories through User Agent
        memories = user_agent.retrieve_memory(
            learner_id=learner_id,
            memory_type=memory_type,
            limit=limit
        )
        
        return jsonify({
            'memories': [memory.to_dict() for memory in memories],
            'total_count': len(memories)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting learner memory: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@sage_bp.route('/system/health', methods=['GET'])
def system_health():
    """Get system health status."""
    try:
        # Check database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        
        # Get system statistics
        total_learners = LearnerProfile.query.count()
        total_interactions = Interaction.query.count()
        total_sessions = WritingSession.query.count()
        
        # Get recent activity (last 24 hours)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        recent_interactions = Interaction.query.filter(
            Interaction.created_at >= yesterday
        ).count()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'statistics': {
                'total_learners': total_learners,
                'total_interactions': total_interactions,
                'total_sessions': total_sessions,
                'recent_interactions_24h': recent_interactions
            },
            'agents': {
                'user_agent': 'active',
                'assistant_agent': 'active',
                'checker_agent': 'active'
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"System health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@sage_bp.route('/intents', methods=['GET'])
def get_intent_types():
    """Get available intent types."""
    try:
        intent_types = [
            {
                'value': intent.value,
                'name': intent.name,
                'description': f"Intent type for {intent.value.lower()} requests"
            }
            for intent in IntentType
        ]
        
        return jsonify({'intent_types': intent_types}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting intent types: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@sage_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@sage_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@sage_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

