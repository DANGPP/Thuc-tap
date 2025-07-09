import React, { useState } from 'react';
import { register } from '../services/authService';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Alert
} from '@mui/material';

function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email_teams: '',
    mk: '',
    sdt: '',
    ten_nh: '',
    stk: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await register(formData);

      if (result.error_uesrs && result.error_uesrs.length > 0) {
        setError(result.error_uesrs[0].reason);
        setMessage('');
      } else {
        setMessage("✅ Đăng ký thành công");
        setError('');
      }
    } catch (err) {
      setError(err.message || "Đăng ký thất bại");
      setMessage('');
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
          Đăng ký tài khoản
        </Typography>

        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <TextField name="name" label="Tên" fullWidth margin="normal" onChange={handleChange} required />
          <TextField name="email_teams" label="Email" type="email" fullWidth margin="normal" onChange={handleChange} required />
          <TextField name="mk" label="Mật khẩu" type="password" fullWidth margin="normal" onChange={handleChange} required />
          <TextField name="sdt" label="Số điện thoại" fullWidth margin="normal" onChange={handleChange} required />
          <TextField name="ten_nh" label="Tên ngân hàng" fullWidth margin="normal" onChange={handleChange} required />
          <TextField name="stk" label="Số tài khoản" fullWidth margin="normal" onChange={handleChange} required />

          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
            Đăng ký
          </Button>

          {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
        </form>
      </Box>
    </Container>
  );
}

export default RegisterPage;
