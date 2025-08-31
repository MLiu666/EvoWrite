"""
Checker Agent Implementation
Handles quality assurance, validation, and consistency checking.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.models.sage_agents import Interaction, LearnerProfile

class CheckerAgent:
    """
    Checker Agent responsible for:
    - Quality validation of assistant responses
    - Educational appropriateness checking
    - Consistency verification across sessions
    - Bias detection and mitigation
    - Learning outcome assessment
    """
    
    def __init__(self):
        self.quality_criteria = self._initialize_quality_criteria()
        self.educational_standards = self._initialize_educational_standards()
        self.bias_patterns = self._initialize_bias_patterns()
        self.consistency_checks = self._initialize_consistency_checks()
        
    def _initialize_quality_criteria(self) -> Dict[str, Dict]:
        """Initialize quality assessment criteria."""
        return {
            'clarity': {
                'min_score': 0.7,
                'indicators': ['clear explanation', 'step-by-step', 'examples provided'],
                'negative_indicators': ['vague', 'confusing', 'unclear']
            },
            'accuracy': {
                'min_score': 0.8,
                'indicators': ['factually correct', 'proper grammar', 'appropriate terminology'],
                'negative_indicators': ['incorrect information', 'grammar errors', 'misleading']
            },
            'helpfulness': {
                'min_score': 0.7,
                'indicators': ['actionable advice', 'specific suggestions', 'relevant examples'],
                'negative_indicators': ['generic response', 'unhelpful', 'irrelevant']
            },
            'engagement': {
                'min_score': 0.6,
                'indicators': ['encouraging tone', 'interactive elements', 'motivational'],
                'negative_indicators': ['dry', 'boring', 'discouraging']
            }
        }
    
    def _initialize_educational_standards(self) -> Dict[str, List[str]]:
        """Initialize educational appropriateness standards."""
        return {
            'age_appropriate': [
                'suitable language level',
                'appropriate content complexity',
                'no inappropriate references'
            ],
            'pedagogically_sound': [
                'builds on prior knowledge',
                'scaffolded learning',
                'clear learning objectives',
                'promotes self-regulation'
            ],
            'culturally_sensitive': [
                'respects cultural differences',
                'inclusive language',
                'avoids stereotypes',
                'considers EFL context'
            ],
            'academically_rigorous': [
                'accurate information',
                'proper citations when needed',
                'evidence-based suggestions',
                'promotes critical thinking'
            ]
        }
    
    def _initialize_bias_patterns(self) -> Dict[str, List[str]]:
        """Initialize bias detection patterns."""
        return {
            'gender_bias': [
                r'\b(he|his|him)\b.*\b(strong|leader|assertive)\b',
                r'\b(she|her)\b.*\b(emotional|sensitive|nurturing)\b'
            ],
            'cultural_bias': [
                r'\b(western|eastern)\s+(way|approach|method)\b',
                r'\b(american|chinese|korean)\s+(students|learners)\s+(are|tend to)\b'
            ],
            'linguistic_bias': [
                r'\bnative\s+speaker\b',
                r'\bperfect\s+english\b',
                r'\bbroken\s+english\b'
            ],
            'ability_bias': [
                r'\b(smart|intelligent)\s+(students|learners)\b',
                r'\b(slow|weak)\s+(learners|students)\b'
            ]
        }
    
    def _initialize_consistency_checks(self) -> Dict[str, str]:
        """Initialize consistency checking patterns."""
        return {
            'terminology': 'Check for consistent use of technical terms',
            'tone': 'Verify consistent supportive and encouraging tone',
            'difficulty_level': 'Ensure appropriate difficulty progression',
            'learning_objectives': 'Align with stated learning goals',
            'feedback_style': 'Maintain consistent feedback approach'
        }
    
    def validate_response(self, assistant_response: Dict, processed_input: Dict, 
                         interaction_id: int) -> Dict:
        """
        Main validation function for assistant responses.
        Returns validation results and recommendations.
        """
        validation_results = {
            'overall_score': 0.0,
            'quality_scores': {},
            'educational_compliance': {},
            'bias_detection': {},
            'consistency_check': {},
            'recommendations': [],
            'approved': False,
            'issues': []
        }
        
        # Perform quality assessment
        quality_scores = self._assess_quality(assistant_response, processed_input)
        validation_results['quality_scores'] = quality_scores
        
        # Check educational appropriateness
        educational_compliance = self._check_educational_standards(
            assistant_response, processed_input
        )
        validation_results['educational_compliance'] = educational_compliance
        
        # Detect potential biases
        bias_detection = self._detect_bias(assistant_response)
        validation_results['bias_detection'] = bias_detection
        
        # Check consistency with previous interactions
        consistency_check = self._check_consistency(assistant_response, processed_input)
        validation_results['consistency_check'] = consistency_check
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            quality_scores, educational_compliance, bias_detection, consistency_check
        )
        validation_results['overall_score'] = overall_score
        
        # Generate recommendations
        recommendations = self._generate_recommendations(validation_results)
        validation_results['recommendations'] = recommendations
        
        # Determine approval status
        validation_results['approved'] = overall_score >= 0.7 and len(bias_detection['detected_biases']) == 0
        
        # Store validation results
        self._store_validation_results(interaction_id, validation_results)
        
        return validation_results
    
    def _assess_quality(self, assistant_response: Dict, processed_input: Dict) -> Dict:
        """Assess the quality of the assistant response."""
        content = assistant_response.get('content', '')
        response_type = assistant_response.get('type', 'general')
        
        quality_scores = {}
        
        for criterion, criteria_config in self.quality_criteria.items():
            score = self._calculate_criterion_score(content, criteria_config)
            quality_scores[criterion] = {
                'score': score,
                'meets_threshold': score >= criteria_config['min_score'],
                'details': self._get_criterion_details(content, criteria_config)
            }
        
        return quality_scores
    
    def _calculate_criterion_score(self, content: str, criteria_config: Dict) -> float:
        """Calculate score for a specific quality criterion."""
        positive_count = 0
        negative_count = 0
        
        content_lower = content.lower()
        
        # Count positive indicators
        for indicator in criteria_config['indicators']:
            if indicator.lower() in content_lower:
                positive_count += 1
        
        # Count negative indicators
        for indicator in criteria_config['negative_indicators']:
            if indicator.lower() in content_lower:
                negative_count += 1
        
        # Calculate score (0.0 to 1.0)
        total_indicators = len(criteria_config['indicators'])
        if total_indicators == 0:
            return 0.5  # Default score if no indicators
        
        positive_ratio = positive_count / total_indicators
        negative_penalty = negative_count * 0.2  # Each negative indicator reduces score by 0.2
        
        score = max(0.0, min(1.0, positive_ratio - negative_penalty))
        return score
    
    def _get_criterion_details(self, content: str, criteria_config: Dict) -> Dict:
        """Get detailed analysis for a quality criterion."""
        content_lower = content.lower()
        
        found_positive = []
        found_negative = []
        
        for indicator in criteria_config['indicators']:
            if indicator.lower() in content_lower:
                found_positive.append(indicator)
        
        for indicator in criteria_config['negative_indicators']:
            if indicator.lower() in content_lower:
                found_negative.append(indicator)
        
        return {
            'positive_indicators_found': found_positive,
            'negative_indicators_found': found_negative,
            'content_length': len(content),
            'word_count': len(content.split())
        }
    
    def _check_educational_standards(self, assistant_response: Dict, 
                                   processed_input: Dict) -> Dict:
        """Check compliance with educational standards."""
        content = assistant_response.get('content', '')
        learner_profile = processed_input.get('learner_profile', {})
        
        compliance_results = {}
        
        for standard, requirements in self.educational_standards.items():
            compliance_score = self._assess_educational_compliance(
                content, requirements, learner_profile
            )
            compliance_results[standard] = {
                'score': compliance_score,
                'compliant': compliance_score >= 0.7,
                'requirements_met': self._check_requirements_met(content, requirements)
            }
        
        return compliance_results
    
    def _assess_educational_compliance(self, content: str, requirements: List[str], 
                                     learner_profile: Dict) -> float:
        """Assess compliance with specific educational standard."""
        content_lower = content.lower()
        met_requirements = 0
        
        for requirement in requirements:
            if self._check_requirement(content_lower, requirement, learner_profile):
                met_requirements += 1
        
        return met_requirements / len(requirements) if requirements else 0.0
    
    def _check_requirement(self, content: str, requirement: str, 
                          learner_profile: Dict) -> bool:
        """Check if a specific educational requirement is met."""
        requirement_lower = requirement.lower()
        
        # Simple keyword-based checking (in practice, this would be more sophisticated)
        if 'appropriate' in requirement_lower:
            return len(content) > 50  # Minimum content length
        elif 'scaffolded' in requirement_lower:
            return 'step' in content or 'first' in content or 'next' in content
        elif 'self-regulation' in requirement_lower:
            srl_keywords = ['goal', 'plan', 'monitor', 'reflect', 'strategy']
            return any(keyword in content for keyword in srl_keywords)
        elif 'cultural' in requirement_lower:
            return 'culture' not in content or 'inclusive' in content
        elif 'evidence' in requirement_lower:
            return 'research' in content or 'study' in content or 'evidence' in content
        
        return True  # Default to compliant for unrecognized requirements
    
    def _detect_bias(self, assistant_response: Dict) -> Dict:
        """Detect potential biases in the response."""
        content = assistant_response.get('content', '')
        
        detected_biases = []
        bias_details = {}
        
        for bias_type, patterns in self.bias_patterns.items():
            matches = []
            for pattern in patterns:
                found_matches = re.findall(pattern, content, re.IGNORECASE)
                matches.extend(found_matches)
            
            if matches:
                detected_biases.append(bias_type)
                bias_details[bias_type] = {
                    'matches': matches,
                    'severity': self._assess_bias_severity(matches, bias_type)
                }
        
        return {
            'detected_biases': detected_biases,
            'bias_details': bias_details,
            'bias_free': len(detected_biases) == 0
        }
    
    def _assess_bias_severity(self, matches: List[str], bias_type: str) -> str:
        """Assess the severity of detected bias."""
        if len(matches) >= 3:
            return 'high'
        elif len(matches) >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _check_consistency(self, assistant_response: Dict, processed_input: Dict) -> Dict:
        """Check consistency with previous interactions."""
        learner_id = processed_input.get('learner_profile', {}).get('id')
        
        if not learner_id:
            return {'consistent': True, 'details': 'No previous interactions to compare'}
        
        # Get recent interactions for comparison
        recent_interactions = self._get_recent_interactions(learner_id, limit=5)
        
        consistency_results = {}
        
        for check_type, description in self.consistency_checks.items():
            consistency_score = self._assess_consistency_aspect(
                assistant_response, recent_interactions, check_type
            )
            consistency_results[check_type] = {
                'score': consistency_score,
                'consistent': consistency_score >= 0.7,
                'description': description
            }
        
        overall_consistency = sum(
            result['score'] for result in consistency_results.values()
        ) / len(consistency_results) if consistency_results else 1.0
        
        return {
            'overall_consistency': overall_consistency,
            'aspect_results': consistency_results,
            'consistent': overall_consistency >= 0.7
        }
    
    def _assess_consistency_aspect(self, current_response: Dict, 
                                 recent_interactions: List[Interaction], 
                                 aspect: str) -> float:
        """Assess consistency for a specific aspect."""
        if not recent_interactions:
            return 1.0  # No previous interactions to compare
        
        current_content = current_response.get('content', '').lower()
        
        if aspect == 'tone':
            # Check for consistent encouraging tone
            encouraging_words = ['great', 'excellent', 'good', 'well done', 'keep up']
            current_encouraging = any(word in current_content for word in encouraging_words)
            
            past_encouraging_count = 0
            for interaction in recent_interactions:
                if interaction.assistant_response:
                    past_content = interaction.assistant_response.lower()
                    if any(word in past_content for word in encouraging_words):
                        past_encouraging_count += 1
            
            if len(recent_interactions) == 0:
                return 1.0
            
            past_encouraging_ratio = past_encouraging_count / len(recent_interactions)
            
            # Consistency score based on whether current response matches past pattern
            if past_encouraging_ratio > 0.5 and current_encouraging:
                return 1.0
            elif past_encouraging_ratio <= 0.5 and not current_encouraging:
                return 1.0
            else:
                return 0.5
        
        # Default consistency score for other aspects
        return 0.8
    
    def _get_recent_interactions(self, learner_id: int, limit: int = 5) -> List[Interaction]:
        """Get recent interactions for consistency checking."""
        return Interaction.query.filter_by(
            learner_id=learner_id
        ).filter(
            Interaction.assistant_response.isnot(None)
        ).order_by(
            Interaction.created_at.desc()
        ).limit(limit).all()
    
    def _calculate_overall_score(self, quality_scores: Dict, educational_compliance: Dict,
                               bias_detection: Dict, consistency_check: Dict) -> float:
        """Calculate overall validation score."""
        # Weight different aspects
        weights = {
            'quality': 0.4,
            'educational': 0.3,
            'bias': 0.2,
            'consistency': 0.1
        }
        
        # Calculate weighted scores
        quality_avg = sum(score['score'] for score in quality_scores.values()) / len(quality_scores)
        educational_avg = sum(score['score'] for score in educational_compliance.values()) / len(educational_compliance)
        bias_score = 1.0 if bias_detection['bias_free'] else 0.0
        consistency_score = consistency_check.get('overall_consistency', 1.0)
        
        overall_score = (
            quality_avg * weights['quality'] +
            educational_avg * weights['educational'] +
            bias_score * weights['bias'] +
            consistency_score * weights['consistency']
        )
        
        return round(overall_score, 3)
    
    def _generate_recommendations(self, validation_results: Dict) -> List[str]:
        """Generate improvement recommendations based on validation results."""
        recommendations = []
        
        # Quality recommendations
        for criterion, result in validation_results['quality_scores'].items():
            if not result['meets_threshold']:
                recommendations.append(
                    f"Improve {criterion}: Current score {result['score']:.2f} "
                    f"is below threshold {self.quality_criteria[criterion]['min_score']}"
                )
        
        # Educational compliance recommendations
        for standard, result in validation_results['educational_compliance'].items():
            if not result['compliant']:
                recommendations.append(
                    f"Address {standard} compliance: Score {result['score']:.2f}"
                )
        
        # Bias recommendations
        if validation_results['bias_detection']['detected_biases']:
            for bias_type in validation_results['bias_detection']['detected_biases']:
                recommendations.append(f"Remove {bias_type} from response")
        
        # Consistency recommendations
        consistency_results = validation_results['consistency_check'].get('aspect_results', {})
        for aspect, result in consistency_results.items():
            if not result['consistent']:
                recommendations.append(f"Improve consistency in {aspect}")
        
        return recommendations
    
    def _store_validation_results(self, interaction_id: int, validation_results: Dict) -> None:
        """Store validation results in the database."""
        from src.models.sage_agents import db
        
        interaction = Interaction.query.get(interaction_id)
        if interaction:
            interaction.checker_validation = json.dumps(validation_results)
            db.session.commit()
    
    def get_validation_summary(self, learner_id: int, days: int = 7) -> Dict:
        """Get validation summary for a learner over specified days."""
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        interactions = Interaction.query.filter(
            Interaction.learner_id == learner_id,
            Interaction.created_at >= cutoff_date,
            Interaction.checker_validation.isnot(None)
        ).all()
        
        if not interactions:
            return {'message': 'No validated interactions found'}
        
        # Aggregate validation results
        total_score = 0
        quality_scores = {'clarity': [], 'accuracy': [], 'helpfulness': [], 'engagement': []}
        bias_count = 0
        approved_count = 0
        
        for interaction in interactions:
            try:
                validation_data = json.loads(interaction.checker_validation)
                total_score += validation_data.get('overall_score', 0)
                
                if validation_data.get('approved', False):
                    approved_count += 1
                
                if validation_data.get('bias_detection', {}).get('detected_biases'):
                    bias_count += 1
                
                # Aggregate quality scores
                for criterion, score_data in validation_data.get('quality_scores', {}).items():
                    if criterion in quality_scores:
                        quality_scores[criterion].append(score_data.get('score', 0))
                        
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Calculate averages
        avg_overall_score = total_score / len(interactions) if interactions else 0
        avg_quality_scores = {
            criterion: sum(scores) / len(scores) if scores else 0
            for criterion, scores in quality_scores.items()
        }
        
        return {
            'period_days': days,
            'total_interactions': len(interactions),
            'avg_overall_score': round(avg_overall_score, 3),
            'approval_rate': round(approved_count / len(interactions), 3) if interactions else 0,
            'bias_detection_rate': round(bias_count / len(interactions), 3) if interactions else 0,
            'avg_quality_scores': avg_quality_scores,
            'recommendations': self._generate_learner_recommendations(avg_quality_scores, avg_overall_score)
        }
    
    def _generate_learner_recommendations(self, quality_scores: Dict, overall_score: float) -> List[str]:
        """Generate recommendations for improving interactions with a specific learner."""
        recommendations = []
        
        if overall_score < 0.7:
            recommendations.append("Focus on improving overall response quality")
        
        for criterion, score in quality_scores.items():
            if score < 0.7:
                recommendations.append(f"Improve {criterion} in responses")
        
        if not recommendations:
            recommendations.append("Maintain current high quality standards")
        
        return recommendations

