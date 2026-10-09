# InternDisha - AI-Based Personalized PM Internship Scheme Recommendation Engine

## Overview

InternDisha is an independent academic project that helps students discover relevant internship opportunities through personalized recommendations. The project is inspired by the Prime Minister's Internship Scheme (PMIS) and uses AI/ML techniques to match student profiles with suitable opportunities.

**Important Disclaimer:** InternDisha is an independent academic project and is not affiliated with or endorsed by the Government of India. Final eligibility, application acceptance, and selection are determined by the official authorities.

## Features

- **User Authentication**: Secure registration, login, and profile management
- **Profile Management**: Multi-step profile completion with education, skills, and preferences
- **Resume Analysis**: Upload PDF/DOCX/TXT resumes or paste resume text; automatically extract skills, add them to the student profile, and use resume content in matching
- **Recommendation Engine**: Hybrid AI-powered recommendation system using:
  - Skill matching (35%)
  - Education compatibility (20%)
  - Text similarity (20%)
  - Preference matching (15%)
  - Location preferences (10%)
- **Personalized Internship Matches**: Analyze a resume and automatically rank currently open internships against the student's skills, education, and preferences; the opportunity entry point opens these matches instead of manual search filters
- **Explainable Recommendations**: Review match-score breakdowns, matched and missing skills, and application deadlines for open internships
- **Application Tracking**: Track application status and progress, and follow the official application link where provided
- **Administrator Dashboard**: Manage opportunities and view platform statistics
- **Government-Style Design**: Professional, formal interface inspired by Indian government digital service portals

## Technology Stack

### Backend
- Python 3.12
- Flask 3.0.0
- Flask-Login (Authentication)
- Flask-SQLAlchemy (ORM)
- Flask-WTF (CSRF Protection)
- pandas (Data processing)
- scikit-learn (ML algorithms)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)

### Database
- MySQL/MariaDB (via XAMPP)
- SQLAlchemy ORM

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Bootstrap 5
- Chart.js (Analytics)

### Development Environment
- Windows 10/11
- XAMPP (MySQL)
- Python Virtual Environment
- VS Code / Windsurf / Cursor

## Project Structure

```
interndisha/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── skill.py
│   │   ├── resume.py
│   │   ├── opportunity.py
│   │   ├── eligibility.py
│   │   ├── recommendation.py
│   │   ├── application.py
│   │   ├── notification.py
│   │   ├── learning.py
│   │   └── audit.py
│   ├── routes/                  # Flask routes
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── resume.py
│   │   ├── opportunities.py
│   │   ├── recommendations.py
│   │   ├── applications.py
│   │   ├── admin.py
│   │   └── errors.py
│   ├── services/                # Business logic
│   │   ├── eligibility_engine.py
│   │   ├── recommendation_engine.py
│   │   └── resume_parser.py
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── opportunities/
│   │   ├── recommendations/
│   │   ├── applications/
│   │   ├── admin/
│   │   └── errors/
│   └── static/
│       └── css/
│           └── style.css
├── scripts/
│   ├── init_db.py              # Database initialization
│   ├── migrate_profile_skills.py # Safe additive profile/resume schema update
│   ├── seed_demo_data.py       # Demo data seeding
│   └── create_admin.py         # Admin creation script
├── tests/
│   ├── test_auth.py
│   └── test_recommendations.py
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore
├── run.py                     # Application entry point
└── README.md
```

## Installation Guide

### Prerequisites

1. **Windows 10/11** operating system
2. **XAMPP** installed and running
3. **Python 3.12** installed
4. **Git** (optional, for cloning)

### Step 1: Install XAMPP

1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP with default settings
3. Start Apache and MySQL from XAMPP Control Panel
4. Open phpMyAdmin at http://localhost/phpmyadmin/

### Step 2: Clone or Download Project

```bash
cd c:\xampp\htdocs
git clone <repository-url> internship
# Or extract the project folder to htdocs
```

### Step 3: Create Python Virtual Environment

