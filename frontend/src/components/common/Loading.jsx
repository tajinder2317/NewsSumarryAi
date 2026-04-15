import React from 'react';
import { Box, CircularProgress, Typography, Paper, Fade } from '@mui/material';

const Loading = ({ message = 'Loading...', size = 40, fullScreen = false }) => {
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
            bgcolor: 'rgba(255, 255, 255, 0.9)',
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
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            minWidth: 300,
          }}
        >
          <Box sx={{ position: 'relative', display: 'inline-block' }}>
            <CircularProgress
              size={size}
              sx={{
                color: 'rgba(255, 255, 255, 0.3)',
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
                color: 'white',
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
