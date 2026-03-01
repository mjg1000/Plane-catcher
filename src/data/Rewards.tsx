import { useState } from "react";
import internalImg from "./inventory.jpg";

export default function Internal() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  const [dragging, setDragging] = useState(false);
  const [start, setStart] = useState({ x: 0, y: 0 });

  const onMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    setDragging(true);
    setStart({ x: e.clientX - pos.x, y: e.clientY - pos.y });
  };

  const onMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!dragging) return;

    const newX = e.clientX - start.x;
    const newY = e.clientY - start.y;

    // Get viewport and image dimensions
    const vw = window.innerWidth;
    const vh = window.innerHeight;

    const img = new Image();
    img.src = internalImg;
    const aspectRatio = img.width / img.height; // approximate ratio
    const imgHeight = vh;
    const imgWidth = imgHeight * aspectRatio;

    // Constrain dragging
    const maxX = 0;
    const minX = Math.min(vw - imgWidth, 0);
    const maxY = 0;
    const minY = Math.min(vh - imgHeight, 0);

    setPos({
      x: Math.max(Math.min(newX, maxX), minX),
      y: Math.max(Math.min(newY, maxY), minY),
    });
  };

  const onMouseUp = () => setDragging(false);
  const onMouseLeave = () => setDragging(false);

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
        cursor: dragging ? "grabbing" : "grab",
        backgroundColor: "#000",
        position: "relative",
      }}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      onMouseLeave={onMouseLeave}
    >
      <img
        src={internalImg}
        alt="Internal Map"
        style={{
          position: "absolute",
          top: pos.y,
          left: pos.x,
          height: "100vh",
          userSelect: "none",
          pointerEvents: "none",
        }}
        draggable={false}
      />
    </div>
  );
}