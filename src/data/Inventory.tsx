import { useEffect, useState } from "react";

interface Plane {
  PlaneID: string;
  Model: string;
  Airline: string;
  BeenOn: number;
}

export default function Inventory() {
  const [items, setItems] = useState<Plane[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch inventory for Player ID 1
    fetch("http://localhost:5000/inventory/1")
      .then((res) => res.json())
      .then((data) => {
        setItems(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching inventory:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: 20 }}>Loading Inventory...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>🎒 My Collection</h1>
      {items.length === 0 ? (
        <p>Your inventory is empty. Start catching planes!</p>
      ) : (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {items.map((plane) => (
            <li 
              key={plane.PlaneID} 
              style={{ 
                borderBottom: "1px solid #ccc", 
                padding: "10px 0",
                display: "flex",
                justifyContent: "space-between"
              }}
            >
              <div>
                <strong>{plane.PlaneID}</strong> - {plane.Airline} {plane.Model}
              </div>
              <span>{plane.BeenOn ? "✅ Flown" : "🔭 Spotted"}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}