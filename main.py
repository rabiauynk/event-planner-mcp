#!/usr/bin/env python3
"""
Minimal Event Planner MCP - Single file solution
"""
import os
import json

# Minimal Flask app
try:
    from flask import Flask, request, jsonify
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

@app.route('/')
def home():
    return {
        "status": "Event Planner MCP is running",
        "version": "1.0.0",
        "api_ready": True
    }

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/events', methods=['POST'])
def events():
    try:
        data = request.get_json() or {}
        city = data.get('city', 'İstanbul')
        date = data.get('date', '2024-12-25')
        
        events = get_events_simple(city, date)
        return jsonify({"events": events})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
