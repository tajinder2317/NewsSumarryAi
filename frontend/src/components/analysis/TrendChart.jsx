import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement
);

const TrendChart = ({ data, type = 'bar', title = '' }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '20px' }}>
        <p>No trend data available</p>
      </div>
    );
  }

  const chartData = {
    labels: data.map(item => item.name || item.label || 'Unknown'),
    datasets: [
      {
        label: title || 'Count',
        data: data.map(item => item.value || item.count || 0),
        backgroundColor: type === 'bar' ? 
          'rgba(54, 162, 235, 0.8)' : 
          'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        tension: type === 'line' ? 0.4 : 0,
        fill: type === 'line',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.parsed.y || 0;
            return `${label}: ${value}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0,
        },
      },
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
        },
      },
    },
  };

  const ChartComponent = type === 'line' ? Line : Bar;

  return (
    <div style={{ height: '300px', position: 'relative' }}>
      <ChartComponent data={chartData} options={options} />
    </div>
  );
};

export default TrendChart;
