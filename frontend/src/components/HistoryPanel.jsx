import React, { useEffect, useState, useCallback } from "react";
import { getHistory } from "../api";
import "./HistoryPanel.css";

export default function HistoryPanel() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState({});

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    getHistory()
      .then((res) => setHistory(res.data))
      .catch((e) => setError(e.displayMessage || "Failed to load history"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const toggle = (id) => setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));

  if (loading) return (
    <div className="history-skeleton">
      {[1, 2, 3].map((i) => <div key={i} className="skeleton-row" />)}
    </div>
  );

  if (error) return (
    <div className="history-error">
      <p className="error">{error}</p>
      <button className="btn-retry" onClick={load}>Retry</button>
    </div>
  );

  if (history.length === 0) return <p className="history-empty">No notes saved yet.</p>;

  return (
    <div className="history-panel">
      {history.map((note) => (
        <div key={note.id} className="history-note">
          <div
            className="history-note-header"
            onClick={() => toggle(note.id)}
            role="button"
            aria-expanded={!!expanded[note.id]}
            tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && toggle(note.id)}
          >
            <div>
              <span className="history-id">Note #{note.id}</span>
              {note.filename && <span className="history-filename">{note.filename}</span>}
            </div>
            <div className="history-meta">
              <span>{note.summaries.length} output(s)</span>
              <span>{new Date(note.created_at).toLocaleDateString()}</span>
              <span className="toggle-icon" aria-hidden="true">{expanded[note.id] ? "▲" : "▼"}</span>
            </div>
          </div>

          {expanded[note.id] && (
            <div className="history-note-body">
              <pre className="history-content">
                {note.content.slice(0, 300)}{note.content.length > 300 ? "…" : ""}
              </pre>
              {note.summaries.length > 0 && (
                <div className="history-summaries">
                  {note.summaries.map((s) => (
                    <div key={s.id} className="history-summary">
                      <span className="summary-type">{s.type}</span>
                      <pre className="summary-output">{s.output}</pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
