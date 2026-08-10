import React from 'react';
import './KPICards.css';

const KPICards = ({ summary }) => {
  if (!summary) return null;

  const cards = [
    { label: 'Total Assets', value: summary.total_assets || 0, color: 'var(--primary)' },
    { label: 'Healthy', value: summary.healthy_count || 0, color: 'var(--success)' },
    { label: 'Monitor', value: summary.monitor_count || 0, color: 'var(--warning)' },
    { label: 'At Risk', value: summary.at_risk_count || 0, color: 'var(--danger)' },
    { label: 'Critical', value: summary.critical_count || 0, color: 'var(--critical)' }
  ];

  return (
    <div className="kpi-container">
      {cards.map((card, index) => {
        const percentage = summary.total_assets ? Math.round((card.value / summary.total_assets) * 100) : 0;
        return (
          <div key={index} className="card kpi-card" style={{ borderLeftColor: card.color, borderLeftWidth: '4px' }}>
            <div className="kpi-content">
              <span className="kpi-label">{card.label}</span>
              <div className="kpi-metrics">
                <span className="kpi-value">{card.value}</span>
                {index > 0 && <span className="kpi-percentage">{percentage}%</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KPICards;
