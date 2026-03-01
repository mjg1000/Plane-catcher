import { useState } from "react";
import { topQuestIconStyle } from "../styles/navStyles";

export default function TopNav() {
  const [open, setOpen] = useState(false);

  return (
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
  );
}