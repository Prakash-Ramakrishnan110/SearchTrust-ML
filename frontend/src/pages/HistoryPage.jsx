import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { History, ChevronRight, Search } from 'lucide-react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await fetch('/api/evaluations');
        const data = await res.json();
        setHistory(data);
      } catch (err) {
        console.error("Error fetching history:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, []);

  const handleViewProfile = (item) => {
    if (item.trust_profile) {
      navigate('/results', { state: { result: item.trust_profile } });
    } else {
      alert("This historical record does not contain the full Trust Profile data.");
    }
  };

  return (
    <div className="dashboard-card full-width">
      <h2><History size={24} color="var(--accent-primary)" /> Evaluation History</h2>
      
      {loading ? (
        <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <div className="spinner" style={{ borderColor: 'rgba(0,0,0,0.1)', borderTopColor: 'var(--accent-primary)', margin: '0 auto 1rem auto' }}></div>
          Loading history...
        </div>
      ) : history.length === 0 ? (
        <div style={{ padding: '4rem', textAlign: 'center', background: '#f8fafc', borderRadius: '12px', border: '1px dashed #cbd5e1' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No previous evaluations found.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {history.map((item) => (
            <div 
              key={item.evaluation_id} 
              style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                padding: '1.25rem', 
                border: '1px solid var(--border-color)', 
                borderRadius: '8px',
                background: 'white',
                boxShadow: 'var(--shadow-sm)'
              }}
            >
              <div style={{ flex: 1, paddingRight: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <Search size={14} color="var(--text-secondary)" />
                  <strong style={{ color: 'var(--text-primary)' }}>{item.query}</strong>
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
                  {item.answer}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.5rem' }}>
                  {item.created_at ? new Date(item.created_at).toLocaleString() : 'Unknown Date'}
                </div>
              </div>
              
              <button 
                className="primary-btn" 
                onClick={() => handleViewProfile(item)}
                disabled={!item.trust_profile}
                style={{ 
                  background: item.trust_profile ? 'var(--accent-light)' : '#f1f5f9', 
                  color: item.trust_profile ? 'var(--accent-primary)' : '#94a3b8', 
                  boxShadow: 'none' 
                }}
              >
                {item.trust_profile ? "View Profile" : "No Data"}
                <ChevronRight size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
