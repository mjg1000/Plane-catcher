import { useState, useEffect } from "react";
import { topQuestIconStyle } from "../styles/navStyles";
import questImg from "../data/quest.jpg"; 

interface Quest {
  PlaneID: string;
  Airline: string;
  Model: string;
  Reward: number;
}

interface TopNavProps {
  points: number;
}

export default function TopNav({ points }: TopNavProps) {
  const [open, setOpen] = useState(false);
  const [quests, setQuests] = useState<Quest[]>([]);

  // Fetch quests specifically for User 1 when the dropdown opens
  useEffect(() => {
    if (open) {
      fetch("http://127.0.0.1:5000/quests/1")
        .then((res) => {
          if (!res.ok) throw new Error("Server error");
          return res.json();
        })
        .then((data) => setQuests(data))
        .catch((err) => console.error("Error fetching quests:", err));
    }
  }, [open]);

  return (
    <>
      {/* Points Display */}
      <div style={{
        position: 'absolute', top: 20, left: 20, zIndex: 1000,
        display: 'flex', alignItems: 'center', backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: '10px 16px', borderRadius: '25px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        fontFamily: 'sans-serif', fontWeight: 'bold', color: '#2c3e50'
      }}>
        <span style={{ fontSize: '1.2rem', marginRight: '8px' }}>🏆</span>
        <span>{points.toLocaleString()} pts</span>
      </div>

      {/* Quest Dropdown */}
      <div style={{ position: "absolute", top: 20, right: 20, zIndex: 1000 }}>
        <div
          style={{ ...topQuestIconStyle, cursor: "pointer" }}
          onClick={() => setOpen(!open)}
        >
          ✔️
        </div>

        {open && (
          <div style={{
            position: "absolute", top: 50, right: 0, background: "white",
            borderRadius: 12, boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            padding: "15px", minWidth: 280, zIndex: 1000,
          }}>
            <h4 style={{ margin: "0 0 10px 0", textAlign: "center" }}>Active Quests</h4>
            
            <div style={{ maxHeight: "200px", overflowY: "auto", marginBottom: "15px" }}>
              {quests.length === 0 ? (
                <p style={{ fontSize: "0.9rem", color: "#666", textAlign: "center" }}>No quests available</p>
              ) : (
                quests.map((q) => (
                  <div key={q.PlaneID} style={{ 
                    padding: "8px", borderBottom: "1px solid #eee", fontSize: "0.9rem",
                    display: "flex", justifyContent: "space-between" 
                  }}>
                    <span><strong>{q.PlaneID}</strong><br/>{q.Airline}</span>
                    <span style={{ color: "green", fontWeight: "bold" }}>+{q.Reward}</span>
                  </div>
                ))
              )}
            </div>

            <img
              src={questImg}
              alt="Daily Quest"
              style={{ width: "100%", borderRadius: 8 }}
            />
          </div>
        )}
      </div>
    </>
  );
}