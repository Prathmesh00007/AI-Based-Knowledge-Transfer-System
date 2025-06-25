// src/components/Auth.jsx
import React from 'react';

const Auth = () => {
  const handleLogin = () => {
    // Redirect to your backend's /login endpoint.
    window.location.href = "http://127.0.0.1:8000/login";
  };

  return (
    <div style={{ margin: '1rem 0' }}>
      <h2>Login</h2>
      <button onClick={handleLogin}>Sign in with Atlassian</button>
    </div>
  );
};

export default Auth;
