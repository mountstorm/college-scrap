import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

function DegreeSelection({ setDegreeData }) {
  const navigate = useNavigate();

  const [majors, setMajors] = useState([]);
  const [minors, setMinors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    majorId: '',
    degreeType: 'B.S.',
    minorId: '',
    classification: 'Freshman',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [majorsData, minorsData] = await Promise.all([
        apiService.getMajors(),
        apiService.getMinors(),
      ]);
      setMajors(majorsData);
      setMinors(minorsData);
    } catch (err) {
      setError('Failed to load majors and minors. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.majorId) {
      setError('Please select a major');
      return;
    }

    try {
      setLoading(true);
      const requirements = await apiService.getDegreeRequirements(
        parseInt(formData.majorId),
        formData.minorId ? parseInt(formData.minorId) : null,
        formData.classification
      );

      setDegreeData({
        ...requirements,
        majorId: formData.majorId,
        minorId: formData.minorId,
      });

      navigate('/requirements');
    } catch (err) {
      setError('Failed to analyze degree requirements. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && majors.length === 0) {
    return (
      <div className="card">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="header">
        <h1>CollegeScrap 🎓</h1>
        <p>Know your degree requirements in 30 seconds</p>
      </div>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="major">What's your major?</label>
          <select
            id="major"
            value={formData.majorId}
            onChange={(e) => setFormData({ ...formData, majorId: e.target.value })}
            required
          >
            <option value="">Select a major...</option>
            {majors.map((major) => (
              <option key={major.id} value={major.id}>
                {major.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Degree type?</label>
          <div className="radio-group">
            <div className="radio-option">
              <input
                type="radio"
                id="bs"
                name="degreeType"
                value="B.S."
                checked={formData.degreeType === 'B.S.'}
                onChange={(e) => setFormData({ ...formData, degreeType: e.target.value })}
              />
              <label htmlFor="bs">B.S.</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="ba"
                name="degreeType"
                value="B.A."
                checked={formData.degreeType === 'B.A.'}
                onChange={(e) => setFormData({ ...formData, degreeType: e.target.value })}
              />
              <label htmlFor="ba">B.A.</label>
            </div>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="minor">Minor? (optional)</label>
          <select
            id="minor"
            value={formData.minorId}
            onChange={(e) => setFormData({ ...formData, minorId: e.target.value })}
          >
            <option value="">No minor</option>
            {minors.map((minor) => (
              <option key={minor.id} value={minor.id}>
                {minor.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Classification?</label>
          <div className="radio-group">
            {['Freshman', 'Sophomore', 'Junior', 'Senior'].map((classification) => (
              <div key={classification} className="radio-option">
                <input
                  type="radio"
                  id={classification}
                  name="classification"
                  value={classification}
                  checked={formData.classification === classification}
                  onChange={(e) =>
                    setFormData({ ...formData, classification: e.target.value })
                  }
                />
                <label htmlFor={classification}>{classification}</label>
              </div>
            ))}
          </div>
        </div>

        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze My Degree →'}
        </button>
      </form>
    </div>
  );
}

export default DegreeSelection;
