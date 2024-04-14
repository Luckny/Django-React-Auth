import React, {
  createContext,
  useCallback,
  useReducer,
  useMemo,
  useEffect,
} from 'react';

import { logoutAction } from '../../constants';
import {
  IAuthContext,
  AuthState,
  UserAction,
  UserPayload,
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
        user: action.payload.user,
        accessToken: action.payload.access_token,
      };
    // For user logout
    case actions.LOGOUT:
      return initialAuthState;
    // Default case if action type doesn't match
    default:
      return state;
  }
};

export function AuthContextProvider({ children }: any) {
  const [authState, dispatch] = useReducer(authReducer, initialAuthState);

  // on first render only
  useEffect(() => {
    const userString = localStorage.getItem('user'); // get json user from local storage
    if (userString) {
      // since user is defined, we should dispatch the LOGIN action
      const user = JSON.parse(userString);
      dispatch({ type: actions.LOGIN, payload: user });
    }
  }, []);

  // dispatch action to set the user state
  const setUser = useCallback((payload: UserPayload) => {
    dispatch({
      type: actions.LOGIN,
      payload,
    });
  }, []);

  // dispatch action to remove the user state
  const removeUser = useCallback(() => {
    dispatch(logoutAction);
  }, []);

  const authContextProviderValue = useMemo(
    () => ({ authState, setUser, removeUser }),
    [setUser, authState, removeUser],
  );

  return (
    <AuthContext.Provider value={authContextProviderValue}>
      {children}
    </AuthContext.Provider>
  );
}
