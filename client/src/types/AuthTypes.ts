export type User =
  | {
      id: string;
      email: string;
      isEmailVerified: boolean;
    }
  | undefined;

export type AuthState = {
  isAuthenticated: boolean;
  user: User | undefined;
  accessToken: string | undefined;
};

export type UserPayload = {
  user: User | undefined;
  access_token: string | undefined;
};

export type TAuthContext = {
  isAuthenticated: boolean;
  user: User | undefined;
  // eslint-disable-next-line no-unused-vars
  setUser: (payload: UserPayload) => void;
  removeUser: () => void;
  accessToken: string | undefined;
};

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
