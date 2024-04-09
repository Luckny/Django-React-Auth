export interface IUser {
  id: string;
  email: string;
  isEmailVerified: boolean;
}

export interface IAuthState {
  isAuthenticated: boolean;
  user: IUser | undefined;
  accessToken: string | undefined;
}

export interface IUserPayload {
  user: IUser | undefined;
  access_token: string | undefined;
}

export interface IAuthContext {
  isAuthenticated: boolean;
  user: IUser | undefined;
  // eslint-disable-next-line no-unused-vars
  setUser: (payload: IUserPayload) => void;
  accessToken: string | undefined;
}

export interface IAction {
  type: string;
  payload: IUserPayload;
}
