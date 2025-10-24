"""
Database Setup and Models
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

# Association table for course prerequisites
prerequisites = Table('prerequisites', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

# Association table for major requirements
major_courses = Table('major_courses', Base.metadata,
    Column('major_id', Integer, ForeignKey('majors.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

# Association table for minor requirements
minor_courses = Table('minor_courses', Base.metadata,
    Column('minor_id', Integer, ForeignKey('minors.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)  # e.g., "CSCI 111"
    name = Column(String(200), nullable=False)
    credits = Column(Integer, nullable=False)
    description = Column(Text)
    workload = Column(String(20))  # Light, Moderate, Heavy
    category = Column(String(50))  # Core, GenEd, Elective

    # Relationships
    prerequisites_required = relationship(
        'Course',
        secondary=prerequisites,
        primaryjoin=id==prerequisites.c.course_id,
        secondaryjoin=id==prerequisites.c.prerequisite_id,
        backref='unlocks'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'credits': self.credits,
            'description': self.description,
            'workload': self.workload,
            'category': self.category,
            'prerequisites': [p.code for p in self.prerequisites_required]
        }

class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    degree_type = Column(String(20))  # B.S., B.A., B.F.A., etc.
    total_credits = Column(Integer, nullable=False)
    major_credits = Column(Integer, nullable=False)

    # Relationships
    required_courses = relationship('Course', secondary=major_courses, backref='majors')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'degree_type': self.degree_type,
            'total_credits': self.total_credits,
            'major_credits': self.major_credits,
            'required_courses': [c.to_dict() for c in self.required_courses]
        }

class Minor(Base):
    __tablename__ = 'minors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    required_credits = Column(Integer, nullable=False)

    # Relationships
    required_courses = relationship('Course', secondary=minor_courses, backref='minors')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'required_credits': self.required_credits,
            'required_courses': [c.to_dict() for c in self.required_courses]
        }

class GenEdRequirement(Base):
    __tablename__ = 'gened_requirements'

    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)  # e.g., "Writing", "Math", "Social Science"
    required_credits = Column(Integer, nullable=False)
    description = Column(Text)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'required_credits': self.required_credits,
            'description': self.description
        }

# Database initialization
def get_engine():
    db_url = os.getenv('DATABASE_URL', 'sqlite:///collegescrap.db')
    return create_engine(db_url)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
