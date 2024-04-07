import {
  Avatar,
  Box,
  Button,
  Grid,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import React, { useState } from 'react';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { Link } from 'react-router-dom';

export default function Signup() {
  const [email, setEmail] = useState('');

  const [password, setPassword] = useState('');

  // Function to handle form submission
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      sx={{ minHeight: '100vh' }}
      maxWidth="xs"
    >
      <Paper elevation={10} sx={{ padding: 3, display: 'flex' }}>
        <Grid
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h2">Sign In</Typography>
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              onChange={(e) => setEmail(e.target.value)}
              value={email}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
              value={password}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Log in
            </Button>
            <Grid container>
              <Grid item xs>
                <Link to="/">Forgot password?</Link>
              </Grid>
              <Grid item>
                <Link to="/">Dont have an account? Sign Up</Link>
              </Grid>
            </Grid>
          </Box>
        </Grid>
      </Paper>
    </Grid>
  );
}
