import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';
import './index.css';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Create Material-UI theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#7dd3fc',
    },
    secondary: {
      main: '#94a3b8',
    },
    text: {
      primary: '#e7edf8',
      secondary: '#9fb0c8',
    },
    background: {
      default: '#070c14',
      paper: '#0e1625',
    },
  },
  typography: {
    fontFamily: '"Plus Jakarta Sans", "Space Grotesk", "Manrope", sans-serif',
    h4: {
      letterSpacing: '-0.01em',
    },
    h5: {
      letterSpacing: '-0.01em',
    },
    h6: {
      letterSpacing: '-0.01em',
    },
    button: {
      fontWeight: 600,
      letterSpacing: '0.01em',
      textTransform: 'none',
    },
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 700,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 700,
    },
  },
  shape: {
    borderRadius: 14,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background:
            'radial-gradient(circle at 10% 0%, rgba(125, 211, 252, 0.08), transparent 32%), radial-gradient(circle at 90% 100%, rgba(148, 163, 184, 0.08), transparent 30%), #070c14',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(180deg, rgba(16, 24, 38, 0.95), rgba(12, 19, 31, 0.95))',
          border: '1px solid rgba(159, 176, 200, 0.18)',
          boxShadow: '0 12px 30px rgba(0, 0, 0, 0.28)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
        containedPrimary: {
          color: '#05111d',
          background: 'linear-gradient(135deg, #7dd3fc, #67b8e4)',
          '&:hover': {
            background: 'linear-gradient(135deg, #8ad8fc, #74bee6)',
          },
        },
        outlined: {
          borderColor: 'rgba(159, 176, 200, 0.4)',
          color: '#d5dfef',
        },
      },
    },
    MuiContainer: {
      defaultProps: {
        maxWidth: 'xl',
      },
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
