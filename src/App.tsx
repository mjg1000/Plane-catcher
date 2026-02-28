import { useState, useEffect, useRef } from "react"
import MapView from "./components/MapView"
import TopNav from "./components/TopNav"
import BottomNav from "./components/BottomNav"
import { centerCircleButton } from "./styles/navStyles"
import { Plane, GATWICK } from "./types/Plane";
import { initialPlanes } from "./data/planes";
//import {getTail} from "./utils/tailAi"

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>(initialPlanes)
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Update planes

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setPlanes(prev =>
        prev.filter(p => p.updatePosition(now, GATWICK.lat, GATWICK.lng))
      );
    }, 1000);

    return () => clearInterval(interval);
  }, []);


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
    //const tail = getTail(imageData)
    //data fetchAircraftInfo(tail)
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

      <BottomNav />
    </div>
  )
}