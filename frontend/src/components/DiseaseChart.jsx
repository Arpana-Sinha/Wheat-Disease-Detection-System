import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function DiseaseChart({ history }) {
  if (!history || history.length === 0) {
    return (
      <div className="app-container">
        <h1>Disease Analytics</h1>
        <p style={{ textAlign: "center", color: "#555", marginTop: "20px" }}>
          No data available to generate analytics
        </p>
      </div>
    );
  }

  const diseaseCount = {};
  history.forEach((item) => {
    diseaseCount[item.disease] =
      (diseaseCount[item.disease] || 0) + 1;
  });

  const data = {
    labels: Object.keys(diseaseCount),
    datasets: [
      {
        label: "Number of detections",
        data: Object.values(diseaseCount),
        backgroundColor: "#66bb6a",
      },
    ],
  };

  return (
    <div className="app-container">
      <h1>Disease Analytics</h1>
      <Bar data={data} />
    </div>
  );
}

export default DiseaseChart;
