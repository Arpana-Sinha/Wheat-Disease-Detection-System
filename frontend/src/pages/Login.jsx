import { useState } from "react";
import { login } from "../api";

function Login({ setUserId, onSwitch }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      alert("Fill all fields");
      return;
    }

    const res = await login(username, password);

    if (res.user_id) {
      localStorage.setItem("user_id", res.user_id);
      localStorage.setItem("username", res.username);
      setUserId(res.user_id);
    } else {
      alert(res.error || "Login failed");
    }
  };

  return (
    <div className="auth-card">
      <h2>Login</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      {/* Password field with eye icon */}
      <div style={{ position: "relative" }}>
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <span
          onClick={() => setShowPassword(!showPassword)}
          style={{
            position: "absolute",
            right: "12px",
            top: "50%",
            transform: "translateY(-50%)",
            cursor: "pointer",
            fontSize: "14px",
            color: "#2e7d32",
            userSelect: "none",
          }}
        >
          {showPassword ? "🙈" : "👁"}
        </span>
      </div>

      <button onClick={handleLogin}>Login</button>

      <button onClick={onSwitch} className="secondary-btn">
        Go to Signup
      </button>
    </div>
  );
}

export default Login;
