import React, { useState, useRef, useEffect } from "react";
import NoteInput from "./NoteInput";
import { askQuestion } from "../api";
import "./ChatInterface.css";

export default function ChatInterface({ noteId, onNoteCreated }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAsk = async () => {
    if (!question.trim() || !noteId) return;
    const q = question.trim();
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await askQuestion(noteId, q);
      setMessages((prev) => [...prev, { role: "assistant", text: res.data.answer }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: e.displayMessage || "Error getting answer." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="chat-view">
      {!noteId && (
        <div className="chat-note-section">
          <p className="chat-hint">First, save a note to chat with:</p>
          <NoteInput onNoteCreated={onNoteCreated} />
        </div>
      )}

      {noteId && (
        <>
          <p className="chat-hint">Ask questions about your note (Note ID: {noteId})</p>
          <div className="chat-messages">
            {messages.length === 0 && (
              <p className="chat-empty">No messages yet. Ask something about your notes.</p>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`chat-bubble ${msg.role}`}>
                <span className="chat-role">{msg.role === "user" ? "You" : "AI"}</span>
                <p>{msg.text}</p>
              </div>
            ))}
            {loading && (
              <div className="chat-bubble assistant">
                <span className="chat-role">AI</span>
                <p className="loading">Thinking...</p>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
          <div className="chat-input-row">
            <textarea
              rows={2}
              placeholder="Ask a question about your notes..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="btn-ask" onClick={handleAsk} disabled={loading || !question.trim()}>
              Ask
            </button>
          </div>
        </>
      )}
    </div>
  );
}
