import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Tooltip,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home,
  Dashboard,
  Analytics,
  Search,
  Article,
  DarkMode,
  LightMode,
} from '@mui/icons-material';

const Header = ({ mode = 'dark', onToggleMode = () => {} }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavigation = (path) => {
    navigate(path);
    handleMenuClose();
  };

  const menuItems = [
    { label: 'Home', path: '/', icon: <Home /> },
    { label: 'News', path: '/news', icon: <Article /> },
    { label: 'Dashboard', path: '/dashboard', icon: <Dashboard /> },
    { label: 'Analysis', path: '/analysis', icon: <Analytics /> },
    { label: 'Search', path: '/search', icon: <Search /> },
  ];

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        backgroundColor: isDark ? 'rgba(10, 16, 28, 0.94)' : 'rgba(255, 255, 255, 0.92)',
        borderBottom: isDark
          ? '1px solid rgba(159, 176, 200, 0.2)'
          : '1px solid rgba(15, 23, 42, 0.12)',
        color: isDark ? '#e7edf8' : '#0f172a',
        backdropFilter: 'blur(10px)',
        boxShadow: 'none',
      }}
    >
      <Toolbar
        sx={{
          py: { xs: 0.5, md: 1 },
          px: { xs: 1, sm: 2 },
          minHeight: { xs: 56, sm: 64 },
        }}
      >
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            cursor: 'pointer',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            fontSize: { xs: '1rem', sm: '1.15rem' },
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            '&:hover': {
              transform: 'scale(1.02)',
              transition: 'transform 0.2s ease'
            }
          }}
          onClick={() => navigate('/')}
        >
          News Analyzer AI
        </Typography>

        <Tooltip title={mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
          <IconButton
            onClick={onToggleMode}
            color="inherit"
            sx={{
              mr: { xs: 0.5, md: 1 },
              border: isDark ? '1px solid rgba(159, 176, 200, 0.35)' : '1px solid rgba(15, 23, 42, 0.2)',
            }}
          >
            {mode === 'dark' ? <LightMode fontSize="small" /> : <DarkMode fontSize="small" />}
          </IconButton>
        </Tooltip>

        {/* Desktop Navigation */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
          {menuItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              variant={location.pathname === item.path ? 'outlined' : 'text'}
              sx={{
                borderColor: 'rgba(159, 176, 200, 0.4)',
                borderRadius: 2,
                px: 2,
                py: 1,
                fontWeight: 500,
                textTransform: 'none',
                transition: 'all 0.3s ease',
                '&:hover': {
                  backgroundColor: 'rgba(125, 211, 252, 0.12)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 10px 20px rgba(0, 0, 0, 0.24)'
                },
                ...(location.pathname === item.path && {
                  backgroundColor: 'rgba(125, 211, 252, 0.18)',
                  borderColor: 'rgba(125, 211, 252, 0.55)',
                  '&:hover': {
                    backgroundColor: 'rgba(125, 211, 252, 0.22)',
                  }
                })
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        {/* Mobile Navigation */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
            sx={{
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.15)',
                transform: 'rotate(90deg)'
              }
            }}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            sx={{
              display: { xs: 'block', md: 'none' },
              '& .MuiPaper-root': {
                backgroundColor: isDark ? '#0e1625' : '#ffffff',
                color: isDark ? '#e7edf8' : '#0f172a',
                minWidth: 200,
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
                borderRadius: 2.5,
                border: isDark ? '1px solid rgba(159, 176, 200, 0.25)' : '1px solid rgba(15, 23, 42, 0.14)',
                mt: 1
              }
            }}
          >
            {menuItems.map((item) => (
              <MenuItem
                key={item.path}
                onClick={() => handleNavigation(item.path)}
                selected={location.pathname === item.path}
                sx={{
                  color: isDark ? '#e7edf8' : '#0f172a',
                  fontWeight: 500,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: 'rgba(125, 211, 252, 0.12)',
                    transform: 'translateX(4px)'
                  },
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(125, 211, 252, 0.16)',
                    '&:hover': {
                      backgroundColor: 'rgba(125, 211, 252, 0.2)'
                    }
                  }
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box sx={{ color: 'inherit' }}>
                    {item.icon}
                  </Box>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    {item.label}
                  </Typography>
                </Box>
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
