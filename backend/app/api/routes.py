"""
API Routes for CollegeScrap
"""
from flask import Blueprint, jsonify, request
from app.models.database import get_session, Major, Minor, Course
from app.utils.degree_analyzer import DegreeAnalyzer
from app.utils.scheduler import ScheduleGenerator

api = Blueprint('api', __name__)

@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'CollegeScrap API is running'})

@api.route('/majors', methods=['GET'])
def get_majors():
    """Get all available majors"""
    session = get_session()
    try:
        majors = session.query(Major).all()
        return jsonify([{
            'id': m.id,
            'name': m.name,
            'degree_type': m.degree_type
        } for m in majors])
    finally:
        session.close()

@api.route('/minors', methods=['GET'])
def get_minors():
    """Get all available minors"""
    session = get_session()
    try:
        minors = session.query(Minor).all()
        return jsonify([{
            'id': m.id,
            'name': m.name,
            'required_credits': m.required_credits
        } for m in minors])
    finally:
        session.close()

@api.route('/degree-requirements', methods=['POST'])
def get_degree_requirements():
    """
    Analyze degree requirements
    POST body: {
        "major_id": int,
        "minor_id": int (optional),
        "classification": str
    }
    """
    data = request.get_json()
    major_id = data.get('major_id')
    minor_id = data.get('minor_id')
    classification = data.get('classification', 'Freshman')

    session = get_session()
    try:
        major = session.query(Major).filter_by(id=major_id).first()
        if not major:
            return jsonify({'error': 'Major not found'}), 404

        minor = None
        if minor_id:
            minor = session.query(Minor).filter_by(id=minor_id).first()

        analyzer = DegreeAnalyzer(session)
        requirements = analyzer.analyze_requirements(major, minor, classification)

        return jsonify(requirements)
    finally:
        session.close()

@api.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    """
    Generate a balanced semester schedule
    POST body: {
        "major_id": int,
        "minor_id": int (optional),
        "semester": str (e.g., "Fall 2025"),
        "credit_load": str ("light", "standard", "heavy"),
        "completed_courses": [course_codes]
    }
    """
    data = request.get_json()
    major_id = data.get('major_id')
    minor_id = data.get('minor_id')
    semester = data.get('semester')
    credit_load = data.get('credit_load', 'standard')
    completed_courses = data.get('completed_courses', [])

    session = get_session()
    try:
        major = session.query(Major).filter_by(id=major_id).first()
        if not major:
            return jsonify({'error': 'Major not found'}), 404

        minor = None
        if minor_id:
            minor = session.query(Minor).filter_by(id=minor_id).first()

        scheduler = ScheduleGenerator(session)
        schedule = scheduler.generate_schedule(
            major, minor, semester, credit_load, completed_courses
        )

        return jsonify(schedule)
    finally:
        session.close()

@api.route('/courses/<course_code>', methods=['GET'])
def get_course(course_code):
    """Get details for a specific course"""
    session = get_session()
    try:
        course = session.query(Course).filter_by(code=course_code).first()
        if not course:
            return jsonify({'error': 'Course not found'}), 404

        return jsonify(course.to_dict())
    finally:
        session.close()
