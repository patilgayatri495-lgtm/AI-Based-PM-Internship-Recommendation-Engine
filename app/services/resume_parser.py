"""
Resume Parser Module
Extracts information from PDF and DOCX resumes
"""
import os
import json
import re
from app.models import Resume, ResumeExtraction
from app.extensions import db

class ResumeParser:
    """Parse resumes and extract structured information"""
    
    def parse_resume(self, resume_id):
        """
        Parse a resume and extract information
        
        Args:
            resume_id: ID of the resume record
            
        Returns:
            dict: Extracted information
        """
        resume = db.session.get(Resume, resume_id)
        if not resume:
            return None
        
        if resume.source_type == 'url':
            raise ValueError('A resume URL is saved, but its document must be uploaded to analyze it.')

        extension = os.path.splitext(resume.filename or '')[1].lower()
        if extension == '.pdf':
            text = self._extract_pdf_text(resume.file_path)
        elif extension == '.docx':
            text = self._extract_docx_text(resume.file_path)
        elif extension == '.txt':
            with open(resume.file_path, encoding='utf-8') as resume_file:
                text = resume_file.read()
        else:
            raise ValueError('Unsupported resume format. Upload a PDF, DOCX, or TXT file.')

        return self._save_extraction(resume, text)

    def parse_text(self, resume_id, text):
        """Analyze resume text pasted by the user."""
        resume = db.session.get(Resume, resume_id)
        if not resume:
            raise ValueError('Resume record was not found.')
        if not text.strip():
            raise ValueError('Resume text cannot be empty.')
        return self._save_extraction(resume, text)

    def _save_extraction(self, resume, text):
        if not text.strip():
            raise ValueError('No readable text was found in this resume.')

        # Extract structured information
        extracted = {
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'projects': self._extract_projects(text),
            'certifications': self._extract_certifications(text),
            'experience': self._extract_experience(text)
        }
        
        # Save extraction
        extraction = ResumeExtraction.query.filter_by(resume_id=resume.id).first()
        if extraction is None:
            extraction = ResumeExtraction(resume_id=resume.id)
            db.session.add(extraction)
        extraction.raw_text = text
        extraction.extracted_skills = json.dumps(extracted['skills'])
        extraction.extracted_education = json.dumps(extracted['education'])
        extraction.extracted_projects = json.dumps(extracted['projects'])
        extraction.extracted_certifications = json.dumps(extracted['certifications'])
        extraction.extracted_experience = json.dumps(extracted['experience'])
        resume.is_processed = True
        db.session.commit()
        
        return extracted
    
    def _extract_pdf_text(self, file_path):
        """Extract text from PDF using PyMuPDF"""
        import fitz  # PyMuPDF
        with fitz.open(file_path) as doc:
            text = ''.join(page.get_text() for page in doc)
        if not text.strip():
            raise ValueError('No selectable text was found in this PDF. Upload a text-based PDF or paste the resume text.')
        return text
    
    def _extract_docx_text(self, file_path):
        """Extract text from DOCX using python-docx"""
        from docx import Document
        doc = Document(file_path)
        text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        if not text.strip():
            raise ValueError('No text was found in this DOCX file.')
        return text
    
    def _extract_skills(self, text):
        """Extract skills from text using keyword matching"""
        # Expanded technical skills
        skill_keywords = [
            'python', 'java', 'javascript', 'sql', 'html', 'css',
            'react', 'angular', 'vue.js', 'node.js', 'django', 'flask',
            'machine learning', 'data analysis', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'linux', 'c++', 'c#',
            'mongodb', 'postgresql', 'mysql', 'redis', 'graphql',
            'typescript', 'tensorflow', 'pytorch', 'pandas', 'numpy',
            'scikit-learn', 'tableau', 'power bi', 'jenkins', 'ci/cd',
            'rest apis', 'microservices', 'unit testing', 'agile',
            'spring boot', 'php', 'laravel', 'devops', 'cybersecurity',
            'ui/ux', 'quality assurance', 'project management',
            'business analysis', 'digital marketing', 'mobile development',
            'product management', 'product strategy', 'market research',
            'user research', 'product analytics', 'roadmapping',
            'stakeholder management', 'communication', 'leadership',
            'problem solving', 'data visualization', 'excel', 'powerpoint'
        ]
        
        text_lower = text.lower()
        found_skills = []
        display_names = {
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'sql': 'SQL',
            'html': 'HTML',
            'css': 'CSS',
            'aws': 'AWS',
            'gcp': 'GCP',
            'ui/ux': 'UI/UX',
            'c++': 'C++',
            'c#': 'C#',
            'ci/cd': 'CI/CD',
            'rest apis': 'REST APIs',
            'power bi': 'Power BI'
        }
        
        for skill in skill_keywords:
            if re.search(r'(?<!\w)' + re.escape(skill) + r'(?!\w)', text_lower):
                found_skills.append(display_names.get(skill, skill.title()))
        
        return found_skills
    
    def _extract_education(self, text):
        """Extract education information"""
        # Simple pattern matching for education
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            'b.tech', 'b.e.', 'b.sc', 'b.com', 'b.a',
            'm.tech', 'm.e.', 'm.sc', 'mba', 'mca',
            'phd', 'doctorate'
        ]
        
        text_lower = text.lower()
        for pattern in degree_patterns:
            if pattern in text_lower:
                education.append({
                    'qualification': pattern.upper(),
                    'institution': 'Unknown',
                    'year': None
                })
        
        return education
    
    def _extract_projects(self, text):
        """Extract project information"""
        # Simple extraction - look for project keywords
        projects = []
        
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented']
        text_lower = text.lower()
        
        # This is a simplified extraction
        # In production, use more sophisticated NLP
        if any(keyword in text_lower for keyword in project_keywords):
            projects.append({
                'name': 'Extracted from resume',
                'description': 'Project details found in resume'
            })
        
        return projects
    
    def _extract_certifications(self, text):
        """Extract certification information"""
        certifications = []
        
        cert_keywords = ['certified', 'certificate', 'certification']
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in cert_keywords):
            certifications.append({
                'name': 'Certification found in resume',
                'issuer': 'Unknown'
            })
        
        return certifications
    
    def _extract_experience(self, text):
        """Extract work experience information"""
        experience = []
        
        exp_keywords = ['experience', 'worked at', 'employed', 'intern']
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in exp_keywords):
            experience.append({
                'company': 'Company found in resume',
                'role': 'Role found in resume',
                'duration': 'Unknown'
            })
        
        return experience
