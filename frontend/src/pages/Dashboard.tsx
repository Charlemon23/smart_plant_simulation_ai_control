import React, { useEffect, useRef, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { WS_URL, API } from "../config";

// =============================================
// Type definitions for telemetry data structure
// =============================================
type Telemetry = {
  ts: number;
  temperature: number;
  pressure: number;
  flow: number;
  composition: number;
  temperature_sp: number;
  pressure_sp: number;
  reflux_ratio: number;
  feed_rate: number;
};

// =============================================
// Main dashboard component
// =============================================
export function Dashboard() {
  const [data, setData] = useState<Telemetry[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  // --- WebSocket live telemetry connection ---
  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => console.log("✅ Connected to WebSocket:", WS_URL);
    ws.onerror = (err) => console.error("WebSocket error:", err);

    ws.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data) as Telemetry;
        setData((d) => {
          const next = [...d, msg];
          return next.slice(-400); // keep last 400 samples
        });
      } catch (err) {
        console.error("WebSocket message error:", err);
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  // --- Health check example using REST API ---
  useEffect(() => {
    fetch(API.health)
      .then((r) => r.json())
      .then((res) => console.log("Backend health:", res))
      .catch(console.error);
  }, []);

  // --- Render charts ---
  return (
    <div
      style={{
        padding: 24,
        fontFamily: "Inter, system-ui, sans-serif",
        background: "#f9fafb",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ fontSize: "1.8rem", marginBottom: 16 }}>
        Smart Plant — Live Telemetry
      </h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Chart title="Temperature" data={data} dataKey="temperature" />
        <Chart title="Pressure" data={data} dataKey="pressure" />
        <Chart title="Flow" data={data} dataKey="flow" />
        <Chart t
