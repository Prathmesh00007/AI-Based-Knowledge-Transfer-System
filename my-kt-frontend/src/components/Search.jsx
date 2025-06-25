// src/components/Search.jsx
import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const Search = () => {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(3);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}`);
      if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
      }
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: "1rem 0" }}>
      <h2>Semantic Search</h2>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Enter search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: "60%", padding: "0.5rem", marginRight: "0.5rem" }}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <div style={{ marginTop: "1rem" }}>
        {searchResults.map((result, index) => (
          <div key={index} style={{ border: "1px solid #ddd", padding: "1rem", marginBottom: "1rem" }}>
            <h3>{result.summary}</h3>
            <p><strong>ID:</strong> {result.id}</p>
            <p>{result.chunk_text}</p>
            <p><strong>Score:</strong> {result.score}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Search;
