import React from "react";
import "./OutputDisplay.css";

export default function OutputDisplay({ output }) {
  if (!output) return null;

  return (
    <div className="output-display">
      <div className="output-header">
        <span className="output-type">{output.type}</span>
        <span className="output-time">{new Date(output.created_at).toLocaleString()}</span>
      </div>
      <pre className="output-content">{output.output}</pre>
    </div>
  );
}
