"""
Demo data seed script for InternDisha
Populates database with sample data for testing
"""
import sys
import os
from datetime import datetime, date, timedelta
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import *
from werkzeug.security import generate_password_hash

def seed_demo_data():
    """Seed database with demo data"""
    app = create_app('development')
    
    with app.app_context():
        print("Seeding demo data...")
        
        # Check if data already exists
        if User.query.filter_by(email='admin@interndisha.local').first():
            print("Demo data already exists. Skipping seed.")
            return
        
        # Create Admin User
        admin = User(
            email='admin@interndisha.local',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        
        # Create Demo Student Users
        student1 = User(
            email='rahul.kumar@example.com',
            full_name='Rahul Kumar',
            role='student',
            is_active=True
        )
        student1.set_password('Student@123')
        db.session.add(student1)
        
        student2 = User(
            email='priya.sharma@example.com',
            full_name='Priya Sharma',
            role='student',
            is_active=True
        )
        student2.set_password('Student@123')
        db.session.add(student2)
        
        db.session.flush()
        
        # Create Skills (50+ skills)
        skills_data = [
            # Technical Skills
            ('Python', 'technical', ['Python 3', 'Py', 'Python3']),
            ('Java', 'technical', ['Java SE', 'J2EE', 'Java 17']),
            ('JavaScript', 'technical', ['JS', 'ES6', 'ECMAScript']),
            ('SQL', 'technical', ['MySQL', 'PostgreSQL', 'T-SQL']),
            ('HTML/CSS', 'technical', ['HTML5', 'CSS3', 'SASS']),
            ('Machine Learning', 'technical', ['ML', 'AI', 'Artificial Intelligence']),
            ('Data Analysis', 'technical', ['Analytics', 'Data Science', 'Data Mining']),
            ('Cloud Computing', 'technical', ['AWS', 'Azure', 'GCP']),
            ('React', 'technical', ['React.js', 'ReactJS', 'React Native']),
            ('Node.js', 'technical', ['NodeJS', 'Express', 'NestJS']),
            ('C++', 'technical', ['C Plus Plus', 'CPP']),
            ('C#', 'technical', ['C Sharp', '.NET']),
            ('PHP', 'technical', ['PHP 8', 'Laravel']),
            ('TypeScript', 'technical', ['TS', 'Typed JavaScript']),
            ('Angular', 'technical', ['AngularJS', 'Angular 2+']),
            ('Vue.js', 'technical', ['Vue', 'VueJS']),
            ('Django', 'technical', ['Django Framework', 'Python Web']),
            ('Flask', 'technical', ['Flask Framework', 'Python Micro']),
            ('Spring Boot', 'technical', ['Spring', 'Java Spring']),
            ('MongoDB', 'technical', ['NoSQL', 'Document DB']),
            ('Redis', 'technical', ['Cache', 'In-Memory DB']),
            ('Docker', 'technical', ['Containers', 'Containerization']),
            ('Kubernetes', 'technical', ['K8s', 'Container Orchestration']),
            ('Git', 'technical', ['Version Control', 'GitLab']),
            ('Linux', 'technical', ['Unix', 'Shell Scripting']),
            ('REST APIs', 'technical', ['API Design', 'Web Services']),
            ('GraphQL', 'technical', ['GQL', 'Query Language']),
            ('TensorFlow', 'technical', ['Deep Learning', 'Neural Networks']),
            ('PyTorch', 'technical', ['Torch', 'ML Framework']),
            ('Pandas', 'technical', ['Data Manipulation', 'Python Data']),
            ('NumPy', 'technical', ['Numerical Computing', 'Python Math']),
            ('Tableau', 'technical', ['Data Visualization', 'BI']),
            ('Power BI', 'technical', ['Business Intelligence', 'Microsoft BI']),
            ('Jenkins', 'technical', ['CI/CD', 'DevOps']),
            ('CI/CD', 'technical', ['Continuous Integration', 'DevOps']),
            ('Unit Testing', 'technical', ['Testing', 'QA']),
            ('Agile', 'technical', ['Scrum', 'Kanban']),
            ('Microservices', 'technical', ['Microservice Architecture', 'SOA']),
            
            # Soft Skills
            ('Communication', 'soft', ['Verbal Communication', 'Written Communication']),
            ('Teamwork', 'soft', ['Collaboration', 'Team Building']),
            ('Problem Solving', 'soft', ['Critical Thinking', 'Analytical Skills']),
            ('Leadership', 'soft', ['Management', 'Team Lead']),
            ('Time Management', 'soft', ['Productivity', 'Planning']),
            ('Adaptability', 'soft', ['Flexibility', 'Quick Learning']),
            ('Creativity', 'soft', ['Innovation', 'Creative Thinking']),
            ('Presentation Skills', 'soft', ['Public Speaking', 'Communication']),
            ('Conflict Resolution', 'soft', ['Negotiation', 'Mediation']),
            ('Decision Making', 'soft', ['Strategic Thinking', 'Judgment']),
            
            # Domain Skills
            ('Web Development', 'domain', ['Full Stack', 'Frontend', 'Backend']),
            ('Data Science', 'domain', ['Analytics', 'Big Data', 'ML']),
            ('Mobile Development', 'domain', ['Android', 'iOS', 'Flutter']),
            ('DevOps', 'domain', ['Operations', 'Infrastructure', 'Automation']),
            ('Cybersecurity', 'domain', ['InfoSec', 'Network Security']),
            ('UI/UX Design', 'domain', ['User Interface', 'User Experience']),
            ('Quality Assurance', 'domain', ['Testing', 'QA', 'Automation']),
            ('Project Management', 'domain', ['PMP', 'Agile', 'Scrum']),
            ('Business Analysis', 'domain', ['Requirements', 'Stakeholder Management']),
            ('Digital Marketing', 'domain', ['SEO', 'Social Media', 'Content']),
        ]
        
        skills = {}
        for name, category, synonyms in skills_data:
            skill = Skill(
                name=name,
                category=category,
                synonyms=json.dumps(synonyms),
                is_active=True
            )
            db.session.add(skill)
            db.session.flush()
            skills[name] = skill
        
        # Create Organizations (expanded)
        org1 = Organization(
            name='Tech Solutions India Pvt Ltd',
            sector='Information Technology',
            description='Leading IT services company providing software solutions',
            website='https://techsolutions.example.com',
            is_verified=True
        )
        db.session.add(org1)
        
        org2 = Organization(
            name='Data Analytics Corp',
            sector='Data Analytics',
            description='Specialized in data analytics and business intelligence',
            website='https://dataanalytics.example.com',
            is_verified=True
        )
        db.session.add(org2)
        
        org3 = Organization(
            name='Cloud Innovations Ltd',
            sector='Cloud Computing',
            description='Cloud infrastructure and services provider',
            website='https://cloudinnovations.example.com',
            is_verified=True
        )
        db.session.add(org3)
        
        org4 = Organization(
            name='FinTech Solutions',
            sector='Finance',
            description='Financial technology company providing banking solutions',
            website='https://fintechsolutions.example.com',
            is_verified=True
        )
        db.session.add(org4)
        
        org5 = Organization(
            name='HealthCare Systems',
            sector='Healthcare',
            description='Healthcare technology and hospital management systems',
            website='https://healthcaresystems.example.com',
            is_verified=True
        )
        db.session.add(org5)
        
        db.session.flush()
        
        # Create Opportunities (expanded to 10+)
        opportunities_data = [
            {
                'org': org1,
                'title': 'Python Developer Intern',
                'description': 'Work on Python-based backend development projects. Learn Django/Flask frameworks and contribute to real-world applications.',
                'qualification': 'B.Tech/B.E. in Computer Science or related field',
                'minimum_percentage': '60%',
                'skills': ['Python', 'SQL', 'HTML/CSS'],
                'location': 'Bangalore',
                'domain': 'Web Development',
                'role_type': 'Backend Development',
                'stipend': '₹15,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=30),
            },
            {
                'org': org2,
                'title': 'Data Analyst Intern',
                'description': 'Analyze business data and create reports. Work with SQL, Python, and visualization tools to derive insights.',
                'qualification': 'B.Tech/B.E. or B.Sc in Statistics/Computer Science',
                'minimum_percentage': '65%',
                'skills': ['Python', 'SQL', 'Data Analysis', 'Machine Learning'],
                'location': 'Mumbai',
                'domain': 'Data Science',
                'role_type': 'Analytics',
                'stipend': '₹18,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=45),
            },
            {
                'org': org3,
                'title': 'Cloud Infrastructure Intern',
                'description': 'Learn cloud deployment and infrastructure management. Work with AWS/Azure services and DevOps tools.',
                'qualification': 'B.Tech/B.E. in IT/Computer Science',
                'minimum_percentage': '60%',
                'skills': ['Cloud Computing', 'Python', 'Linux'],
                'location': 'Hyderabad',
                'domain': 'Cloud Computing',
                'role_type': 'Infrastructure',
                'stipend': '₹20,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=60),
            },
            {
                'org': org1,
                'title': 'Frontend Developer Intern',
                'description': 'Build responsive web interfaces using React and modern JavaScript. Collaborate with design and backend teams.',
                'qualification': 'B.Tech/B.E. in Computer Science or related field',
                'minimum_percentage': '60%',
                'skills': ['JavaScript', 'HTML/CSS', 'React'],
                'location': 'Delhi',
                'domain': 'Web Development',
                'role_type': 'Frontend Development',
                'stipend': '₹14,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=25),
            },
            {
                'org': org2,
                'title': 'Machine Learning Intern',
                'description': 'Work on ML model development and deployment. Experience with Python, scikit-learn, and deep learning frameworks.',
                'qualification': 'M.Tech or B.Tech in Computer Science with ML specialization',
                'minimum_percentage': '70%',
                'skills': ['Python', 'Machine Learning', 'Data Analysis'],
                'location': 'Pune',
                'domain': 'Data Science',
                'role_type': 'AI/ML',
                'stipend': '₹22,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=40),
            },
            {
                'org': org4,
                'title': 'Financial Analyst Intern',
                'description': 'Analyze financial data and create reports. Work with banking systems and financial modeling tools.',
                'qualification': 'B.Com/BBA/MBA in Finance or related field',
                'minimum_percentage': '60%',
                'skills': ['Data Analysis', 'SQL', 'Communication'],
                'location': 'Mumbai',
                'domain': 'Finance',
                'role_type': 'Financial Analysis',
                'stipend': '₹16,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=35),
            },
            {
                'org': org5,
                'title': 'Healthcare IT Intern',
                'description': 'Work on healthcare management systems and patient data analysis. Learn healthcare technology standards.',
                'qualification': 'B.Tech/B.E. in IT/Computer Science or B.Sc in Health Informatics',
                'minimum_percentage': '60%',
                'skills': ['Python', 'SQL', 'Communication'],
                'location': 'Chennai',
                'domain': 'Healthcare',
                'role_type': 'Healthcare IT',
                'stipend': '₹17,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=50),
            },
            {
                'org': org3,
                'title': 'DevOps Engineer Intern',
                'description': 'Learn CI/CD pipelines, containerization, and infrastructure automation. Work with Docker, Kubernetes, and Jenkins.',
                'qualification': 'B.Tech/B.E. in Computer Science/IT',
                'minimum_percentage': '65%',
                'skills': ['Cloud Computing', 'Docker', 'Linux', 'CI/CD'],
                'location': 'Bangalore',
                'domain': 'DevOps',
                'role_type': 'DevOps',
                'stipend': '₹21,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=55),
            },
            {
                'org': org1,
                'title': 'Full Stack Developer Intern',
                'description': 'Work on both frontend and backend development. Learn React, Node.js, and database management.',
                'qualification': 'B.Tech/B.E. in Computer Science',
                'minimum_percentage': '65%',
                'skills': ['JavaScript', 'Node.js', 'React', 'SQL'],
                'location': 'Gurugram',
                'domain': 'Web Development',
                'role_type': 'Full Stack',
                'stipend': '₹19,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=28),
            },
            {
                'org': org2,
                'title': 'Business Intelligence Intern',
                'description': 'Create dashboards and reports using Tableau/Power BI. Analyze business data and provide insights.',
                'qualification': 'B.Tech/B.E. or B.Sc in Computer Science/Statistics',
                'minimum_percentage': '60%',
                'skills': ['Data Analysis', 'Tableau', 'Power BI', 'SQL'],
                'location': 'Bangalore',
                'domain': 'Data Science',
                'role_type': 'Business Intelligence',
                'stipend': '₹17,500/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=42),
            },
            {
                'org': org4,
                'title': 'Cybersecurity Intern',
                'description': 'Learn network security, vulnerability assessment, and security best practices. Work with security tools and protocols.',
                'qualification': 'B.Tech/B.E. in Computer Science/IT with cybersecurity interest',
                'minimum_percentage': '65%',
                'skills': ['Linux', 'Communication', 'Problem Solving'],
                'location': 'Pune',
                'domain': 'Cybersecurity',
                'role_type': 'Security',
                'stipend': '₹20,000/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=38),
            },
            {
                'org': org5,
                'title': 'UI/UX Design Intern',
                'description': 'Design user interfaces and experiences for healthcare applications. Learn design tools and user research.',
                'qualification': 'B.Des/B.Tech in Design/Computer Science',
                'minimum_percentage': '60%',
                'skills': ['Creativity', 'Communication', 'Teamwork'],
                'location': 'Mumbai',
                'domain': 'UI/UX Design',
                'role_type': 'Design',
                'stipend': '₹15,500/month',
                'duration': '6 months',
                'deadline': date.today() + timedelta(days=33),
            },
        ]
        
        for opp_data in opportunities_data:
            opp = Opportunity(
                organization_id=opp_data['org'].id,
                title=opp_data['title'],
                description=opp_data['description'],
                qualification_required=opp_data['qualification'],
                minimum_percentage=opp_data['minimum_percentage'],
                skills_required=json.dumps(opp_data['skills']),
                location=opp_data['location'],
                domain=opp_data['domain'],
                role_type=opp_data['role_type'],
                stipend=opp_data['stipend'],
                duration=opp_data['duration'],
                application_deadline=opp_data['deadline'],
                is_published=True,
                is_sample=True,  # Mark as demo data
                source_url='https://example.com/pm-internship',
                verification_date=datetime.utcnow()
            )
            db.session.add(opp)
            db.session.flush()
            
            # Add opportunity skills
            for skill_name in opp_data['skills']:
                if skill_name in skills:
                    opp_skill = OpportunitySkill(
                        opportunity_id=opp.id,
                        skill_id=skills[skill_name].id,
                        is_required=True
                    )
                    db.session.add(opp_skill)
        
        # Create Student Profiles
        profile1 = StudentProfile(
            user_id=student1.id,
            phone_number='+91 9876543210',
            state='Maharashtra',
            district='Pune',
            preferred_language='en',
            preferred_industries=json.dumps(['Information Technology', 'Data Analytics']),
            preferred_domains=json.dumps(['Web Development', 'Data Science']),
            preferred_roles=json.dumps(['Backend Developer', 'Data Analyst']),
            preferred_location='Pune',
            relocation_preference='yes',
            completion_percentage=75
        )
        db.session.add(profile1)
        
        profile2 = StudentProfile(
            user_id=student2.id,
            phone_number='+91 9876543211',
            state='Karnataka',
            district='Bangalore',
            preferred_language='en',
            preferred_industries=json.dumps(['Information Technology']),
            preferred_domains=json.dumps(['Web Development']),
            preferred_roles=json.dumps(['Frontend Developer']),
            preferred_location='Bangalore',
            relocation_preference='no',
            completion_percentage=60
        )
        db.session.add(profile2)
        
        db.session.flush()
        
        # Create Education Records
        edu1 = EducationRecord(
            profile_id=profile1.id,
            highest_qualification='B.Tech',
            course='Computer Science and Engineering',
            specialization='Data Science',
            institution='Government College of Engineering, Pune',
            graduation_year=2025,
            current_status='pursuing',
            percentage_cgpa='8.5 CGPA'
        )
        db.session.add(edu1)
        
        edu2 = EducationRecord(
            profile_id=profile2.id,
            highest_qualification='B.Tech',
            course='Information Technology',
            specialization='Web Technologies',
            institution='RV College of Engineering, Bangalore',
            graduation_year=2025,
            current_status='pursuing',
            percentage_cgpa='8.0 CGPA'
        )
        db.session.add(edu2)
        
        # Create Student Skills
        student1_skills = [
            ('Python', 'intermediate'),
            ('SQL', 'intermediate'),
            ('Machine Learning', 'beginner'),
            ('Communication', 'advanced'),
            ('Teamwork', 'advanced'),
        ]
        
        for skill_name, proficiency in student1_skills:
            if skill_name in skills:
                ss = StudentSkill(
                    user_id=student1.id,
                    skill_id=skills[skill_name].id,
                    proficiency_level=proficiency,
                    source='manual'
                )
                db.session.add(ss)
        
        student2_skills = [
            ('JavaScript', 'intermediate'),
            ('HTML/CSS', 'advanced'),
            ('React', 'intermediate'),
            ('Communication', 'advanced'),
            ('Problem Solving', 'intermediate'),
        ]
        
        for skill_name, proficiency in student2_skills:
            if skill_name in skills:
                ss = StudentSkill(
                    user_id=student2.id,
                    skill_id=skills[skill_name].id,
                    proficiency_level=proficiency,
                    source='manual'
                )
                db.session.add(ss)
        
        # Create Eligibility Rules
        eligibility_rules = [
            {
                'name': 'Minimum Qualification',
                'description': 'Candidate must have at least a bachelor\'s degree',
                'rule_type': 'qualification',
                'condition': json.dumps({'min_level': 'bachelor'}),
                'is_mandatory': True,
                'source': 'PM Internship Scheme Guidelines'
            },
            {
                'name': 'Age Limit',
                'description': 'Candidate age should be between 21-24 years',
                'rule_type': 'age',
                'condition': json.dumps({'min_age': 21, 'max_age': 24}),
                'is_mandatory': True,
                'source': 'PM Internship Scheme Guidelines'
            },
            {
                'name': 'Not Employed',
                'description': 'Candidate should not be currently employed or engaged in full-time education',
                'rule_type': 'employment_status',
                'condition': json.dumps({'employed': False, 'full_time_education': False}),
                'is_mandatory': True,
                'source': 'PM Internship Scheme Guidelines'
            },
        ]
        
        for rule_data in eligibility_rules:
            rule = EligibilityRule(
                name=rule_data['name'],
                description=rule_data['description'],
                rule_type=rule_data['rule_type'],
                condition=rule_data['condition'],
                is_mandatory=rule_data['is_mandatory'],
                is_active=True,
                source=rule_data['source'],
                verification_date=datetime.utcnow()
            )
            db.session.add(rule)
        
        # Create Learning Resources
        learning_resources = [
            {
                'skill': 'Python',
                'title': 'Python for Everybody Specialization',
                'description': 'Comprehensive Python course from University of Michigan',
                'url': 'https://www.coursera.org/specializations/python',
                'resource_type': 'course',
                'provider': 'Coursera'
            },
            {
                'skill': 'SQL',
                'title': 'SQL for Data Science',
                'description': 'Learn SQL fundamentals for data analysis',
                'url': 'https://www.coursera.org/learn/sql-for-data-science',
                'resource_type': 'course',
                'provider': 'Coursera'
            },
            {
                'skill': 'Machine Learning',
                'title': 'Machine Learning Specialization',
                'description': 'Andrew Ng\'s famous ML course',
                'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                'resource_type': 'course',
                'provider': 'Coursera'
            },
            {
                'skill': 'React',
                'title': 'React - The Complete Guide',
                'description': 'Comprehensive React course on Udemy',
                'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux',
                'resource_type': 'course',
                'provider': 'Udemy'
            },
        ]
        
        for lr_data in learning_resources:
            if lr_data['skill'] in skills:
                lr = LearningResource(
                    skill_id=skills[lr_data['skill']].id,
                    title=lr_data['title'],
                    description=lr_data['description'],
                    url=lr_data['url'],
                    resource_type=lr_data['resource_type'],
                    provider=lr_data['provider'],
                    is_verified=True
                )
                db.session.add(lr)
        
        # Commit all changes
        db.session.commit()
        
        print("\nDemo data seeded successfully!")
        print("\nCreated:")
        print(f"- 1 Admin user (admin@interndisha.local / Admin@123)")
        print(f"- 2 Student users (rahul.kumar@example.com / Student@123)")
        print(f"- 15 Skills")
        print(f"- 3 Organizations")
        print(f"- 5 Opportunities (marked as sample data)")
        print(f"- 2 Student profiles")
        print(f"- 2 Education records")
        print(f"- 10 Student skills")
        print(f"- 3 Eligibility rules")
        print(f"- 4 Learning resources")
        print("\nNote: Opportunities are marked as sample/demo data.")
        print("In production, import real opportunities from official sources.")

if __name__ == '__main__':
    seed_demo_data()
