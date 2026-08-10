import React, { useState } from 'react';
import './AssetTable.css';

const AssetTable = ({ assets, onSelectAsset }) => {
  const [sortConfig, setSortConfig] = useState({ key: 'health_score', direction: 'ascending' });

  const sortedAssets = React.useMemo(() => {
    let sortableAssets = [...assets];
    if (sortConfig !== null) {
      sortableAssets.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableAssets;
  }, [assets, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const getHealthClass = (score) => {
    if (score >= 85) return 'healthy';
    if (score >= 70) return 'monitor';
    if (score >= 50) return 'at_risk';
    return 'critical';
  };

  const renderHealthScore = (score) => {
    const healthClass = getHealthClass(score);
    return (
      <div className="health-bar-container">
        <span className="health-score-value">{score}</span>
        <div className="health-bar-bg">
          <div className={`health-bar-fill ${healthClass}`} style={{ width: `${score}%` }}></div>
        </div>
      </div>
    );
  };

  const renderRiskBadge = (risk) => {
    const riskClass = risk.toLowerCase().replace(/\s+/g, '_');
    return <span className={`badge ${riskClass}`}>{risk.replace(/_/g, ' ')}</span>;
  };

  return (
    <div className="table-container asset-table-wrapper">
      <table>
        <thead>
          <tr>
            <th onClick={() => requestSort('asset_id')}>Asset ID</th>
            <th onClick={() => requestSort('location')}>Location</th>
            <th onClick={() => requestSort('health_score')}>Health Score</th>
            <th onClick={() => requestSort('risk_level')}>Risk Level</th>
            <th onClick={() => requestSort('defect')}>Defect</th>
            <th onClick={() => requestSort('power')}>Power (kW)</th>
            <th onClick={() => requestSort('temp')}>Temp (°C)</th>
            <th onClick={() => requestSort('priority')}>Priority</th>
          </tr>
        </thead>
        <tbody>
          {sortedAssets.map((asset) => (
            <tr key={asset.asset_id} onClick={() => onSelectAsset(asset)} className="clickable-row">
              <td className="asset-id-col">{asset.asset_id}</td>
              <td>{asset.location}</td>
              <td>{renderHealthScore(Math.round(asset.health_score))}</td>
              <td>{renderRiskBadge(asset.risk_level)}</td>
              <td>{asset.defect_class || asset.defect || '—'}</td>
              <td>{(asset.current_power_kw || asset.power || 0).toFixed?.(1) ?? asset.current_power_kw}</td>
              <td>{(asset.temperature_c || asset.temp || 0).toFixed?.(1) ?? asset.temperature_c}</td>
              <td>{asset.maintenance_priority || asset.priority || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssetTable;
