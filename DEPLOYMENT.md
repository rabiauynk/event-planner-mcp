# Deployment Troubleshooting Guide

## ✅ Deployment Hatası Çözüldü!

### Yapılan İyileştirmeler

1. **Robust Startup Script**
   - `run.py` - Detaylı startup logging
   - Import error handling
   - Dependency checking

2. **Simplified App Structure**
   - Minimal import dependencies
   - Built-in API key (kod içinde gömülü)
   - Graceful error handling

3. **Enhanced Configuration**
   - `smithery.yaml` güncellendi
   - Health check endpoints
   - Production-ready settings

4. **Deployment Testing**
   - `test_deployment.py` - Deployment readiness testi
   - Automated verification

### Deployment için Environment Variables

**Artık gerekli değil!** API key kod içinde gömülü olarak gelir.

İsteğe bağlı olarak override etmek için:
```
TICKETMASTER_API_KEY=your_custom_api_key
```

### Test Endpoints

1. **Health Check**
```bash
GET /health
```

2. **Status Check**
```bash
GET /
```

3. **Events API**
```bash
POST /events
Content-Type: application/json
{
  "city": "İstanbul",
  "date": "2024-12-25"
}
```

### Deployment Platform Ayarları

#### GitHub Actions / Vercel / Heroku
Environment Variables artık gerekli değil! Doğrudan deploy edebilirsiniz.

İsteğe bağlı:
- `FLASK_ENV`: `production`

#### Docker Deployment
```bash
docker run -p 5000:5000 event-planner-mcp
```

API key kod içinde gömülü olduğu için environment variable gerekli değil.

### Troubleshooting

1. **"Unexpected internal error"**
   - Environment variable eksik olabilir
   - Health check endpoint'ini test edin: `/health`

2. **API Key Status Kontrolü**
   - Ana endpoint'i kontrol edin: `/`
   - `api_key_status` field'ını kontrol edin

3. **Timeout Issues**
   - Health check 30 saniye interval ile çalışır
   - Start period 5 saniye olarak ayarlandı

### Deployment Sonrası Test

```bash
# Health check
curl https://your-deployment-url/health

# Status check
curl https://your-deployment-url/

# API test
curl -X POST https://your-deployment-url/events \
  -H "Content-Type: application/json" \
  -d '{"city": "İstanbul", "date": "2024-12-25"}'
```
