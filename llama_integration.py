"""
Meta-Llama-3-8B-Instruct Integration
Handles integration with the Meta-Llama-3-8B-Instruct model for generating educational content.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class LlamaIntegration:
    """
    Integration class for Meta-Llama-3-8B-Instruct model.
    Provides educational content generation and writing assistance.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        
        # Educational prompts for different intent types
        self.educational_prompts = self._initialize_educational_prompts()
        
        # Self-regulated learning strategies
        self.srl_strategies = self._initialize_srl_strategies()
        
    def _initialize_educational_prompts(self) -> Dict[str, str]:
        """Initialize educational prompt templates for different intent types."""
        return {
            'Answer': """You are an expert EFL (English as a Foreign Language) writing instructor. 
            A student has asked: "{user_input}"
            
            Provide a clear, educational answer that:
            1. Directly addresses their question
            2. Uses language appropriate for their proficiency level ({proficiency_level})
            3. Includes specific examples
            4. Encourages further learning
            
            Keep your response supportive and encouraging.""",
            
            'R Language Use': """You are an expert EFL writing instructor specializing in language use and grammar.
            A student has submitted this text for language improvement: "{user_input}"
            
            Provide specific feedback on:
            1. Grammar and syntax issues
            2. Word choice and vocabulary improvements
            3. Sentence structure enhancements
            4. Clarity and coherence
            
            Proficiency level: {proficiency_level}
            Course type: {course_type}
            
            Format your response with clear explanations and examples.""",
            
            'R Revision': """You are an expert EFL writing instructor helping with text revision.
            Student's text: "{user_input}"
            
            Provide revision suggestions focusing on:
            1. Content organization and structure
            2. Argument development and support
            3. Transitions and flow
            4. Overall coherence and unity
            
            Consider the student's proficiency level ({proficiency_level}) and course type ({course_type}).
            Provide specific, actionable suggestions.""",
            
            'R Evaluation': """You are an expert EFL writing instructor providing comprehensive evaluation.
            Student's text: "{user_input}"
            
            Provide a balanced evaluation covering:
            1. Strengths of the writing
            2. Areas for improvement
            3. Specific suggestions for enhancement
            4. Overall assessment and encouragement
            
            Proficiency level: {proficiency_level}
            Course type: {course_type}
            
            Be constructive and supportive in your feedback.""",
            
            'R Generation': """You are an expert EFL writing instructor helping with content generation.
            Student's request: "{user_input}"
            
            Generate helpful content such as:
            1. Ideas and examples related to their topic
            2. Outline suggestions
            3. Sample sentences or paragraphs
            4. Vocabulary and phrases relevant to the topic
            
            Adapt to proficiency level ({proficiency_level}) and course type ({course_type}).
            Encourage the student to develop ideas in their own voice.""",
            
            'R Information': """You are an expert EFL writing instructor providing educational information.
            Student's inquiry: "{user_input}"
            
            Provide comprehensive information about:
            1. The topic or concept they're asking about
            2. Relevant examples and applications
            3. How it relates to their writing development
            4. Additional resources or next steps
            
            Tailor to proficiency level ({proficiency_level}) and course type ({course_type})."""
        }
    
    def _initialize_srl_strategies(self) -> Dict[str, List[str]]:
        """Initialize self-regulated learning strategy prompts."""
        return {
            'cognitive': [
                "Break down complex writing tasks into smaller, manageable steps.",
                "Use graphic organizers or mind maps to organize your ideas before writing.",
                "Practice summarizing main points to improve comprehension and clarity.",
                "Connect new writing concepts to what you already know."
            ],
            'metacognitive': [
                "Set specific, achievable goals for each writing session.",
                "Monitor your progress and adjust your writing strategies as needed.",
                "Reflect on what writing techniques work best for you.",
                "Plan your writing process before you begin."
            ],
            'social_behavioral': [
                "Seek feedback from peers or instructors on your writing.",
                "Join writing groups or discussion forums for practice.",
                "Create a dedicated, distraction-free writing environment.",
                "Establish regular writing schedules and stick to them."
            ],
            'motivational': [
                "Remember your personal goals for improving English writing.",
                "Celebrate small improvements and progress in your writing.",
                "Focus on learning from mistakes rather than avoiding them.",
                "Connect your writing practice to your future academic or career goals."
            ]
        }
    
    def generate_response(self, intent: str, user_input: str, learner_profile: Dict, 
                         context: Dict) -> Dict:
        """
        Generate an educational response using Meta-Llama-3-8B-Instruct.
        
        Args:
            intent: The classified intent type
            user_input: The user's input text
            learner_profile: Learner's profile information
            context: Additional context information
            
        Returns:
            Dictionary containing the generated response and metadata
        """
        try:
            # Get the appropriate prompt template
            prompt_template = self.educational_prompts.get(intent, self.educational_prompts['Answer'])
            
            # Format the prompt with learner information
            formatted_prompt = prompt_template.format(
                user_input=user_input,
                proficiency_level=learner_profile.get('proficiency_level', 'intermediate'),
                course_type=learner_profile.get('course_type', 'general'),
                preferred_language=learner_profile.get('preferred_language', 'en')
            )
            
            # Add context-specific instructions
            if context.get('is_multilingual'):
                formatted_prompt += "\n\nNote: The student may use code-switching (mixing languages). Address this appropriately."
            
            if context.get('mentions_essay'):
                formatted_prompt += "\n\nNote: This relates to essay writing. Focus on academic writing skills."
            
            # Generate response using the LLM
            response = self._call_llm(formatted_prompt, learner_profile)
            
            # Add self-regulated learning strategy
            srl_strategy = self._select_srl_strategy(intent, context, learner_profile)
            
            return {
                'content': response,
                'intent': intent,
                'srl_strategy': srl_strategy,
                'model_used': self.model_name,
                'timestamp': datetime.utcnow().isoformat(),
                'personalized': True
            }
            
        except Exception as e:
            # Fallback response if LLM fails
            return self._generate_fallback_response(intent, user_input, learner_profile)
    
    def _call_llm(self, prompt: str, learner_profile: Dict) -> str:
        """
        Make API call to Meta-Llama-3-8B-Instruct model.
        
        Args:
            prompt: The formatted prompt
            learner_profile: Learner's profile for personalization
            
        Returns:
            Generated response text
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Adjust parameters based on proficiency level
            proficiency = learner_profile.get('proficiency_level', 'intermediate')
            
            if proficiency == 'beginner':
                max_tokens = 300
                temperature = 0.3
            elif proficiency == 'advanced':
                max_tokens = 600
                temperature = 0.7
            else:  # intermediate
                max_tokens = 450
                temperature = 0.5
            
            payload = {
                'model': self.model_name,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert EFL (English as a Foreign Language) writing instructor. Provide helpful, educational, and encouraging responses to students.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': max_tokens,
                'temperature': temperature,
                'top_p': 0.9,
                'frequency_penalty': 0.1,
                'presence_penalty': 0.1
            }
            
            response = requests.post(
                f'{self.api_base}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"API call failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Error calling LLM: {str(e)}")
            raise e
    
    def _select_srl_strategy(self, intent: str, context: Dict, learner_profile: Dict) -> str:
        """Select appropriate self-regulated learning strategy."""
        # Map intents to SRL strategy types
        intent_to_srl = {
            'Answer': 'cognitive',
            'R Language Use': 'cognitive',
            'R Revision': 'metacognitive',
            'R Evaluation': 'metacognitive',
            'R Generation': 'cognitive',
            'R Information': 'cognitive',
            'ACK': 'motivational',
            'Negotiation': 'social_behavioral'
        }
        
        srl_type = intent_to_srl.get(intent, 'cognitive')
        strategies = self.srl_strategies.get(srl_type, self.srl_strategies['cognitive'])
        
        # Simple selection based on context (in practice, this could be more sophisticated)
        if context.get('interaction_count', 0) < 5:
            # New learners get motivational strategies
            return self.srl_strategies['motivational'][0]
        elif context.get('avg_rating', 0) < 3:
            # Struggling learners get more support
            return self.srl_strategies['social_behavioral'][0]
        else:
            # Regular strategy selection
            return strategies[0]
    
    def _generate_fallback_response(self, intent: str, user_input: str, 
                                  learner_profile: Dict) -> Dict:
        """Generate a fallback response when LLM is unavailable."""
        fallback_responses = {
            'Answer': "I'd be happy to help answer your question. Could you please provide more specific details about what you'd like to know?",
            'R Language Use': "I can help you improve your language use. Please share the text you'd like me to review, and I'll provide specific suggestions for grammar, vocabulary, and clarity.",
            'R Revision': "I can assist you with revising your writing. Please share your draft, and I'll help you improve its organization, development, and flow.",
            'R Evaluation': "I can provide feedback on your writing. Please share your text, and I'll give you a balanced evaluation with specific suggestions for improvement.",
            'R Generation': "I can help you generate ideas and content for your writing. What specific topic or type of writing are you working on?",
            'R Information': "I can provide information to help with your writing. What specific topic or writing concept would you like to learn more about?"
        }
        
        content = fallback_responses.get(intent, "I'm here to help you with your English writing. How can I assist you today?")
        
        return {
            'content': content,
            'intent': intent,
            'srl_strategy': "Focus on your learning goals and don't hesitate to ask for help when you need it.",
            'model_used': 'fallback',
            'timestamp': datetime.utcnow().isoformat(),
            'personalized': False
        }
    
    def generate_writing_feedback(self, essay_text: str, learner_profile: Dict) -> Dict:
        """
        Generate comprehensive writing feedback for an essay.
        
        Args:
            essay_text: The student's essay text
            learner_profile: Learner's profile information
            
        Returns:
            Comprehensive feedback dictionary
        """
        feedback_prompt = f"""You are an expert EFL writing instructor. Please provide comprehensive feedback on this student essay.

