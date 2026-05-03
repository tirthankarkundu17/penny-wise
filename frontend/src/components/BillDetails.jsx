import { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Store, Calendar, Hash, CreditCard, Trash2, Loader2 } from 'lucide-react';
import { billsApi } from '../services/api';

const BillDetails = ({ bill: initialBill, onClose, onRefresh }) => {
  const [bill, setBill] = useState(initialBill);
  const [deleting, setDeleting] = useState(false);
  const [deletingItem, setDeletingItem] = useState(null);

  const handleDeleteBill = async () => {
    if (!window.confirm('Are you sure you want to delete this entire bill? This action cannot be undone.')) return;
    
    setDeleting(true);
    try {
      await billsApi.delete(bill.id);
      onRefresh();
      onClose();
    } catch {
      alert('Failed to delete bill');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteItem = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    
    setDeletingItem(itemId);
    try {
      await billsApi.deleteItem(itemId);
      // Update local state
      const updatedItems = bill.items.filter(item => item.id !== itemId);
      const newTotal = updatedItems.reduce((sum, item) => sum + item.value, 0);
      setBill({ ...bill, items: updatedItems, grand_total: newTotal });
      onRefresh();
    } catch {
      alert('Failed to delete item');
    } finally {
      setDeletingItem(null);
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
        className="card glass mobile-p-1"
        style={{
          width: '100%',
          maxWidth: '600px',
          maxHeight: '90vh',
          overflowY: 'auto',
          padding: 0
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ 
          padding: '1rem', 
          borderBottom: '1px solid var(--border)', 
          display: 'flex', 
          justifyContent: 'space-between',
          alignItems: 'center',
          position: 'sticky',
          top: 0,
          background: 'var(--surface)',
          zIndex: 1
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Bill Details</h2>
            <button 
                onClick={handleDeleteBill} 
                className="btn-secondary" 
                disabled={deleting}
                style={{ color: 'var(--error)', padding: '0.4rem 0.6rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem' }}
            >
                {deleting ? <Loader2 size={16} className="animate-spin" /> : <Trash2 size={16} />}
                <span className="mobile-hide">Delete Bill</span>
                <span style={{ display: 'none' }} className="mobile-show">Delete</span>
            </button>
          </div>
          <button onClick={onClose} className="btn-secondary" style={{ padding: '0.5rem', borderRadius: '50%' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Store size={18} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Store</div>
                <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{bill.store_name}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Calendar size={18} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Date</div>
                <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{bill.bill_date}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Hash size={18} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Bill #</div>
                <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{bill.bill_number || 'N/A'}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              < CreditCard size={18} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Total Amount</div>
                <div style={{ fontWeight: '700', color: 'var(--text)', fontSize: '1rem' }}>₹{bill.grand_total.toFixed(2)}</div>
              </div>
            </div>
            {bill.description && (
              <div style={{ gridColumn: '1 / -1', background: 'rgba(255,255,255,0.02)', padding: '0.75rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Description</div>
                <div style={{ fontSize: '0.85rem' }}>{bill.description}</div>
              </div>
            )}
          </div>

          <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Items</h3>
          <div style={{ border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', overflowX: 'auto', WebkitOverflowScrolling: 'touch' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.05)', textAlign: 'left', fontSize: '0.875rem' }}>
                  <th style={{ padding: '0.75rem 1rem' }}>Item</th>
                  <th style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>Qty</th>
                  <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Price</th>
                  <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {bill.items.map((item, idx) => (
                  <tr key={idx} style={{ borderTop: '1px solid var(--border)', fontSize: '0.875rem' }}>
                    <td style={{ padding: '0.75rem 1rem' }}>
                      <div style={{ fontWeight: '500' }}>{item.item_name}</div>
                      {item.description && <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{item.description}</div>}
                    </td>
                    <td style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>{item.qty}</td>
                    <td style={{ padding: '0.75rem 1rem', textAlign: 'right', fontWeight: '600' }}>₹{item.net_price.toFixed(2)}</td>
                    <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                        <button 
                            onClick={() => handleDeleteItem(item.id)} 
                            disabled={deletingItem === item.id}
                            style={{ color: 'var(--error)', background: 'none', border: 'none', cursor: 'pointer', opacity: 0.7 }}
                        >
                            {deletingItem === item.id ? <Loader2 size={16} className="animate-spin" /> : <Trash2 size={16} />}
                        </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default BillDetails;
