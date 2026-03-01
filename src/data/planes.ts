import { Plane, GATWICK, CRUISE_SPEED_KMH, EARTH_RADIUS_KM } from "../types/Plane";

const API_BASE_URL = "http://127.0.0.1:5000";

// Helper to convert degrees to radians
const toRad = (deg: number) => deg * (Math.PI / 180);
// Helper to convert radians to degrees
const toDeg = (rad: number) => rad * (180 / Math.PI);

/**
 * Calculates a starting position by moving a certain distance 
 * away from a center point along a specific bearing.
 */
/**
 * Calculates a starting position by moving a certain distance 
 * away from a center point along a specific bearing.
 */
function getStartingPoint(destLat: number, destLng: number, distanceKm: number, bearingDeg: number) {
  const R = EARTH_RADIUS_KM; 
  const brng = toRad((bearingDeg + 180) % 360); // Reverse the bearing to move AWAY from Gatwick
  const d_R = distanceKm / R; // This is the angular distance
  
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
      // 1. Parse the Arrival Date from DB string (format: "D/M/YYYY")
      const [day, month, year] = p.ArrivalDate.split('/').map(Number);
      
      // 2. Create the arrival date object using minutes from midnight
      // In JS Date, months are 0-indexed (0 = Jan, 2 = March)
      const arrivalDateTime = new Date(year, month - 1, day, 0, 0, 0);
      arrivalDateTime.setMinutes(p.ArrivalTime); 
      
      // 3. Calculate duration until arrival in seconds
      const diffMs = arrivalDateTime.getTime() - now.getTime();
      const durationSeconds = diffMs / 1000;

      // If already arrived, use a tiny buffer; otherwise use the actual duration
      const travelTimeSeconds = durationSeconds > 0 ? durationSeconds : 1;

      // 4. Distance = Speed * Time (Converting speed to KM/sec)
      const travelTimeHours = travelTimeSeconds / 3600;
      const distance = CRUISE_SPEED_KMH * travelTimeHours;

      // 5. Project starting point away from Gatwick based on DB Angle
      const { lat, lng } = getStartingPoint(GATWICK.lat, GATWICK.lng, distance, p.Angle);
      let url = "../utils/images/default.png";
      let sizex = 32, sizey = 32;
      let anchx = 16, anchy = 16;

      
      if (!p.PlaneType){
        sizex = 18; sizey = 18*2.1; anchx = 9; anchy = 9*2.1;
        url = "../utils/images//B35.png";
      } else if (p.PlaneType === "B737") {
        sizex = 14*2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "TUI" 
          ? "../utils/images//737-Tui.png" 
          : "../utils/images//737-default.png";

      } else if (p.PlaneType === "B777") {
        sizex = 14*2.6; sizey = 14; anchx = 7; anchy = 7;
        if (p.Airline === "Emirates") url = "../utils/images/777-Emirates.png";
        else if (p.Airline === "TUI") url = "../utils/images//777-Tui.png";
        else url = "../utils/images/s/777-default.png";

      } else if (p.PlaneType === "A320") {
        sizex = 14*2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "EasyJet" 
          ? "../utils/images//A320-EasyJet.png" 
          : "../utils/images//A320-default.png";

      } else if (p.PlaneType === "A380") {
        sizex = 14*2.6; sizey = 14; anchx = 7; anchy = 7;
        url = p.Airline === "Emirates" 
          ? "../utils/images//A380-Emirates.png" 
          : "../utils/images//A380-default.png";
      }
      else{
        sizex = 14*2.6; sizey = 14; anchx = 7; anchy = 7;
        url = "../utils/images//SAAB.png";

      }

      // 5. Instantiate Plane with new metadata
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