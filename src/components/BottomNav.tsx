import { bottomNavStyle, navButton } from "../styles/navStyles";
interface BottomNavProps {
  setPage: (page: "map" | "inventory" | "rewards") => void;
}

export default function BottomNav({ setPage }: BottomNavProps) {
  return (
    <div style={bottomNavStyle}>
      <button style={navButton} onClick={() => setPage("map")}>🗺 Map</button>
      <button style={navButton} onClick={() => setPage("inventory")}>🎒 Inventory</button>
      <button style={navButton} onClick={() => setPage("rewards")}>🏆 Rewards</button>
    </div>
  );
}