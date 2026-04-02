import { useRef, useState } from "react";
import { predictDisease } from "../api";

function ImageUpload({ setResult, userId }) {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [predictionDone, setPredictionDone] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const resetForNewImage = () => {
    setImage(null);
    setPreview(null);
    setConfirmed(false);
    setPredictionDone(false);
    setResult(null);
  };

  const startCamera = async () => {
    resetForNewImage();
    setCameraOn(true);
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
      const file = new File([blob], "camera.jpg", { type: "image/jpeg" });
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setConfirmed(false);
    }, "image/jpeg");

    const stream = video.srcObject;
    stream.getTracks().forEach((track) => track.stop());
    setCameraOn(false);
  };

  const handleFileChange = (e) => {
    resetForNewImage();
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const confirmImage = () => {
    setConfirmed(true);
  };

  const retakeImage = () => {
    resetForNewImage();
  };

  const handleSubmit = async () => {
    if (!image) return;

    setLoading(true);
    const res = await predictDisease(image, userId);
    setResult(res);
    setLoading(false);
    setPredictionDone(true);
  };

  return (
    <div className="upload-card">
      {!cameraOn && !preview && !predictionDone && (
        <>
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button onClick={startCamera}>📷 Open Camera</button>
        </>
      )}

      {cameraOn && (
        <>
          <video
            ref={videoRef}
            autoPlay
            style={{ width: "100%", borderRadius: "10px" }}
          />
          <button onClick={capturePhoto}>📸 Capture</button>
        </>
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />

      {preview && (
        <img src={preview} alt="preview" className="preview-img" />
      )}

      {preview && !confirmed && !predictionDone && (
        <>
          <p style={{ marginTop: "10px" }}>Is this image okay?</p>
          <button onClick={confirmImage}>✅ Yes, Use This</button>
          <button onClick={retakeImage}>🔄 Retake / Choose Another</button>
        </>
      )}

      {confirmed && !predictionDone && (
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Detecting..." : "Detect Disease"}
        </button>
      )}

      {predictionDone && (
        <button onClick={resetForNewImage}>
          🔁 Detect Another Image
        </button>
      )}
    </div>
  );
}

export default ImageUpload;
