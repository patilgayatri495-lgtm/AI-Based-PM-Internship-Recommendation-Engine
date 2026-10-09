"""Apply additive profile and resume-source schema updates."""
import os
import sys

from sqlalchemy import inspect, text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def migrate_workflow_schema(engine):
    """Add workflow columns to existing tables; return whether any changed."""
    inspector = inspect(engine)
    if not inspector.has_table('student_profiles') or not inspector.has_table('resumes'):
        raise RuntimeError(
            "The student_profiles or resumes table does not exist. Initialize the database first."
        )

    changed = False
    profile_columns = {column['name'] for column in inspector.get_columns('student_profiles')}
    resume_columns = {column['name'] for column in inspector.get_columns('resumes')}
    statements = []

    if 'skills' not in profile_columns:
        statements.append('ALTER TABLE student_profiles ADD COLUMN skills TEXT NULL')
    if 'source_type' not in resume_columns:
        statements.append(
            "ALTER TABLE resumes ADD COLUMN source_type VARCHAR(20) NOT NULL DEFAULT 'file'"
        )
    if 'source_url' not in resume_columns:
        statements.append('ALTER TABLE resumes ADD COLUMN source_url VARCHAR(500) NULL')

    if statements:
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))
        changed = True
    return changed


def main():
    from app import create_app, db

    app = create_app('development')
    with app.app_context():
        if migrate_workflow_schema(db.engine):
            print("Applied missing profile and resume-source columns.")
        else:
            print("Profile and resume-source columns already exist; no changes made.")


if __name__ == '__main__':
    main()
