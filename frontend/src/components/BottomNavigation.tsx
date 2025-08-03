import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/mobile-navigation.css';

interface BottomNavigationProps {
  navigation: Array<{
    name: string;
    href: string;
    icon: React.ComponentType<any>;
  }>;
}

const BottomNavigation: React.FC<BottomNavigationProps> = ({ navigation }) => {
  const location = useLocation();

  return (
    <nav className="d-md-none fixed-bottom bottom-nav" style={{ zIndex: 1030 }}>
      <div className="d-flex justify-content-around align-items-center py-2 px-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`nav-link d-flex flex-column align-items-center text-decoration-none py-2 px-2 position-relative touch-target ${
                isActive ? 'active text-primary' : 'text-muted'
              }`}
              style={{ minWidth: '60px', minHeight: '50px' }}
            >
              <item.icon 
                size={20} 
                className={`nav-icon mb-1 ${isActive ? 'text-primary' : 'text-muted'}`}
              />
              <span 
                className={`nav-text ${isActive ? 'text-primary fw-medium' : 'text-muted'}`}
                style={{ 
                  fontSize: '11px', 
                  lineHeight: '1.2',
                  textAlign: 'center',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '50px'
                }}
              >
                {item.name}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNavigation; 