Student's proficiency level: {learner_profile.get('proficiency_level', 'intermediate')}
Course type: {learner_profile.get('course_type', 'general')}

Essay text:
{essay_text}

Please provide feedback in the following areas:
1. Content and Ideas (strengths and suggestions)
2. Organization and Structure
3. Language Use and Grammar
4. Vocabulary and Word Choice
5. Overall Assessment and Next Steps

Be specific, constructive, and encouraging in your feedback."""
        
        try:
            response = self._call_llm(feedback_prompt, learner_profile)
            
            return {
                'feedback': response,
                'essay_length': len(essay_text.split()),
                'feedback_type': 'comprehensive',
                'model_used': self.model_name,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'feedback': "I'm unable to provide detailed feedback at the moment. Please try again later or contact your instructor for assistance.",
                'essay_length': len(essay_text.split()),
                'feedback_type': 'fallback',
                'model_used': 'fallback',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }
    
    def generate_writing_prompts(self, topic: str, proficiency_level: str, 
                               course_type: str) -> List[str]:
        """
        Generate writing prompts for a given topic.
        
        Args:
            topic: The writing topic
            proficiency_level: Student's proficiency level
            course_type: Type of course (SW, AW, IRW)
            
        Returns:
            List of writing prompts
        """
        prompt = f"""Generate 5 writing prompts for EFL students on the topic: {topic}

