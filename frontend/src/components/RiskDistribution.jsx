import React from 'react';
import './RiskDistribution.css';

const RiskDistribution = ({ summary }) => {
  if (!summary) return null;

  const total = summary.total_assets || 1;
  
  const categories = [
    { label: 'Healthy', count: summary.healthy_count || 0, color: 'var(--success)' },
    { label: 'Monitor', count: summary.monitor_count || 0, color: 'var(--warning)' },
    { label: 'At Risk', count: summary.at_risk_count || 0, color: 'var(--danger)' },
    { label: 'Critical', count: summary.critical_count || 0, color: 'var(--critical)' }
  ];

  return (
    <div className="card risk-distribution-card">
      <h3 className="sidebar-title">Risk Distribution</h3>
      <div className="bars-container">
        {categories.map((cat, idx) => {
          const width = Math.max((cat.count / total) * 100, 2);
          return (
            <div key={idx} className="risk-bar-row">
              <div className="risk-bar-labels">
                <span className="risk-label">{cat.label}</span>
                <span className="risk-count">{cat.count}</span>
              </div>
              <div className="risk-bar-bg">
                <div 
                  className="risk-bar-fill" 
                  style={{ width: cat.count > 0 ? `${width}%` : '0%', backgroundColor: cat.color }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RiskDistribution;
