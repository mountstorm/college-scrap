import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DegreeSelection from './pages/DegreeSelection';
import RequirementsResults from './pages/RequirementsResults';
import ScheduleBuilder from './pages/ScheduleBuilder';
import GeneratedSchedule from './pages/GeneratedSchedule';

function App() {
  const [degreeData, setDegreeData] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route
            path="/"
            element={<DegreeSelection setDegreeData={setDegreeData} />}
          />
          <Route
            path="/requirements"
            element={
              degreeData ? (
                <RequirementsResults degreeData={degreeData} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route
            path="/schedule-builder"
            element={
              degreeData ? (
                <ScheduleBuilder
                  degreeData={degreeData}
                  setScheduleData={setScheduleData}
                />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route
            path="/schedule"
            element={
              scheduleData ? (
                <GeneratedSchedule scheduleData={scheduleData} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
