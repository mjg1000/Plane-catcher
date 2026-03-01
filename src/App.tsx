import { useState, useEffect, useRef } from "react"
import MapView from "./components/MapView"
import TopNav from "./components/TopNav"
import BottomNav from "./components/BottomNav"
import { centerCircleButton } from "./styles/navStyles"
import { Plane, GATWICK } from "./types/Plane";
import { getLivePlanes } from "./data/planes";
//import {getTail} from "./utils/tailAi"
import Inventory from "./data/Inventory";
import Rewards from "./data/Rewards";

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>([]);
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [currentPage, setCurrentPage] = useState<"map" | "inventory" | "rewards">("map");

  useEffect(() => {
    getLivePlanes().then(liveData => setPlanes(liveData));
  }, []);

  // Update planes

    useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setPlanes(prev => {
        // 1. Filter out planes that have finished their journey
        const remaining = prev.filter(p => p.updatePosition(now, GATWICK.lat, GATWICK.lng));
        
        // 2. Return a NEW array reference so React re-renders the markers
        return [...remaining]; 
      });
    }, 50);

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
  async function handleCameraClick() {
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

    try {
      // 2. Send to Flask server
      const response = await fetch("http://127.0.0.1:5000/tail", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageData }),
      });

      const result = await response.json();
      console.log("Server response:", result);
      
      // You could then do something with result.tail_no
    } catch (err) {
      console.error("Error sending image to server:", err);
    }
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
    {/* Render the main content depending on current page */}
    {currentPage === "map" && (
      <>
        <MapView planes={planes} />
        {/* Hidden video & canvas for capture */}
        <video ref={videoRef} style={{ display: "none" }} autoPlay playsInline />
        <canvas ref={canvasRef} style={{ display: "none" }} />

        {/* Camera button */}
        <button style={centerCircleButton} onClick={handleCameraClick}>
          📸
        </button>
      </>
    )}

    {currentPage === "inventory" && <Inventory />}
    {currentPage === "rewards" && <Rewards />}

    <TopNav />
    <BottomNav setPage={setCurrentPage} />
  </div>
);
}