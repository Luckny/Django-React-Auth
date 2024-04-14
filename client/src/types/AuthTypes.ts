export type User =
  | {
      id: string;
      email: string;
      isEmailVerified: boolean;
    }
  | undefined;

export type AuthState = {
  user: User | undefined;
  accessToken: string | undefined;
};

export type UserPayload = {
  user: User | undefined;
  access_token: string | undefined;
};

export interface IAuthContext {
  authState: AuthState;
  // eslint-disable-next-line no-unused-vars
  setUser: (payload: UserPayload) => void;
  removeUser: () => void;
}

export type UserAction = {
  type: string;
  payload: UserPayload;
};

export type ValidationError =
  | {
      email?: string[];
      non_field_errors?: string[];
    }
  | undefined;
