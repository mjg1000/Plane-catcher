import { useState, useEffect, useRef } from "react";
import MapView from "./components/MapView";
import TopNav from "./components/TopNav";
import BottomNav from "./components/BottomNav";
import { centerCircleButton } from "./styles/navStyles";
import { Plane, GATWICK } from "./types/Plane";
import { getLivePlanes } from "./data/planes";
import Inventory from "./data/Inventory";
import Rewards from "./data/Rewards";
import Internal from "./data/internalMap"; // internal map view

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>([]);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Add "internalMap" to page type
  const [currentPage, setCurrentPage] = useState<
    "map" | "inventory" | "rewards" | "internalMap"
  >("map");

  useEffect(() => {
    getLivePlanes().then((liveData) => setPlanes(liveData));
  }, []);

  // Update planes
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setPlanes((prev) => {
        const remaining = prev.filter((p) =>
          p.updatePosition(now, GATWICK.lat, GATWICK.lng)
        );
        return [...remaining];
      });
    }, 50);

    return () => clearInterval(interval);
  }, []);

  // Request webcam access
  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    }
    startCamera();
  }, []);

  // Take a snapshot
  async function handleCameraClick() {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(video, 0, 0);
    const imageData = canvas.toDataURL("image/png");
    console.log("Snapshot taken!");

    try {
      const response = await fetch("http://127.0.0.1:5000/tail", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData }),
      });

      const result = await response.json();
      console.log("Server response:", result);
      if (result["status"] != "Failure") {
        console.log(result["reward"])
      }
    } catch (err) {
      console.error("Error sending image to server:", err);
    }
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
          <video ref={videoRef} style={{ display: "none" }} autoPlay playsInline />
          <canvas ref={canvasRef} style={{ display: "none" }} />

          <button style={centerCircleButton} onClick={handleCameraClick}>
            📸
          </button>
        </>
      )}

      {currentPage === "internalMap" && <Internal />}
      {currentPage === "inventory" && <Inventory />}
      {currentPage === "rewards" && <Rewards />}

      <TopNav />
      <BottomNav setPage={setCurrentPage} currentPage={currentPage} />
    </div>
  );
}