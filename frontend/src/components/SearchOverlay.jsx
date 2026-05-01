import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Search, TrendingUp, Store, Calendar, ArrowRight } from 'lucide-react';
import { analyticsApi } from '../services/api';

const SearchOverlay = ({ onClose }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const response = await analyticsApi.getPriceHistory(query);
      setResults(response.data);
    } catch (err) {
      console.error('Search failed', err);
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
        background: 'rgba(15, 23, 42, 0.95)',
        backdropFilter: 'blur(12px)',
        zIndex: 200,
        padding: '2rem'
      }}
    >
      <div className="container" style={{ maxWidth: '800px' }}>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '2rem' }}>
          <button onClick={onClose} className="btn-secondary" style={{ padding: '0.5rem', borderRadius: '50%' }}>
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSearch} style={{ position: 'relative', marginBottom: '3rem' }}>
          <Search 
            size={24} 
            style={{ position: 'absolute', left: '1.25rem', top: '50%', transform: 'translateY(-50%)', opacity: 0.5 }} 
          />
          <input 
            autoFocus
            type="text" 
            placeholder="Search for an item (e.g. Milk, Bread...)" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ 
              padding: '1.25rem 1.25rem 1.25rem 3.5rem', 
              fontSize: '1.25rem', 
              borderRadius: 'var(--radius-xl)',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border)'
            }}
          />
          <button 
            type="submit"
            className="btn-primary"
            style={{ 
              position: 'absolute', 
              right: '0.75rem', 
              top: '50%', 
              transform: 'translateY(-50%)',
              padding: '0.5rem 1.25rem'
            }}
          >
            Search
          </button>
        </form>

        <div style={{ minHeight: '400px' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '4rem' }}>
              <p>Searching for "{query}"...</p>
            </div>
          ) : results ? (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem' }}>
                <TrendingUp size={24} color="var(--primary)" />
                <h2>Price History for "{query}"</h2>
              </div>

              {results.length === 0 ? (
                <div className="card glass" style={{ textAlign: 'center', padding: '3rem' }}>
                  <p>No price history found for this item.</p>
                </div>
              ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                  {results.map((item, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className="card glass"
                      style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.25rem' }}
                    >
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                          <Store size={16} color="var(--primary)" />
                          <span style={{ fontWeight: '600' }}>{item.store}</span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                          <Calendar size={14} />
                          {item.date}
                          {item.item_description && <span>• {item.item_description}</span>}
                        </div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontWeight: '700', fontSize: '1.25rem', color: 'var(--text)' }}>
                          ₹{item.price.toFixed(2)}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '4rem', opacity: 0.5 }}>
              <TrendingUp size={48} style={{ margin: '0 auto 1rem' }} />
              <p>Search for an item to see its price trends across different stores.</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default SearchOverlay;
