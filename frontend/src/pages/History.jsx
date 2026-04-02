import { useEffect, useState } from "react";
import { fetchHistory } from "../api";

function History({ userId }) {
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetchHistory(userId).then((data) => setHistory(data || []));
  }, [userId]);

  return (
    <>
      {history.length === 0 && (
        <p style={{ textAlign: "center", marginTop: "40px", color: "#555" }}>
          No history available
        </p>
      )}

      {history.length > 0 && (
        <div className="history-grid">
          {history.map((item, i) => (
            <div
              key={i}
              className="history-card"
              onClick={() => setSelected(item)}
            >
              {item.image_url && (
                <img
                  src={item.image_url}
                  alt="uploaded"
                  className="history-img"
                />
              )}

              <h4>{item.disease}</h4>
              <small>{item.confidence}%</small>
              <br />
              <small>Detected on: {item.date}</small>
            </div>
          ))}
        </div>
      )}

      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelected(null)}>
              ✕
            </button>

            <p><strong>Disease:</strong> {selected.disease}</p>
            <p><strong>Confidence:</strong> {selected.confidence}%</p>
            <p><strong>Date:</strong> {selected.date}</p>

            {selected.image_url && (
              <img
                src={selected.image_url}
                alt="original"
                className="modal-img"
              />
            )}

            {selected.gradcam_url && (
              <>
                <h4 style={{ marginTop: "12px" }}>Grad-CAM</h4>
                <img
                  src={selected.gradcam_url}
                  alt="gradcam"
                  className="modal-img"
                />
              </>
            )}

            {selected.symptoms && (
              <>
                <hr style={{ margin: "12px 0" }} />
                <p><strong>Symptoms:</strong> {selected.symptoms}</p>
                <p><strong>Cause:</strong> {selected.cause}</p>
                <p><strong>Prevention:</strong> {selected.prevention}</p>
                <p><strong>Cure:</strong> {selected.cure}</p>
              </>
            )}

          </div>
        </div>
      )}
    </>
  );
}

export default History;
