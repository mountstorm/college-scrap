"""
Degree Requirement Analyzer
Analyzes and calculates degree requirements for students
"""
from app.models.database import GenEdRequirement

class DegreeAnalyzer:
    def __init__(self, session):
        self.session = session

    def analyze_requirements(self, major, minor, classification):
        """
        Analyze all degree requirements for a student

        Args:
            major: Major object
            minor: Minor object (optional)
            classification: Student classification (Freshman, Sophomore, etc.)

        Returns:
            Dictionary with complete degree analysis
        """
        # Calculate total credits needed
        total_credits = major.total_credits
        major_credits = major.major_credits
        minor_credits = minor.required_credits if minor else 0

        # Get general education requirements
        gened_requirements = self.session.query(GenEdRequirement).all()
        gened_credits = sum(req.required_credits for req in gened_requirements)

        # Calculate elective credits
        elective_credits = total_credits - major_credits - minor_credits - gened_credits

        # Get all required courses
        major_courses = major.required_courses
        minor_courses = minor.required_courses if minor else []

        # Find prerequisite chains (courses that unlock many others)
        prereq_chains = self._analyze_prerequisite_chains(major_courses)

        # Estimate graduation date based on classification
        graduation_date = self._estimate_graduation(classification)

        return {
            'degree': {
                'major': major.name,
                'degree_type': major.degree_type,
                'minor': minor.name if minor else None
            },
            'classification': classification,
            'graduation_date': graduation_date,
            'credits': {
                'total': total_credits,
                'major': major_credits,
                'minor': minor_credits,
                'gened': gened_credits,
                'electives': elective_credits
            },
            'courses': {
                'major': [c.to_dict() for c in major_courses],
                'minor': [c.to_dict() for c in minor_courses],
                'gened_categories': [req.to_dict() for req in gened_requirements]
            },
            'prerequisite_chains': prereq_chains
        }

    def _analyze_prerequisite_chains(self, courses):
        """Identify important prerequisite chains"""
        chains = []

        for course in courses:
            # Count how many courses this course unlocks
            unlocked_count = len(course.unlocks)

            # Count how many prerequisites this course needs
            prereq_count = len(course.prerequisites_required)

            if unlocked_count >= 3 or prereq_count >= 3:
                chains.append({
                    'course': course.code,
                    'name': course.name,
                    'unlocks': unlocked_count,
                    'requires': prereq_count,
                    'prerequisites': [p.code for p in course.prerequisites_required]
                })

        # Sort by importance (courses that unlock the most)
        chains.sort(key=lambda x: x['unlocks'], reverse=True)

        return chains[:10]  # Return top 10 most important chains

    def _estimate_graduation(self, classification):
        """Estimate graduation date based on classification"""
        from datetime import datetime

        current_year = datetime.now().year
        current_month = datetime.now().month

        # Determine semesters remaining
        semesters_map = {
            'Freshman': 8,
            'Sophomore': 6,
            'Junior': 4,
            'Senior': 2
        }

        semesters_left = semesters_map.get(classification, 8)

        # Calculate years (2 semesters per year)
        years_left = semesters_left // 2

        # Determine graduation month (May or December)
        if current_month <= 5:
            grad_month = "May"
        else:
            grad_month = "May"
            years_left += 1

        grad_year = current_year + years_left

        return f"{grad_month} {grad_year}"
