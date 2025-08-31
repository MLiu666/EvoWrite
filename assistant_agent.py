"""
Assistant Agent Implementation
Handles content generation, writing feedback, and instructional support.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.models.sage_agents import IntentType, LearnerProfile, Interaction, WritingSession
from src.llm.llama_integration import LlamaIntegration

class AssistantAgent:
    """
    Assistant Agent responsible for:
    - Generating educational content and feedback
    - Providing writing assistance and revision suggestions
    - Implementing self-regulated learning strategies
    - Adapting responses based on learner profiles
    """
    
    def __init__(self):
        self.llama_integration = LlamaIntegration()
        self.response_templates = self._initialize_response_templates()
        self.srl_strategies = self._initialize_srl_strategies()
        self.writing_feedback_patterns = self._initialize_feedback_patterns()
        
    def _initialize_response_templates(self) -> Dict[str, Dict]:
        """Initialize response templates for different intent types."""
        return {
            IntentType.ANSWER.value: {
                'greeting': "I'd be happy to help answer your question.",
                'structure': "Let me explain {topic} step by step:",
                'conclusion': "Does this answer your question? Feel free to ask for clarification."
            },
            IntentType.R_LANGUAGE_USE.value: {
                'greeting': "I can help you improve the language in your writing.",
                'structure': "Here are some suggestions for better language use:",
                'conclusion': "These changes will make your writing clearer and more professional."
            },
            IntentType.R_REVISION.value: {
                'greeting': "Let's work on revising your text together.",
                'structure': "I suggest the following revisions:",
                'conclusion': "These revisions will strengthen your argument and improve clarity."
            },
            IntentType.R_EVALUATION.value: {
                'greeting': "I'll provide feedback on your writing.",
                'structure': "Here's my evaluation of your work:",
                'conclusion': "Overall, you're making good progress. Keep up the excellent work!"
            },
            IntentType.R_GENERATION.value: {
                'greeting': "I can help you generate content for your writing.",
                'structure': "Here are some ideas and examples:",
                'conclusion': "Use these as starting points and develop them in your own voice."
            }
        }
    
    def _initialize_srl_strategies(self) -> Dict[str, List[str]]:
        """Initialize self-regulated learning strategy prompts."""
        return {
            'cognitive': [
                "Let's break this down into smaller, manageable parts.",
                "Try organizing your ideas using an outline or mind map.",
                "Consider different perspectives on this topic.",
                "Look for patterns and connections in your writing."
            ],
            'metacognitive': [
                "What is your main goal for this writing task?",
                "How do you plan to approach this assignment?",
                "What strategies have worked well for you before?",
                "Take a moment to reflect on your writing process."
            ],
            'social_behavioral': [
                "Consider discussing this topic with classmates or friends.",
                "You might benefit from peer feedback on this draft.",
                "Create a quiet, focused environment for writing.",
                "Set specific times for writing and stick to your schedule."
            ],
            'motivational': [
                "Remember why this writing task is important to you.",
                "Celebrate the progress you've already made.",
                "Break this into smaller goals to maintain motivation.",
                "Focus on improvement rather than perfection."
            ]
        }
    
    def _initialize_feedback_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for writing feedback based on RECIPE4U analysis."""
        return {
            'grammar': [
                r'\b(is|are|was|were)\s+\w+ing\b',  # Progressive tense issues
                r'\b(a|an)\s+(consonant|vowel)',     # Article usage
                r'\b\w+,\s*\w+\b',                   # Comma usage
                r'\b(because|since|although)\s+',    # Subordinate clauses
            ],
            'structure': [
                r'^[A-Z]',                           # Paragraph starts
                r'\.\s+[A-Z]',                       # Sentence boundaries
                r'\b(first|second|third|finally)\b', # Transition words
                r'\b(however|therefore|moreover)\b'   # Logical connectors
            ],
            'vocabulary': [
                r'\b(very|really|quite)\s+\w+',      # Intensifiers
                r'\b(good|bad|nice|big)\b',          # Basic adjectives
                r'\b(thing|stuff|get|put)\b'         # Vague words
            ]
        }
    
    def generate_response(self, processed_input: Dict) -> Dict:
        """
        Generate appropriate response based on processed user input.
        Main entry point for the Assistant Agent.
        """
        intent = processed_input['intent']
        context = processed_input['context']
        learner_profile = processed_input['learner_profile']
        
        # Select appropriate response strategy
        if intent == IntentType.ANSWER.value:
            response = self._handle_answer_request(processed_input)
        elif intent == IntentType.R_LANGUAGE_USE.value:
            response = self._handle_language_use_request(processed_input)
        elif intent == IntentType.R_REVISION.value:
            response = self._handle_revision_request(processed_input)
        elif intent == IntentType.R_EVALUATION.value:
            response = self._handle_evaluation_request(processed_input)
        elif intent == IntentType.R_GENERATION.value:
            response = self._handle_generation_request(processed_input)
        elif intent == IntentType.R_INFORMATION.value:
            response = self._handle_information_request(processed_input)
        elif intent == IntentType.ACK.value:
            response = self._handle_acknowledgment(processed_input)
        elif intent == IntentType.NEGOTIATION.value:
            response = self._handle_negotiation(processed_input)
        else:
            response = self._handle_general_request(processed_input)
        
        # Add SRL strategy suggestions
        response = self._add_srl_strategies(response, context, learner_profile)
        
        # Personalize response based on learner profile
        response = self._personalize_response(response, learner_profile)
        
        return response
    
    def _handle_answer_request(self, processed_input: Dict) -> Dict:
        """Handle direct answer requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Extract question from input
        question = self._extract_question(user_input)
        
        response_content = f"""I'd be happy to help answer your question about {question}.

