import { useState } from "react";
import { topQuestIconStyle } from "../styles/navStyles";
// Import the image
import questImg from "../data/quest.jpg"; 

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
        borderRadius: '25px',
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
        
        {/* Trigger Icon Button (Resolved from HEAD) */}
        <div
          style={{ ...topQuestIconStyle, cursor: "pointer" }}
          onClick={() => setOpen(!open)}
        >
          ✔️
        </div>

        {/* Quest Menu (Resolved from origin/temp_b) */}
        {open && (
          <div
            style={{
              position: "absolute",
              top: 50, // Positioned below the checkmark
              right: 0,
              background: "white",
              borderRadius: 12,
              boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
              padding: 20,
              minWidth: 250,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              zIndex: 1000,
            }}
          >
            {/* The Large Quest Image provided in the branch */}
            <img
              src={questImg}
              alt="Daily Quest"
              style={{
                height: "300px", 
                width: "auto",
                borderRadius: 8,
                marginBottom: "15px"
              }}
            />
            
            <div style={{ width: "100%" }}>
              <div style={{ padding: "8px 10px", cursor: "pointer", fontWeight: "bold", borderBottom: "1px solid #eee" }}>Daily Quest</div>
              <div style={{ padding: "8px 10px", cursor: "pointer" }}>Active Missions</div>
              <div style={{ padding: "8px 10px", cursor: "pointer" }}>Completed</div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}