import './App.css'; // Kita import CSS kustom kita
import Sidebar from './components/Sidebar';
import StatCard from './components/StatCard';
import PriceChart from './components/PriceChart';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      
      <main className="main-content">
        <header className="dashboard-header">
          <h1>Price Prediction Dashboard</h1>
          <p>Visualisasi data harga crypto dan hasil prediksi model.</p>
        </header>

        {/* Komponen Grafik */}
        <PriceChart />

        {/* Komponen Statistik */}
        <div className="stats-container">
          <h2>Next Prediction Result</h2>
          <div className="stats-grid">
            <StatCard title="Open" value="$49240.38" />
            <StatCard title="High" value="$53268.19" change="up" />
            <StatCard title="Low" value="$45763.01" change="down" />
            <StatCard title="Close" value="$48245.58" />
            <StatCard title="Volume" value="1062.34M" />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;