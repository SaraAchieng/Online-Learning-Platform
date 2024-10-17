from models import db, User, Course, Enrollment
from werkzeug.security import generate_password_hash
from app import app  # Import the Flask app from your main app file

def seed_data():
    try:
        print("Dropping all tables...")
        db.drop_all()
        print("Creating new tables...")
        db.create_all()

        print("Seeding users...")
        # Create users
        users = [
            User(username="student1", password=generate_password_hash("password123"), role="student"),
            User(username="instructor1", password=generate_password_hash("password123"), role="instructor"),
            User(username="approver1", password=generate_password_hash("password123"), role="approver"),
        ]

        db.session.add_all(users)
        db.session.commit()
        print("Users added successfully!")

        print("Seeding courses...")
        # Create courses
        courses = [
            Course(title="Introduction to Python", instructor_id=2, status="Pending"),  # instructor1 creates this course
            Course(title="Advanced Flask Development", instructor_id=2, status="Pending"),
            Course(title="Data Science with Python", instructor_id=2, status="Pending"),
        ]

        db.session.add_all(courses)
        db.session.commit()
        print("Courses added successfully!")

        print("Seeding enrollments...")
        # Enroll student1 in the first course (after approval)
        course_to_enroll = Course.query.first()  # Getting the first course
        enrollment = Enrollment(student_id=1, course_id=course_to_enroll.id)  # student1 enrolls in the first course
        db.session.add(enrollment)
        db.session.commit()
        print("Enrollments added successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
    else:
        print("Seeding completed successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_data()

