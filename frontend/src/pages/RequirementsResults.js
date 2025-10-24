import React from 'react';
import { useNavigate } from 'react-router-dom';

function RequirementsResults({ degreeData }) {
  const navigate = useNavigate();

  const { degree, classification, graduation_date, credits, courses, prerequisite_chains } =
    degreeData;

  return (
    <div className="card">
      <div className="header">
        <h1>
          {degree.degree_type} {degree.major}
          {degree.minor && ` + ${degree.minor} Minor`}
        </h1>
        <p>
          Current: {classification} | Target: {graduation_date}
        </p>
      </div>

      <div className="info-section">
        <h2>📊 DEGREE REQUIREMENTS</h2>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{credits.total}</div>
            <div className="stat-label">Total Credits</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{credits.major}</div>
            <div className="stat-label">Major Credits</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{credits.minor}</div>
            <div className="stat-label">Minor Credits</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{credits.gened}</div>
            <div className="stat-label">GenEd Credits</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{credits.electives}</div>
            <div className="stat-label">Elective Credits</div>
          </div>
        </div>

        <h3>Core {degree.major} Courses ({courses.major.length} classes)</h3>
        <ul className="course-list">
          {courses.major.map((course) => (
            <li key={course.code} className="course-item">
              <span className="course-code">{course.code}</span>
              <span className="course-name">{course.name}</span>
              <span className="course-credits">{course.credits} hrs</span>
              <span className={`workload-badge workload-${course.workload.toLowerCase()}`}>
                {course.workload}
              </span>
            </li>
          ))}
        </ul>

        {degree.minor && (
          <>
            <h3>{degree.minor} Minor Courses ({courses.minor.length} classes)</h3>
            <ul className="course-list">
              {courses.minor.map((course) => (
                <li key={course.code} className="course-item">
                  <span className="course-code">{course.code}</span>
                  <span className="course-name">{course.name}</span>
                  <span className="course-credits">{course.credits} hrs</span>
                </li>
              ))}
            </ul>
          </>
        )}

        <h3>General Education Requirements</h3>
        <ul className="course-list">
          {courses.gened_categories.map((category) => (
            <li key={category.id} className="course-item">
              <span className="course-code">{category.category}</span>
              <span className="course-name">{category.description}</span>
              <span className="course-credits">{category.required_credits} hrs</span>
            </li>
          ))}
        </ul>

        {prerequisite_chains.length > 0 && (
          <>
            <h3>⚠️ Prerequisite Chains to Watch</h3>
            <ul className="course-list">
              {prerequisite_chains.map((chain) => (
                <li key={chain.course} className="course-item">
                  <span className="course-code">{chain.course}</span>
                  <span className="course-name">{chain.name}</span>
                  <div style={{ marginTop: '8px', fontSize: '0.9rem', color: '#666' }}>
                    Requires {chain.requires} course(s) | Unlocks {chain.unlocks} course(s)
                    {chain.prerequisites.length > 0 && (
                      <div style={{ marginTop: '4px' }}>
                        Prerequisites: {chain.prerequisites.join(', ')}
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>

      <div className="button-group">
        <button className="btn btn-secondary" onClick={() => navigate('/')}>
          ← Start Over
        </button>
        <button className="btn" onClick={() => navigate('/schedule-builder')}>
          📅 Build My Schedule →
        </button>
      </div>
    </div>
  );
}

export default RequirementsResults;
