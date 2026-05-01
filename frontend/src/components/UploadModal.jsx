import { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Upload, Loader2, Image as ImageIcon, CheckCircle2 } from 'lucide-react';
import { billsApi } from '../services/api';

const UploadModal = ({ onClose, onSuccess }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [done, setDone] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type.startsWith('image/')) {
      setFile(selected);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(selected);
      setError('');
    } else {
      setError('Please select a valid image file (PNG, JPG, etc.)');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      await billsApi.upload(file);
      setDone(true);
      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process receipt. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(15, 23, 42, 0.8)',
        backdropFilter: 'blur(8px)',
        zIndex: 100,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1.5rem'
      }}
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        className="card glass"
        style={{
          width: '100%',
          maxWidth: '480px',
          padding: '2rem'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>Upload Receipt</h2>
          {!loading && !done && (
            <button onClick={onClose} className="btn-secondary" style={{ padding: '0.5rem', borderRadius: '50%' }}>
              <X size={20} />
            </button>
          )}
        </div>

        {done ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              style={{ color: 'var(--success)', marginBottom: '1.5rem' }}
            >
              <CheckCircle2 size={64} style={{ margin: '0 auto' }} />
            </motion.div>
            <h3 style={{ color: 'var(--text)' }}>Receipt Processed!</h3>
            <p>Your bill has been added to your dashboard.</p>
          </div>
        ) : (
          <>
            <div 
              style={{ 
                border: '2px dashed var(--border)', 
                borderRadius: 'var(--radius-lg)', 
                padding: '2.5rem', 
                textAlign: 'center',
                marginBottom: '1.5rem',
                background: preview ? 'none' : 'rgba(255,255,255,0.02)',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              {preview ? (
                <img src={preview} alt="Preview" style={{ width: '100%', height: '200px', objectFit: 'contain' }} />
              ) : (
                <>
                  <Upload size={40} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
                  <p style={{ marginBottom: '1rem' }}>Click or drag a photo of your receipt</p>
                  <input 
                    type="file" 
                    accept="image/*" 
                    onChange={handleFileChange}
                    style={{ 
                      position: 'absolute', 
                      top: 0, 
                      left: 0, 
                      width: '100%', 
                      height: '100%', 
                      opacity: 0, 
                      cursor: 'pointer' 
                    }}
                  />
                  <button className="btn-secondary" style={{ pointerEvents: 'none' }}>Choose Image</button>
                </>
              )}
            </div>

            {error && (
              <div style={{ 
                color: 'var(--error)', 
                background: 'rgba(239, 68, 68, 0.1)', 
                padding: '0.75rem', 
                borderRadius: 'var(--radius-md)', 
                marginBottom: '1.5rem',
                fontSize: '0.875rem'
              }}>
                {error}
              </div>
            )}

            <div style={{ display: 'flex', gap: '1rem' }}>
              <button 
                onClick={onClose} 
                className="btn-secondary" 
                style={{ flex: 1 }}
                disabled={loading}
              >
                Cancel
              </button>
              <button 
                onClick={handleUpload} 
                className="btn-primary" 
                style={{ flex: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                disabled={!file || loading}
              >
                {loading ? <Loader2 size={20} className="animate-spin" /> : <ImageIcon size={20} />}
                {loading ? 'Processing with AI...' : 'Upload & Analyze'}
              </button>
            </div>
          </>
        )}
      </motion.div>
    </motion.div>
  );
};

export default UploadModal;
