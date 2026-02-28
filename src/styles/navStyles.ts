import React from "react"

export const topQuestIconStyle: React.CSSProperties = {
  position: "absolute",
  top: 15,
  right: 15,
  zIndex: 1000,
  width: 40,
  height: 40,
  borderRadius: "50%",
  background: "gold",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  fontSize: "22px",
  cursor: "pointer",
  boxShadow: "0 0 8px rgba(0,0,0,0.5)"
}

export const bottomNavStyle: React.CSSProperties = {
  position: "absolute",
  bottom: 0,
  width: "100%",
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  padding: "10px 0",
  background: "rgba(0,0,0,0.6)",
  backdropFilter: "blur(6px)",
  zIndex: 1000
}

export const navButton: React.CSSProperties = {
  background: "transparent",
  border: "none",
  color: "white",
  fontSize: "18px",
  cursor: "pointer"
}

export const centerCircleButton: React.CSSProperties = {
  position: "absolute",
  bottom: 60, // above bottom nav
  left: "50%",
  transform: "translateX(-50%)",
  width: 60,
  height: 60,
  borderRadius: "50%",
  background: "gold",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  fontSize: "24px",
  cursor: "pointer",
  zIndex: 1000,
  boxShadow: "0 0 10px rgba(0,0,0,0.5)"
}