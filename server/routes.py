from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Course, Enrollment
from werkzeug.security import generate_password_hash

api_blueprint = Blueprint('api', __name__)

# User registration
@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

# User login
@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Courses - Instructors can create courses, students can view approved courses
@api_blueprint.route('/courses', methods=['GET', 'POST'])
@jwt_required()
def courses():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    # Create new course (Instructor only)
    if request.method == 'POST':
        if user.role == 'instructor':
            data = request.json
            new_course = Course(title=data['title'], instructor_id=user.id)
            db.session.add(new_course)
            db.session.commit()
            return jsonify({'message': 'Course created'}), 201
        return jsonify({'message': 'Unauthorized'}), 403

    # View approved courses (Student)
    courses = Course.query.filter_by(status='Approved').all()
    return jsonify([{'id': course.id, 'title': course.title} for course in courses]), 200

# Enroll in a course (Student only)
@api_blueprint.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if user.role == 'student':
        data = request.json
        course = Course.query.filter_by(id=data['course_id'], status='Approved').first()
        if course:
            enrollment = Enrollment(student_id=user.id, course_id=course.id)
            db.session.add(enrollment)
            db.session.commit()
            return jsonify({'message': 'Enrolled successfully'}), 201
        return jsonify({'message': 'Course not found'}), 404
    return jsonify({'message': 'Unauthorized'}), 403

# Approve a course (Approver only)
@api_blueprint.route('/approve/<int:course_id>', methods=['PUT'])
@jwt_required()
def approve_course(course_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if user.role == 'approver':
        course = Course.query.get(course_id)
        if course:
            course.status = 'Approved'
            db.session.commit()
            return jsonify({'message': 'Course approved'}), 200
        return jsonify({'message': 'Course not found'}), 404
    return jsonify({'message': 'Unauthorized'}), 403
