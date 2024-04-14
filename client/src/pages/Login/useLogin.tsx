import { useState } from 'react';
import axios, { isAxiosError } from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { LOGIN_URL } from '../../constants';
import { UserPayload, ValidationError } from '../../types/AuthTypes';

export default function useLogin() {
  const [errors, setErrors] = useState<ValidationError>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useAuthContext();

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
      localStorage.setItem('user', JSON.stringify(data));
      setUser(data);

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
