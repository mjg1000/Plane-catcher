import { useState } from "react";
import { topQuestIconStyle } from "../styles/navStyles";

// Added interface for points prop
interface TopNavProps {
  points: number;
}

export default function TopNav({ points }: TopNavProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* --- Points Display (Top Left) --- */}
      <div style={{
        position: 'absolute',
        top: 20,
        left: 20,
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: '10px 16px',
        borderRadius: '25px', // Pill shape
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: '#2c3e50'
      }}>
        <span style={{ fontSize: '1.2rem', marginRight: '8px' }}>🏆</span>
        <span>{points.toLocaleString()} pts</span>
      </div>

      {/* --- Quest Dropdown (Top Right) --- */}
      <div style={{ position: "absolute", top: 20, right: 20, zIndex: 1000 }}>
        {/* Icon button */}
        <div
          style={{ ...topQuestIconStyle, cursor: "pointer" }}
          onClick={() => setOpen(!open)}
        >
          ✔️
        </div>

        {/* Dropdown */}
        {open && (
          <div
            style={{
              position: "absolute",
              top: 40, // slightly below the icon
              right: 0,
              background: "white",
              borderRadius: 8,
              boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
              padding: 10,
              minWidth: 150,
              zIndex: 1000,
            }}
          >
            <div style={{ padding: "5px 10px", cursor: "pointer" }}>Daily Quest</div>
            <div style={{ padding: "5px 10px", cursor: "pointer" }}>Active Missions</div>
            <div style={{ padding: "5px 10px", cursor: "pointer" }}>Completed</div>
          </div>
        )}
      </div>
    </>
  );
}