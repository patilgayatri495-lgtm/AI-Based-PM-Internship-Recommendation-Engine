"""
Eligibility Evaluation Engine
Evaluates student eligibility based on configurable rules
"""
import json
from app.extensions import db
from app.models import EligibilityRule, StudentProfile, EducationRecord, StudentSkill

class EligibilityEngine:
    """Engine for evaluating student eligibility against rules"""
    
    def __init__(self):
        self.rules = EligibilityRule.query.filter_by(is_active=True).all()
    
    def evaluate_student(self, user_id):
        """
        Evaluate a student's eligibility
        
        Returns:
            dict: Eligibility status with details
        """
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        education = EducationRecord.query.filter_by(profile_id=profile.id).all() if profile else []
        skills = StudentSkill.query.filter_by(user_id=user_id).all()
        
        results = {
            'eligible': True,
            'mandatory_failures': [],
            'warnings': [],
            'insufficient_info': []
        }
        
        for rule in self.rules:
            if not rule.is_mandatory:
                continue
            
            evaluation = self._evaluate_rule(rule, profile, education, skills)
            
            if evaluation['status'] == 'fail':
                results['eligible'] = False
                results['mandatory_failures'].append({
                    'rule': rule.name,
                    'reason': evaluation['reason']
                })
            elif evaluation['status'] == 'warning':
                results['warnings'].append({
                    'rule': rule.name,
                    'reason': evaluation['reason']
                })
            elif evaluation['status'] == 'insufficient_info':
                results['insufficient_info'].append({
                    'rule': rule.name,
                    'reason': evaluation['reason']
                })
        
        # Determine overall status
        if results['mandatory_failures']:
            results['overall_status'] = 'ineligible'
        elif results['insufficient_info']:
            results['overall_status'] = 'insufficient_info'
        else:
            results['overall_status'] = 'eligible'
        
        return results
    
    def _evaluate_rule(self, rule, profile, education, skills):
        """
        Evaluate a single eligibility rule
        
        Returns:
            dict: Evaluation result with status and reason
        """
        condition = json.loads(rule.condition) if rule.condition else {}
        
        if rule.rule_type == 'qualification':
            return self._evaluate_qualification(condition, education)
        elif rule.rule_type == 'age':
            return self._evaluate_age(condition, profile)
        elif rule.rule_type == 'employment_status':
            return self._evaluate_employment(condition, profile)
        else:
            return {'status': 'insufficient_info', 'reason': 'Unknown rule type'}
    
    def _evaluate_qualification(self, condition, education):
        """Evaluate qualification requirements"""
        min_level = condition.get('min_level', 'bachelor')
        
        if not education:
            return {'status': 'insufficient_info', 'reason': 'No education records found'}
        
        # Check if any education meets minimum level
        qualification_levels = {
            'diploma': 1,
            'bachelor': 2,
            'master': 3,
            'phd': 4
        }
        
        for edu in education:
            qual = edu.highest_qualification.lower() if edu.highest_qualification else ''
            if 'b.tech' in qual or 'b.e.' in qual or 'b.sc' in qual or 'b.com' in qual or 'b.a' in qual:
                if qualification_levels.get('bachelor', 0) >= qualification_levels.get(min_level, 0):
                    return {'status': 'pass', 'reason': 'Qualification meets requirement'}
            elif 'm.tech' in qual or 'm.e.' in qual or 'm.sc' in qual or 'mba' in qual:
                if qualification_levels.get('master', 0) >= qualification_levels.get(min_level, 0):
                    return {'status': 'pass', 'reason': 'Qualification meets requirement'}
        
        return {'status': 'fail', 'reason': f'Qualification below minimum level ({min_level})'}
    
    def _evaluate_age(self, condition, profile):
        """Evaluate age requirements"""
        # Note: Age is not currently stored in profile
        # This is a placeholder for future implementation
        return {'status': 'insufficient_info', 'reason': 'Age information not provided'}
    
    def _evaluate_employment(self, condition, profile):
        """Evaluate employment status requirements"""
        # Note: Employment status is not currently stored in profile
        # This is a placeholder for future implementation
        return {'status': 'insufficient_info', 'reason': 'Employment status not provided'}
