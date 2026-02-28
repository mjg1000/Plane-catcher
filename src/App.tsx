import { useState, useEffect } from "react"
import { initialPlanes } from "./data/planes"
import type { Plane } from "./types/Plane"
import MapView from "./components/MapView"
import TopNav from "./components/TopNav"
import BottomNav from "./components/BottomNav"
import { centerCircleButton } from "./styles/navStyles"

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>(initialPlanes)

  useEffect(() => {
    const interval = setInterval(() => {
      setPlanes(prev =>
        prev.map(p => ({
          ...p,
          lat: p.lat + (Math.random() - 0.5) * 0.5,
          lng: p.lng + (Math.random() - 0.5) * 0.5
        }))
      )
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div
  style={{
    position: "fixed", /* important: fixed locks to viewport */
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    overflow: "hidden" /* ensures no inner scroll */
  }}
>
  <MapView planes={planes} />
  <TopNav />
  <div style={centerCircleButton}>📸</div>
  <BottomNav />
</div>
  )
}