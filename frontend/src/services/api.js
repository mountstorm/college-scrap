import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get all majors
  getMajors: async () => {
    const response = await api.get('/majors');
    return response.data;
  },

  // Get all minors
  getMinors: async () => {
    const response = await api.get('/minors');
    return response.data;
  },

  // Get degree requirements
  getDegreeRequirements: async (majorId, minorId, classification) => {
    const response = await api.post('/degree-requirements', {
      major_id: majorId,
      minor_id: minorId,
      classification: classification,
    });
    return response.data;
  },

  // Generate schedule
  generateSchedule: async (majorId, minorId, semester, creditLoad, completedCourses) => {
    const response = await api.post('/generate-schedule', {
      major_id: majorId,
      minor_id: minorId,
      semester: semester,
      credit_load: creditLoad,
      completed_courses: completedCourses,
    });
    return response.data;
  },

  // Get course details
  getCourse: async (courseCode) => {
    const response = await api.get(`/courses/${courseCode}`);
    return response.data;
  },
};

export default api;
