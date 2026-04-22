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

const getDesignTokens = (mode) => {
  const isDark = mode === 'dark';
  return {
    palette: {
      mode,
      primary: {
        main: isDark ? '#7dd3fc' : '#0f4c81',
      },
      secondary: {
        main: isDark ? '#94a3b8' : '#4b5563',
      },
      text: {
        primary: isDark ? '#e7edf8' : '#0f172a',
        secondary: isDark ? '#9fb0c8' : '#475569',
      },
      background: {
        default: isDark ? '#070c14' : '#f3f6fb',
        paper: isDark ? '#0e1625' : '#ffffff',
      },
    },
    typography: {
      fontFamily: '"Plus Jakarta Sans", "Space Grotesk", "Manrope", sans-serif',
      h4: { letterSpacing: '-0.01em' },
      h5: { letterSpacing: '-0.01em' },
      h6: { letterSpacing: '-0.01em' },
      button: {
        fontWeight: 600,
        letterSpacing: '0.01em',
        textTransform: 'none',
      },
      h1: { fontSize: '2.5rem', fontWeight: 700 },
      h2: { fontSize: '2rem', fontWeight: 700 },
      h3: { fontSize: '1.75rem', fontWeight: 700 },
    },
    shape: {
      borderRadius: 14,
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          body: {
            background: isDark ? '#070c14' : '#f3f6fb',
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            background: isDark ? 'rgba(14, 22, 37, 0.95)' : '#ffffff',
            border: isDark ? '1px solid rgba(159, 176, 200, 0.18)' : '1px solid rgba(15, 23, 42, 0.08)',
            boxShadow: isDark
              ? '0 12px 30px rgba(0, 0, 0, 0.28)'
              : '0 10px 24px rgba(15, 23, 42, 0.08)',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 12,
          },
          containedPrimary: {
            color: isDark ? '#05111d' : '#ffffff',
            background: isDark ? '#7dd3fc' : '#0f4c81',
            '&:hover': {
              background: isDark ? '#93ddfc' : '#0c3f6d',
            },
          },
          outlined: {
            borderColor: isDark ? 'rgba(159, 176, 200, 0.4)' : 'rgba(15, 23, 42, 0.2)',
            color: isDark ? '#d5dfef' : '#0f172a',
          },
        },
      },
      MuiContainer: {
        defaultProps: {
          maxWidth: 'xl',
        },
      },
    },
  };
};

function ThemedApp() {
  const [mode, setMode] = React.useState(() => localStorage.getItem('news-ui-mode') || 'dark');

  const theme = React.useMemo(() => createTheme(getDesignTokens(mode)), [mode]);

  const toggleMode = React.useCallback(() => {
    setMode((prev) => {
      const next = prev === 'dark' ? 'light' : 'dark';
      localStorage.setItem('news-ui-mode', next);
      return next;
    });
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <App mode={mode} onToggleMode={toggleMode} />
      </BrowserRouter>
    </ThemeProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemedApp />
    </QueryClientProvider>
  </React.StrictMode>
);
