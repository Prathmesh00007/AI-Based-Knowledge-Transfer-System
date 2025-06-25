import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const JiraConnector = () => {
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleIngestJira = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/ingest/jira`);
      if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
      }
      const data = await res.json();
      setResponseData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "1rem", padding: "1rem", border: "1px solid #ccc" }}>
      <h2>Jira Ingestion</h2>
      <button onClick={handleIngestJira} disabled={loading}>
        {loading ? "Ingesting..." : "Ingest Jira Data"}
      </button>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {responseData && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Response:</h3>
          <pre style={{ background: "#f4f4f4", padding: "1rem" }}>
            {JSON.stringify(responseData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default JiraConnector;
