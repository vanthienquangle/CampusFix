const API = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

export async function loginAdmin(username, password) {
  try {
    const res = await fetch(`${API}/admin-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const result = await res.json();
    return result.success;
  } catch (err) {
    console.error('Login error:', err);
    return false;
  }
}

export async function fetchReports() {
  try {
    const res = await fetch(`${API}/api/reports`);
    return await res.json();
  } catch (err) {
    console.error('Fetch reports error:', err);
    return [];
  }
}

export async function finishReport(id) {
  try {
    await fetch(`${API}/api/finish/${id}`, { method: 'POST' });
  } catch (err) {
    console.error('Finish report error:', err);
  }
}
