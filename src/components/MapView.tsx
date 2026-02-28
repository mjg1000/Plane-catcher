import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet"
import type { Plane } from "../types/Plane"
import { planeIcon } from "../utils/leafletSetup"

type Props = {
  planes: Plane[]
}

export default function MapView({ planes }: Props) {
  return (
    <MapContainer
      center={[20, 0] as [number, number]}
      zoom={2}
      style={{ height: "100%", width: "100%" }}
      zoomControl={false}
    >
      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />

      {planes.map(plane => (
        <Marker
          key={plane.tail}
          position={[plane.lat, plane.lng]}
          icon={planeIcon}
        >
          <Popup>
            <strong>{plane.tail}</strong>
            <br />
            Destination: {plane.dest}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}