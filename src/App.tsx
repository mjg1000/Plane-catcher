import { useState, useEffect, useRef } from "react";
import MapView from "./components/MapView";
import TopNav from "./components/TopNav";
import BottomNav from "./components/BottomNav";
import { centerCircleButton } from "./styles/navStyles";
import { Plane, GATWICK } from "./types/Plane";
import { getLivePlanes } from "./data/planes";
import Inventory from "./data/Inventory";
import Rewards from "./data/Rewards";
import Internal from "./data/internalMap";

export default function App() {
  const [planes, setPlanes] = useState<Plane[]>([]);
  const [points, setPoints] = useState<number>(0); // Added points state
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [currentPage, setCurrentPage] = useState<
    "map" | "inventory" | "rewards" | "internalMap"
  >("map");

  // Function to fetch points from the backend
  const fetchUserStats = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/user/stats");
      if (response.ok) {
        const data = await response.json();
        console.log(data.points)
        setPoints(data.points);
      }
    } catch (error) {
      console.error("Failed to fetch user stats:", error);
    }
  };

  // Initial data load
  useEffect(() => {
    getLivePlanes().then((liveData) => setPlanes(liveData));
    fetchUserStats(); // Initial points fetch
  }, []);

  // Polling to keep points in sync
  useEffect(() => {
    const statsInterval = setInterval(fetchUserStats, 5000);
    return () => clearInterval(statsInterval);
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
      
      // If identification succeeded, refresh points immediately
      if (result["status"] !== "Failure") {
        console.log("Reward earned:", result["reward"]);
        fetchUserStats(); 
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
      {/* Pass the points state to TopNav */}
      <TopNav points={points} />

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

      <BottomNav setPage={setCurrentPage} currentPage={currentPage} />
    </div>
  );
}