"""
SAGE Agents Model
Database models for the SAGE multi-agent system including User, Assistant, and Checker agents.
"""

from src.models.user import db
from datetime import datetime
import json
from enum import Enum

class AgentType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    CHECKER = "checker"

class IntentType(Enum):
    ANSWER = "Answer"
    ACK = "ACK"
    R_LANGUAGE_USE = "R Language Use"
    R_INFORMATION = "R Information"
    R_REVISION = "R Revision"
    R_EVALUATION = "R Evaluation"
    R_GENERATION = "R Generation"
    NEGOTIATION = "Negotiation"
    OTHER = "Other"
    QUESTION = "Question"
    R_CONFIRMATION = "R Confirmation"
    CONVERSATION = "Conversation"
    R_TRANSLATION = "R Translation"

class LearnerProfile(db.Model):
    """Model for storing learner profiles and preferences."""
    __tablename__ = 'learner_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    course_type = db.Column(db.String(20), nullable=False)  # SW, AW, IRW
    proficiency_level = db.Column(db.String(20), default='intermediate')
    preferred_language = db.Column(db.String(10), default='en')  # en, zh, mixed
    learning_goals = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to interactions
    interactions = db.relationship('Interaction', backref='learner', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'course_type': self.course_type,
            'proficiency_level': self.proficiency_level,
            'preferred_language': self.preferred_language,
            'learning_goals': self.learning_goals,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Interaction(db.Model):
    """Model for storing all agent interactions."""
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner_profiles.id'), nullable=False)
    
    # Interaction content
    user_input = db.Column(db.Text, nullable=False)
    assistant_response = db.Column(db.Text, nullable=True)
    checker_validation = db.Column(db.Text, nullable=True)
    
    # Metadata
    intent_type = db.Column(db.Enum(IntentType), nullable=True)
    confidence_score = db.Column(db.Float, default=0.0)
    user_rating = db.Column(db.Integer, nullable=True)  # 1-5 scale
    
    # Context and memory
    context_data = db.Column(db.Text, nullable=True)  # JSON string
    memory_key = db.Column(db.String(200), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'learner_id': self.learner_id,
            'user_input': self.user_input,
            'assistant_response': self.assistant_response,
            'checker_validation': self.checker_validation,
            'intent_type': self.intent_type.value if self.intent_type else None,
            'confidence_score': self.confidence_score,
            'user_rating': self.user_rating,
            'context_data': json.loads(self.context_data) if self.context_data else None,
            'memory_key': self.memory_key,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def set_context_data(self, data):
        """Set context data as JSON string."""
        self.context_data = json.dumps(data) if data else None
    
    def get_context_data(self):
        """Get context data as Python object."""
        return json.loads(self.context_data) if self.context_data else None

class AgentMemory(db.Model):
    """Model for storing agent memory using SAGE framework principles."""
    __tablename__ = 'agent_memory'
    
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner_profiles.id'), nullable=False)
    memory_key = db.Column(db.String(200), nullable=False)
    memory_type = db.Column(db.String(50), nullable=False)  # short_term, long_term, episodic
    
    # Memory content
    content = db.Column(db.Text, nullable=False)
    importance_score = db.Column(db.Float, default=1.0)
    access_count = db.Column(db.Integer, default=0)
    
    # Ebbinghaus forgetting curve implementation
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    decay_factor = db.Column(db.Float, default=1.0)
    retention_strength = db.Column(db.Float, default=1.0)
    
    # Metadata
    tags = db.Column(db.Text, nullable=True)  # JSON array of tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'memory_key': self.memory_key,
            'memory_type': self.memory_type,
            'content': self.content,
            'importance_score': self.importance_score,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'decay_factor': self.decay_factor,
            'retention_strength': self.retention_strength,
            'tags': json.loads(self.tags) if self.tags else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def update_access(self):
        """Update access statistics and apply forgetting curve."""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()
        
        # Simple forgetting curve implementation
        time_since_creation = (datetime.utcnow() - self.created_at).total_seconds() / 86400  # days
        self.retention_strength = self.importance_score * (1 / (1 + 0.1 * time_since_creation))
        
        db.session.commit()

class WritingSession(db.Model):
    """Model for tracking writing sessions and progress."""
    __tablename__ = 'writing_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner_profiles.id'), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # Writing content
    essay_title = db.Column(db.String(200), nullable=True)
    essay_content = db.Column(db.Text, nullable=True)
    writing_goal = db.Column(db.Text, nullable=True)
    
    # Progress tracking
    word_count = db.Column(db.Integer, default=0)
    revision_count = db.Column(db.Integer, default=0)
    interaction_count = db.Column(db.Integer, default=0)
    
    # Self-regulated learning metrics
    planning_score = db.Column(db.Float, default=0.0)
    monitoring_score = db.Column(db.Float, default=0.0)
    evaluation_score = db.Column(db.Float, default=0.0)
    
    # Session metadata
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'session_id': self.session_id,
            'essay_title': self.essay_title,
            'essay_content': self.essay_content,
            'writing_goal': self.writing_goal,
            'word_count': self.word_count,
            'revision_count': self.revision_count,
            'interaction_count': self.interaction_count,
            'planning_score': self.planning_score,
            'monitoring_score': self.monitoring_score,
            'evaluation_score': self.evaluation_score,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class LearningAnalytics(db.Model):
    """Model for storing learning analytics and progress metrics."""
    __tablename__ = 'learning_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('learner_profiles.id'), nullable=False)
    
    # Performance metrics
    writing_proficiency_score = db.Column(db.Float, default=0.0)
    engagement_score = db.Column(db.Float, default=0.0)
    self_regulation_score = db.Column(db.Float, default=0.0)
    
    # Interaction patterns
    avg_session_duration = db.Column(db.Float, default=0.0)
    total_interactions = db.Column(db.Integer, default=0)
    avg_satisfaction_rating = db.Column(db.Float, default=0.0)
    
    # Learning progression
    weeks_active = db.Column(db.Integer, default=0)
    essays_completed = db.Column(db.Integer, default=0)
    revision_rate = db.Column(db.Float, default=0.0)
    
    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'learner_id': self.learner_id,
            'writing_proficiency_score': self.writing_proficiency_score,
            'engagement_score': self.engagement_score,
            'self_regulation_score': self.self_regulation_score,
            'avg_session_duration': self.avg_session_duration,
            'total_interactions': self.total_interactions,
            'avg_satisfaction_rating': self.avg_satisfaction_rating,
            'weeks_active': self.weeks_active,
            'essays_completed': self.essays_completed,
            'revision_rate': self.revision_rate,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

