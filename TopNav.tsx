import React from 'react';

interface TopNavProps {
  points: number;
}

const TopNav: React.FC<TopNavProps> = ({ points }) => {
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      left: '20px',
      zIndex: 1000, // Ensure it sits above the map
      display: 'flex',
      alignItems: 'center',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      padding: '10px 16px',
      borderRadius: '25px', // "Pill" shape for a modern look
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
      fontFamily: 'sans-serif',
      fontWeight: 'bold',
      color: '#2c3e50',
      pointerEvents: 'none' // Allows clicking the map behind it if needed
    }}>
      {/* Trophy Icon for gamification */}
      <span style={{ 
        fontSize: '1.2rem', 
        marginRight: '8px',
        display: 'flex',
        alignItems: 'center'
      }}>
        🏆
      </span>
      {/* Numeric value badge */}
      <span style={{ fontSize: '1.1rem' }}>
        {points.toLocaleString()} pts
      </span>
    </div>
  );
};

export default TopNav;