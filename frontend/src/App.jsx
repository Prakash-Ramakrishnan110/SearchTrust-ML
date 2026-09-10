import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileSearch, Info, ShieldCheck, History } from 'lucide-react';
import InputPage from './pages/InputPage';
import ResultsPage from './pages/ResultsPage';
import AboutPage from './pages/AboutPage';
import HistoryPage from './pages/HistoryPage';

function Sidebar() {
  const location = useLocation();
  
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>
          <ShieldCheck size={28} color="var(--accent-primary)" /> 
          SearchTrust
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
          ML Evaluation Protocol
        </p>
      </div>
      <nav className="sidebar-nav">
        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
          <LayoutDashboard size={20} />
          Evaluate
        </Link>
        <Link to="/history" className={location.pathname === '/history' ? 'active' : ''}>
          <History size={20} />
          History
        </Link>
        <Link to="/results" className={location.pathname === '/results' ? 'active' : ''}>
          <FileSearch size={20} />
          Results
        </Link>
        <Link to="/about" className={location.pathname === '/about' ? 'active' : ''}>
          <Info size={20} />
          About
        </Link>
      </nav>
    </aside>
  );
}

export default function App() {
  return (
    <Router>
      <div className="dashboard-container">
        <Sidebar />
        <main className="dashboard-content">
          <Routes>
            <Route path="/" element={<InputPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
