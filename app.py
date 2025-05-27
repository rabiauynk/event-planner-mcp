import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from planner import get_events

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Event Planner MCP is running"}

@app.route("/events", methods=["POST"])
def events():
    data = request.get_json()
    city = data.get("city")
    date = data.get("date")

    if not city or not date:
        return jsonify({"error": "Missing 'city' or 'date' in request."}), 400

    try:
        events = get_events(city, date)
        return jsonify({"events": events})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)