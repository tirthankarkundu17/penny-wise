import React from 'react';

const Layout = ({ children }) => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      <footer style={{ 
        padding: '2rem', 
        textAlign: 'center', 
        fontSize: '0.875rem', 
        color: 'var(--text-muted)',
        borderTop: '1px solid var(--border)',
        marginTop: 'auto'
      }}>
        &copy; {new Date().getFullYear()} PennyWise AI. All rights reserved.
      </footer>
    </div>
  );
};

export default Layout;
