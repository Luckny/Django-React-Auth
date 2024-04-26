import { Dispatch } from 'react';

export declare namespace server {
  export type IUser =
    | {
        id: string;
        email: string;
        is_active: boolean;
      }
    | undefined;
}
export type User =
  | {
      id: string;
      email: string;
      isActive: boolean;
    }
  | undefined;

export type AuthState = {
  user: User | undefined;
  accessToken: string | undefined;
  isAuthenticated: boolean;
};

export type UserPayload = {
  user: server.IUser | undefined;
  access_token: string | undefined;
};

export type UserAction = {
  type: string;
  payload: UserPayload;
};
export interface IAuthContext {
  authState: AuthState;
  dispatch: Dispatch<UserAction>;
}

export type ValidationError =
  | {
      email?: string[];
      non_field_errors?: string[];
    }
  | undefined;

export type UserError =
  | {
      token: string;
      wrongOTP: string;
      expiredOTP: string;
      message: string;
    }
  | undefined;
