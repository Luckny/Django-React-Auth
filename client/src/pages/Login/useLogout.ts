import useAuthContext from '../../contexts/AuthContext/useAuthContext';

export default function useLogout() {
  const { removeUser } = useAuthContext();

  const logout = () => {
    // remove user from storage
    localStorage.removeItem('user');
    removeUser();
  };

  return { logout };
}
