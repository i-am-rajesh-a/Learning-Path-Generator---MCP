import React, { useState } from "react";
import ReactMarkdown from 'react-markdown';
import "./App.css";
import axios from "axios";

function App() {
  const [userGoal, setUserGoal] = useState("");
  const [secondaryTool, setSecondaryTool] = useState("Drive");
  const [isGenerating, setIsGenerating] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [learningPath, setLearningPath] = useState([]);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!userGoal.trim()) {
      setStatusMessage("Please enter a valid learning goal.");
      return;
    }
    setIsGenerating(true);
    setStatusMessage("Generating your learning path...");
    setLearningPath([]);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const API_URL = `${backendUrl}/generate-path`;
      console.log("Sending request with payload:", { user_goal: userGoal, secondary_tool: secondaryTool });
      const response = await axios.post(API_URL, {
        user_goal: userGoal,
        secondary_tool: secondaryTool,
      });
      const data = response.data;
      console.log("API response:", data);
      if (data.messages && data.messages.length > 0) {
        setStatusMessage("Learning path generation complete!");
        setLearningPath(data.messages);
      } else {
        setStatusMessage("No results were generated. Please check the server logs and try again.");
      }
      if (data.connection_links) {
        console.log("Connection links:", data.connection_links);
      }
    } catch (error) {
      console.error(error);
      setStatusMessage(`Error: ${error.message}. Check if the server is running on http://127.0.0.1:5000.`);
    }
    setIsGenerating(false);
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>Configuration</h2>
        <div>
          <div className="sidebar-label">Select Secondary Tool:</div>
          <label className="sidebar-radio">
            <input
              type="radio"
              name="tool"
              value="Drive"
              checked={secondaryTool === "Drive"}
              onChange={() => setSecondaryTool("Drive")}
            />
            Drive
          </label>
          <label className="sidebar-radio">
            <input
              type="radio"
              name="tool"
              value="Notion"
              checked={secondaryTool === "Notion"}
              onChange={() => setSecondaryTool("Notion")}
            />
            Notion
          </label>
        </div>
      </aside>
      <main className="main-content">
        <h1 className="main-title">
          Model Context Protocol(MCP) - Learning Path Generator
        </h1>
        <div className="quick-guide">
          <strong>Quick Guide:</strong>
          <ol>
            <li>Select your secondary tool (Drive or Notion)</li>
            <li>
              Enter a clear learning goal, for example:
              <ul>
                <li>"I want to learn python basics in 3 days"</li>
                <li>"I want to learn data science basics in 10 days"</li>
              </ul>
            </li>
          </ol>
        </div>
        <section className="goal-section">
          <h2>Enter Your Goal</h2>
          <form onSubmit={handleGenerate} className="goal-form">
            <label htmlFor="goal-input" className="goal-label">
              Enter your learning goal:
            </label>
            <input
              id="goal-input"
              type="text"
              className="goal-input"
              placeholder="E.g., I want to learn Python in 3 days"
              value={userGoal}
              onChange={(e) => setUserGoal(e.target.value)}
              disabled={isGenerating}
              autoComplete="off"
            />
            <button
              type="submit"
              className="generate-btn"
              disabled={isGenerating}
            >
              {isGenerating ? "Generating..." : "Generate Learning Path"}
            </button>
          </form>
        </section>
        {statusMessage && (
          <div className="status-message">{statusMessage}</div>
        )}
        {learningPath.length > 0 && (
          <div className="chat-results">
            <h2>
              <span role="img" aria-label="book" style={{ marginRight: 8 }}>
                📚
              </span>
              Your Learning Path
            </h2>
            <div className="chat-single-response">
              <ReactMarkdown>
                {learningPath.join('\n\n')}
              </ReactMarkdown>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;