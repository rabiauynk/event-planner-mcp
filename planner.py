import os
from datetime import datetime

import requests


def get_events(city, date):
    """
    Ticketmaster API'sini kullanarak belirli bir şehir ve tarihe göre etkinlikleri getirir.
    """
    # Ticketmaster API Key - doğrudan kod içinde
    api_key = os.getenv('TICKETMASTER_API_KEY') or 'iEXnISiQ5GXqqBWIlBzLOwP3cej3CKlo'

    # Ticketmaster API endpoint
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    # API parametreleri
    params = {
        'apikey': api_key,
        'city': city,
        'startDateTime': f"{date}T00:00:00Z",
        'endDateTime': f"{date}T23:59:59Z",
        'size': 20,  # Maksimum 20 etkinlik getir
        'sort': 'date,asc',
        'countryCode': 'TR'  # Türkiye için
    }

    try:
        # API çağrısı yap
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Etkinlik verilerini işle
        events = []
        if '_embedded' in data and 'events' in data['_embedded']:
            for event in data['_embedded']['events']:
                # Fiyat bilgisini al
                price_info = "Fiyat bilgisi mevcut değil"
                if 'priceRanges' in event and event['priceRanges']:
                    min_price = event['priceRanges'][0].get('min', 0)
                    max_price = event['priceRanges'][0].get('max', 0)
                    currency = event['priceRanges'][0].get('currency', 'TRY')
                    if min_price == max_price:
                        price_info = f"{min_price} {currency}"
                    else:
                        price_info = f"{min_price}-{max_price} {currency}"

                # Mekan bilgisini al
                venue_name = "Mekan bilgisi mevcut değil"
                if '_embedded' in event and 'venues' in event['_embedded'] and event['_embedded']['venues']:
                    venue_name = event['_embedded']['venues'][0].get('name', venue_name)

                # Kategori bilgisini al
                event_type = "Etkinlik"
                if 'classifications' in event and event['classifications']:
                    segment = event['classifications'][0].get('segment', {}).get('name', '')
                    genre = event['classifications'][0].get('genre', {}).get('name', '')
                    if segment:
                        event_type = segment
                    elif genre:
                        event_type = genre

                events.append({
                    "title": event.get('name', 'İsimsiz Etkinlik'),
                    "date": event.get('dates', {}).get('start', {}).get('localDate', date),
                    "time": event.get('dates', {}).get('start', {}).get('localTime', 'Saat belirtilmemiş'),
                    "location": venue_name,
                    "city": city,
                    "type": event_type,
                    "price": price_info,
                    "url": event.get('url', ''),
                    "description": event.get('info', 'Açıklama mevcut değil')
                })

        # Eğer API'den etkinlik bulunamazsa, örnek etkinlikler döndür
        if not events:
            events = [
                {
                    "title": f"{city} - Etkinlik bulunamadı",
                    "date": date,
                    "time": "Belirtilmemiş",
                    "location": f"{city} çevresinde",
                    "city": city,
                    "type": "Bilgi",
                    "price": "Ücretsiz",
                    "url": "",
                    "description": f"{date} tarihinde {city} şehrinde Ticketmaster'da kayıtlı etkinlik bulunamadı."
                }
            ]

        return events

    except requests.exceptions.RequestException as e:
        # API hatası durumunda örnek veri döndür
        return [
            {
                "title": f"API Hatası - {city} Örnek Etkinlik",
                "date": date,
                "time": "20:00",
                "location": f"{city} Kültür Merkezi",
                "city": city,
                "type": "Konser",
                "price": "50-100 TRY",
                "url": "",
                "description": f"Ticketmaster API'sine bağlanılamadı. Hata: {str(e)}"
            }
        ]
    except Exception as e:
        raise Exception(f"Etkinlik verilerini alırken hata oluştu: {str(e)}")