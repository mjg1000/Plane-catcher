import { Plane, GATWICK, CRUISE_SPEED_KMH, EARTH_RADIUS_KM } from "../types/Plane";

const API_BASE_URL = "http://127.0.0.1:5000";

const toRad = (deg: number) => deg * (Math.PI / 180);
const toDeg = (rad: number) => rad * (180 / Math.PI);

function getStartingPoint(destLat: number, destLng: number, distanceKm: number, bearingDeg: number) {
  const R = EARTH_RADIUS_KM; 
  const brng = toRad((bearingDeg + 180) % 360); 
  const d_R = distanceKm / R; 
  
  const lat1 = toRad(destLat);
  const lon1 = toRad(destLng);

  const lat2 = Math.asin(
    Math.sin(lat1) * Math.cos(d_R) +
    Math.cos(lat1) * Math.sin(d_R) * Math.cos(brng)
  );

  const lon2 = lon1 + Math.atan2(
    Math.sin(brng) * Math.sin(d_R) * Math.cos(lat1),
    Math.cos(d_R) - Math.sin(lat1) * Math.sin(lat2)
  );

  return { lat: toDeg(lat2), lng: toDeg(lon2) };
}

export async function getLivePlanes(): Promise<Plane[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/planes`);
    if (!response.ok) return [];
    const data = await response.json();

    const now = new Date();

    return data.map((p: any) => {
      const [day, month, year] = p.ArrivalDate.split('/').map(Number);
      const arrivalDateTime = new Date(year, month - 1, day, 0, 0, 0);
      arrivalDateTime.setMinutes(p.ArrivalTime); 
      
      const diffMs = arrivalDateTime.getTime() - now.getTime();
      const durationSeconds = diffMs / 1000;
      const travelTimeSeconds = durationSeconds > 0 ? durationSeconds : 1;

      const travelTimeHours = travelTimeSeconds / 3600;
      const distance = CRUISE_SPEED_KMH * travelTimeHours;

      const { lat, lng } = getStartingPoint(GATWICK.lat, GATWICK.lng, distance, p.Angle);
      
      // Corrected: Absolute paths relative to the 'public' folder
      let url = "/images/planes/737-default.png"; 
      let sizex = 32, sizey = 32;
      let anchx = 16, anchy = 16;
      
      console.log(p.PlaneModel)
      if (!p.PlaneModel) { // Checking PlaneModel from your DB schema
        sizex = 18; sizey = 18 * 2.1; anchx = 9; anchy = 9 * 2.1;
        url = "/images/planes/B35.png";
      } else if (p.PlaneModel === "B737") {
        sizex = 14 * 2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "TUI" 
          ? "/images/planes/737-Tui.png" 
          : "/images/planes/737-default.png";

      } else if (p.PlaneModel === "B777") {
        sizex = 14 * 2.6; sizey = 14; anchx = 7; anchy = 7;
        if (p.Airline === "Emirates") url = "/images/planes/777-Emirates.png";
        else if (p.Airline === "TUI") url = "/images/planes/777-Tui.png";
        else url = "/images/planes/777-default.png";

      } else if (p.PlaneModel === "A320") {
        sizex = 14 * 2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "EasyJet" 
          ? "/images/planes/A320-EasyJet.png" 
          : "/images/planes/A320-default.png";

      } else if (p.PlaneModel === "A380") {
        sizex = 14 * 2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "Emirates" 
          ? "/images/planes/A380-Emirates.png" 
          : "/images/planes/A380-default.png";
      } else {
        sizex = 14 * 2.6; sizey = 14; anchx = 7; anchy = 7;
        url = "/images/planes/B35.png";
      }

      return new Plane(
        `DB${p.PlaneID}`,
        lat,
        lng,
        "LGW",
        travelTimeSeconds,
        p.Angle,
        url,
        sizex, 
        sizey,
        anchx,
        anchy
      );
    });
  } catch (error) {
    console.error("Server connection failed", error);
    return [];
  }
}