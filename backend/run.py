"""
CollegeScrap Backend Entry Point
"""
from app import create_app
from app.models.database import init_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
