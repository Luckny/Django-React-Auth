import { User, UserAction } from './types/AuthTypes';

export const logoutAction: UserAction = {
  type: 'LOGOUT',
  payload: { user: undefined, access_token: undefined }, // Payload is null for logout action
};

export const createUser = (user: any): User => ({
  id: user.id,
  email: user.email,
  isEmailVerified: user.is_email_confirmed,
});

export const SIGNUP_URL = `${process.env.REACT_APP_API_URL}/users/`;
export const LOGIN_URL = `${process.env.REACT_APP_API_URL}/login/`;
export const USERS_URL = `${process.env.REACT_APP_API_URL}/users`;
