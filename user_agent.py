"""
User Agent Implementation
Handles user interface, intent classification, and conversation management.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.models.sage_agents import IntentType, LearnerProfile, Interaction, AgentMemory

class UserAgent:
    """
    User Agent responsible for:
    - Understanding learner intent
    - Managing conversation context
    - Maintaining learner profiles
    - Facilitating natural language interactions
    """
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
        self.context_window = 5  # Number of previous interactions to consider
        
    def _initialize_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize regex patterns for intent classification based on RECIPE4U analysis."""
        return {
            IntentType.ANSWER: [
                r'\b(what|how|why|when|where|which|who)\b',
                r'\b(question|ask|tell me|explain)\b',
                r'\?',
                r'\b(help me understand|clarify|define)\b'
            ],
            IntentType.ACK: [
                r'\b(yes|ok|okay|right|correct|thanks|thank you)\b',
                r'\b(i see|i understand|got it|makes sense)\b',
                r'\b(good|great|perfect|excellent)\b'
            ],
            IntentType.R_LANGUAGE_USE: [
                r'\b(grammar|syntax|word choice|vocabulary)\b',
                r'\b(correct|fix|improve|better way)\b',
                r'\b(comma|period|punctuation|spelling)\b',
                r'\b(tense|verb|noun|adjective|adverb)\b'
            ],
            IntentType.R_INFORMATION: [
                r'\b(information|details|facts|data)\b',
                r'\b(research|source|reference|citation)\b',
                r'\b(background|context|history)\b'
            ],
            IntentType.R_REVISION: [
                r'\b(revise|edit|rewrite|improve|modify)\b',
                r'\b(draft|version|change|update)\b',
                r'\b(better|enhance|polish|refine)\b'
            ],
            IntentType.R_EVALUATION: [
                r'\b(evaluate|assess|judge|rate|score)\b',
                r'\b(feedback|opinion|thoughts|review)\b',
                r'\b(good|bad|quality|strength|weakness)\b'
            ],
            IntentType.R_GENERATION: [
                r'\b(generate|create|write|produce|make)\b',
                r'\b(example|sample|template|outline)\b',
                r'\b(idea|suggestion|topic|theme)\b'
            ],
            IntentType.NEGOTIATION: [
                r'\b(but|however|although|disagree|different)\b',
                r'\b(alternative|another way|instead)\b',
                r'\b(negotiate|discuss|debate)\b'
            ],
            IntentType.R_CONFIRMATION: [
                r'\b(confirm|verify|check|sure|certain)\b',
                r'\b(is this right|am i correct|does this work)\b'
            ],
            IntentType.CONVERSATION: [
                r'\b(hello|hi|hey|good morning|good afternoon)\b',
                r'\b(how are you|nice to meet|chat|talk)\b'
            ],
            IntentType.R_TRANSLATION: [
                r'\b(translate|translation|chinese|korean)\b',
                r'\b(mean in|say in|express in)\b'
            ]
        }
    
    def classify_intent(self, user_input: str) -> Tuple[IntentType, float]:
        """
        Classify user intent based on input text.
        Returns intent type and confidence score.
        """
        user_input_lower = user_input.lower()
        intent_scores = {}
        
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, user_input_lower))
                score += matches
            
            if score > 0:
                # Normalize score by input length
                intent_scores[intent_type] = score / len(user_input.split())
        
        if not intent_scores:
            return IntentType.OTHER, 0.5
        
        # Get intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] * 2, 1.0)  # Cap at 1.0
        
        return best_intent, confidence
    
    def extract_context(self, user_input: str, learner_profile: LearnerProfile) -> Dict:
        """Extract contextual information from user input."""
        context = {
            'input_length': len(user_input),
            'word_count': len(user_input.split()),
            'has_question_mark': '?' in user_input,
            'has_essay_content': len(user_input) > 200,
            'course_type': learner_profile.course_type,
            'proficiency_level': learner_profile.proficiency_level,
            'preferred_language': learner_profile.preferred_language
        }
        
        # Detect language mixing (code-switching)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', user_input)
        korean_chars = re.findall(r'[\uac00-\ud7af]', user_input)
        
        context['has_chinese'] = len(chinese_chars) > 0
        context['has_korean'] = len(korean_chars) > 0
        context['is_multilingual'] = context['has_chinese'] or context['has_korean']
        
        # Detect essay-related content
        essay_indicators = ['paragraph', 'essay', 'draft', 'writing', 'composition']
        context['mentions_essay'] = any(indicator in user_input.lower() for indicator in essay_indicators)
        
        return context
    
    def manage_conversation_state(self, session_id: str, user_input: str, 
                                learner_id: int) -> Dict:
        """Manage conversation state and context across interactions."""
        from src.models.sage_agents import db
        
        # Get recent interactions for context
        recent_interactions = Interaction.query.filter_by(
            session_id=session_id,
            learner_id=learner_id
        ).order_by(Interaction.created_at.desc()).limit(self.context_window).all()
        
        conversation_state = {
            'session_id': session_id,
            'interaction_count': len(recent_interactions),
            'recent_intents': [i.intent_type.value for i in recent_interactions if i.intent_type],
            'recent_ratings': [i.user_rating for i in recent_interactions if i.user_rating],
            'session_duration': self._calculate_session_duration(recent_interactions),
            'context_summary': self._generate_context_summary(recent_interactions)
        }
        
        return conversation_state
    
    def _calculate_session_duration(self, interactions: List[Interaction]) -> float:
        """Calculate session duration in minutes."""
        if len(interactions) < 2:
            return 0.0
        
        start_time = interactions[-1].created_at
        end_time = interactions[0].created_at
        duration = (end_time - start_time).total_seconds() / 60
        
        return round(duration, 2)
    
    def _generate_context_summary(self, interactions: List[Interaction]) -> str:
        """Generate a summary of recent conversation context."""
        if not interactions:
            return "New conversation session."
        
        intent_counts = {}
        for interaction in interactions:
            if interaction.intent_type:
                intent = interaction.intent_type.value
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        if intent_counts:
            primary_intent = max(intent_counts, key=intent_counts.get)
            return f"Recent focus on {primary_intent} with {len(interactions)} interactions."
        
        return f"Ongoing conversation with {len(interactions)} interactions."
    
    def update_learner_profile(self, learner_id: int, interaction_data: Dict) -> None:
        """Update learner profile based on interaction patterns."""
        from src.models.sage_agents import db
        
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            return
        
        # Update based on interaction patterns
        if interaction_data.get('is_multilingual'):
            learner.preferred_language = 'mixed'
        
        # Update proficiency level based on interaction complexity
        avg_input_length = interaction_data.get('avg_input_length', 0)
        if avg_input_length > 500:
            if learner.proficiency_level == 'beginner':
                learner.proficiency_level = 'intermediate'
            elif learner.proficiency_level == 'intermediate':
                learner.proficiency_level = 'advanced'
        
        learner.updated_at = datetime.utcnow()
        db.session.commit()
    
    def store_memory(self, learner_id: int, memory_key: str, content: str, 
                    memory_type: str = 'short_term', importance: float = 1.0) -> None:
        """Store information in agent memory using SAGE principles."""
        from src.models.sage_agents import db
        
        memory = AgentMemory(
            learner_id=learner_id,
            memory_key=memory_key,
            memory_type=memory_type,
            content=content,
            importance_score=importance
        )
        
        db.session.add(memory)
        db.session.commit()
    
    def retrieve_memory(self, learner_id: int, memory_key: str = None, 
                       memory_type: str = None, limit: int = 10) -> List[AgentMemory]:
        """Retrieve relevant memories for context."""
        query = AgentMemory.query.filter_by(learner_id=learner_id)
        
        if memory_key:
            query = query.filter(AgentMemory.memory_key.contains(memory_key))
        
        if memory_type:
            query = query.filter_by(memory_type=memory_type)
        
        # Order by importance and recency
        memories = query.order_by(
            AgentMemory.importance_score.desc(),
            AgentMemory.last_accessed.desc()
        ).limit(limit).all()
        
        # Update access statistics
        for memory in memories:
            memory.update_access()
        
        return memories
    
    def process_user_input(self, user_input: str, learner_id: int, 
                          session_id: str) -> Dict:
        """
        Main processing function for user input.
        Returns processed information for the Assistant Agent.
        """
        from src.models.sage_agents import db
        
        # Get learner profile
        learner = LearnerProfile.query.get(learner_id)
        if not learner:
            raise ValueError(f"Learner with ID {learner_id} not found")
        
        # Classify intent
        intent, confidence = self.classify_intent(user_input)
        
        # Extract context
        context = self.extract_context(user_input, learner)
        
        # Manage conversation state
        conversation_state = self.manage_conversation_state(session_id, user_input, learner_id)
        
        # Retrieve relevant memories
        relevant_memories = self.retrieve_memory(learner_id, limit=5)
        
        # Create interaction record
        interaction = Interaction(
            session_id=session_id,
            learner_id=learner_id,
            user_input=user_input,
            intent_type=intent,
            confidence_score=confidence
        )
        
        # Set context data
        full_context = {
            **context,
            **conversation_state,
            'memories': [m.to_dict() for m in relevant_memories]
        }
        interaction.set_context_data(full_context)
        
        db.session.add(interaction)
        db.session.commit()
        
        return {
            'interaction_id': interaction.id,
            'intent': intent.value,
            'confidence': confidence,
            'context': full_context,
            'learner_profile': learner.to_dict(),
            'memories': [m.to_dict() for m in relevant_memories]
        }
    
    def handle_feedback(self, interaction_id: int, rating: int, 
                       feedback_text: str = None) -> None:
        """Handle user feedback on assistant responses."""
        from src.models.sage_agents import db
        
        interaction = Interaction.query.get(interaction_id)
        if interaction:
            interaction.user_rating = rating
            interaction.completed_at = datetime.utcnow()
            
            # Store feedback as memory if provided
            if feedback_text:
                self.store_memory(
                    learner_id=interaction.learner_id,
                    memory_key=f"feedback_{interaction_id}",
                    content=feedback_text,
                    memory_type='long_term',
                    importance=rating / 5.0  # Convert rating to importance score
                )
            
            db.session.commit()
    
    def get_personalization_data(self, learner_id: int) -> Dict:
        """Get personalization data for adaptive responses."""
        from src.models.sage_agents import db
        
        # Get interaction statistics
        interactions = Interaction.query.filter_by(learner_id=learner_id).all()
        
        if not interactions:
            return {'interaction_count': 0}
        
        # Calculate statistics
        ratings = [i.user_rating for i in interactions if i.user_rating]
        intents = [i.intent_type.value for i in interactions if i.intent_type]
        
        personalization_data = {
            'interaction_count': len(interactions),
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0,
            'preferred_intents': self._get_top_intents(intents),
            'avg_input_length': sum(len(i.user_input) for i in interactions) / len(interactions),
            'session_count': len(set(i.session_id for i in interactions)),
            'recent_activity': len([i for i in interactions if 
                                  (datetime.utcnow() - i.created_at).days <= 7])
        }
        
        return personalization_data
    
    def _get_top_intents(self, intents: List[str], top_n: int = 3) -> List[str]:
        """Get the most common intents for a learner."""
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        return sorted(intent_counts.keys(), key=intent_counts.get, reverse=True)[:top_n]

