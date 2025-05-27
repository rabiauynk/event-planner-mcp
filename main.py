#!/usr/bin/env python3
"""
Event Planner MCP Server - HTTP Implementation
"""
import json
import os
from urllib.parse import parse_qs

# Minimal Flask app
try:
    from flask import Flask, Response, jsonify, request
except ImportError:
    print("Flask not available")
    exit(1)

# Try to import requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

app = Flask(__name__)

# Built-in API key
TICKETMASTER_API_KEY = 'iEXnISiQ5GXqqBWIlBzLOwP3cej3CKlo'

# MCP Protocol Implementation
MCP_TOOLS = [
    {
        "name": "get_events",
        "description": "Get events for a specific city and date using Ticketmaster API",
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name to search for events"
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                }
            },
            "required": ["city", "date"]
        }
    }
]

def get_events_simple(city, date):
    """Simple event fetcher with fallback"""
    if not REQUESTS_AVAILABLE:
        return [{
            "title": f"{city} - Requests modülü mevcut değil",
            "date": date,
            "location": city,
            "type": "Bilgi",
            "price": "Ücretsiz"
        }]
    
    try:
        # Ticketmaster API call
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            'apikey': TICKETMASTER_API_KEY,
            'city': city,
            'startDateTime': f"{date}T00:00:00Z",
            'endDateTime': f"{date}T23:59:59Z",
            'size': 10,
            'countryCode': 'TR'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            events = []
            
            if '_embedded' in data and 'events' in data['_embedded']:
                for event in data['_embedded']['events'][:5]:  # Limit to 5
                    events.append({
                        "title": event.get('name', 'İsimsiz Etkinlik'),
                        "date": date,
                        "location": event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Mekan belirtilmemiş') if event.get('_embedded', {}).get('venues') else 'Mekan belirtilmemiş',
                        "type": event.get('classifications', [{}])[0].get('segment', {}).get('name', 'Etkinlik') if event.get('classifications') else 'Etkinlik',
                        "price": "Fiyat bilgisi mevcut değil"
                    })
            
            if not events:
                events = [{
                    "title": f"{city} - Etkinlik bulunamadı",
                    "date": date,
                    "location": city,
                    "type": "Bilgi",
                    "price": "Ücretsiz"
                }]
            
            return events
        else:
            raise Exception(f"API Error: {response.status_code}")
            
    except Exception as e:
        # Fallback data
        return [{
            "title": f"{city} - API Hatası",
            "date": date,
            "location": city,
            "type": "Bilgi",
            "price": "Ücretsiz",
            "error": str(e)
        }]

# MCP HTTP Server Endpoints
@app.route('/mcp', methods=['POST'])
def mcp_handler():
    """Main MCP endpoint"""
    try:
        data = request.get_json()
        method = data.get('method')

        if method == 'tools/list':
            return jsonify({
                "tools": MCP_TOOLS
            })

        elif method == 'tools/call':
            tool_name = data.get('params', {}).get('name')
            arguments = data.get('params', {}).get('arguments', {})

            if tool_name == 'get_events':
                city = arguments.get('city', 'İstanbul')
                date = arguments.get('date', '2024-12-25')
                events = get_events_simple(city, date)

                return jsonify({
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"events": events}, ensure_ascii=False, indent=2)
                        }
                    ]
                })
            else:
                return jsonify({"error": f"Unknown tool: {tool_name}"}), 400

        else:
            return jsonify({"error": f"Unknown method: {method}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return {
        "status": "Event Planner MCP Server",
        "version": "1.0.0",
        "mcp_endpoint": "/mcp"
    }

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
