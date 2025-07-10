import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../services/authService';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Alert
} from '@mui/material';

function LoginPage() {
  const [email_teams, setEmail] = useState('');
  const [mk, setMk] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/events");
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await login(email_teams, mk);
      localStorage.setItem("token", result.token);
      navigate("/events");
    } catch (err) {
      setError(err.message || "Đăng nhập thất bại");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        mt={8}
        p={4}
        boxShadow={3}
        borderRadius={2}
        bgcolor="white"
      >
        <Typography variant="h4" gutterBottom>
          Đăng nhập
        </Typography>

        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <TextField
            label="Email"
            type="email"
            fullWidth
            margin="normal"
            value={email_teams}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Mật khẩu"
            type="password"
            fullWidth
            margin="normal"
            value={mk}
            onChange={(e) => setMk(e.target.value)}
            required
          />
          <Button
            variant="contained"
            color="primary"
            type="submit"
            fullWidth
            sx={{ mt: 2 }}
          >
            Đăng nhập
          </Button>
          <Button
            component={Link}
            to="/register"
            variant="contained"
            color="primary"

            fullWidth
            sx={{ mt: 2 }}
          >
            Đăng Ký
          </Button>
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </form>
      </Box>
    </Container>
  );
}

export default LoginPage;
