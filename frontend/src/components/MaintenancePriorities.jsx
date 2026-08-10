import React from 'react';
import './SidebarList.css';

const MaintenancePriorities = ({ priorities }) => {
  const topPriorities = priorities.slice(0, 5);

  return (
    <div className="card maintenance-priorities-card sidebar-list-card">
      <h3 className="sidebar-title">Maintenance Priorities</h3>
      {topPriorities.length === 0 ? (
        <p className="empty-state">No pending maintenance.</p>
      ) : (
        <ul className="sidebar-list priority-list">
          {topPriorities.map((item, idx) => (
            <li key={idx} className="sidebar-list-item priority-item">
              <div className="priority-number">#{idx + 1}</div>
              <div className="priority-content">
                <div className="item-header">
                  <span className="item-id">{item.asset_id}</span>
                  <span className={`badge ${item.risk_level.toLowerCase()}`}>{item.risk_level.replace('_', ' ')}</span>
                </div>
                <div className="action-text">{item.recommended_action}</div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MaintenancePriorities;
