import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Upload, Loader2, Image as ImageIcon, CheckCircle2, Save, Plus, Trash2, Edit2 } from 'lucide-react';
import { billsApi } from '../services/api';

const UploadModal = ({ onClose, onSuccess }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState('select'); // 'select', 'edit', 'done'
  const [billData, setBillData] = useState(null);

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

  const handleExtract = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const response = await billsApi.extract(file);
      setBillData(response.data);
      setStep('edit');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process receipt. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError('');
    try {
      await billsApi.create(billData);
      setStep('done');
      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save bill. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const updateBillField = (field, value) => {
    setBillData(prev => ({ ...prev, [field]: value }));
  };

  const updateItemField = (index, field, value) => {
    const newItems = [...billData.items];
    newItems[index] = { ...newItems[index], [field]: value };
    
    // Recalculate value if qty or net_price changes
    if (field === 'qty' || field === 'net_price') {
        const qty = field === 'qty' ? parseFloat(value) || 0 : newItems[index].qty;
        const price = field === 'net_price' ? parseFloat(value) || 0 : newItems[index].net_price;
        newItems[index].value = qty * price;
    }
    
    setBillData(prev => ({ ...prev, items: newItems }));
  };

  const removeItem = (index) => {
    setBillData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const addItem = () => {
    setBillData(prev => ({
      ...prev,
      items: [...prev.items, { item_name: '', net_price: 0, qty: 1, value: 0 }]
    }));
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
          maxWidth: step === 'edit' ? '800px' : '480px',
          maxHeight: '90vh',
          padding: '2rem',
          overflowY: 'auto'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>{step === 'edit' ? 'Review & Edit Data' : 'Upload Receipt'}</h2>
          {!loading && step !== 'done' && (
            <button onClick={onClose} className="btn-secondary" style={{ padding: '0.5rem', borderRadius: '50%' }}>
              <X size={20} />
            </button>
          )}
        </div>

        <AnimatePresence mode="wait">
          {step === 'select' && (
            <motion.div
              key="select"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
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
                  onClick={handleExtract} 
                  className="btn-primary" 
                  style={{ flex: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                  disabled={!file || loading}
                >
                  {loading ? <Loader2 size={20} className="animate-spin" /> : <ImageIcon size={20} />}
                  {loading ? 'Processing with AI...' : 'Analyze Receipt'}
                </button>
              </div>
            </motion.div>
          )}

          {step === 'edit' && billData && (
            <motion.div
              key="edit"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
            >
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                  <div className="input-group">
                      <label>Store Name</label>
                      <input 
                          type="text" 
                          value={billData.store_name} 
                          onChange={(e) => updateBillField('store_name', e.target.value)}
                          className="glass"
                          style={{ width: '100%', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', color: 'var(--text)' }}
                      />
                  </div>
                  <div className="input-group">
                      <label>Bill Date</label>
                      <input 
                          type="text" 
                          value={billData.bill_date} 
                          onChange={(e) => updateBillField('bill_date', e.target.value)}
                          className="glass"
                          style={{ width: '100%', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', color: 'var(--text)' }}
                      />
                  </div>
                  <div className="input-group">
                      <label>Grand Total</label>
                      <input 
                          type="number" 
                          value={billData.grand_total} 
                          onChange={(e) => updateBillField('grand_total', parseFloat(e.target.value) || 0)}
                          className="glass"
                          style={{ width: '100%', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', color: 'var(--text)' }}
                      />
                  </div>
                  <div className="input-group">
                      <label>Bill ID (Number)</label>
                      <input 
                          type="text" 
                          value={billData.bill_number || ''} 
                          onChange={(e) => updateBillField('bill_number', e.target.value)}
                          className="glass"
                          style={{ width: '100%', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', color: 'var(--text)' }}
                          placeholder="Optional"
                      />
                  </div>
                  <div className="input-group" style={{ gridColumn: 'span 2' }}>
                      <label>Bill Description</label>
                      <input 
                          type="text" 
                          value={billData.description || ''} 
                          onChange={(e) => updateBillField('description', e.target.value)}
                          className="glass"
                          style={{ width: '100%', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', color: 'var(--text)' }}
                          placeholder="e.g. Monthly groceries, Office supplies"
                      />
                  </div>
              </div>

              <div style={{ marginTop: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                      <h3>Items</h3>
                      <button onClick={addItem} className="btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                          <Plus size={14} /> Add Item
                      </button>
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      {billData.items.map((item, index) => (
                          <div key={index} style={{ 
                              display: 'grid', 
                              gridTemplateColumns: '2fr 1fr 1fr 1fr auto', 
                              gap: '0.5rem', 
                              alignItems: 'center',
                              background: 'rgba(255,255,255,0.02)',
                              padding: '0.75rem',
                              borderRadius: 'var(--radius-md)',
                              border: '1px solid rgba(255,255,255,0.05)'
                          }}>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                                  <input 
                                      placeholder="Item Name"
                                      type="text" 
                                      value={item.item_name} 
                                      onChange={(e) => updateItemField(index, 'item_name', e.target.value)}
                                      style={{ background: 'transparent', border: 'none', color: 'var(--text)', width: '100%', fontWeight: '500' }}
                                  />
                                  <input 
                                      placeholder="Description"
                                      type="text" 
                                      value={item.description || ''} 
                                      onChange={(e) => updateItemField(index, 'description', e.target.value)}
                                      style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', width: '100%', fontSize: '0.75rem' }}
                                  />
                              </div>
                              <input 
                                  placeholder="Qty"
                                  type="number" 
                                  value={item.qty} 
                                  onChange={(e) => updateItemField(index, 'qty', e.target.value)}
                                  style={{ background: 'transparent', border: 'none', color: 'var(--text)', width: '100%' }}
                              />
                              <input 
                                  placeholder="Price"
                                  type="number" 
                                  value={item.net_price} 
                                  onChange={(e) => updateItemField(index, 'net_price', e.target.value)}
                                  style={{ background: 'transparent', border: 'none', color: 'var(--text)', width: '100%' }}
                              />
                              <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', textAlign: 'right', paddingRight: '0.5rem' }}>
                                  ₹{(item.value || 0).toFixed(2)}
                              </div>
                              <button onClick={() => removeItem(index)} style={{ color: 'var(--error)', background: 'none', border: 'none', cursor: 'pointer', opacity: 0.7 }}>
                                  <Trash2 size={16} />
                              </button>
                          </div>
                      ))}
                  </div>
              </div>

              {error && (
                <div style={{ color: 'var(--error)', background: 'rgba(239, 68, 68, 0.1)', padding: '0.75rem', borderRadius: 'var(--radius-md)', fontSize: '0.875rem' }}>
                  {error}
                </div>
              )}

              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                <button 
                  onClick={() => setStep('select')} 
                  className="btn-secondary" 
                  style={{ flex: 1 }}
                  disabled={loading}
                >
                  Back
                </button>
                <button 
                  onClick={handleSave} 
                  className="btn-primary" 
                  style={{ flex: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                  disabled={loading}
                >
                  {loading ? <Loader2 size={20} className="animate-spin" /> : <Save size={20} />}
                  {loading ? 'Saving...' : 'Confirm & Save'}
                </button>
              </div>
            </motion.div>
          )}

          {step === 'done' && (
            <motion.div
              key="done"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{ textAlign: 'center', padding: '2rem' }}
            >
              <div style={{ color: 'var(--success)', marginBottom: '1.5rem' }}>
                <CheckCircle2 size={64} style={{ margin: '0 auto' }} />
              </div>
              <h3 style={{ color: 'var(--text)' }}>Receipt Processed!</h3>
              <p>Your bill has been added to your dashboard.</p>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};

export default UploadModal;
