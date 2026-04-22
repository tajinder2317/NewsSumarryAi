import React from 'react';
import { Box, CircularProgress, Typography, Paper, Fade } from '@mui/material';
import { useTheme } from '@mui/material/styles';

const Loading = ({ message = 'Loading...', size = 40, fullScreen = false }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';

  return (
    <Fade in timeout={300}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: fullScreen ? '100vh' : '200px',
          gap: 3,
          p: 3,
          ...(fullScreen && {
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            bgcolor: isDark ? 'rgba(7, 12, 20, 0.9)' : 'rgba(243, 246, 251, 0.9)',
            zIndex: 9999,
          })
        }}
      >
        <Paper
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
            borderRadius: 3,
            boxShadow: '0 12px 30px rgba(0, 0, 0, 0.28)',
            backgroundColor: isDark ? '#0e1625' : '#ffffff',
            border: isDark ? '1px solid rgba(159, 176, 200, 0.22)' : '1px solid rgba(15, 23, 42, 0.12)',
            color: isDark ? '#e7edf8' : '#0f172a',
            minWidth: 300,
          }}
        >
          <Box sx={{ position: 'relative', display: 'inline-block' }}>
            <CircularProgress
              size={size}
              sx={{
                color: isDark ? 'rgba(159, 176, 200, 0.3)' : 'rgba(15, 23, 42, 0.2)',
                '& .MuiCircularProgress-circle': {
                  strokeLinecap: 'round',
                },
              }}
            />
            <CircularProgress
              size={size}
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  color: isDark ? '#7dd3fc' : '#0f4c81',
                  animationDuration: '1s',
                  '& .MuiCircularProgress-circle': {
                    strokeLinecap: 'round',
                },
              }}
              variant="determinate"
              value={75}
            />
          </Box>
          <Typography
            variant="body1"
            sx={{
              fontWeight: 500,
              textAlign: 'center',
              opacity: 0.95
            }}
          >
            {message}
          </Typography>
        </Paper>
      </Box>
    </Fade>
  );
};

export default Loading;
