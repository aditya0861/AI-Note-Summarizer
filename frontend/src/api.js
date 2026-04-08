import axios from "axios";

const api = axios.create({
  baseURL: "",
  timeout: 45000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.error ||
      (err.code === "ECONNABORTED" ? "Request timed out. Please try again." : null) ||
      (err.message === "Network Error" ? "Network error. Check your connection." : null) ||
      "Something went wrong. Please try again.";
    err.displayMessage = message;
    return Promise.reject(err);
  }
);

export const uploadNote = (content) =>
  api.post("/api/notes", { content });

export const uploadNoteFile = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/api/notes", form, { headers: { "Content-Type": "multipart/form-data" } });
};

export const summarize = (note_id, mode) =>
  api.post("/api/summarize", { note_id, mode });

export const askQuestion = (note_id, question) =>
  api.post("/api/ask", { note_id, question });

export const getHistory = () =>
  api.get("/api/history");
