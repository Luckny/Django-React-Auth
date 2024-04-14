import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link, Outlet } from 'react-router-dom';
import { Grid } from '@mui/material';
import useLogout from '../pages/Login/useLogout';
import useAuthContext from '../contexts/AuthContext/useAuthContext';

export default function Navbar() {
  const { logout } = useLogout();
  const { authState } = useAuthContext();
  const handleClick = () => logout();
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Grid container justifyContent="space-between">
              <Button color="inherit" component={Link} to="/">
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                  Home
                </Typography>
              </Button>
              <Grid>
                {authState.user && (
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <Typography marginRight={2} variant="caption">
                      {authState.user.email}
                    </Typography>
                    <Button onClick={handleClick} color="inherit">
                      Log out
                    </Button>
                  </div>
                )}

                {!authState.user && (
                  <Button component={Link} to="/login" color="inherit">
                    Login
                  </Button>
                )}
              </Grid>
            </Grid>
          </Toolbar>
        </AppBar>
      </Box>
      <Outlet />
    </>
  );
}
