import Chart from 'react-apexcharts';
import { type ApexOptions } from 'apexcharts';

// Data dummy untuk grafik
const series = [
  {
    name: 'Harga Crypto',
    data: [
      47500, 48800, 50000, 49500, 51000, 52000, 51500, 52500, 50500, 49000, 
      49500, 48500, 48000, 47000, 47500, 48500, 49000, 48800, 49200, 48500,
      48000, 48300, 49000, 49500,
    ],
  },
];

// Opsi untuk styling grafik (dark mode, dll.)
const options: ApexOptions = {
  chart: {
    type: 'area',
    height: 350,
    zoom: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
    foreColor: '#9CA3AF', // Warna teks di sumbu
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.1,
      stops: [0, 90, 100],
    },
  },
  xaxis: {
    type: 'category',
    categories: [
      '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00',
      '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00',
      '22:00', '00:00', '02:00', '04:00',
    ],
    labels: {
      style: {
        colors: '#9CA3AF',
      },
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: '#9CA3AF',
      },
      formatter: (val) => `$${val.toLocaleString()}`,
    },
  },
  grid: {
    borderColor: '#374151',
    strokeDashArray: 4,
  },
  tooltip: {
    theme: 'dark',
    x: {
      format: 'HH:mm',
    },
    y: {
      formatter: (val) => `$${val.toLocaleString()}`,
    },
  },
  legend: {
    show: true,
    labels: {
      colors: '#E5E7EB'
    },
    markers: {
      fillColors: ['#3B82F6', '#10B981', '#EF4444']
    }
  },
  // Ini untuk meniru sinyal beli/jual, Anda bisa membuatnya lebih dinamis nanti
  annotations: {
    points: [
      {
        x: '10:00', // Sesuai kategori x
        y: 49000,
        marker: {
          size: 6,
          fillColor: '#10B981',
          strokeColor: '#fff',
          strokeWidth: 2,
          shape: 'circle',
        },
        label: {
          borderColor: '#10B981',
          offsetY: 0,
          style: {
            color: '#fff',
            background: '#10B981',
          },
          text: 'Sinyal Beli',
        },
      },
      {
        x: '12:00', // Sesuai kategori x
        y: 48800,
        marker: {
          size: 6,
          fillColor: '#EF4444',
          strokeColor: '#fff',
          strokeWidth: 2,
          shape: 'circle',
        },
        label: {
          borderColor: '#EF4444',
          offsetY: 0,
          style: {
            color: '#fff',
            background: '#EF4444',
          },
          text: 'Sinyal Jual',
        },
      },
    ],
  },
};

export default function PriceChart() {
  return (
    <div className="chart-container">
      <Chart options={options} series={series} type="area" height={350} />
    </div>
  );
}