import { useState } from "react"
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet"
import type { Plane } from "../types/Plane"
import { planeIcon } from "../utils/leafletSetup"

type Props = {
  planes: Plane[]
}

function PlanePopup({ plane }: { plane: Plane }) {
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleOpen = async () => {
    // Prevent re-fetching if we already have data
    if (details || loading) return;

    setLoading(true);
    setError(null);
    try {
      // This calls the method you added to your Plane class
      const data = await plane.fetchMetadata(); 
      setDetails(data);
    } catch (err) {
      console.error("Popup fetch error:", err);
      setError("Failed to load plane data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Popup eventHandlers={{ add: handleOpen }}>
      <div style={{ minWidth: "150px", color: "black" }}>
        {/* Changed from plane.id to plane.tail to match your class */}
        <strong>Tail No: {plane.tail}</strong><br />
        <hr />
        {loading && <div>Loading details...</div>}
        {error && <div style={{ color: 'red' }}>{error}</div>}
        {details && (
          <pre style={{ 
            fontSize: '10px', 
            maxHeight: '200px', 
            overflowY: 'auto',
            backgroundColor: '#eee',
            padding: '5px' 
          }}>
            {JSON.stringify(details, null, 2)}
          </pre>
        )}
      </div>
    </Popup>
  );
}

export default function MapView({ planes }: Props) {
  return (
    <MapContainer
      center={[51.1537, -0.1821] as [number, number]} 
      zoom={8}
      style={{ height: "100%", width: "100%" }}
      zoomControl={false}
    >
      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />

      {planes.map(p => (
        <Marker
          key={p.tail} // Changed from p.id to p.tail
          position={[p.lat, p.lng]}
          icon={planeIcon}
          rotationAngle={p.angle - 30} // This property actually rotates the icon
          rotationOrigin="center"
        >
          <PlanePopup plane={p} />
        </Marker>
      ))}
    </MapContainer>
  )
}