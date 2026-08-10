import React from 'react';
import './AssetDetailModal.css';

const AssetDetailModal = ({ asset, onClose, isDemo }) => {
  if (!asset) return null;

  const handleBackdropClick = (e) => {
    if (e.target.classList.contains('modal-overlay')) {
      onClose();
    }
  };

  const getHealthClass = (score) => {
    if (score >= 90) return 'healthy';
    if (score >= 75) return 'monitor';
    if (score >= 50) return 'at_risk';
    return 'critical';
  };
  
  const hs = Math.round(asset.health_score || 0);
  const healthClass = getHealthClass(hs);
  
  // Handle both backend and demo field names
  const power = asset.current_power_kw || asset.power || 0;
  const expectedPower = asset.expected_power_kw || asset.expected_power || 1;
  const temp = asset.temperature_c || asset.temp || 0;
  const defect = asset.defect_class || asset.defect || 'none';
  const defectProb = asset.defect_probability != null ? Math.round(asset.defect_probability * 100) : null;
  const anomalyScore = asset.anomaly_score != null ? Math.round(asset.anomaly_score * 100) : null;
  const priority = asset.maintenance_priority || asset.priority || '—';
  const recAction = asset.recommended_action || 'No action required';
  const assetType = asset.asset_type || asset.type || 'Solar PV Panel';
  const ratedCapacity = asset.rated_capacity_kw || '—';

  return (
    <div className="modal-overlay" onClick={handleBackdropClick}>
      <div className="modal-content asset-modal">
        <button className="close-btn" onClick={onClose}>&times;</button>
        
        <div className="modal-header">
          <h2>Digital Twin: {asset.asset_id}</h2>
          <span className={`badge ${(asset.risk_level || '').toLowerCase().replace(' ', '_')}`}>{(asset.risk_level || '').replace('_', ' ')}</span>
        </div>

        <div className="modal-grid">
          {/* Section 1: Asset Information */}
          <div className="modal-section info-section">
            <h3>Asset Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Type</span>
                <span className="info-value">{assetType}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Location</span>
                <span className="info-value">{asset.location}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Rated Capacity</span>
                <span className="info-value">{typeof ratedCapacity === 'number' ? ratedCapacity.toFixed(1) + ' kW' : ratedCapacity}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Install Date</span>
                <span className="info-value">{asset.installation_date ? asset.installation_date.split('T')[0] : '—'}</span>
              </div>
            </div>
          </div>

          {/* Section 2: Health Assessment */}
          <div className="modal-section health-section">
            <h3>Health Assessment</h3>
            <div className="health-assessment-content">
              <div className={`large-health-score ${healthClass}`}>
                {hs}
              </div>
              <div className="health-bar-container large-bar-container">
                <div className="health-bar-bg">
                  <div className={`health-bar-fill ${healthClass}`} style={{ width: `${hs}%` }}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Current State */}
          <div className="modal-section state-section">
            <h3>Current State</h3>
            <div className="state-info">
              <div className="state-item">
                <div className="state-item-header">
                  <span className="info-label">Power Output</span>
                  <span className="info-value">{typeof power === 'number' ? power.toFixed(1) : power} / {typeof expectedPower === 'number' ? expectedPower.toFixed(1) : expectedPower} kW</span>
                </div>
                <div className="progress-bg">
                  <div className="progress-fill" style={{ width: `${Math.min((power / expectedPower) * 100, 100)}%`, backgroundColor: 'var(--primary)' }}></div>
                </div>
              </div>
              <div className="state-item">
                <span className="info-label">Temperature</span>
                <span className="info-value temp-value">{typeof temp === 'number' ? temp.toFixed(1) : temp} °C</span>
              </div>
              <div className="state-item">
                <span className="info-label">Performance Deviation</span>
                <span className="info-value">{expectedPower > 0 ? Math.round(((expectedPower - power) / expectedPower) * 100) : 0}%</span>
              </div>
            </div>
          </div>

          {/* Section 4: AI Analysis */}
          <div className="modal-section ai-section">
            <h3>AI Analysis</h3>
            <div className="ai-info">
              <div className="info-item">
                <span className="info-label">Detected Defect</span>
                <span className="info-value highlight-defect">{defect}</span>
              </div>
              {defectProb != null && (
                <div className="state-item">
                  <div className="state-item-header">
                    <span className="info-label">Defect Probability</span>
                    <span className="info-value">{defectProb}%</span>
                  </div>
                  <div className="progress-bg">
                    <div className="progress-fill" style={{ width: `${defectProb}%`, backgroundColor: 'var(--warning)' }}></div>
                  </div>
                </div>
              )}
              {anomalyScore != null && (
                <div className="state-item">
                  <div className="state-item-header">
                    <span className="info-label">Anomaly Score</span>
                    <span className="info-value">{anomalyScore}%</span>
                  </div>
                  <div className="progress-bg">
                    <div className="progress-fill" style={{ width: `${anomalyScore}%`, backgroundColor: 'var(--danger)' }}></div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Section 5: Maintenance */}
          <div className="modal-section maintenance-section" style={{ gridColumn: '1 / -1' }}>
            <h3>Maintenance Recommendations</h3>
            <div className="maintenance-info">
              <div className="priority-badge">Priority #{priority}</div>
              <p className="recommendation-text">{recAction}</p>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <span className="footer-label">Prototype Asset Health Index</span>
          <span className="footer-demo-badge">SYNTHETIC DEMO DATA</span>
        </div>
      </div>
    </div>
  );
};

export default AssetDetailModal;
