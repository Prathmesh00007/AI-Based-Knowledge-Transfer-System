// src/components/Record.jsx
import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const Record = () => {
  const [recordResponse, setRecordResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRecord = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/record`);
      if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
      }
      const data = await res.json();
      setRecordResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: "1rem 0" }}>
      <h2>Record and Transcribe</h2>
      <button onClick={handleRecord} disabled={loading}>
        {loading ? "Recording..." : "Record Audio"}
      </button>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {recordResponse && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Transcription:</h3>
          <pre style={{ background: "#f0f0f0", padding: "1rem" }}>
            {recordResponse.transcription}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Record;
