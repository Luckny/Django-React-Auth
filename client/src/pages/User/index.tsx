import React, { useEffect } from 'react';

import axios from 'axios';
import { Alert } from '@mui/material';
import { USERS_URL } from '../../constants';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { server } from '../../types/AuthTypes';
import UsersList from './UsersList';

export default function Users() {
  const { authState, dispatch } = useAuthContext();

  useEffect(() => {
    async function updateState() {
      try {
        // if user is set but the email is not verified
        if (!authState.user?.isEmailVerified) {
          // sync with the databse
          const { data } = await axios.get<server.IUser>(
            `${USERS_URL}/${authState.user?.id}`,
            {
              headers: { Authorization: `Token ${authState.accessToken}` },
            },
          );

          // if the email was confirmed
          if (data?.is_email_confirmed) {
            // update state
            dispatch({
              type: 'UPDATE_USER',
              payload: { user: data, access_token: authState.accessToken },
            });
            // update local storage
            localStorage.setItem(
              'user',
              JSON.stringify({
                user: data,
                access_token: authState.accessToken,
              }),
            );
          }
        }
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error(e);
      }
    }
    if (authState.user) updateState();
  }, [authState, dispatch]);
  return authState.user?.isEmailVerified ? (
    <UsersList />
  ) : (
    <Alert severity="info">Please confirm you email address.</Alert>
  );
}
