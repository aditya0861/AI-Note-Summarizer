import React, { useState } from "react";
import NoteInput from "./components/NoteInput";
import ModeSelector from "./components/ModeSelector";
import OutputDisplay from "./components/OutputDisplay";
import ChatInterface from "./components/ChatInterface";
import HistoryPanel from "./components/HistoryPanel";
import { summarize } from "./api";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("summarize");
  const [noteId, setNoteId] = useState(null);
  const [mode, setMode] = useState("concise");
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSummarize = async () => {
    if (!noteId) return;
    setLoading(true);
    setError(null);
    setOutput(null);
    try {
      const res = await summarize(noteId, mode);
      setOutput(res.data);
    } catch (e) {
      setError(e.displayMessage || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Note Summarizer</h1>
        <p>Upload notes, generate summaries, and chat with your content</p>
      </header>

      <nav className="tabs">
        {["summarize", "chat", "history"].map((tab) => (
          <button
            key={tab}
            className={`tab-btn ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </nav>

      <main className="app-main">
        {activeTab === "summarize" && (
          <div className="summarize-view">
            <NoteInput onNoteCreated={setNoteId} />
            {noteId && (
              <>
                <ModeSelector mode={mode} onChange={setMode} />
                <button
                  className="btn-primary"
                  onClick={handleSummarize}
                  disabled={loading}
                >
                  {loading ? "Generating..." : "Generate"}
                </button>
                {error && <p className="error">{error}</p>}
                {output && <OutputDisplay output={output} />}
              </>
            )}
          </div>
        )}

        {activeTab === "chat" && (
          <ChatInterface noteId={noteId} onNoteCreated={setNoteId} />
        )}

        {activeTab === "history" && <HistoryPanel />}
      </main>
    </div>
  );
}
