const BASE_URL = "http://localhost:8000";

export const signup = async (username, password) => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    body: formData,
  });
  return res.json();
};

export const login = async (username, password) => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    body: formData,
  });
  return res.json();
};

export const predictDisease = async (image, userId) => {
  const formData = new FormData();
  formData.append("file", image);
  formData.append("user_id", userId);

  const res = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });
  return res.json();
};

export const fetchHistory = async (userId) => {
  const res = await fetch(`${BASE_URL}/history/${userId}`);
  return res.json();
};

export const getGradCAM = async (image) => {
  const formData = new FormData();
  formData.append("file", image);

  const res = await fetch(`${BASE_URL}/gradcam`, {
    method: "POST",
    body: formData,
  });

  return URL.createObjectURL(await res.blob());
};

export const fetchMonthlyTrends = async (userId) => {
  const res = await fetch(`http://localhost:8000/monthly-trends/${userId}`);
  return res.json();
};
