import { useState } from 'react';
import { authApi } from '../services/api';
import { AuthContext } from './AuthContext';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const [loading] = useState(false);

  const login = async (email, password) => {
    const response = await authApi.login(email, password);
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    // For now, we don't have a /me endpoint, so we'll just store the email as user info
    const userInfo = { email };
    localStorage.setItem('user', JSON.stringify(userInfo));
    setUser(userInfo);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
