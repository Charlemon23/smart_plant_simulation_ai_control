// =====================================
// Global configuration for API endpoints
// =====================================

export const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const WS_URL = BACKEND_URL.replace("https", "wss") + "/ws/telemetry";

export const API = {
  health: `${BACKEND_URL}/api/v1/health`,
  config: `${BACKEND_URL}/api/v1/config`,
  setpoints: `${BACKEND_URL}/api/v1/setpoints`,
  controlTick: `${BACKEND_URL}/api/v1/control/tick`,
};

// Optional: log at build time for debugging
console.log("Backend:", BACKEND_URL);
console.log("WebSocket:", WS_URL);
