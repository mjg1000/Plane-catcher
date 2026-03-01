import L from "leaflet";
import "leaflet-rotatedmarker"; // make sure this is installed via npm/yarn

// Fix default icon for Vite
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "",
  iconUrl: "",
  shadowUrl: "",
});

// Plane icon, properly centered for rotation
export const planeIcon = new L.DivIcon({
  html: "✈️",
  className: "",
  iconSize: [25, 25],
  iconAnchor: [12, 12], // center for rotation
});