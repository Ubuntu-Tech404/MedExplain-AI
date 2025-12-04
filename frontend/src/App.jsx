import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { auth } from './firebase/config';
import { onAuthStateChanged } from 'firebase/auth';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Upload from './components/Upload';
import Results from './components/Results';
import AuthGuard from './components/AuthGuard';
import './index.css';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
      
      // Cache user in localStorage for persistence
      if (user) {
        localStorage.setItem('medexplain_user', JSON.stringify({
          uid: user.uid,
          email: user.email,
          name: user.displayName,
          photoURL: user.photoURL
        }));
      } else {
        localStorage.removeItem('medexplain_user');
      }
    });

    // Check for cached user
    const cachedUser = localStorage.getItem('medexplain_user');
    if (cachedUser && !user) {
      setUser(JSON.parse(cachedUser));
      setLoading(false);
    }

    return unsubscribe;
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-white">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-4"></div>
        <p className="text-gray-600 text-lg">Loading MedExplain AI...</p>
        <p className="text-gray-500 text-sm mt-2">Your medical report explainer</p>
      </div>
    );
  }

  return (
    <Router>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1e40af',
            color: '#fff',
            fontSize: '16px',
            padding: '16px',
          },
        }}
      />
      
      <Routes>
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/" element={<AuthGuard user={user}><Dashboard /></AuthGuard>} />
        <Route path="/upload" element={<AuthGuard user={user}><Upload /></AuthGuard>} />
        <Route path="/results/:reportId" element={<AuthGuard user={user}><Results /></AuthGuard>} />
      </Routes>
    </Router>
  );
}
