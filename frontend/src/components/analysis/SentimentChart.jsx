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

  const getPercentage = (key) => {
    const value = data?.[key];

    // Trends endpoint shape: { positive: { current_percentage, trend_direction, ... }, ... }
    if (value && typeof value === 'object' && typeof value.current_percentage === 'number') {
      return value.current_percentage;
    }

    // Analysis endpoint shape: { positive: 0.6, negative: 0.1, neutral: 0.3, ... }
    if (typeof value === 'number') {
      return value <= 1 ? value * 100 : value;
    }

    return 0;
  };

  const getTrendDirection = (key) => {
    const value = data?.[key];
    return value && typeof value === 'object' ? value.trend_direction : undefined;
  };

  
  const chartData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        label: 'Sentiment Distribution',
        data: [
          getPercentage('positive'),
          getPercentage('negative'),
          getPercentage('neutral'),
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
            color: getTrendDirection('positive') === 'increasing' ? '#4caf50' : 
                   getTrendDirection('positive') === 'decreasing' ? '#f44336' : '#666',
            fontWeight: 'bold'
          }}>
            {getTrendDirection('positive') === 'increasing' ? ' Rising' : 
             getTrendDirection('positive') === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            color: getTrendDirection('negative') === 'increasing' ? '#f44336' : 
                   getTrendDirection('negative') === 'decreasing' ? '#4caf50' : '#666',
            fontWeight: 'bold'
          }}>
            {getTrendDirection('negative') === 'increasing' ? ' Rising' : 
             getTrendDirection('negative') === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ 
            color: getTrendDirection('neutral') === 'increasing' ? '#4caf50' : 
                   getTrendDirection('neutral') === 'decreasing' ? '#f44336' : '#666',
            fontWeight: 'bold'
          }}>
            {getTrendDirection('neutral') === 'increasing' ? ' Rising' : 
             getTrendDirection('neutral') === 'decreasing' ? ' Falling' : ' Stable'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;
