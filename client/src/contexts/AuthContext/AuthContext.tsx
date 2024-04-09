import React, { createContext, useCallback, useReducer, useMemo } from 'react';
import {
  IAction,
  IAuthContext,
  IAuthState,
  IUserPayload,
} from '../../types/AuthTypes';

// initial authenticate state of the context
const initialAuthState: IAuthState = {
  isAuthenticated: false,
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
export const authReducer = (state: IAuthState, action: IAction): IAuthState => {
  // Switch statement to handle different action types
  switch (action.type) {
    // For register and login
    case actions.LOGIN:
      return {
        isAuthenticated: true,
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
  const [state, dispatch] = useReducer(authReducer, initialAuthState);

  // eslint-disable-next-line no-console
  console.log('AuthContext state: ', state); // debugging

  const setUser = useCallback((payload: IUserPayload) => {
    dispatch({
      type: actions.LOGIN,
      payload,
    });
  }, []);

  const authContextProviderValue = useMemo(
    () => ({ ...state, setUser }),
    [setUser, state],
  );

  return (
    <AuthContext.Provider value={authContextProviderValue}>
      {children}
    </AuthContext.Provider>
  );
}
