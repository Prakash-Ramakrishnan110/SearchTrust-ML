import { Info, Cpu, Search, CheckCircle, Clock, ShieldAlert } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="dashboard-card full-width">
      <h2><Info size={24} color="var(--accent-primary)" /> About SearchTrust ML</h2>
      
      <div style={{ color: 'var(--text-secondary)', lineHeight: '1.7', marginBottom: '2rem' }}>
        <p style={{ fontSize: '1.1rem' }}>
          <strong>SearchTrust ML</strong> is an open, calibrated evaluation protocol for analyzing the reliability of AI-generated search answers at the claim level.
        </p>
      </div>

      <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#e2e8f0' }}>How It Works</h3>
      
      <div className="about-grid">
        <div className="about-card">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Cpu size={18} color="var(--accent-primary)" /> Claim Extraction</h3>
          <p>Decomposes a monolithic generated answer into individual, verifiable atomic claims using NLP models.</p>
        </div>
        
        <div className="about-card">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Search size={18} color="var(--accent-primary)" /> Hybrid Retrieval</h3>
          <p>Searches for grounding evidence across sources using both exact match (BM25) and dense semantic vectors.</p>
        </div>
        
        <div className="about-card">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><CheckCircle size={18} color="var(--status-supported)" /> NLI Verification</h3>
          <p>A Natural Language Inference model checks if the retrieved evidence logically entails the claim (SUPPORTED, REFUTED, or UNKNOWN).</p>
        </div>
        
        <div className="about-card">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Clock size={18} color="var(--status-unknown)" /> Temporal & Contradiction Risk</h3>
          <p>Checks for source freshness and identifies potential contradictory passages across different retrieved documents.</p>
        </div>
        
        <div className="about-card">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><ShieldAlert size={18} color="var(--status-refuted)" /> Abstention Policy</h3>
          <p>A holistic policy that recommends the AI abstain from answering if the risk of hallucination or contradiction is too high.</p>
        </div>
      </div>
    </div>
  );
}
