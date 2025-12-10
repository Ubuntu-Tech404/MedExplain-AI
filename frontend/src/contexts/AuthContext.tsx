import React, { createContext, useContext, useState, useEffect } from 'react';
import ApiService from '../services/api';
import LocalStorageService from '../services/localStorage';
import toast from 'react-hot-toast';

interface User {
  id: string;
  email: string;
  name: string;
  token: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for saved user on mount
    const savedUser = LocalStorageService.getUser();
    if (savedUser) {
      setUser(savedUser);
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      // In production, use real API
      // const response = await ApiService.login(email, password);
      
      // For demo, simulate login
      const demoUser: User = {
        id: 'demo-user-001',
        email,
        name: 'Dr. John Smith',
        token: 'demo-jwt-token'
      };

      LocalStorageService.saveUser(demoUser);
      setUser(demoUser);
      
      toast.success('Logged in successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      setLoading(true);
      // In production, use real API
      // const response = await ApiService.register(name, email, password);
      
      // For demo, simulate registration
      const demoUser: User = {
        id: `user-${Date.now()}`,
        email,
        name,
        token: 'demo-jwt-token'
      };

      LocalStorageService.saveUser(demoUser);
      setUser(demoUser);
      
      toast.success('Account created successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    LocalStorageService.logout();
    setUser(null);
    toast.success('Logged out successfully');
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};