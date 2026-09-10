import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Beaker, Search, Plus, Trash2 } from 'lucide-react';

export default function InputPage() {
  const [query, setQuery] = useState("Who is the current CEO of Example Company?");
  const [answer, setAnswer] = useState("Alex Smith became CEO in 2019. He remains the current CEO.");
  
  // Sources is now a managed array of objects instead of a raw JSON string
  const [sources, setSources] = useState([
    {
      source_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      title: "Company announcement",
      content: "Alex Smith became CEO of Example Company in 2019.",
      source_type: "NEWS"
    }
  ]);
  
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleAddSource = () => {
    setSources([...sources, {
      source_id: crypto.randomUUID(),
      title: "",
      content: "",
      source_type: "UNKNOWN"
    }]);
  };

  const handleRemoveSource = (index) => {
    setSources(sources.filter((_, i) => i !== index));
  };

  const handleSourceChange = (index, field, value) => {
    const newSources = [...sources];
    newSources[index][field] = value;
    setSources(newSources);
  };

  const handleAutoFetch = async () => {
    if (!query) {
      alert("Please enter a Search Query first.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Search failed");
      
      // Append the new sources
      setSources([...sources, ...data]);
    } catch (err) {
      alert("Error fetching sources: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          answer,
          sources: sources,
          query_time: new Date().toISOString()
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail ? JSON.stringify(data.detail) : "API Error");
      }
      navigate('/results', { state: { result: data } });
    } catch (err) {
      alert("Error analyzing input: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-card">
      <h2><Beaker size={24} color="var(--accent-primary)" /> New Evaluation</h2>
      <form onSubmit={handleAnalyze}>
        <div className="form-group">
          <label>Search Query</label>
          <input 
            value={query} 
            onChange={e => setQuery(e.target.value)} 
            placeholder="e.g. Who is the CEO?"
            required 
          />
        </div>
        <div className="form-group">
          <label>AI Generated Answer to Evaluate</label>
          <textarea 
            rows={3} 
            value={answer} 
            onChange={e => setAnswer(e.target.value)} 
            placeholder="e.g. The CEO is..."
            required 
          />
        </div>
        
        <div className="form-group" style={{ marginTop: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <label style={{ margin: 0 }}>Retrieved Evidence Sources</label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="button" onClick={handleAutoFetch} className="primary-btn" disabled={loading} style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                <Search size={16} /> Auto-Fetch Web
              </button>
              <button type="button" onClick={handleAddSource} className="primary-btn" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem', background: '#e2e8f0', color: '#334155', boxShadow: 'none' }}>
                <Plus size={16} /> Add Manual
              </button>
            </div>
          </div>
          
          {sources.length === 0 && (
            <div style={{ padding: '2rem', textAlign: 'center', background: '#f8fafc', borderRadius: '8px', border: '1px dashed #cbd5e1', color: '#64748b' }}>
              No sources added. The AI answer will likely be marked as UNKNOWN.
            </div>
          )}

          {sources.map((source, index) => (
            <div key={source.source_id} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '1.25rem', marginBottom: '1rem', position: 'relative' }}>
              <button 
                type="button" 
                onClick={() => handleRemoveSource(index)}
                style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '0.25rem' }}
                title="Remove Source"
              >
                <Trash2 size={18} />
              </button>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem', paddingRight: '2.5rem' }}>
                <div>
                  <label style={{ fontSize: '0.75rem', color: '#64748b' }}>Source Title</label>
                  <input 
                    value={source.title} 
                    onChange={e => handleSourceChange(index, 'title', e.target.value)} 
                    placeholder="e.g. Wikipedia Article"
                    required 
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', color: '#64748b' }}>Source Type</label>
                  <select 
                    value={source.source_type} 
                    onChange={e => handleSourceChange(index, 'source_type', e.target.value)}
                    style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', border: '1px solid #cbd5e1', background: 'white' }}
                  >
                    <option value="NEWS">News</option>
                    <option value="WIKIPEDIA">Wikipedia</option>
                    <option value="BLOG">Blog</option>
                    <option value="DOCUMENT">Document</option>
                    <option value="UNKNOWN">Unknown</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label style={{ fontSize: '0.75rem', color: '#64748b' }}>Passage Content</label>
                <textarea 
                  rows={2}
                  value={source.content} 
                  onChange={e => handleSourceChange(index, 'content', e.target.value)} 
                  placeholder="Paste the raw text of the source document here..."
                  required 
                />
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: '2rem' }}>
          <button type="submit" className="primary-btn" disabled={loading} style={{ width: '100%' }}>
            {loading ? (
              <>
                <div className="spinner"></div>
                Analyzing Trust Profile...
              </>
            ) : (
              <>
                <Search size={18} />
                Generate Trust Profile
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
