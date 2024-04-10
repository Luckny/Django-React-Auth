import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link, Outlet } from 'react-router-dom';
import { Grid } from '@mui/material';
import useLogout from '../pages/Login/useLogout';

export default function Navbar() {
  const { logout } = useLogout();
  const handleClick = () => logout();
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Grid container justifyContent="space-between">
              <Button component={Link} to="/">
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                  Home
                </Typography>
              </Button>
              <Button onClick={handleClick} color="inherit">
                Log out
              </Button>
              <Button component={Link} to="/login" color="inherit">
                Login
              </Button>
            </Grid>
          </Toolbar>
        </AppBar>
      </Box>
      <Outlet />
    </>
  );
}
