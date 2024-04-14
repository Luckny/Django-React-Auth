import { useState } from 'react';
import axios, { isAxiosError } from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { LOGIN_URL } from '../../constants';
import { UserPayload, ValidationError } from '../../types/AuthTypes';

export default function useLogin() {
  const [errors, setErrors] = useState<ValidationError>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const { dispatch } = useAuthContext();

  const login = async (email: string, password: string) => {
    if (!LOGIN_URL) return;

    setIsLoading(true); // Start loading on function call

    setErrors(undefined); // reset error

    try {
      const { data } = await axios.post<UserPayload>(LOGIN_URL, {
        email,
        password,
      });

      // add user to state and local storage
      localStorage.setItem('token', JSON.stringify(data.access_token));
      localStorage.setItem('id', JSON.stringify(data.user?.id));
      dispatch({ type: 'LOGIN', payload: data });

      setIsLoading(false); // stop loading
    } catch (e) {
      setIsLoading(false);
      if (isAxiosError<ValidationError>(e)) setErrors(e.response?.data);
      // eslint-disable-next-line no-console
      else console.error(e);
    }
  };

  return { login, isLoading, errors };
}
