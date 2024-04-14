import { useState } from 'react';
import axios, { isAxiosError } from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { SIGNUP_URL } from '../../constants';
import { ValidationError, UserPayload } from '../../types/AuthTypes';

export default function useSignup() {
  const [errors, setErrors] = useState<ValidationError>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useAuthContext();

  const signup = async (email: string, password: string) => {
    // if url is not defined cancel operation
    if (!SIGNUP_URL) return;
    // Start loading on function call
    setIsLoading(true);
    // reset error
    setErrors({ email: [] });
    try {
      const { data } = await axios.post<UserPayload>(SIGNUP_URL, {
        email,
        password,
      });

      localStorage.setItem('user', JSON.stringify(data));
      setUser(data);

      setIsLoading(false);
    } catch (e) {
      setIsLoading(false);
      if (isAxiosError<ValidationError>(e)) setErrors(e.response?.data);
      // eslint-disable-next-line no-console
      else console.error(e);
    }
  };

  return { signup, isLoading, errors };
}
