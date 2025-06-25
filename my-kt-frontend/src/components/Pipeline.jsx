// src/components/PipelineTest.jsx
import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const PipelineTest = () => {
  const [rawText, setRawText] = useState("");
  const [sourceId, setSourceId] = useState("manual_test"); // a default source id for testing
  const [pipelineOutput, setPipelineOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleTestPipeline = async () => {
    setLoading(true);
    setError("");
    setPipelineOutput(null);

    try {
      const response = await fetch(`${API_BASE_URL}/test/pipeline`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ raw_text: rawText, source_id: sourceId })
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      setPipelineOutput(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: "1rem 0", padding: "1rem", border: "1px solid #ccc" }}>
      <h2>Test the Pipeline</h2>
      <textarea
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
        placeholder="Enter raw text to process..."
        rows={6}
        style={{ width: "100%", padding: "0.5rem" }}
      />
      <br />
      <button onClick={handleTestPipeline} disabled={loading || rawText.trim() === ""}>
        {loading ? "Processing..." : "Test Pipeline"}
      </button>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {pipelineOutput && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Pipeline Output:</h3>
          <pre style={{ background: "#f4f4f4", padding: "1rem" }}>
            {JSON.stringify(pipelineOutput, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default PipelineTest;
