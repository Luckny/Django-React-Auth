import React, { useState } from 'react';
import { Send } from '@mui/icons-material';
import {
  Alert,
  Divider,
  Grid,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import axios, { isAxiosError } from 'axios';
import { CONFIRM_EMAIL_URL, getUserFromDB } from '../utils';
import { UserError } from '../types/AuthTypes';
import useAuthContext from '../contexts/AuthContext/useAuthContext';

export default function ActivateAcount() {
  const [otp, setOtp] = useState<string>('');
  const [otpError, setOtpError] = useState<string>('');
  const { authState, dispatch } = useAuthContext();

  const handleSubmit = async () => {
    try {
      setOtpError(''); // reset error
      const response = await axios.post(CONFIRM_EMAIL_URL, { code: otp });
      if (response.status === 200) {
        // if successfull refresh the user
        const user = await getUserFromDB(
          authState.user?.id!,
          authState.accessToken!,
        );
        dispatch({ type: 'UPDATE_USER', payload: user });
      }
    } catch (e) {
      if (isAxiosError<UserError>(e)) {
        const { data } = e.response!;
        if (data?.wrongOTP) setOtpError(data.wrongOTP);
        if (data?.expiredOTP) setOtpError(data.expiredOTP);
      }
    }
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
      {otpError && (
        <Alert sx={{ margin: 2 }} severity="error">
          {otpError}
        </Alert>
      )}
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
            onChange={(e) => setOtp(e.target.value)}
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
