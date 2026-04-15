import React from 'react';
import { Box, Typography, Container, Link } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          {'© '}
          {new Date().getFullYear()}
          {' News Analyzer AI. Built with React & FastAPI. '}
          <Link color="inherit" href="https://github.com" target="_blank" rel="noopener">
            View on GitHub
          </Link>
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          AI-powered news analysis and summarization platform
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
