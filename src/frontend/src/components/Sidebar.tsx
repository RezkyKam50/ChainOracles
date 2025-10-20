import { FiGrid, FiTrendingUp, FiSettings, FiChevronLeft } from 'react-icons/fi';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        ChainOracles
      </div>
      
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="model" style={{ fontSize: '0.75rem', color: '#9CA3AF' }}>Pilihan Model</label>
        <select 
          id="model" 
          style={{ 
            width: '100%', 
            padding: '0.5rem', 
            backgroundColor: '#374151', 
            color: 'white', 
            border: '1px solid #4B5563', 
            borderRadius: '8px', 
            marginTop: '0.5rem' 
          }}
        >
          <option>Transformer_SOL_1D</option>
          <option>LSTM_BTC_1H</option>
        </select>
      </div>

      <nav className="sidebar-menu">
        <a href="#" className="sidebar-menu-item">
          <FiGrid size={20} />
          <span>Dashboard</span>
        </a>
        <a href="#" className="sidebar-menu-item">
          <FiTrendingUp size={20} />
          <span>Train on Newest</span>
        </a>
        <a href="#" className="sidebar-menu-item">
          <FiSettings size={20} />
          <span>Visualize Metrics</span>
        </a>
      </nav>

      <div className="sidebar-footer">
        <a href="#" className="sidebar-menu-item">
          <FiChevronLeft size={20} />
          <span>Collapse</span>
        </a>
      </div>
    </aside>
  );
}