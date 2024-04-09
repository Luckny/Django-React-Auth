import { useState } from 'react';
import axios from 'axios';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';
import { IUserPayload } from '../../types/AuthTypes';

function isUserPayload(object: unknown): object is IUserPayload {
  if (object !== null && typeof object === 'object') {
    return 'access_token' in object;
  }

  return false;
}

export default function useSignup() {
  interface ErrorState {
    email: string[]; // Define the type for the email array as string[]
  }

  const [error, setError] = useState<ErrorState>({ email: [] });
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useAuthContext();
  const url = `${process.env.REACT_APP_API_URL}/users/`;

  const signup = async (email: string, password: string) => {
    // if url is not defined cancel operation
    if (!url) return;
    // Start loading on function call
    setIsLoading(true);
    // reset error
    setError({ email: [] });
    try {
      const { data }: { data: unknown } = await axios.post(url, {
        email,
        password,
      });

      if (isUserPayload(data)) {
        localStorage.setItem('token', data.access_token!);
        setUser(data);
      }
      setIsLoading(false);
    } catch (e: any) {
      setIsLoading(false);
      setError(e.response.data);
    }
  };

  return { signup, isLoading, error: error.email[0] };
}
