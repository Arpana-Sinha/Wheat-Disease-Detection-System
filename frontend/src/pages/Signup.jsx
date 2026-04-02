import { useState } from "react";
import { signup } from "../api";

function Signup({ onSwitch }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSignup = async () => {
    if (!username || !password) {
      alert("Fill all fields");
      return;
    }

    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

    if (!passwordRegex.test(password)) {
      alert(
        "Password must be at least 8 characters long and include uppercase, lowercase, and a number"
      );
      return;
    }

    const res = await signup(username, password);

    if (res.message) {
      alert("Signup successful. Login now.");
      onSwitch();
    } else {
      alert(res.error || "Signup failed");
    }
  };

  return (
    <div className="auth-card">
      <h2>Signup</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

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

      <button onClick={handleSignup}>Signup</button>

      <button onClick={onSwitch} className="secondary-btn">
        Go to Login
      </button>
    </div>
  );
}

export default Signup;
