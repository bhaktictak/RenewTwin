import React from 'react';
import './SidebarList.css';

const CriticalAssets = ({ assets }) => {
  const sorted = [...assets].sort((a, b) => a.health_score - b.health_score).slice(0, 8);

  return (
    <div className="card critical-assets-card sidebar-list-card">
      <h3 className="sidebar-title">Critical Assets</h3>
      {sorted.length === 0 ? (
        <p className="empty-state">No critical assets found.</p>
      ) : (
        <ul className="sidebar-list">
          {sorted.map(asset => (
            <li key={asset.asset_id} className="sidebar-list-item">
              <div className="item-header">
                <span className="item-id">{asset.asset_id}</span>
                <span className={`badge ${asset.risk_level.toLowerCase()}`}>{asset.risk_level.replace('_', ' ')}</span>
              </div>
              <div className="item-details">
                <span className="item-score">Score: {asset.health_score}</span>
                <span className="item-defect">{asset.defect}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CriticalAssets;
