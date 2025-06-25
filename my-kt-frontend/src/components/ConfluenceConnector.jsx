// src/components/ConfluenceBulkIngest.jsx
import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const ConfluenceIngest = () => {
  const [spaceKey, setSpaceKey] = useState("");
  const [limit, setLimit] = useState(10);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleBulkIngest = async () => {
    if (!spaceKey.trim()) {
      setError("Please enter a Confluence space key.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/ingest/confluence/bulk?space_key=${encodeURIComponent(spaceKey)}&limit=${limit}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      const data = await response.json();
      setResult(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: "1rem 0", padding: "1rem", border: "1px solid #ddd" }}>
      <h2>Bulk Ingest Confluence Documentation</h2>
      <input
        type="text"
        placeholder="Enter Confluence Space Key"
        value={spaceKey}
        onChange={(e) => setSpaceKey(e.target.value)}
        style={{ padding: "0.5rem", width: "40%", marginRight: "1rem" }}
      />
      <input
        type="number"
        placeholder="Limit pages"
        value={limit}
        onChange={(e) => setLimit(e.target.value)}
        style={{ padding: "0.5rem", width: "15%", marginRight: "1rem" }}
      />
      <button onClick={handleBulkIngest} disabled={loading}>
        {loading ? "Ingesting..." : "Ingest Documentation"}
      </button>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Processed Documents:</h3>
          <pre style={{ background: "#f4f4f4", padding: "1rem" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ConfluenceIngest;
