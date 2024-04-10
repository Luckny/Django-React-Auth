import { useState } from 'react';
import axios from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { SIGNUP_URL } from '../../constants';
import { UserError, UserPayload } from '../../types/AuthTypes';

export default function useSignup() {
  const [error, setError] = useState<UserError>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useAuthContext();

  const signup = async (email: string, password: string) => {
    // if url is not defined cancel operation
    if (!SIGNUP_URL) return;
    // Start loading on function call
    setIsLoading(true);
    // reset error
    setError({ email: [] });
    try {
      const { data } = await axios.post<UserPayload>(SIGNUP_URL, {
        email,
        password,
      });

      localStorage.setItem('token', data.access_token!);
      setUser(data);

      setIsLoading(false);
    } catch (e: any) {
      setIsLoading(false);
      setError(e.response.data);
    }
  };

  return { signup, isLoading, error: error?.email[0] };
}
