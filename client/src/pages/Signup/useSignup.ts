import { useState } from 'react';
import axios, { isAxiosError } from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { SIGNUP_URL } from '../../utils';
import { UserError, UserPayload } from '../../types/AuthTypes';

export default function useSignup() {
  const [errors, setErrors] = useState<UserError>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const { dispatch } = useAuthContext();

  const signup = async (email: string, password: string) => {
    // if url is not defined cancel operation
    if (!SIGNUP_URL) return;
    // Start loading on function call
    setIsLoading(true);
    // reset error
    setErrors(undefined);
    try {
      const { data } = await axios.post<UserPayload>(SIGNUP_URL, {
        email,
        password,
      });

      localStorage.setItem('token', JSON.stringify(data.access_token));
      localStorage.setItem('id', JSON.stringify(data.user?.id));
      dispatch({ type: 'LOGIN', payload: data });

      setIsLoading(false);
    } catch (e) {
      setIsLoading(false);
      if (isAxiosError<UserError>(e)) setErrors(e.response?.data);
      // eslint-disable-next-line no-console
      else console.error(e);
    }
  };

  return { signup, isLoading, errors };
}
