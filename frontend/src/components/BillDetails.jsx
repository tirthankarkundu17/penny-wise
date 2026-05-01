import { motion } from 'framer-motion';
import { X, Store, Calendar, Hash, CreditCard } from 'lucide-react';

const BillDetails = ({ bill, onClose }) => {
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
          maxWidth: '600px',
          maxHeight: '90vh',
          overflowY: 'auto',
          padding: 0
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ 
          padding: '1.5rem', 
          borderBottom: '1px solid var(--border)', 
          display: 'flex', 
          justifyContent: 'space-between',
          alignItems: 'center',
          position: 'sticky',
          top: 0,
          background: 'var(--surface)',
          zIndex: 1
        }}>
          <h2>Bill Details</h2>
          <button onClick={onClose} className="btn-secondary" style={{ padding: '0.5rem', borderRadius: '50%' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1.5rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Store size={20} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Store</div>
                <div style={{ fontWeight: '600' }}>{bill.store_name}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Calendar size={20} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Date</div>
                <div style={{ fontWeight: '600' }}>{bill.bill_date}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Hash size={20} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Bill #</div>
                <div style={{ fontWeight: '600' }}>{bill.bill_number || 'N/A'}</div>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <CreditCard size={20} color="var(--primary)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Total Amount</div>
                <div style={{ fontWeight: '700', color: 'var(--text)', fontSize: '1.1rem' }}>₹{bill.grand_total.toFixed(2)}</div>
              </div>
            </div>
          </div>

          <h3 style={{ marginBottom: '1rem' }}>Items</h3>
          <div style={{ border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.05)', textAlign: 'left', fontSize: '0.875rem' }}>
                  <th style={{ padding: '0.75rem 1rem' }}>Item</th>
                  <th style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>Qty</th>
                  <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Price</th>
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
