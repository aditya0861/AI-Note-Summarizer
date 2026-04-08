import React, { useState } from "react";
import { uploadNote, uploadNoteFile } from "../api";
import "./NoteInput.css";

export default function NoteInput({ onNoteCreated }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);

  const handleSaveText = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await uploadNote(text.trim());
      onNoteCreated(res.data.id);
      setSaved(true);
    } catch (e) {
      setError(e.displayMessage || "Failed to save note");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    setError(null);
    setSaved(false);
    try {
      const res = await uploadNoteFile(file);
      onNoteCreated(res.data.id);
      setText(res.data.content);
      setSaved(true);
    } catch (e) {
      setError(e.displayMessage || "Failed to upload file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="note-input">
      <label className="label">Paste your notes</label>
      <textarea
        rows={8}
        placeholder="Type or paste your notes here..."
        value={text}
        onChange={(e) => { setText(e.target.value); setSaved(false); }}
      />
      <div className="note-input-actions">
        <button className="btn-save" onClick={handleSaveText} disabled={loading || !text.trim()}>
          {loading ? "Saving..." : saved ? "Saved ✓" : "Save Note"}
        </button>
        <label className="btn-upload">
          Upload File (PDF/TXT)
          <input type="file" accept=".txt,.pdf" onChange={handleFileUpload} hidden />
        </label>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
