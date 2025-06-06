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
      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="zip-input" style={{ marginBottom: "0.25rem", display: "block" }}>
          Enter your U.S. ZIP code
        </label>
        <input
          id="zip-input"
          placeholder="e.g., 77002"
          value={zip}
          onChange={(e) => setZip(e.target.value)}
          style={{ width: "100%", padding: "0.5rem" }}
        />
      </div>
      <button onClick={fetchGasPrices} disabled={!zip || loading} style={{ padding: "0.5rem 1rem" }}>
        {loading ? "Searching..." : "Find Cheapest"}
      </button>

      <div style={{ marginTop: "2rem" }}>
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
            <div>{s.price.toLocaleString("en-US", { style: "currency", currency: "USD" })}</div>
            <div style={{ fontSize: "0.8rem", color: "#555" }}>
              Updated: {s.updated}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
