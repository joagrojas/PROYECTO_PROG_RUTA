import { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/api';

// Crear contexto
export const AuthContext = createContext(null);

// Hook
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};

// Provider
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      setUser(JSON.parse(savedUser));
    }
    
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password);
      const { access_token } = response;
      
      localStorage.setItem('token', access_token);
      
      const userInfo = await authService.getProfile();
      localStorage.setItem('user', JSON.stringify(userInfo));
      setUser(userInfo);
      
      return { success: true };
    } catch (error) {
      console.error('Error en login:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Error al iniciar sesión' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const isAdmin = () => user?.rol === 'admin';
  const isEditor = () => user?.rol === 'editor' || user?.rol === 'admin';

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin,
    isEditor,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}