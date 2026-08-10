import React, { useState, useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onClose }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleBackdropClick = (e) => {
    if (e.target.classList.contains('modal-overlay')) {
      onClose();
    }
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setResult(null);
      setError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const dropped = e.dataTransfer.files[0];
      setFile(dropped);
      setPreview(URL.createObjectURL(dropped));
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Inference API unavailable');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.warn('API Error, using demo inference result', err);
      // Demo inference fallback
      setTimeout(() => {
        setResult({
          defect_class: 'Micro-crack',
          probability: 0.89,
          confidence: 'High'
        });
        setError('API unavailable. Showing demo inference result.');
        setLoading(false);
      }, 1500);
      return;
    }

    setLoading(false);
  };

  return (
    <div className="modal-overlay" onClick={handleBackdropClick}>
      <div className="modal-content upload-modal">
        <button className="close-btn" onClick={onClose}>&times;</button>
        
        <div className="modal-header">
          <h2>Upload Asset Image for AI Inspection</h2>
        </div>

        <div className="upload-container">
          {!preview ? (
            <div 
              className="dropzone"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <div className="dropzone-icon">📷</div>
              <p>Drag and drop an image here, or click to select</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                accept="image/*" 
                style={{ display: 'none' }}
              />
            </div>
          ) : (
            <div className="preview-container">
              <img src={preview} alt="Preview" className="image-preview" />
              <div className="preview-actions">
                <button className="btn" onClick={() => { setFile(null); setPreview(null); setResult(null); }}>
                  Change Image
                </button>
                <button className="btn btn-primary" onClick={handleUpload} disabled={loading}>
                  {loading ? 'Analyzing...' : 'Run Analysis'}
                </button>
              </div>
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          {result && (
            <div className="result-section">
              <h3>Analysis Result</h3>
              <div className="demo-inference-badge">DEMO INFERENCE</div>
              <div className="result-grid">
                <div className="result-item">
                  <span className="result-label">Defect Class</span>
                  <span className={`result-value ${result.defect_class !== 'None' ? 'text-danger' : 'text-success'}`}>
                    {result.defect_class}
                  </span>
                </div>
                <div className="result-item">
                  <span className="result-label">Probability</span>
                  <span className="result-value">{(result.probability * 100).toFixed(1)}%</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Confidence</span>
                  <span className="result-value">{result.confidence}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
