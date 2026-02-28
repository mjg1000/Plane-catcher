import { bottomNavStyle, navButton } from "../styles/navStyles"

export default function BottomNav() {
  return (
    <div style={bottomNavStyle}>
      <button style={navButton}>🗺 Map</button>
      <button style={navButton}>🎒 Inventory</button>
      <button style={navButton}>🏆 Awards</button>
    </div>
  )
}