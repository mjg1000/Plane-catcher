export const GATWICK = { lat: 51.1537, lng: -0.1821 };
export const EARTH_RADIUS_KM = 6371;
export const CRUISE_SPEED_KMH = 900;
export const MAX_DISTANCE_KM = 160.93; // 100 miles

// Helpers
function toRad(deg: number) { return deg * (Math.PI / 180); }
function toDeg(rad: number) { return rad * (180 / Math.PI); }

export function calculateBearing(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const φ1 = toRad(lat1);
  const φ2 = toRad(lat2);
  const Δλ = toRad(lon2 - lon1);
  const y = Math.sin(Δλ) * Math.cos(φ2);
  const x = Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
  return (toDeg(Math.atan2(y, x)) + 360) % 360;
}

export function generatePointWithinRadius(centerLat: number, centerLng: number, maxDistanceKm: number) {
  const distance = Math.sqrt(Math.random()) * maxDistanceKm;
  const bearing = Math.random() * 2 * Math.PI;
  const lat1 = toRad(centerLat);
  const lng1 = toRad(centerLng);
  const angularDistance = distance / EARTH_RADIUS_KM;

  const lat2 = Math.asin(
    Math.sin(lat1) * Math.cos(angularDistance) +
    Math.cos(lat1) * Math.sin(angularDistance) * Math.cos(bearing)
  );

  const lng2 = lng1 + Math.atan2(
    Math.sin(bearing) * Math.sin(angularDistance) * Math.cos(lat1),
    Math.cos(angularDistance) - Math.sin(lat1) * Math.sin(lat2)
  );

  return { lat: toDeg(lat2), lng: toDeg(lng2), distance };
}

// Plane class
export class Plane {
  tail: string;
  startLat: number;
  startLng: number;
  lat: number;
  lng: number;
  dest: string;
  arrivalDurationSeconds: number; // Coherent: Total travel time in seconds
  angle: number;
  spawnedAt: number;
  arrivedAt: number | null;

  constructor(tail: string, lat: number, lng: number, dest: string, arrivalDurationSeconds: number, angle: number) {
    this.tail = tail;
    this.startLat = lat;
    this.startLng = lng;
    this.lat = lat;
    this.lng = lng;
    this.dest = dest;
    this.arrivalDurationSeconds = arrivalDurationSeconds; //
    this.angle = angle;
    this.spawnedAt = Date.now();
    this.arrivedAt = null;
  }

  // Returns true if plane should remain in state
  updatePosition(now: number, destLat: number, destLng: number): boolean {
    const elapsedSeconds = (now - this.spawnedAt) / 1000; //

    if (elapsedSeconds < this.arrivalDurationSeconds) {
      const progress = elapsedSeconds / this.arrivalDurationSeconds;
      this.lat = this.startLat + (destLat - this.startLat) * progress;
      this.lng = this.startLng + (destLng - this.startLng) * progress;
      return true;
    }

    if (!this.arrivedAt) {
      this.lat = destLat;
      this.lng = destLng;
      this.arrivedAt = now;
      return true;
    }

    const timeSinceArrival = (now - this.arrivedAt) / 1000;
    return timeSinceArrival < 10;
  }

  async fetchMetadata(): Promise<any> {
    try {
      // Extract numerical ID from 'DB1234' format
      const tailId = this.tail.replace('DB', ''); 
      const response = await fetch(`http://127.0.0.1:5000/plane/${tailId}`);
      return await response.json();
    } catch (error) {
      console.error("fetchMetadata error:", error);
      throw error;
    }
  }
}