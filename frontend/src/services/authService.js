// src/services/authService.js
const API_BASE = process.env.REACT_APP_API_BACKEND;

export const login = async (email_teams, mk) => {
  const res = await fetch(`${API_BASE}login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email_teams, mk })
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || 'Đăng nhập thất bại');
  }

  return res.json();
};

export const register = async (userData) => {
  const res = await fetch(`${API_BASE}register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([userData]) // vì route nhận mảng
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || 'Đăng ký thất bại');
  }

  return res.json();
};
