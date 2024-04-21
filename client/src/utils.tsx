import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { User, UserAction } from './types/AuthTypes';
import useAuthContext from './contexts/AuthContext/useAuthContext';

export const logoutAction: UserAction = {
  type: 'LOGOUT',
  payload: { user: undefined, access_token: undefined }, // Payload is null for logout action
};

export const createUser = (user: any): User => ({
  id: user.id,
  email: user.email,
  isActive: user.is_active,
});

export const SIGNUP_URL = `${process.env.REACT_APP_API_URL}/users/`;
export const LOGIN_URL = `${process.env.REACT_APP_API_URL}/login/`;
export const USERS_URL = `${process.env.REACT_APP_API_URL}/users`;
export const CONFIRM_EMAIL_URL = `${process.env.REACT_APP_API_URL}/confirm_email/`;

export function ProtectedRoutes() {
  const { authState } = useAuthContext();

  return authState.user?.isActive ? <Outlet /> : <Navigate to="/" />;
}
