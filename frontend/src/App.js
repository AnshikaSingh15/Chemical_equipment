import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";
import "./App.css";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://127.0.0.1:8000/api/upload/", formData);
      fetchSummary();
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    }
  };

  const fetchSummary = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/latest-summary/");
    setSummary(res.data);
  };

  return (
    <div className="container">
      <h1 className="title">📊 Chemical Equipment Visualizer</h1>

      <div className="upload-card">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Upload CSV</button>
      </div>

      {summary && (
        <>
          <div className="summary-grid">
            <div className="summary-card">
              <h3>Total Equipment</h3>
              <p>{summary.total_count}</p>
            </div>

            <div className="summary-card">
              <h3>Avg Flowrate</h3>
              <p>{summary.avg_flowrate.toFixed(2)}</p>
            </div>

            <div className="summary-card">
              <h3>Avg Pressure</h3>
              <p>{summary.avg_pressure.toFixed(2)}</p>
            </div>

            <div className="summary-card">
              <h3>Avg Temperature</h3>
              <p>{summary.avg_temperature.toFixed(2)}</p>
            </div>
          </div>

          <div className="chart-card">
            <h2>Equipment Type Distribution</h2>
            <Bar
              data={{
                labels: Object.keys(summary.type_distribution),
                datasets: [
                  {
                    label: "Equipment Count",
                    data: Object.values(summary.type_distribution)
                  }
                ]
              }}
            />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
