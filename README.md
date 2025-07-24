# MCP Learning Path Generator

A full-stack AI-powered web application for generating personalized, day-wise learning paths using the Model Context Protocol (MCP). The app features a modern React.js frontend and a Python (Flask) backend, integrating with Gemini, YouTube, Google Drive, and Notion via Pipedream. Users receive rich, chat-style AI responses and actionable learning plans.

---

## Features

- 🎯 Generate custom learning paths based on your goals
- 🤖 AI-powered (Gemini) with chat-style responses
- 🎥 YouTube integration for curated video content
- 📁 Google Drive and 📝 Notion integration for document/note creation
- 🔗 All links are provided as clickable links (most important!)
- 🚀 Real-time, interactive web UI (React.js)
- 🛠️ Modern, maintainable codebase (React + Flask)

---

## Prerequisites

- Python 3.10+
- Node.js (for React frontend)
- Google AI Studio API Key
- Pipedream URLs for integrations:
  - YouTube (required)
  - Google Drive or Notion (at least one required)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   pip install -r requirements.txt
   ```

3. **Frontend setup:**
   ```bash
   cd ../frontend
   npm install
   ```

---

## Configuration

1. In the `backend` folder, create a `.env` file with:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   YOUTUBE_PIPEDREAM_URL=your_youtube_pipedream_url
   DRIVE_PIPEDREAM_URL=your_drive_pipedream_url
   NOTION_PIPEDREAM_URL=your_notion_pipedream_url
   ```
   - Only YouTube is required; Drive/Notion are optional but recommended.

---

## Running the Application

1. **Start the backend (Flask API):**
   ```bash
   cd backend
   venv/Scripts/activate  # or source venv/bin/activate
   flask run
   # The backend will run at http://127.0.0.1:5000
   ```

2. **Start the frontend (React):**
   ```bash
   cd ../frontend
   npm start
   # The frontend will run at http://localhost:3000
   ```

---

## Usage

1. Open [http://localhost:3000](http://localhost:3000) in your browser.
2. Select your secondary tool (Drive or Notion).
3. Enter your learning goal (e.g., "I want to learn Python in 3 days").
4. Click "Generate Learning Path".
5. The AI will generate a day-wise plan, with clickable links to videos and resources.
6. If prompted, connect your YouTube/Drive/Notion accounts via the provided Pipedream links.

---

## Project Structure

- `backend/`
  - `app.py` - Flask backend API
  - `utils.py` - Core logic for learning path generation
  - `prompt.py` - AI prompt template (with clickable link emphasis)
  - `requirements.txt` - Python dependencies
  - `.env` - API keys and Pipedream URLs (not committed)
- `frontend/`
  - `src/App.js` - Main React component (chat UI)
  - `src/App.css` - Styles for the frontend
  - `package.json` - Frontend dependencies
- `.gitignore` - Ignore venv, .env, node_modules, etc.
- `README.md` - Project documentation

---

## Notes
- **Clickable links in all AI responses are a top priority.**
- The backend filters out prompt/instruction messages and only returns actionable AI responses.
- If you see connection links, open them to authorize Pipedream integrations.
- For any issues, check backend logs for debug output.

---

## License
MIT