Let me provide a clear explanation:

{self._generate_educational_content(question, processed_input['learner_profile'])}

Does this answer your question? Feel free to ask for more details or clarification on any part."""
        
        return {
            'content': response_content,
            'type': 'answer',
            'suggestions': self._get_follow_up_suggestions(question),
            'srl_focus': 'cognitive'
        }
    
    def _handle_language_use_request(self, processed_input: Dict) -> Dict:
        """Handle language use and grammar requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Analyze text for language issues
        language_analysis = self._analyze_language_use(user_input)
        
        response_content = f"""I can help you improve the language in your writing. Here are some specific suggestions:

{self._format_language_feedback(language_analysis)}

These changes will make your writing clearer and more professional. Would you like me to explain any of these suggestions in more detail?"""
        
        return {
            'content': response_content,
            'type': 'language_feedback',
            'analysis': language_analysis,
            'srl_focus': 'cognitive'
        }
    
    def _handle_revision_request(self, processed_input: Dict) -> Dict:
        """Handle revision and editing requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Analyze text for revision opportunities
        revision_analysis = self._analyze_for_revision(user_input)
        
        response_content = f"""Let's work on revising your text together. I've identified several areas for improvement:

{self._format_revision_suggestions(revision_analysis)}

These revisions will strengthen your argument and improve clarity. Would you like to work on any specific area first?"""
        
        return {
            'content': response_content,
            'type': 'revision_feedback',
            'analysis': revision_analysis,
            'srl_focus': 'metacognitive'
        }
    
    def _handle_evaluation_request(self, processed_input: Dict) -> Dict:
        """Handle evaluation and assessment requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Evaluate writing quality
        evaluation = self._evaluate_writing(user_input, processed_input['learner_profile'])
        
        response_content = f"""Here's my evaluation of your writing:

**Strengths:**
{self._format_strengths(evaluation['strengths'])}

**Areas for Improvement:**
{self._format_improvements(evaluation['improvements'])}

**Overall Assessment:**
{evaluation['overall_feedback']}

You're making excellent progress! Keep up the good work and continue focusing on these areas."""
        
        return {
            'content': response_content,
            'type': 'evaluation',
            'evaluation': evaluation,
            'srl_focus': 'metacognitive'
        }
    
    def _handle_generation_request(self, processed_input: Dict) -> Dict:
        """Handle content generation requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Generate content based on request
        generated_content = self._generate_writing_content(user_input, processed_input['learner_profile'])
        
        response_content = f"""I can help you generate content for your writing. Here are some ideas and examples:

{generated_content}

