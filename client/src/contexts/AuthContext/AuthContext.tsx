import React, { createContext, useReducer, useMemo, useEffect } from 'react';

import axios, { isAxiosError } from 'axios';
import { USERS_URL, createUser } from '../../utils';
import {
  IAuthContext,
  AuthState,
  UserAction,
  UserError,
} from '../../types/AuthTypes';

// initial authenticate state of the context
const initialAuthState: AuthState = {
  user: undefined,
  accessToken: undefined,
};

// custom authentification context
export const AuthContext = createContext<IAuthContext | undefined>(undefined);

// reducer actions
const actions = {
  LOGIN: 'LOGIN',
  LOGOUT: 'LOGOUT',
  UPDATE_USER: 'UPDATE_USER',
};

/**
 * Reducer function for managing authentication state.
 * @param state The current authentication state.
 * @param action The action object that describes the state change.
 * @returns The new authentication state based on the action.
 */
export const authReducer = (
  state: AuthState,
  action: UserAction,
): AuthState => {
  // Switch statement to handle different action types
  switch (action.type) {
    // For register and login
    case actions.LOGIN:
      return {
        user: createUser(action.payload.user),
        accessToken: action.payload.access_token,
      };
    // For user logout
    case actions.LOGOUT:
      return initialAuthState;
    case actions.UPDATE_USER:
      return {
        user: createUser(action.payload),
        accessToken: state.accessToken,
      };
    // Default case if action type doesn't match
    default:
      return state;
  }
};

export function AuthContextProvider({ children }: any) {
  const [authState, dispatch] = useReducer(authReducer, initialAuthState);

  // on first render only
  useEffect(() => {
    const initiateState = async () => {
      const idStr = localStorage.getItem('id'); // get json user from local storage
      const tokenStr = localStorage.getItem('token');

      if (idStr && tokenStr) {
        const id = JSON.parse(idStr);
        const token = JSON.parse(tokenStr);
        try {
          // since user is defined, we should dispatch the LOGIN action
          const { data } = await axios.get(`${USERS_URL}/${id}`, {
            headers: { Authorization: `Token ${token}` },
          });
          // update state
          dispatch({
            type: actions.LOGIN,
            payload: { user: data, access_token: token },
          });
        } catch (e) {
          if (isAxiosError<UserError>(e)) {
            // eslint-disable-next-line no-console
            console.error(e);
          }
        }
      }

      // if invalid token go to login
    };
    initiateState();
  }, []);

  const authContextProviderValue = useMemo(
    () => ({ authState, dispatch }),
    [authState, dispatch],
  );

  return (
    <AuthContext.Provider value={authContextProviderValue}>
      {children}
    </AuthContext.Provider>
  );
}
