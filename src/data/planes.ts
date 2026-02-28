import { Plane, GATWICK, calculateBearing, generatePointWithinRadius } from "../types/Plane";

export const initialPlanes: Plane[] = Array.from({ length: 60 }).map((_, i) => {
  const { lat, lng, distance } = generatePointWithinRadius(GATWICK.lat, GATWICK.lng, 160.93);
  const arrivalTime = Number((distance / 900).toFixed(2)); // hours
  const angle = calculateBearing(lat, lng, GATWICK.lat, GATWICK.lng);
  return new Plane(`SIM${10000 + i}`, lat, lng, "LGW", arrivalTime, angle);
});