import { useState } from "react";
import { topQuestIconStyle } from "../styles/navStyles";
// Import the image
import questImg from "../data/quest.jpg"; // adjust the path if different

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
            top: 40,
            right: 0,
            background: "white",
            borderRadius: 12,
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            padding: 20,
            minWidth: 250,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          {/* Large image */}
          <img
            src={questImg}
            alt="Daily Quest"
            style={{
              height: "400px", // make it much bigger
              width: "auto",
              cursor: "pointer",
              borderRadius: 8,
            }}
          />
        </div>
      )}
    </div>
  );
}