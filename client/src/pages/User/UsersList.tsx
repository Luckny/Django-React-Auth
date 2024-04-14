import React, { useEffect, useState } from 'react';
import {
  Avatar,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
} from '@mui/material';
import axios from 'axios';
import { USERS_URL } from '../../constants';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { server } from '../../types/AuthTypes';

export default function UsersList() {
  const [users, setUsers] = useState<server.IUser[] | undefined>(undefined);
  const { authState } = useAuthContext();

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await axios.get(USERS_URL, {
        headers: { Authorization: `Token ${authState.accessToken}` },
      });

      setUsers(response.data);
    };
    fetchUsers();
  }, [authState.accessToken]);
  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      marginTop={5}
      maxWidth="xs"
    >
      {users && (
        <List
          sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
        >
          {users.map((user) => (
            <div key={user?.id}>
              <ListItem key={user?.id} alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar />
                </ListItemAvatar>
                <ListItemText primary={user?.email} />
              </ListItem>
              <Divider />
            </div>
          ))}
        </List>
      )}
    </Grid>
  );
}
