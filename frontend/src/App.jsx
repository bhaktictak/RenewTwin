import React from 'react';
import './App.css';
import Header from './components/Header';
import KPICards from './components/KPICards';
import AssetTable from './components/AssetTable';
import RiskDistribution from './components/RiskDistribution';
import CriticalAssets from './components/CriticalAssets';
import MaintenancePriorities from './components/MaintenancePriorities';
import AssetDetailModal from './components/AssetDetailModal';
import ImageUpload from './components/ImageUpload';
import { demoAssets, demoSummary, demoPriorities } from './data/demoData';

function App() {
  const [assets, setAssets] = React.useState([]);
  const [summary, setSummary] = React.useState({});
  const [priorities, setPriorities] = React.useState([]);
  const [selectedAsset, setSelectedAsset] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [isDemo, setIsDemo] = React.useState(false);
  const [showUpload, setShowUpload] = React.useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [assetsRes, summaryRes, prioritiesRes] = await Promise.all([
        fetch('http://localhost:8000/assets'),
        fetch('http://localhost:8000/dashboard/summary'),
        fetch('http://localhost:8000/dashboard/maintenance/priorities')
      ]);

      if (!assetsRes.ok || !summaryRes.ok || !prioritiesRes.ok) {
        throw new Error('API unavailable');
      }

      const assetsData = await assetsRes.json();
      const summaryData = await summaryRes.json();
      const prioritiesData = await prioritiesRes.json();

      setAssets(assetsData);
      setSummary(summaryData);
      setPriorities(prioritiesData);
      setIsDemo(false);
    } catch (error) {
      console.warn('Falling back to demo data', error);
      setAssets(demoAssets);
      setSummary(demoSummary);
      setPriorities(demoPriorities);
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Auto-refresh every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      <Header isDemo={isDemo} />
      
      <main className="main-content">
        {loading && assets.length === 0 ? (
          <div className="loading-spinner">Loading...</div>
        ) : (
          <>
            <KPICards summary={summary} />
            
            <div className="dashboard-grid">
              <div className="main-panel">
                <div className="card panel-header">
                  <h2>Asset Fleet Overview</h2>
                  <button className="btn btn-primary" onClick={() => setShowUpload(true)}>
                    + New Image Upload
                  </button>
                </div>
                <div className="card table-wrapper">
                  <AssetTable assets={assets} onSelectAsset={setSelectedAsset} />
                </div>
              </div>
              
              <div className="sidebar">
                <RiskDistribution summary={summary} />
                <CriticalAssets assets={assets.filter(a => a.risk_level === 'AT RISK' || a.risk_level === 'AT_RISK' || a.risk_level === 'CRITICAL')} />
                <MaintenancePriorities priorities={priorities} />
              </div>
            </div>
          </>
        )}
      </main>

      {selectedAsset && (
        <AssetDetailModal asset={selectedAsset} onClose={() => setSelectedAsset(null)} isDemo={isDemo} />
      )}
      
      {showUpload && (
        <ImageUpload onClose={() => setShowUpload(false)} />
      )}
    </div>
  );
}

export default App;
