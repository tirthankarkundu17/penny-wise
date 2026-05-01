import React, { useEffect, useState } from 'react';
import { billsApi } from '../services/api';
import { Plus, Receipt, Search, LogOut, ChevronRight, Calendar, Store, CreditCard } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import BillDetails from '../components/BillDetails';
import UploadModal from '../components/UploadModal';
import SearchOverlay from '../components/SearchOverlay';

const Dashboard = () => {
  const [bills, setBills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBill, setSelectedBill] = useState(null);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const { logout, user } = useAuth();

  const fetchBills = async () => {
    try {
      const response = await billsApi.list();
      setBills(response.data);
    } catch (err) {
      console.error('Failed to fetch bills', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBills();
  }, []);

  return (
    <div className="container" style={{ paddingTop: '2rem', paddingBottom: '5rem' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h1 style={{ marginBottom: '0.25rem' }}>Hello, {user?.email.split('@')[0]}</h1>
          <p>You have {bills.length} bills tracked</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            onClick={() => setIsSearchOpen(true)}
            className="btn-secondary" 
            style={{ borderRadius: '50%', padding: '0.75rem', width: '48px', height: '48px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >
            <Search size={20} />
          </button>
          <button 
            onClick={logout}
            className="btn-secondary" 
            style={{ borderRadius: '50%', padding: '0.75rem', width: '48px', height: '48px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >
            <LogOut size={20} />
          </button>
        </div>
      </header>

      <section>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2>Recent Bills</h2>
          <button 
            onClick={() => setIsUploadOpen(true)}
            className="btn-primary" 
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={20} />
            <span>Add New</span>
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem' }}>
            <p>Loading your bills...</p>
          </div>
        ) : bills.length === 0 ? (
          <div className="card glass" style={{ textAlign: 'center', padding: '4rem' }}>
            <Receipt size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
            <p>No bills found. Upload your first receipt!</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '1rem' }}>
            {bills.map((bill) => (
              <motion.div
                key={bill.id}
                whileHover={{ x: 4 }}
                onClick={() => setSelectedBill(bill)}
                className="card glass"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between', 
                  cursor: 'pointer',
                  padding: '1.25rem'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                  <div style={{ 
                    background: 'rgba(99, 102, 241, 0.1)', 
                    color: 'var(--primary)',
                    width: '48px', 
                    height: '48px', 
                    borderRadius: '12px', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center' 
                  }}>
                    <Store size={24} />
                  </div>
                  <div>
                    <h3 style={{ marginBottom: '0.25rem', fontSize: '1.1rem' }}>{bill.store_name}</h3>
                    <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Calendar size={14} />
                        {bill.bill_date}
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Receipt size={14} />
                        {bill.items.length} items
                      </span>
                    </div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontWeight: '700', fontSize: '1.25rem', color: 'var(--text)' }}>
                      ₹{bill.grand_total.toFixed(2)}
                    </div>
                  </div>
                  <ChevronRight size={20} style={{ opacity: 0.5 }} />
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </section>

      <AnimatePresence>
        {selectedBill && (
          <BillDetails 
            bill={selectedBill} 
            onClose={() => setSelectedBill(null)} 
          />
        )}
        {isUploadOpen && (
          <UploadModal 
            onClose={() => setIsUploadOpen(false)} 
            onSuccess={() => {
              setIsUploadOpen(false);
              fetchBills();
            }}
          />
        )}
        {isSearchOpen && (
          <SearchOverlay 
            onClose={() => setIsSearchOpen(false)} 
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Dashboard;
