import { Send } from '@mui/icons-material';
import {
  Divider,
  Grid,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import React from 'react';

export default function ActivateAcount() {
  const handleSubmit = () => {
    console.log('handing submit');
  };
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      justifyContent="center"
      sx={{ minHeight: '80vh' }}
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
          <Typography margin={2} variant="h5">
            Email verification required
          </Typography>
          <Divider />
          <Typography margin={2}>
            Please enter the confirmation code from your email address.
          </Typography>
          <TextField
            required
            size="small"
            variant="standard"
            sx={{ width: 100 }}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={handleSubmit}
                    size="small"
                    edge="end"
                    color="primary"
                  >
                    <Send />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </Grid>
      </Paper>
    </Grid>
  );
}
