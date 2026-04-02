import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

function Analytics({ userId }) {
  const [monthlyData, setMonthlyData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/monthly-trends/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Monthly Data:", data); 
        setMonthlyData(data);
      })
      .catch((err) => console.error(err));
  }, [userId]);

  if (!monthlyData.length) {
    return (
      <div style={{ padding: "40px", textAlign: "center" }}>
        No monthly data available
      </div>
    );
  }

  const chartData = {
    labels: monthlyData.map((item) => item.month),
    datasets: [
      {
        label: "Detections per Month",
        data: monthlyData.map((item) => item.count),
        borderColor: "#2e7d32",
        backgroundColor: "rgba(46,125,50,0.2)",
        tension: 0.3,
        fill: true,
      },
    ],
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
        Monthly Detection Trends
      </h2>
      <Line data={chartData} />
    </div>
  );
}

export default Analytics;
