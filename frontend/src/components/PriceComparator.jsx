import { useState } from 'react';
import { Calculator, CheckCircle2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const PriceComparator = () => {
  const [prevPrice, setPrevPrice] = useState('');
  const [prevQty, setPrevQty] = useState('');
  const [newPrice, setNewPrice] = useState('');
  const [newQty, setNewQty] = useState('');

  const pPrice = parseFloat(prevPrice);
  const pQty = parseFloat(prevQty);
  const nPrice = parseFloat(newPrice);
  const nQty = parseFloat(newQty);

  const prevUnit = (!isNaN(pPrice) && !isNaN(pQty) && pQty > 0) ? pPrice / pQty : null;
  const newUnit = (!isNaN(nPrice) && !isNaN(nQty) && nQty > 0) ? nPrice / nQty : null;

  const getComparison = () => {
    if (prevUnit === null || newUnit === null) return null;
    if (newUnit < prevUnit) {
      const savings = ((prevUnit - newUnit) / prevUnit * 100).toFixed(1);
      return {
        type: 'better',
        message: `New price is ${savings}% cheaper! Better value.`,
        color: 'var(--success)'
      };
    } else if (newUnit > prevUnit) {
      const increase = ((newUnit - prevUnit) / prevUnit * 100).toFixed(1);
      return {
        type: 'worse',
        message: `New price is ${increase}% more expensive. Old price was better.`,
        color: 'var(--error)'
      };
    }
    return {
      type: 'equal',
      message: 'Prices are identical per unit.',
      color: 'var(--primary)'
    };
  };

  const comparison = getComparison();

  return (
    <div className="card glass mobile-p-1" style={{ marginTop: '2rem', border: '1px solid var(--primary)', background: 'rgba(99, 102, 241, 0.05)', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <Calculator size={20} color="var(--primary)" />
        <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Price Comparison Tool</h3>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }} className="mobile-gap-1">
        <div style={{ display: 'grid', gap: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>PREVIOUS PURCHASE</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '0.75rem' }}>
            <div>
              <label style={{ fontSize: '0.7rem', display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>Price (₹)</label>
              <input 
                type="number" 
                placeholder="0.00" 
                value={prevPrice} 
                onChange={(e) => setPrevPrice(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', fontSize: '0.9rem' }}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.7rem', display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>Quantity</label>
              <input 
                type="number" 
                placeholder="1" 
                value={prevQty} 
                onChange={(e) => setPrevQty(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', fontSize: '0.9rem' }}
              />
            </div>
          </div>
          <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', fontWeight: '500', minHeight: '1.25rem' }}>
            Unit Price: <span style={{ color: 'var(--text)' }}>{prevUnit !== null ? `₹${prevUnit.toFixed(2)}` : '—'}</span>
          </div>
        </div>

        <div style={{ display: 'grid', gap: '1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>NEW OPTION</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '0.75rem' }}>
            <div>
              <label style={{ fontSize: '0.7rem', display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>Price (₹)</label>
              <input 
                type="number" 
                placeholder="0.00" 
                value={newPrice} 
                onChange={(e) => setNewPrice(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', fontSize: '0.9rem' }}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.7rem', display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>Quantity</label>
              <input 
                type="number" 
                placeholder="1" 
                value={newQty} 
                onChange={(e) => setNewQty(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', fontSize: '0.9rem' }}
              />
            </div>
          </div>
          <div style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', fontWeight: '500', minHeight: '1.25rem' }}>
            Unit Price: <span style={{ color: 'var(--text)' }}>{newUnit !== null ? `₹${newUnit.toFixed(2)}` : '—'}</span>
          </div>
        </div>
      </div>

      <AnimatePresence>
        {comparison && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{ overflow: 'hidden' }}
          >
            <div style={{ 
              marginTop: '1.5rem', 
              padding: '1rem', 
              borderRadius: 'var(--radius-md)', 
              background: `${comparison.color}15`,
              border: `1px solid ${comparison.color}30`,
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem'
            }}>
              {comparison.type === 'better' ? (
                <CheckCircle2 size={20} color={comparison.color} />
              ) : (
                <AlertCircle size={20} color={comparison.color} />
              )}
              <div style={{ fontWeight: '600', color: comparison.color, fontSize: '0.95rem' }}>
                {comparison.message}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PriceComparator;
