# Event Planner MCP

Ticketmaster API'sini kullanarak belirli bir şehir ve tarihe göre etkinlik önerileri sunan MCP API.

## Kurulum

### Gereksinimler
- Python 3.10+
- Ticketmaster API Key

### Yerel Kurulum

1. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını oluşturun ve Ticketmaster API key'inizi ekleyin:
```
TICKETMASTER_API_KEY=your_api_key_here
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

### Docker ile Kurulum

1. Docker image'ını oluşturun:
```bash
docker build -t event-planner-mcp .
```

2. Container'ı çalıştırın:
```bash
docker run -p 5000:5000 -e TICKETMASTER_API_KEY=your_api_key_here event-planner-mcp
```

## API Kullanımı

### Endpoint: `/events`
**Method:** POST  
**Content-Type:** application/json

#### İstek Formatı:
```json
{
    "city": "İstanbul",
    "date": "2024-12-25"
}
```

#### Yanıt Formatı:
```json
{
    "events": [
        {
            "title": "Etkinlik Adı",
            "date": "2024-12-25",
            "time": "20:00",
            "location": "Mekan Adı",
            "city": "İstanbul",
            "type": "Konser",
            "price": "100-200 TRY",
            "url": "https://ticketmaster.com/...",
            "description": "Etkinlik açıklaması"
        }
    ]
}
```

### Örnek Kullanım

```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"city": "İstanbul", "date": "2024-12-25"}'
```

## Özellikler

- ✅ Ticketmaster API entegrasyonu
- ✅ Şehir ve tarih bazlı etkinlik arama
- ✅ Fiyat bilgisi
- ✅ Mekan bilgisi
- ✅ Etkinlik kategorisi
- ✅ Hata yönetimi
- ✅ Docker desteği
- ✅ Environment variable desteği

## Notlar

- API key'inizi `.env` dosyasında saklayın
- Türkiye (TR) ülke kodu ile sınırlıdır
- Maksimum 20 etkinlik döndürür
- API hatası durumunda örnek veri döndürür