```bash
cd c:\xampp\htdocs\internship
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Edit `.env` file and configure:
   - Database credentials (default XAMPP: root, empty password)
   - Secret key (generate a random string)
   - Email settings (optional)

### Step 6: Create MySQL Database

1. Open phpMyAdmin at http://localhost/phpmyadmin/
2. Create a new database named `interndisha_db`
3. Or use the initialization script (see Step 7)

### Step 7: Initialize Database

```bash
python scripts\init_db.py
```

This will create all required tables in the database.

### Step 8: Seed Demo Data (Optional)

```bash
python scripts\seed_demo_data.py
```

This will populate the database with sample data for testing:
- 1 Admin user (admin@interndisha.local / Admin@123)
- 2 Student users
- 15 Skills
- 3 Organizations
- 5 Sample opportunities
- 3 Eligibility rules
- 4 Learning resources

### Step 9: Create Admin User (Optional)

If you didn't seed demo data, create an admin manually:

```bash
python scripts\create_admin.py
```

Follow the prompts to create an administrator account.

### Step 10: Run the Application

```bash
python run.py
```

The application will start at http://localhost:5000

## Usage

### For Students

1. **Register**: Create an account with email and password
2. **Complete Profile**: Fill in personal details, education, skills, and preferences
3. **Analyze Resume**: Upload PDF/DOCX/TXT or paste resume text to extract skills
4. **Review Matches**: Resume analysis automatically generates ranked recommendations with match explanations and missing skills
5. **Open an Internship**: Review the recommendation and its deadline, then use the official application link when provided
6. **Track Applications**: Track application status and progress

### For Administrators

1. **Login** with admin credentials
2. **Access Dashboard** at /admin
3. **Manage Opportunities**: Add, edit, publish, or unpublish opportunities
4. **View Statistics**: Monitor platform usage and statistics
5. **Import Data**: Import opportunities from CSV (future feature)

## Database Schema

The application uses the following main tables:

- **users**: User accounts and authentication
- **student_profiles**: Student profile information
- **education_records**: Education history
- **skills**: Master skill list
- **student_skills**: Student-skill relationships
- **resumes**: Resume uploads
- **resume_extractions**: Extracted resume data
- **organizations**: Organizations offering internships
- **opportunities**: Internship opportunities
- **opportunity_skills**: Opportunity-skill relationships
- **eligibility_rules**: Eligibility criteria
- **recommendations**: Recommendation runs
- **recommendation_items**: Individual recommendations
- **applications**: Application tracking
- **notifications**: User notifications
- **learning_resources**: Learning materials
- **audit_logs**: Security audit trail

## Recommendation Algorithm

The recommendation engine uses a hybrid approach with the following weighted components:

1. **Skills Match (35%)**: Compares student skills against opportunity requirements
2. **Education Compatibility (20%)**: Evaluates qualification alignment
3. **Text Similarity (20%)**: Uses TF-IDF and cosine similarity on profile/opportunity text
4. **Preference Match (15%)**: Matches industry, domain, and role preferences
5. **Location Preference (10%)**: Considers preferred work location

The final score is a weighted sum of these components, normalized to 0-1 range.

## Security Features

- Password hashing using Werkzeug
- CSRF protection via Flask-WTF
- Secure session cookies
- Input validation and sanitization
- SQL injection prevention via ORM
- Secure file upload handling
- Role-based access control
- Audit logging for sensitive actions

## Testing

Run the test suite:

```bash
pytest tests/
```

Run specific test file:

```bash
pytest tests/test_auth.py
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Troubleshooting

### Database Connection Error

**Problem**: Can't connect to MySQL database

**Solution**:
1. Ensure XAMPP MySQL is running
2. Check database credentials in `.env`
3. Verify database `interndisha_db` exists in phpMyAdmin
4. Check if MySQL is running on port 3306

### Import Errors

**Problem**: Module not found errors

**Solution**:
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check Python version (requires 3.12)

### File Upload Errors

**Problem**: Resume upload fails

**Solution**:
1. Ensure `uploads` directory exists
2. Check file size (max 16MB)
3. Verify file format (PDF or DOCX only)
4. Check directory permissions

## Known Limitations

1. **Resume Parsing**: Basic keyword-based extraction; not as sophisticated as commercial solutions
2. **Eligibility Rules**: Currently limited to qualification checks; age and employment status require additional profile fields
3. **Real-time Data**: Demo data is used; production would require integration with official PMIS portal
4. **OCR Support**: Scanned PDFs are not supported; requires text-based documents
5. **Multilingual**: Currently English-only; translations are planned for future

## Future Enhancements

- OCR support for scanned resumes
- Advanced NLP for resume parsing
- Real-time integration with official PMIS portal
- Multilingual support (Hindi, Marathi)
- Email notifications for new opportunities
- Skill-gap analysis with learning roadmap
- Opportunity comparison feature
- CSV import/export for opportunities
- Mobile-responsive improvements
- Advanced analytics dashboard

## Contributing

This is an academic project. For contributions:

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass before submitting

## License

This project is for academic purposes. Please cite appropriately if used for research or educational purposes.

## Disclaimer

InternDisha is an independent academic project inspired by the Prime Minister's Internship Scheme. It is not affiliated with, endorsed by, or connected to the Government of India or any official government portal.

All internship opportunities listed are for demonstration purposes unless otherwise stated. Final eligibility, application acceptance, and selection are determined by the official authorities and participating organizations.

Users must verify all information on the official PM Internship Scheme portal before making any decisions.

## Contact

For questions about this academic project, please contact through the project repository or academic institution.

## Official Resources

- [PM India Portal](https://www.pmindia.gov.in/)
- [Official PMIS Portal](https://www.pmis.gov.in/) (Coming Soon)

## Acknowledgments

- Inspired by the Prime Minister's Internship Scheme
- Built as a B.Tech Information Technology semester project
- Uses open-source libraries and frameworks
