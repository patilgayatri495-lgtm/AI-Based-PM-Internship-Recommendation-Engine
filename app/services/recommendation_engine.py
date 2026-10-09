"""
Hybrid Recommendation Engine
Combines rule-based eligibility, skill matching, and text similarity
"""
import json
from datetime import date, datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import or_

from app.extensions import db
from app.models import (
    StudentProfile, EducationRecord, StudentSkill,
    Opportunity, OpportunitySkill, Recommendation, RecommendationItem,
    Resume, ResumeExtraction
)
from app.services.eligibility_engine import EligibilityEngine
from config import Config

class RecommendationEngine:
    """Hybrid recommendation engine for internship opportunities"""
    
    def __init__(self):
        self.eligibility_engine = EligibilityEngine()
        self.weights = Config.RECOMMENDATION_WEIGHTS
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def generate_recommendations(self, user_id):
        """
        Generate recommendations for a user
        
        Args:
            user_id: ID of the user to generate recommendations for
            
        Returns:
            int: ID of the generated recommendation
        """
        # Get user profile data
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        education = EducationRecord.query.filter_by(profile_id=profile.id).all() if profile else []
        user_skills = StudentSkill.query.filter_by(user_id=user_id).all()
        
        skill_names = [us.skill.name for us in user_skills if us.skill]
        if profile and profile.skills:
            skill_names.extend(self._json_list(profile.skills))

        resume = Resume.query.filter_by(user_id=user_id).first()
        extraction = ResumeExtraction.query.filter_by(resume_id=resume.id).first() if resume else None
        if extraction and extraction.extracted_skills:
            skill_names.extend(self._json_list(extraction.extracted_skills))
        skill_names = list(dict.fromkeys(skill.strip() for skill in skill_names if skill.strip()))
        profile_text = self._build_profile_text(profile, education, skill_names, extraction)
        
        # Exclude opportunities whose application deadlines have passed.
        opportunities = Opportunity.query.filter_by(is_published=True).filter(
            or_(
                Opportunity.application_deadline.is_(None),
                Opportunity.application_deadline >= date.today()
            )
        ).all()
        
        if not opportunities:
            return None
        
        # Calculate scores for each opportunity
        scored_opportunities = []
        for opp in opportunities:
            score_data = self._calculate_opportunity_score(
                user_id, opp, profile, education, skill_names, profile_text
            )
            scored_opportunities.append({
                'opportunity': opp,
                'score': score_data
            })
        
        # Sort by score
        scored_opportunities.sort(key=lambda x: x['score']['total_score'], reverse=True)
        
        # Create recommendation record
        recommendation = Recommendation(
            user_id=user_id,
            algorithm_version=Config.RECOMMENDATION_ALGORITHM_VERSION,
            profile_snapshot=json.dumps({
                'skills': skill_names,
                'education': [{'qualification': e.highest_qualification, 'course': e.course} for e in education],
                'preferences': {
                    'industries': self._json_list(profile.preferred_industries) if profile else [],
                    'domains': self._json_list(profile.preferred_domains) if profile else [],
                    'location': profile.preferred_location
                } if profile else {},
                'resume_analyzed': extraction is not None
            })
        )
        db.session.add(recommendation)
        db.session.flush()
        
        # Create recommendation items (top 10)
        for rank, item in enumerate(scored_opportunities[:10], 1):
            rec_item = RecommendationItem(
                recommendation_id=recommendation.id,
                opportunity_id=item['opportunity'].id,
                match_score=item['score']['total_score'],
                skills_score=item['score']['skills_score'],
                education_score=item['score']['education_score'],
                text_similarity_score=item['score']['text_similarity_score'],
                preference_score=item['score']['preference_score'],
                location_score=item['score']['location_score'],
                eligibility_status=item['score']['eligibility_status'],
                explanation=item['score']['explanation'],
                matching_skills=json.dumps(item['score']['matching_skills']),
                missing_skills=json.dumps(item['score']['missing_skills']),
                rank=rank
            )
            db.session.add(rec_item)
        
        db.session.commit()
        
        return recommendation.id
    
    def _calculate_opportunity_score(self, user_id, opp, profile, education, user_skills, profile_text):
        """
        Calculate match score for a single opportunity
        
        Returns:
            dict: Score breakdown and explanation
        """
        # Get opportunity skills
        opp_skills = OpportunitySkill.query.filter_by(opportunity_id=opp.id).all()
        opp_skill_names = [item.skill.name for item in opp_skills if item.skill]
        if opp.skills_required:
            opp_skill_names.extend(self._json_list(opp.skills_required))
        opp_skill_names = list(dict.fromkeys(skill.strip() for skill in opp_skill_names if skill.strip()))
        
        # Calculate component scores
        skills_score = self._calculate_skills_score(user_skills, opp_skill_names)
        education_score = self._calculate_education_score(education, opp)
        text_similarity_score = self._calculate_text_similarity(profile_text, opp)
        preference_score = self._calculate_preference_score(profile, opp)
        location_score = self._calculate_location_score(profile, opp)
        
        # Calculate weighted total
        total_score = (
            skills_score * self.weights['skills_match'] +
            education_score * self.weights['education_compatibility'] +
            text_similarity_score * self.weights['text_similarity'] +
            preference_score * self.weights['preference_match'] +
            location_score * self.weights['location_match']
        )
        
        # Determine matching and missing skills
        user_skill_lookup = {skill.casefold(): skill for skill in user_skills}
        opp_skill_lookup = {skill.casefold(): skill for skill in opp_skill_names}
        matching_keys = user_skill_lookup.keys() & opp_skill_lookup.keys()
        matching_skills = sorted(opp_skill_lookup[key] for key in matching_keys)
        missing_skills = sorted(
            skill for key, skill in opp_skill_lookup.items() if key not in user_skill_lookup
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            skills_score, education_score, text_similarity_score,
            preference_score, location_score, matching_skills, missing_skills
        )
        
        # Evaluate eligibility
        eligibility_result = self.eligibility_engine.evaluate_student(user_id)
        eligibility_status = eligibility_result['overall_status']
        
        return {
            'total_score': total_score,
            'skills_score': skills_score,
            'education_score': education_score,
            'text_similarity_score': text_similarity_score,
            'preference_score': preference_score,
            'location_score': location_score,
            'eligibility_status': eligibility_status,
            'explanation': explanation,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills
        }
    
    def _calculate_skills_score(self, user_skills, opp_skills):
        """Calculate skills match score"""
        if not opp_skills:
            return 1.0  # No skills required, full score
        
        if not user_skills:
            return 0.0  # No user skills
        
        # Calculate overlap
        matching = len(set(user_skills) & set(opp_skills))
        total_required = len(opp_skills)
        
        return matching / total_required if total_required > 0 else 1.0
    
    def _calculate_education_score(self, education, opp):
        """Calculate education compatibility score"""
        if not education or not opp.qualification_required:
            return 0.5  # Neutral score when data missing
        
        # Simple matching based on qualification string
        opp_qual = opp.qualification_required.lower()
        
        for edu in education:
            if edu.highest_qualification:
                qual = edu.highest_qualification.lower()
                if 'b.tech' in qual and 'b.tech' in opp_qual:
                    return 1.0
                elif 'b.e.' in qual and 'b.e.' in opp_qual:
                    return 1.0
                elif 'computer science' in qual.lower() and 'computer science' in opp_qual:
                    return 0.9
        
        return 0.3  # Partial match for any bachelor's degree
    
    def _calculate_text_similarity(self, profile_text, opp):
        """Calculate text similarity using TF-IDF"""
        # Build opportunity text
        opp_text = opp.title + ' ' + opp.description
        if opp.skills_required:
            opp_text += ' ' + ' '.join(self._json_list(opp.skills_required))
        
        if not profile_text or not opp_text:
            return 0.5  # Neutral score
        
        # Calculate TF-IDF similarity
        try:
            corpus = [profile_text, opp_text]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except ValueError:
            return 0.5

    def _build_profile_text(self, profile, education, user_skills, extraction):
        """Build searchable text from profile, education, and analyzed resume data."""
        parts = list(user_skills)
        if profile:
            for preference in (
                profile.preferred_domains,
                profile.preferred_roles,
                profile.preferred_industries
            ):
                parts.extend(self._json_list(preference))
        for record in education:
            parts.extend(filter(None, (
                record.course,
                record.specialization,
                record.highest_qualification
            )))
        if extraction and extraction.raw_text:
            parts.append(extraction.raw_text[:10000])
        return ' '.join(parts)
    
    def _calculate_preference_score(self, profile, opp):
        """Calculate preference match score"""
        if not profile:
            return 0.5
        
        score = 0.0
        factors = 0
        
        # Industry preference
        if profile.preferred_industries:
            factors += 1
            industries = self._json_list(profile.preferred_industries)
            if opp.organization.sector in industries:
                score += 1.0
        
        # Domain preference
        if profile.preferred_domains:
            factors += 1
            domains = self._json_list(profile.preferred_domains)
            if opp.domain in domains:
                score += 1.0
        
        # Role preference
        if profile.preferred_roles:
            factors += 1
            roles = self._json_list(profile.preferred_roles)
            if opp.role_type in roles:
                score += 1.0
        
        return score / factors if factors > 0 else 0.5

    @staticmethod
    def _json_list(value):
        """Decode JSON list fields, treating empty or malformed values as empty."""
        if not value:
            return []
        try:
            decoded = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []
        return decoded if isinstance(decoded, list) else []
    
    def _calculate_location_score(self, profile, opp):
        """Calculate location match score"""
        if not profile or not profile.preferred_location or not opp.location:
            return 0.5
        
        if profile.preferred_location.lower() in opp.location.lower():
            return 1.0
        
        # Check relocation preference
        if profile.relocation_preference == 'yes':
            return 0.8
        elif profile.relocation_preference == 'maybe':
            return 0.6
        
        return 0.3
    
    def _generate_explanation(self, skills_score, education_score, text_similarity_score,
                            preference_score, location_score, matching_skills, missing_skills):
        """Generate human-readable explanation"""
        parts = []
        
        if matching_skills:
            parts.append(f"Your profile matches {len(matching_skills)} required skills: {', '.join(matching_skills[:3])}")
        
        if missing_skills:
            parts.append(f"You may want to develop {len(missing_skills)} additional skills: {', '.join(missing_skills[:3])}")
        
        if skills_score > 0.7:
            parts.append("Strong skill alignment with opportunity requirements.")
        elif skills_score > 0.4:
            parts.append("Moderate skill alignment. Consider developing additional skills.")
        
        if education_score > 0.8:
            parts.append("Your education background is well-suited for this role.")
        
        if preference_score > 0.7:
            parts.append("This opportunity aligns with your industry and role preferences.")
        
        if location_score > 0.8:
            parts.append("Location matches your preference.")
        
        return '. '.join(parts) + '.' if parts else "Based on your profile, this opportunity may be relevant."
