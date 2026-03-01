import { Plane, GATWICK, generatePointWithinRadius, calculateBearing, CRUISE_SPEED_KMH, MAX_DISTANCE_KM } from "../types/Plane";

let planeCounter = 1; // unique tail counter

export function respawnPlane(): Plane {
  const { lat, lng, distance } = generatePointWithinRadius(GATWICK.lat, GATWICK.lng, MAX_DISTANCE_KM);
  const arrivalTime = Number((distance / CRUISE_SPEED_KMH).toFixed(2));
  const tail = `SIM${10000 + planeCounter}`; // generate a unique tail
  const angle = calculateBearing(lat, lng, GATWICK.lat, GATWICK.lng);
  planeCounter++;
  return new Plane(tail, lat, lng, "LGW", arrivalTime, angle);
}