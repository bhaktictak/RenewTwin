import React from 'react';
import './Header.css';

const Header = ({ isDemo }) => {
  return (
    <header className="app-header">
      <div className="header-left">
        <h1 className="logo">RENEWTWIN</h1>
        <span className="subtitle">Renewable Asset Intelligence Platform</span>
      </div>
      <div className="header-right">
        <div className="system-status">
          <span className="status-dot"></span>
          <span className="status-text">SYSTEM ONLINE</span>
        </div>
        {isDemo && (
          <div className="demo-badge">DEMO MODE</div>
        )}
      </div>
    </header>
  );
};

export default Header;
