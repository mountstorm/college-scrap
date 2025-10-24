"""
Schedule Generator
Creates balanced semester schedules based on prerequisites and workload
"""
from app.models.database import Course

class ScheduleGenerator:
    def __init__(self, session):
        self.session = session
        self.credit_loads = {
            'light': (12, 13),
            'standard': (15, 16),
            'heavy': (18, 21)
        }

    def generate_schedule(self, major, minor, semester, credit_load, completed_courses):
        """
        Generate a balanced schedule for a semester

        Args:
            major: Major object
            minor: Minor object (optional)
            semester: Semester string (e.g., "Fall 2025")
            credit_load: "light", "standard", or "heavy"
            completed_courses: List of course codes already completed

        Returns:
            Dictionary with recommended schedule
        """
        min_credits, max_credits = self.credit_loads.get(credit_load, (15, 16))

        # Get all required courses
        all_required = list(major.required_courses)
        if minor:
            all_required.extend(minor.required_courses)

        # Filter out completed courses
        remaining_courses = [
            c for c in all_required
            if c.code not in completed_courses
        ]

        # Find courses that can be taken this semester
        available_courses = self._filter_by_prerequisites(
            remaining_courses,
            completed_courses
        )

        # Build the schedule
        schedule = self._build_balanced_schedule(
            available_courses,
            min_credits,
            max_credits
        )

        # Analyze workload balance
        warnings = self._analyze_workload(schedule)

        return {
            'semester': semester,
            'total_credits': sum(c['credits'] for c in schedule),
            'courses': schedule,
            'warnings': warnings,
            'alternatives': self._suggest_alternatives(
                available_courses,
                schedule
            )
        }

    def _filter_by_prerequisites(self, courses, completed_courses):
        """Filter courses by whether prerequisites are met"""
        available = []

        for course in courses:
            prereqs = [p.code for p in course.prerequisites_required]

            # Check if all prerequisites are completed
            if all(prereq in completed_courses for prereq in prereqs):
                available.append(course)

        return available

    def _build_balanced_schedule(self, available_courses, min_credits, max_credits):
        """Build a balanced schedule within credit range"""
        schedule = []
        total_credits = 0
        workload_distribution = {'Heavy': 0, 'Moderate': 0, 'Light': 0}

        # Sort courses by importance (prerequisite to many others)
        sorted_courses = sorted(
            available_courses,
            key=lambda c: len(c.unlocks),
            reverse=True
        )

        for course in sorted_courses:
            if total_credits + course.credits <= max_credits:
                schedule.append({
                    'code': course.code,
                    'name': course.name,
                    'credits': course.credits,
                    'workload': course.workload or 'Moderate',
                    'category': course.category or 'Core',
                    'prerequisites_met': True
                })

                total_credits += course.credits
                workload_distribution[course.workload or 'Moderate'] += 1

                # Stop if we've reached minimum and have good balance
                if total_credits >= min_credits:
                    if workload_distribution['Heavy'] <= 2:
                        break

        return schedule

    def _analyze_workload(self, schedule):
        """Analyze schedule for workload warnings"""
        warnings = []

        heavy_count = sum(1 for c in schedule if c['workload'] == 'Heavy')

        if heavy_count >= 3:
            warnings.append({
                'level': 'warning',
                'message': f'{heavy_count} heavy courses. This may be overwhelming.'
            })
        elif heavy_count == 2:
            warnings.append({
                'level': 'info',
                'message': '2 heavy courses. Consider swapping one for a lighter option.'
            })

        total_credits = sum(c['credits'] for c in schedule)
        if total_credits < 12:
            warnings.append({
                'level': 'warning',
                'message': 'Below full-time status (12 credits). May affect financial aid.'
            })

        return warnings

    def _suggest_alternatives(self, available_courses, current_schedule):
        """Suggest alternative courses"""
        scheduled_codes = [c['code'] for c in current_schedule]

        alternatives = [
            {
                'code': c.code,
                'name': c.name,
                'credits': c.credits,
                'workload': c.workload or 'Moderate'
            }
            for c in available_courses
            if c.code not in scheduled_codes
        ]

        return alternatives[:5]  # Return top 5 alternatives
