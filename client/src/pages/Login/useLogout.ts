import { useNavigate } from 'react-router-dom';
import { logoutAction } from '../../utils';
import useAuthContext from '../../contexts/AuthContext/useAuthContext';

export default function useLogout() {
  const { dispatch } = useAuthContext();
  const navigate = useNavigate();

  const logout = () => {
    // remove user from storage
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    dispatch(logoutAction);
    navigate('/');
  };

  return { logout };
}
