import { useEffect, useState } from "react";
import diseaseInfo from "../../../backend/disease_info";

const API_KEY = "YOUR_OPENWEATHER_API_KEY";

function WeatherAlert({ disease }) {
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    if (!diseaseInfo[disease]) return;

    navigator.geolocation.getCurrentPosition(async (pos) => {
      const { latitude, longitude } = pos.coords;

      const res = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric`
      );
      const data = await res.json();

      const { temp, humidity } = data.main;
      const risk = diseaseInfo[disease].weatherRisk;

      if (
        temp >= risk.minTemp &&
        temp <= risk.maxTemp &&
        humidity >= risk.humidity
      ) {
        setAlert(
          `⚠️ High weather risk for ${disease}. Current humidity and temperature favor disease spread.`
        );
      }
    });
  }, [disease]);

  if (!alert) return null;

  return (
    <div
      style={{
        marginTop: "16px",
        padding: "12px",
        background: "#fff3cd",
        borderRadius: "8px",
        color: "#856404"
      }}
    >
      {alert}
    </div>
  );
}

export default WeatherAlert;
