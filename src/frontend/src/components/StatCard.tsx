import { FiArrowUp, FiArrowDown } from 'react-icons/fi';

// Tentukan 'bentuk' dari props yang akan diterima komponen ini
type StatCardProps = {
  title: string;
  value: string;
  change?: 'up' | 'down'; // '?' berarti opsional
};

// CSS untuk StatCard
const cardStyle = {
  backgroundColor: '#1F2937',
  padding: '1.5rem',
  borderRadius: '12px',
};

const titleStyle = {
  fontSize: '0.875rem',
  color: '#9CA3AF',
  textTransform: 'uppercase' as 'uppercase',
  marginBottom: '0.5rem',
};

const valueStyle = {
  fontSize: '1.875rem',
  fontWeight: '600' as '600',
  color: 'white',
  display: 'flex',
  alignItems: 'center',
  gap: '0.5rem',
};

export default function StatCard({ title, value, change }: StatCardProps) {
  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>{title}</h3>
      <div style={valueStyle}>
        {value}
        {change === 'up' && <FiArrowUp size={20} color="#10B981" />}
        {change === 'down' && <FiArrowDown size={20} color="#EF4444" />}
      </div>
    </div>
  );
}