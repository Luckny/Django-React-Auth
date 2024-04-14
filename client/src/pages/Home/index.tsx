import { Grid, Typography } from '@mui/material';
import React from 'react';

export default function Home() {
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      sx={{ minHeight: '100vh' }}
      maxWidth="xs"
    >
      <Typography variant="h3">Welcome</Typography>
    </Grid>
  );
}
