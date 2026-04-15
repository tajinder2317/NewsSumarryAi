import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const SentimentChart = ({ data, type = 'doughnut' }) => {
  if (!data) {
    return (
      <div style={{ textAlign: 'center', padding: '20px' }}>
        <p>No sentiment data available</p>
      </div>
    );
  }

  // Get current sentiment values
  const currentData = data.positive?.current_percentage || 
                     data.negative?.current_percentage || 
                     data.neutral?.current_percentage;

  const chartData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        label: 'Sentiment Distribution',
        data: [
          data.positive?.current_percentage || 0,
          data.negative?.current_percentage || 0,
          data.neutral?.current_percentage || 0,
        ],
        backgroundColor: [
          'rgba(75, 192, 192, 0.8)',  // Green for positive
          'rgba(255, 99, 132, 0.8)',  // Red for negative
          'rgba(201, 203, 207, 0.8)', // Gray for neutral
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(201, 203, 207, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: type === 'doughnut' ? 'right' : 'top',
      },
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || context.parsed.y || 0;
            return `${label}: ${value.toFixed(1)}%`;
          }
        }
      }
    },
    scales: type === 'bar' ? {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        }
      }
    } : undefined,
  };

  const ChartComponent = type === 'doughnut' ? Doughnut : Bar;

  return (
    <div style={{ height: '300px', position: 'relative' }}>
      <ChartComponent data={chartData} options={options} />
      
      {/* Trend indicators */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-around', 
        marginTop: '10px',
        fontSize: '12px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            color: data.positive?.trend_direction === 'increasing' ? '#4caf50' : 
                   data.positive?.trend_direction === 'decreasing' ? '#f44336' : '#666',
            fontWeight: 'bold'
          }}>
            {data.positive?.trend_direction === 'increasing' ? ' Rising' : 
             data.positive?.trend_direction === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            color: data.negative?.trend_direction === 'increasing' ? '#f44336' : 
                   data.negative?.trend_direction === 'decreasing' ? '#4caf50' : '#666',
            fontWeight: 'bold'
          }}>
            {data.negative?.trend_direction === 'increasing' ? ' Rising' : 
             data.negative?.trend_direction === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            color: data.neutral?.trend_direction === 'increasing' ? '#4caf50' : 
                   data.neutral?.trend_direction === 'decreasing' ? '#f44336' : '#666',
            fontWeight: 'bold'
          }}>
            {data.neutral?.trend_direction === 'increasing' ? ' Rising' : 
             data.neutral?.trend_direction === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;
