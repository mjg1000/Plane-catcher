import L from "leaflet"

// Fix Leaflet default icon issue in Vite
delete (L.Icon.Default.prototype as any)._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: "",
  iconUrl: "",
  shadowUrl: ""
})

export const planeIcon = new L.DivIcon({
  html: "✈️",
  className: "",
  iconSize: [25, 25]
})