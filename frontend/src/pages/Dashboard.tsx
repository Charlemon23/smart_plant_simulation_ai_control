import React, { useEffect, useRef, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

type Telemetry = {
  ts: number
  temperature: number
  pressure: number
  flow: number
  composition: number
  temperature_sp: number
  pressure_sp: number
  reflux_ratio: number
  feed_rate: number
}

const WS_URL = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws/telemetry'

export function Dashboard() {
  const [data, setData] = useState<Telemetry[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(WS_URL)
    wsRef.current = ws
    ws.onmessage = (evt) => {
      const msg = JSON.parse(evt.data) as Telemetry
      setData(d => {
        const next = [...d, msg]
        return next.slice(-400)
      })
    }
    return () => ws.close()
  }, [])

  return (
    <div style={{ padding: 24, fontFamily: 'Inter, system-ui, sans-serif' }}>
      <h1>Smart Plant — Live Telemetry</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <Chart title="Temperature" data={data} dataKey="temperature" />
        <Chart title="Pressure" data={data} dataKey="pressure" />
        <Chart title="Flow" data={data} dataKey="flow" />
        <Chart title="Composition" data={data} dataKey="composition" />
      </div>
    </div>
  )
}

function Chart({ title, data, dataKey }: { title: string, data: Telemetry[], dataKey: keyof Telemetry }) {
  return (
    <div style={{ background: '#fff', padding: 16, borderRadius: 12, boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
      <h3>{title}</h3>
      <LineChart width={600} height={260} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="ts" tickFormatter={(t) => new Date(t * 1000).toLocaleTimeString()} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey={dataKey as string} dot={false} />
      </LineChart>
    </div>
  )
}
