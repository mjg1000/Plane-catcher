import { useState, useEffect, useRef } from "react"
import { initialPlanes } from "./data/planes"
import type { Plane } from "./types/Plane"
import MapView from "./components/MapView"
import TopNav from "./components/TopNav"
import BottomNav from "./components/BottomNav"
import { centerCircleButton } from "./styles/navStyles"

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>(initialPlanes)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [photo] = useState<string | null>(null)

  // Update planes every 3 seconds
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

  // Request webcam access
  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        if (videoRef.current) videoRef.current.srcObject = stream
      } catch (err) {
        console.error("Error accessing camera:", err)
      }
    }
    startCamera()
  }, [])

  // Take a snapshot UNTESTED MEED WEBCAM
  function handleCameraClick() {
    if (!videoRef.current || !canvasRef.current) return
    const video = videoRef.current
    const canvas = canvasRef.current
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    ctx.drawImage(video, 0, 0)
    const imageData = canvas.toDataURL("image/png")
    console.log("Snapshot taken!")
    return imageData
  }

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <MapView planes={planes} />
      <TopNav />

      {/* Hidden video & canvas for capture */}
      <video ref={videoRef} style={{ display: "none" }} autoPlay playsInline />
      <canvas ref={canvasRef} style={{ display: "none" }} />

      {/* Camera button */}
      <button style={centerCircleButton} onClick={handleCameraClick}>
        📸
      </button>

      {/* Display captured photo */}
      {photo && (
        <img
          src={photo}
          alt="Snapshot"
          style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            width: "200px",
            border: "2px solid white",
            borderRadius: "8px",
          }}
        />
      )}

      <BottomNav />
    </div>
  )
}