import L from "leaflet"

// Fix Leaflet default icon issue in Vite
delete (L.Icon.Default.prototype as any)._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: "",
  iconUrl: "",
  shadowUrl: ""
})

// export const planeIcon = L.icon({
//   iconUrl: "src/utils/Images/777-Emirates.png", // Replace with your image path (e.g., 'plane-icon.png' in public folder)
//   iconSize: [14*2.6, 14],                // Adjust size as needed
//   iconAnchor: [7*2.6, 7],              // Anchor at the center
//   popupAnchor: [0, -7],             // Where the popup opens relative to the anchor
// });
export const planeIcon = L.icon({
  iconUrl: "src/utils/Images/B35.png", // Replace with your image path (e.g., 'plane-icon.png' in public folder)
  iconSize: [18, 18*2.1],                // Adjust size as needed
  iconAnchor: [9, 9*2.1],              // Anchor at the center
  popupAnchor: [0, -9],             // Where the popup opens relative to the anchor
});