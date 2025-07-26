from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import run_agent_sync
import os
from dotenv import load_dotenv
import time



# Your existing routes go below this


app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://learning-path-generator-fiu1y891w.vercel.app",
        "https://learning-path-generator-io4sv3wer.vercel.app",
        "https://learning-path-generator-lcw4uft9w.vercel.app"
    ],
    "supports_credentials": True,
    "allow_headers": "*",
    "methods": ["GET", "POST", "OPTIONS"]
}})


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
YOUTUBE_PIPEDREAM_URL = os.getenv("YOUTUBE_PIPEDREAM_URL")
DRIVE_PIPEDREAM_URL = os.getenv("DRIVE_PIPEDREAM_URL")
NOTION_PIPEDREAM_URL = os.getenv("NOTION_PIPEDREAM_URL")

# Debug environment variables
print("GOOGLE_API_KEY:", GOOGLE_API_KEY)
print("YOUTUBE_PIPEDREAM_URL:", YOUTUBE_PIPEDREAM_URL)
print("DRIVE_PIPEDREAM_URL:", DRIVE_PIPEDREAM_URL)
print("NOTION_PIPEDREAM_URL:", NOTION_PIPEDREAM_URL)

@app.route("/")
def home():
    return "✅ Flask backend is running!"
    
@app.route('/generate-path', methods=['GET', 'POST'])
def generate_path():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"messages": ["Content-Type must be application/json"]}), 415
        data = request.get_json()
        print("Received payload:", data)
        user_goal = data.get("user_goal")
        secondary_tool = data.get("secondary_tool")
        if not user_goal or not secondary_tool:
            return jsonify({"messages": ["Missing user_goal or secondary_tool"]}), 400

        drive_url = DRIVE_PIPEDREAM_URL if secondary_tool == "Drive" else None
        notion_url = NOTION_PIPEDREAM_URL if secondary_tool == "Notion" else None

        try:
            start_time = time.time()
            print(f"Calling run_agent_sync with goal: {user_goal}, tool: {secondary_tool}")
            result = run_agent_sync(
                google_api_key=GOOGLE_API_KEY,
                youtube_pipedream_url=YOUTUBE_PIPEDREAM_URL,
                drive_pipedream_url=drive_url,
                notion_pipedream_url=notion_url,
                user_goal=user_goal,
                progress_callback=lambda x: print(f"Progress: {x}")
            )
            elapsed_time = time.time() - start_time
            print(f"run_agent_sync completed in {elapsed_time:.2f} seconds, result:", result)

            # Filter out prompt/instruction/connection messages
            messages = []
            connection_links = []
            if result and "messages" in result:
                for msg in result["messages"]:
                    content = msg.content.strip()
                    content_lower = content.lower()
                    if not content:
                        continue
                    if (
                        content_lower.startswith("user goal:") or
                        "main instruction:" in content_lower
                    ):
                        continue
                    if "the user must be shown the following url" in content_lower:
                        connection_links.append(content)
                        continue
                    messages.append(content)
            else:
                print("No messages in result or result is None")

            response = {"messages": messages}
            if connection_links:
                response["connection_links"] = connection_links
            if not messages and not connection_links:
                response["messages"] = ["No AI response was generated. Check API keys and Pipedream connections."]
            return jsonify(response)
        except Exception as e:
            print(f"Error in run_agent_sync: {str(e)}")
            return jsonify({"messages": [f"Error generating path: {str(e)}"]}), 500
    else:
        return jsonify({"messages": ["Use POST with Content-Type: application/json"]}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)