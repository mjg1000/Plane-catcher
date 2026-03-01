import { bottomNavStyle, navButton } from "../styles/navStyles";

interface BottomNavProps {
  setPage: (page: "map" | "inventory" | "rewards" | "internalMap") => void;
  currentPage: "map" | "inventory" | "rewards" | "internalMap";
}

export default function BottomNav({ setPage, currentPage }: BottomNavProps) {
  const handleMapClick = () => {
    if (currentPage === "map") {
      // Switch to internal map
      setPage("internalMap");
    } else {
      // Go to map page
      setPage("map");
    }
  };

  return (
    <div style={bottomNavStyle}>
      <button style={navButton} onClick={handleMapClick}>
        🗺 Map
      </button>
      <button style={navButton} onClick={() => setPage("inventory")}>
        🎒 Inventory
      </button>
      <button style={navButton} onClick={() => setPage("rewards")}>
        🏆 Rewards
      </button>
    </div>
  );
}