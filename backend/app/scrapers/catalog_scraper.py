"""
Ole Miss Catalog Scraper
Scrapes course and degree information from Ole Miss catalog
"""
import requests
from bs4 import BeautifulSoup
import re
from app.models.database import Course, Major, Minor, GenEdRequirement, get_session

class OleMissCatalogScraper:
    def __init__(self, base_url="https://catalog.olemiss.edu"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_computer_science_major(self):
        """
        Scrape Computer Science major requirements
        This is a sample implementation - adjust URL based on actual catalog structure
        """
        # Sample data structure (in production, this would scrape the actual catalog)
        cs_courses = [
            {
                'code': 'CSCI 111',
                'name': 'Computer Science I',
                'credits': 3,
                'description': 'Introduction to computer science and programming',
                'workload': 'Moderate',
                'category': 'Core',
                'prerequisites': []
            },
            {
                'code': 'CSCI 112',
                'name': 'Computer Science II',
                'credits': 3,
                'description': 'Object-oriented programming and data structures',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['CSCI 111']
            },
            {
                'code': 'CSCI 211',
                'name': 'Computer Science III',
                'credits': 3,
                'description': 'Advanced data structures and algorithms',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['CSCI 112']
            },
            {
                'code': 'CSCI 223',
                'name': 'Computer Organization and Assembly Language',
                'credits': 3,
                'description': 'Computer architecture and assembly programming',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['CSCI 111']
            },
            {
                'code': 'CSCI 433',
                'name': 'Algorithm Design and Analysis',
                'credits': 3,
                'description': 'Design and analysis of algorithms',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['CSCI 211', 'MATH 261']
            },
            {
                'code': 'CSCI 531',
                'name': 'Artificial Intelligence',
                'credits': 3,
                'description': 'Introduction to artificial intelligence',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['CSCI 211', 'CSCI 433', 'MATH 261', 'MATH 262']
            },
            {
                'code': 'MATH 261',
                'name': 'Calculus I',
                'credits': 4,
                'description': 'Differential calculus',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': []
            },
            {
                'code': 'MATH 262',
                'name': 'Calculus II',
                'credits': 4,
                'description': 'Integral calculus',
                'workload': 'Heavy',
                'category': 'Core',
                'prerequisites': ['MATH 261']
            },
            {
                'code': 'WRIT 101',
                'name': 'Writing I',
                'credits': 3,
                'description': 'Composition and rhetoric',
                'workload': 'Light',
                'category': 'GenEd',
                'prerequisites': []
            },
            {
                'code': 'WRIT 102',
                'name': 'Writing II',
                'credits': 3,
                'description': 'Advanced composition',
                'workload': 'Light',
                'category': 'GenEd',
                'prerequisites': ['WRIT 101']
            },
            {
                'code': 'HIST 105',
                'name': 'World History I',
                'credits': 3,
                'description': 'Survey of world history',
                'workload': 'Light',
                'category': 'GenEd',
                'prerequisites': []
            }
        ]

        return cs_courses

    def populate_database(self):
        """Populate database with sample data"""
        db_session = get_session()

        try:
            # Clear existing data
            db_session.query(Course).delete()
            db_session.query(Major).delete()
            db_session.query(Minor).delete()
            db_session.query(GenEdRequirement).delete()

            # Create courses
            cs_courses_data = self.scrape_computer_science_major()
            course_map = {}

            for course_data in cs_courses_data:
                course = Course(
                    code=course_data['code'],
                    name=course_data['name'],
                    credits=course_data['credits'],
                    description=course_data['description'],
                    workload=course_data['workload'],
                    category=course_data['category']
                )
                db_session.add(course)
                course_map[course_data['code']] = (course, course_data['prerequisites'])

            db_session.commit()

            # Add prerequisites
            for code, (course, prereq_codes) in course_map.items():
                for prereq_code in prereq_codes:
                    if prereq_code in course_map:
                        prereq_course = course_map[prereq_code][0]
                        course.prerequisites_required.append(prereq_course)

            db_session.commit()

            # Create Computer Science major
            cs_major = Major(
                name='Computer Science',
                degree_type='B.S.',
                total_credits=120,
                major_credits=60
            )

            # Add core CS courses to major
            cs_course_codes = ['CSCI 111', 'CSCI 112', 'CSCI 211', 'CSCI 223', 'CSCI 433', 'CSCI 531', 'MATH 261', 'MATH 262']
            for code in cs_course_codes:
                if code in course_map:
                    cs_major.required_courses.append(course_map[code][0])

            db_session.add(cs_major)

            # Create Accounting minor (sample)
            accounting_minor = Minor(
                name='Accounting',
                required_credits=18
            )
            db_session.add(accounting_minor)

            # Create General Education requirements
            gened_reqs = [
                GenEdRequirement(
                    category='Writing',
                    required_credits=6,
                    description='WRIT 101 and WRIT 102'
                ),
                GenEdRequirement(
                    category='Social Sciences',
                    required_credits=9,
                    description='Including HIST 105 or equivalent'
                ),
                GenEdRequirement(
                    category='Natural Sciences',
                    required_credits=6,
                    description='Two science courses with labs'
                ),
                GenEdRequirement(
                    category='Fine Arts',
                    required_credits=3,
                    description='One fine arts course'
                ),
                GenEdRequirement(
                    category='Humanities',
                    required_credits=6,
                    description='Two humanities courses'
                )
            ]

            for req in gened_reqs:
                db_session.add(req)

            db_session.commit()

            print("Database populated with sample data successfully!")
            print(f"Created {len(cs_courses_data)} courses")
            print(f"Created 1 major (Computer Science)")
            print(f"Created 1 minor (Accounting)")
            print(f"Created {len(gened_reqs)} GenEd requirements")

        except Exception as e:
            db_session.rollback()
            print(f"Error populating database: {e}")
            raise
        finally:
            db_session.close()

if __name__ == '__main__':
    scraper = OleMissCatalogScraper()
    scraper.populate_database()
