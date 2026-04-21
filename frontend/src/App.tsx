import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Moon, Sun, Languages, TrendingUp } from 'lucide-react';
import PrasnaForm from './components/PrasnaForm';
import ResultDashboard from './components/ResultDashboard';
import ElectionAnalysis from './components/ElectionAnalysis';
import type { PrasnaResponse } from './types';

const App: React.FC = () => {
  const [result, setResult] = useState<PrasnaResponse | null>(null);
  const [view, setView] = useState<'prasna' | 'election'>('prasna');
  const [loading] = useState(false);
  const [lang, setLang] = useState('en');
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'}`}>
      <nav className="glass-panel" style={{ margin: '1rem', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div 
          onClick={() => setView('prasna')} 
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}
        >
          <Sparkles className="text-gold" size={28} />
          <h1 className="text-gold" style={{ fontSize: '1.5rem', margin: 0 }}>JAMAKKAL PRASNA</h1>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            onClick={() => {
              setView(view === 'election' ? 'prasna' : 'election');
              setResult(null); // Reset result when switching
            }}
            className="glass-panel"
            style={{ 
              padding: '8px 16px', 
              cursor: 'pointer', 
              border: view === 'election' ? '1px solid var(--color-gold)' : '1px solid rgba(255,255,255,0.1)', 
              color: view === 'election' ? 'var(--color-gold)' : 'white',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <TrendingUp size={20} />
            <span style={{ fontWeight: '600' }}>Election 2026</span>
          </button>
          <button
            onClick={() => setLang(l => l === 'en' ? 'ta' : 'en')}
            className="glass-panel"
            style={{ padding: '8px', cursor: 'pointer', border: 'none', color: 'white' }}
          >
            <Languages size={20} />
          </button>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="glass-panel"
            style={{ padding: '8px', cursor: 'pointer', border: 'none', color: 'white' }}
          >
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </nav>

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '1rem' }}>
        {view === 'election' ? (
          <ElectionAnalysis />
        ) : !result ? (
          <PrasnaForm onResult={setResult} lang={lang} />
        ) : (
          <ResultDashboard result={result} onReset={() => setResult(null)} lang={lang} />
        )}
      </main>

      {loading && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1 }}
          >
            <Sparkles size={48} className="text-gold" />
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default App;
