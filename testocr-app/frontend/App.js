import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setResults([]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const res = await axios.post(`${API_URL}/newocr`, formData);
      setResults(res.data.results || []);
    } catch (err) {
      console.error(err);
      setResults(['Error: ' + (err.response?.data?.error || err.message)]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>OCR App (Image & PDF)</h1>
      <input type="file" accept="image/*,.pdf" onChange={handleChange} />
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? 'Processing...' : 'Upload & OCR'}
      </button>

      <div style={{ marginTop: 20 }}>
        <h3>Extracted Text:</h3>
        <ul> {results.map((r, i) => (
              <li key={i}>{r.text}</li>
            ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
