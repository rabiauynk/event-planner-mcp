import os

from flask import Flask, jsonify, request

# Try to load dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)

# Import planner module
from planner import get_events


@app.route("/")
def home():
    # API key ya environment variable'dan ya da kod içinden gelir
    api_key = os.getenv('TICKETMASTER_API_KEY') or 'iEXnISiQ5GXqqBWIlBzLOwP3cej3CKlo'
    api_key_status = "configured (built-in)" if api_key else "not configured"
    return {
        "status": "Event Planner MCP is running",
        "api_key_status": api_key_status,
        "version": "1.0.0",
        "ticketmaster_ready": True
    }

@app.route("/health")
def health():
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy", "timestamp": "2024-12-27"}

@app.route("/events", methods=["POST"])
def events():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        city = data.get("city")
        date = data.get("date")

        if not city or not date:
            return jsonify({"error": "Missing 'city' or 'date' in request."}), 400

        events = get_events(city, date)
        return jsonify({"events": events})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use debug=False for production, debug=True for development
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)