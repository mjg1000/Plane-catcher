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
  const [points, setPoints] = useState<number>(0);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [currentPage, setCurrentPage] = useState<
    "map" | "inventory" | "rewards" | "internalMap"
  >("map");

  /**
   * Fetch current user points from the backend.
   * This ensures the TopNav reflects accurate point totals.
   */
  const fetchUserStats = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/user/stats");
      if (response.ok) {
        const data = await response.json();
        setPoints(data.points);
      }
    } catch (error) {
      console.error("Failed to fetch user stats:", error);
    }
  };

  // Initial data load for planes and user points
  useEffect(() => {
    getLivePlanes().then((liveData) => setPlanes(liveData));
    fetchUserStats(); 
  }, []);

  // Periodic polling to keep points in sync (every 5 seconds)
  useEffect(() => {
    const statsInterval = setInterval(fetchUserStats, 5000);
    return () => clearInterval(statsInterval);
  }, []);

  // Plane position update loop
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
  
  // Camera initialization
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

  /**
   * Captures an image and sends it to the backend for identification.
   * If a quest is completed, points are refreshed immediately.
   */
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

    try {
      const response = await fetch("http://127.0.0.1:5000/tail", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData }),
      });

      const result = await response.json();
      
      // Update points immediately if the plane was a quest target
      if (result["status"] !== "Failure") {
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
      {/* TopNav now receives 'points' and manages its own 
          internal quest list fetching. 
      */}
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