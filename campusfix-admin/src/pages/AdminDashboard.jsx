import { useState, useEffect } from 'react';
import LoginForm from '../components/LoginForm';
import ReportBoard from '../components/ReportBoard';
import { loginAdmin, fetchReports, finishReport } from '../api/reportService';

export default function AdminDashboard() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [reports, setReports] = useState([]);

  const handleLogin = async (username, password) => {
    const success = await loginAdmin(username, password);
    if (success) {
      setLoggedIn(true);
      loadReports();
    } else {
      alert('Invalid credentials or server error');
    }
  };

  const loadReports = async () => {
    const data = await fetchReports();
    setReports(data);
  };

  const handleFinish = async (id) => {
    await finishReport(id);
    loadReports();
  };

  useEffect(() => {
    if (loggedIn) {
      const interval = setInterval(loadReports, 3000);
      return () => clearInterval(interval);
    }
  }, [loggedIn]);

  return loggedIn ? (
    <ReportBoard reports={reports} onFinish={handleFinish} />
  ) : (
    <LoginForm onLogin={handleLogin} />
  );
}
