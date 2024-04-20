import { Grid, Typography } from '@mui/material';
import React from 'react';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import ActivateAcount from '../../components/ActivateAcount';

export default function Home() {
  const { authState } = useAuthContext();
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
    >
      {authState.user && !authState.user.isActive ? (
        <ActivateAcount />
      ) : (
        <Typography variant="h3">Welcome</Typography>
      )}
    </Grid>
  );
}
