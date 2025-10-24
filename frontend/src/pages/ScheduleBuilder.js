import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

function ScheduleBuilder({ degreeData, setScheduleData }) {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    semester: 'Fall 2025',
    creditLoad: 'standard',
    completedCourses: [],
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get all courses for checkboxes
  const allCourses = [
    ...degreeData.courses.major,
    ...(degreeData.courses.minor || []),
  ];

  const handleCourseToggle = (courseCode) => {
    setFormData((prev) => ({
      ...prev,
      completedCourses: prev.completedCourses.includes(courseCode)
        ? prev.completedCourses.filter((code) => code !== courseCode)
        : [...prev.completedCourses, courseCode],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      const schedule = await apiService.generateSchedule(
        degreeData.majorId,
        degreeData.minorId,
        formData.semester,
        formData.creditLoad,
        formData.completedCourses
      );

      setScheduleData(schedule);
      navigate('/schedule');
    } catch (err) {
      setError('Failed to generate schedule. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="header">
        <h1>📅 BUILD YOUR BALANCED SCHEDULE</h1>
      </div>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="semester">Which semester are you planning?</label>
          <select
            id="semester"
            value={formData.semester}
            onChange={(e) => setFormData({ ...formData, semester: e.target.value })}
          >
            <option value="Fall 2025">Fall 2025</option>
            <option value="Spring 2026">Spring 2026</option>
            <option value="Summer 2026">Summer 2026</option>
            <option value="Fall 2026">Fall 2026</option>
            <option value="Spring 2027">Spring 2027</option>
          </select>
        </div>

        <div className="form-group">
          <label>Credit load preference?</label>
          <div className="radio-group">
            <div className="radio-option">
              <input
                type="radio"
                id="light"
                name="creditLoad"
                value="light"
                checked={formData.creditLoad === 'light'}
                onChange={(e) => setFormData({ ...formData, creditLoad: e.target.value })}
              />
              <label htmlFor="light">Light (12-13)</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="standard"
                name="creditLoad"
                value="standard"
                checked={formData.creditLoad === 'standard'}
                onChange={(e) => setFormData({ ...formData, creditLoad: e.target.value })}
              />
              <label htmlFor="standard">Standard (15-16)</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="heavy"
                name="creditLoad"
                value="heavy"
                checked={formData.creditLoad === 'heavy'}
                onChange={(e) => setFormData({ ...formData, creditLoad: e.target.value })}
              />
              <label htmlFor="heavy">Heavy (18+)</label>
            </div>
          </div>
        </div>

        <div className="form-group">
          <label>Already completed? (check all that apply)</label>
          <div style={{ maxHeight: '300px', overflowY: 'auto', marginTop: '10px' }}>
            {allCourses.slice(0, 10).map((course) => (
              <div
                key={course.code}
                style={{
                  padding: '10px',
                  marginBottom: '8px',
                  background: '#f9f9f9',
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                <input
                  type="checkbox"
                  id={course.code}
                  checked={formData.completedCourses.includes(course.code)}
                  onChange={() => handleCourseToggle(course.code)}
                  style={{ marginRight: '10px', cursor: 'pointer' }}
                />
                <label
                  htmlFor={course.code}
                  style={{ cursor: 'pointer', margin: 0, fontWeight: 'normal' }}
                >
                  <span style={{ fontWeight: 600, color: '#667eea' }}>{course.code}</span>
                  {' - '}
                  {course.name}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div className="button-group">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/requirements')}
          >
            ← Back to Requirements
          </button>
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Schedule →'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ScheduleBuilder;
