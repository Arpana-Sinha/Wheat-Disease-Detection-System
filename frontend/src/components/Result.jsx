import { useState } from "react";

function Result({ result }) {
  const [showSymptoms, setShowSymptoms] = useState(false);
  const [showCause, setShowCause] = useState(false);
  const [showPrevention, setShowPrevention] = useState(false);
  const [showCure, setShowCure] = useState(false);
  const [showGradcam, setShowGradcam] = useState(false);

  if (!result) return null;

  return (
    <div className="result-card">
      <h3>Disease: {result.disease}</h3>
      <p className="confidence">Confidence: {result.confidence}%</p>

      {/* IMAGE TOGGLE */}
      {result.image_url && (
        <>
          <div className="toggle-container">
            <button
              className={!showGradcam ? "toggle-active" : ""}
              onClick={() => setShowGradcam(false)}
            >
              Original
            </button>

            {result.gradcam_url && (
              <button
                className={showGradcam ? "toggle-active" : ""}
                onClick={() => setShowGradcam(true)}
              >
                Grad-CAM
              </button>
            )}
          </div>

          <img
            src={showGradcam && result.gradcam_url ? result.gradcam_url : result.image_url}
            alt="prediction"
            className="preview-img"
          />
        </>
      )}

      <hr style={{ margin: "16px 0" }} />

      {/* COLLAPSIBLE CARDS */}

      {result.symptoms && (
        <div className="info-section">
          <div className="info-title" onClick={() => setShowSymptoms(!showSymptoms)}>
            📌 Symptoms
          </div>
          {showSymptoms && <p>{result.symptoms}</p>}
        </div>
      )}

      {result.cause && (
        <div className="info-section">
          <div className="info-title" onClick={() => setShowCause(!showCause)}>
            ⚠ Cause
          </div>
          {showCause && <p>{result.cause}</p>}
        </div>
      )}

      {result.prevention && (
        <div className="info-section">
          <div className="info-title" onClick={() => setShowPrevention(!showPrevention)}>
            🛡 Prevention
          </div>
          {showPrevention && <p>{result.prevention}</p>}
        </div>
      )}

      {result.cure && (
        <div className="info-section">
          <div className="info-title" onClick={() => setShowCure(!showCure)}>
            💊 Cure
          </div>
          {showCure && <p>{result.cure}</p>}
        </div>
      )}
    </div>
  );
}

export default Result;
