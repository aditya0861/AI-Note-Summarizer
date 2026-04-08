import React from "react";
import "./ModeSelector.css";

const MODES = [
  { value: "concise", label: "Concise Summary" },
  { value: "detailed", label: "Detailed Summary" },
  { value: "keypoints", label: "Key Points" },
  { value: "flashcards", label: "Flashcards" },
  { value: "keywords", label: "Keywords" },
];

export default function ModeSelector({ mode, onChange }) {
  return (
    <div className="mode-selector">
      <label className="label">Select Mode</label>
      <div className="mode-options">
        {MODES.map((m) => (
          <button
            key={m.value}
            className={`mode-btn ${mode === m.value ? "active" : ""}`}
            onClick={() => onChange(m.value)}
          >
            {m.label}
          </button>
        ))}
      </div>
    </div>
  );
}
