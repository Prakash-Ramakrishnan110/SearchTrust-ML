import { useLocation, useNavigate } from 'react-router-dom';
import { ShieldAlert, ShieldCheck, FileSearch, ArrowLeft, ShieldQuestion, ShieldX, Info, Printer } from 'lucide-react';
import ProvenanceGraph from '../components/ProvenanceGraph';

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result || !result.claims) {
    return (
      <div className="dashboard-card" style={{ textAlign: 'center', padding: '4rem', maxWidth: '600px', margin: '0 auto' }}>
        <h2 style={{ justifyContent: 'center' }}>No Results Found</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Please run an evaluation from the input page first.</p>
        <button className="primary-btn" onClick={() => navigate('/')} style={{ width: 'auto', padding: '0.75rem 2rem', margin: '0 auto' }}>
          <ArrowLeft size={18} />
          Back to Input
        </button>
      </div>
    );
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'SUPPORTED': return <ShieldCheck size={14} />;
      case 'REFUTED': return <ShieldX size={14} />;
      case 'UNKNOWN': return <ShieldQuestion size={14} />;
      case 'NEEDS_QUALIFICATION': return <Info size={14} />;
      default: return null;
    }
  };

  return (
    <div className="dashboard-card full-width">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 style={{ margin: 0 }}><FileSearch size={24} color="var(--accent-primary)" /> Trust Profile & Provenance</h2>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button 
            className="primary-btn" 
            onClick={() => window.print()} 
            style={{ width: 'auto', padding: '0.6rem 1.25rem', background: '#f1f5f9', color: '#334155', border: '1px solid var(--panel-border)', boxShadow: 'none' }}
          >
            <Printer size={18} />
            Export PDF
          </button>
          <button 
            className="primary-btn"
            onClick={() => navigate('/')} 
            style={{ width: 'auto', padding: '0.6rem 1.25rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--panel-border)', boxShadow: 'none' }}
          >
            New Evaluation
          </button>
        </div>
      </div>
      
      <div className="results-container">
        {result.abstention?.recommended && (
          <div className="abstain-warning">
            <ShieldAlert size={28} />
            <div>
              <strong style={{ display: 'block', fontSize: '1.1rem', marginBottom: '0.25rem' }}>Abstention Recommended</strong>
              <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>High risk detected based on contradiction, temporal decay, or lack of support.</div>
            </div>
          </div>
        )}

        <div className="results-overview">
          <div className="metric-card">
            <div className="metric-value">{result.claims.total}</div>
            <div className="metric-label">Claims Extracted</div>
          </div>
          <div className="metric-card">
            <div className="metric-value" style={{ color: 'var(--status-supported)' }}>
              {Math.round((result.claims.supported / Math.max(1, result.claims.total)) * 100)}%
            </div>
            <div className="metric-label">Support Ratio</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{result.temporal.freshness_warnings}</div>
            <div className="metric-label">Freshness Warnings</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{(result.contradiction.possible_risk * 100).toFixed(1)}%</div>
            <div className="metric-label">Contradiction Risk</div>
          </div>
        </div>

        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', fontWeight: 600 }}>Claim Explorer</h3>
        <div>
          {result.claims.details && result.claims.details.length > 0 ? (
            result.claims.details.map((claim, idx) => (
              <div key={idx} className="claim-item">
                <p>{claim.text}</p>
                <span className={`status-badge status-${claim.status}`}>
                  {getStatusIcon(claim.status)} {claim.status}
                </span>
              </div>
            ))
          ) : (
            <div style={{ color: 'var(--text-secondary)', fontStyle: 'italic', padding: '1rem' }}>No claims extracted.</div>
          )}
        </div>
      </div>
    </div>
  );
}
