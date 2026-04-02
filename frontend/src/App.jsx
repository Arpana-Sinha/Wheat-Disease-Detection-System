import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import History from "./pages/History";
import Analytics from "./pages/Analytics";
import ImageUpload from "./components/ImageUpload";
import Result from "./components/Result";

function App() {
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState("");
  const [result, setResult] = useState(null);
  const [showSignup, setShowSignup] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [page, setPage] = useState("detect");

  useEffect(() => {
  const storedId = localStorage.getItem("user_id");
  const storedName = localStorage.getItem("username");

  if (storedId) {
    setUserId(storedId);
    setUsername(storedName);
    setSidebarOpen(false);
  }
}, []);


  const navigate = (p) => {
    setPage(p);
    setSidebarOpen(false);

    if (p !== "detect") {
      setResult(null); // ✅ clear detection when leaving page
    }
  };

  if (!userId) {
    return (
      <div className="center-wrapper">
        {showSignup ? (
          <Signup onSwitch={() => setShowSignup(false)} />
        ) : (
          <Login
            setUserId={setUserId}
            onSwitch={() => setShowSignup(true)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="layout">
      <div className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="user-section">
          <div className="user-icon">👤</div>
          <div className="username">{username}</div>
        </div>

        <button onClick={() => navigate("detect")}>Detect Disease</button>
        <button onClick={() => navigate("history")}>History</button>
        <button onClick={() => navigate("analytics")}>Analytics</button>

        <button
          className="logout-btn"
          onClick={() => {
            localStorage.clear();
            setUserId(null);
          }}
        >
          Logout
        </button>
      </div>

      <div className="main-content">
        <button
          className="menu-btn"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          ☰
        </button>

        {page === "detect" && (
          <div className="center-wrapper">
            <div className="app-container">
              <h1>Wheat Disease Detection</h1>
              <ImageUpload setResult={setResult} userId={userId} />
              {result && <Result result={result} />}
            </div>
          </div>
        )}

        {page === "history" && <History userId={userId} />}
        {page === "analytics" && <Analytics userId={userId} />}
      </div>
    </div>
  );
}

export default App;
