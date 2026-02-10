import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const uploadCSV = (formData) =>
  API.post("/api/upload-csv/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