Student level: {proficiency_level}
Course type: {course_type}

The prompts should be:
1. Appropriate for the proficiency level
2. Engaging and relevant
3. Clear and specific
4. Suitable for the course type

Please provide exactly 5 prompts, numbered 1-5."""
        
        try:
            response = self._call_llm(prompt, {
                'proficiency_level': proficiency_level,
                'course_type': course_type
            })
            
            # Parse the response to extract individual prompts
            lines = response.split('\n')
            prompts = []
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-')):
                    # Remove numbering and clean up
                    clean_prompt = line.split('.', 1)[-1].strip()
                    if clean_prompt:
                        prompts.append(clean_prompt)
            
            return prompts[:5]  # Ensure we return exactly 5 prompts
            
        except Exception as e:
            # Fallback prompts
            return [
                f"Write about your experience with {topic}",
                f"Discuss the advantages and disadvantages of {topic}",
                f"Explain how {topic} affects your daily life",
                f"Compare {topic} in your country with other countries",
                f"Describe your opinion about {topic} and support it with examples"
            ]
    
    def check_model_availability(self) -> bool:
        """Check if the Meta-Llama-3-8B-Instruct model is available."""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Simple test call
            payload = {
                'model': self.model_name,
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'max_tokens': 10
            }
            
            response = requests.post(
                f'{self.api_base}/chat/completions',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception:
            return False

    def generate_educational_response(self, user_input: str, proficiency_level: str = 'intermediate', course_type: str = 'IRW') -> Dict:
        """
        Generate a simple educational response for chat.
        
        Args:
            user_input: The user's message
            proficiency_level: Learner's proficiency level
            course_type: Type of course
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Use the existing generate_response method
            learner_profile = {
                'proficiency_level': proficiency_level,
                'course_type': course_type,
                'preferred_language': 'en'
            }
            
            context = {}
            
            # For now, use 'Answer' intent for all chat messages
            response = self.generate_response('Answer', user_input, learner_profile, context)
            
            return {
                'content': response['content'],
                'intent': response['intent'],
                'confidence': 0.9,
                'srl_suggestion': response.get('srl_strategy', 'Keep practicing!'),
                'suggestions': []
            }
            
        except Exception as e:
            print(f"Error generating educational response: {e}")
            # Fallback response
            return {
                'content': f"I'm here to help you with your {course_type} writing! Your message was: '{user_input}'. Please try asking a specific question about writing, grammar, or essay structure.",
                'intent': 'Answer',
                'confidence': 0.7,
                'srl_suggestion': 'Keep practicing!',
                'suggestions': ['Ask about grammar', 'Ask about essay structure', 'Ask about vocabulary']
            }