Use these as starting points and develop them in your own voice. Remember to cite any sources you use and make the content your own."""
        
        return {
            'content': response_content,
            'type': 'content_generation',
            'generated_content': generated_content,
            'srl_focus': 'cognitive'
        }
    
    def _handle_information_request(self, processed_input: Dict) -> Dict:
        """Handle information and explanation requests."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        # Extract topic from request
        topic = self._extract_topic(user_input)
        
        response_content = f"""Here's the information you requested about {topic}:

{self._provide_educational_information(topic, processed_input['learner_profile'])}

This information should help you with your writing. Let me know if you need more details on any specific aspect."""
        
        return {
            'content': response_content,
            'type': 'information',
            'topic': topic,
            'srl_focus': 'cognitive'
        }
    
    def _handle_acknowledgment(self, processed_input: Dict) -> Dict:
        """Handle acknowledgment and confirmation responses."""
        response_content = """Great! I'm glad that was helpful. 

What would you like to work on next? I can help you with:
- Reviewing and improving your writing
- Generating new content or ideas
- Explaining writing concepts
- Providing feedback on your work

Feel free to ask me anything about your writing!"""
        
        return {
            'content': response_content,
            'type': 'acknowledgment',
            'srl_focus': 'motivational'
        }
    
    def _handle_negotiation(self, processed_input: Dict) -> Dict:
        """Handle negotiation and discussion responses."""
        user_input = processed_input['context']['user_input'] if 'user_input' in processed_input['context'] else ""
        
        response_content = f"""I understand you have a different perspective. Let's discuss this further.

{self._generate_discussion_response(user_input)}

What are your thoughts on this? I'm here to help you explore different approaches and find what works best for your writing."""
        
        return {
            'content': response_content,
            'type': 'negotiation',
            'srl_focus': 'social_behavioral'
        }
    
    def _handle_general_request(self, processed_input: Dict) -> Dict:
        """Handle general or unclear requests."""
        response_content = """I'm here to help you with your writing! I can assist you with:

- **Grammar and Language Use**: Improving sentence structure, word choice, and clarity
- **Content Development**: Generating ideas, organizing thoughts, and developing arguments
- **Revision and Editing**: Reviewing your work and suggesting improvements
- **Writing Strategies**: Teaching techniques for better writing

What specific aspect of writing would you like to work on today?"""
        
        return {
            'content': response_content,
            'type': 'general',
            'srl_focus': 'metacognitive'
        }
    
    def _add_srl_strategies(self, response: Dict, context: Dict, learner_profile: Dict) -> Dict:
        """Add self-regulated learning strategy suggestions to response."""
        srl_focus = response.get('srl_focus', 'cognitive')
        
        if srl_focus in self.srl_strategies:
            strategies = self.srl_strategies[srl_focus]
            # Select appropriate strategy based on context
            selected_strategy = self._select_srl_strategy(strategies, context, learner_profile)
            
            response['srl_suggestion'] = selected_strategy
            response['content'] += f"\n\n**Learning Strategy Tip:** {selected_strategy}"
        
        return response
    
    def _personalize_response(self, response: Dict, learner_profile: Dict) -> Dict:
        """Personalize response based on learner profile."""
        # Adjust language complexity based on proficiency level
        proficiency = learner_profile.get('proficiency_level', 'intermediate')
        
        if proficiency == 'beginner':
            response['content'] = self._simplify_language(response['content'])
        elif proficiency == 'advanced':
            response['content'] = self._enhance_language(response['content'])
        
        # Add course-specific context
        course_type = learner_profile.get('course_type', 'general')
        if course_type == 'SW':  # Scientific Writing
            response['content'] += "\n\n*Note: For scientific writing, focus on clarity, precision, and logical structure.*"
        elif course_type == 'AW':  # Advanced Writing
            response['content'] += "\n\n*Note: Consider advanced rhetorical strategies and sophisticated argumentation.*"
        
        return response
    
    # Helper methods for content analysis and generation
    
    def _extract_question(self, text: str) -> str:
        """Extract the main question or topic from user input."""
        # Simple extraction - in practice, this would use more sophisticated NLP
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who']
        
        for word in question_words:
            if word in text.lower():
                # Extract sentence containing question word
                sentences = text.split('.')
                for sentence in sentences:
                    if word in sentence.lower():
                        return sentence.strip()
        
        return "your writing question"
    
    def _analyze_language_use(self, text: str) -> Dict:
        """Analyze text for language use issues."""
        analysis = {
            'grammar_issues': [],
            'vocabulary_suggestions': [],
            'structure_improvements': []
        }
        
        # Check for common grammar patterns
        for pattern in self.writing_feedback_patterns['grammar']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                analysis['grammar_issues'].extend(matches)
        
        # Check vocabulary usage
        for pattern in self.writing_feedback_patterns['vocabulary']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                analysis['vocabulary_suggestions'].extend(matches)
        
        return analysis
    
    def _format_language_feedback(self, analysis: Dict) -> str:
        """Format language analysis into readable feedback."""
        feedback = []
        
        if analysis['grammar_issues']:
            feedback.append("**Grammar Suggestions:**")
            for issue in analysis['grammar_issues'][:3]:  # Limit to top 3
                feedback.append(f"- Consider revising: '{issue}'")
        
        if analysis['vocabulary_suggestions']:
            feedback.append("\n**Vocabulary Enhancements:**")
            for suggestion in analysis['vocabulary_suggestions'][:3]:
                feedback.append(f"- Try using more specific words instead of: '{suggestion}'")
        
        return '\n'.join(feedback) if feedback else "Your language use looks good overall!"
    
    def _generate_educational_content(self, topic: str, learner_profile: Dict) -> str:
        """Generate educational content based on topic and learner level."""
        # This would integrate with the LLM in practice
        return f"Here's an explanation of {topic} tailored to your learning level..."
    
    def _select_srl_strategy(self, strategies: List[str], context: Dict, learner_profile: Dict) -> str:
        """Select appropriate SRL strategy based on context."""
        # Simple selection - in practice, this would be more sophisticated
        return strategies[0] if strategies else "Focus on your learning goals."
    
    def _simplify_language(self, text: str) -> str:
        """Simplify language for beginner learners."""
        # Basic simplification - replace complex words with simpler ones
        replacements = {
            'utilize': 'use',
            'demonstrate': 'show',
            'facilitate': 'help',
            'implement': 'do'
        }
        
        for complex_word, simple_word in replacements.items():
            text = text.replace(complex_word, simple_word)
        
        return text
    
    def _enhance_language(self, text: str) -> str:
        """Enhance language for advanced learners."""
        # Add more sophisticated vocabulary and structures
        return text  # Placeholder for enhancement logic

