import { useState } from "react";

export default function App() {
  const [zip, setZip] = useState("");
  const [loading, setLoading] = useState(false);
  const [stations, setStations] = useState([]);

  const fetchGasPrices = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `https://YOUR-BACKEND.onrender.com/api/gas?zip=${zip}`
      );
      const data = await response.json();
      setStations(data);
    } catch (error) {
      console.error("Error fetching gas prices:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h1>Find the Cheapest Gas in Your ZIP</h1>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <input
          placeholder="Enter ZIP code"
          value={zip}
          onChange={(e) => setZip(e.target.value)}
        />
        <button onClick={fetchGasPrices} disabled={!zip || loading}>
          {loading ? "Searching..." : "Find Cheapest"}
        </button>
      </div>
      <div>
        {stations.map((s, i) => (
          <div
            key={i}
            style={{
              border: "1px solid #ddd",
              padding: "1rem",
              marginBottom: "0.5rem",
            }}
          >
            <strong>{s.name}</strong>
            <div>{s.address}</div>
            <div>${s.price}</div>
            <div style={{ fontSize: "0.8rem", color: "#555" }}>
              Updated: {s.updated}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
