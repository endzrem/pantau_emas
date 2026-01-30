# Production Configuration Guide

## Security Checklist for Production Deployment

### 1. Disable Debug Mode
Set environment variable:
```bash
export FLASK_DEBUG=False
```

Or modify `app.py` directly to set `debug=False`.

### 2. Use Production WSGI Server
Don't use Flask's built-in server in production. Use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Add Authentication
Protect the `/api/train-model` endpoint with authentication:
- Implement API key authentication
- Use OAuth2 or JWT tokens
- Add rate limiting

### 4. Configure HTTPS
- Use a reverse proxy (nginx, Apache)
- Obtain SSL certificate (Let's Encrypt)
- Redirect HTTP to HTTPS

### 5. Use Database for Price History
Replace in-memory storage with a proper database:
- PostgreSQL for production
- Redis for caching
- Implement proper data persistence

### 6. Environment Variables
Store sensitive configuration in environment variables:
```bash
export SECRET_KEY='your-secret-key'
export DATABASE_URL='postgresql://...'
export ALLOWED_HOSTS='your-domain.com'
```

### 7. Add Rate Limiting
Implement rate limiting to prevent abuse:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/predict')
@limiter.limit("10 per minute")
def predict_price():
    # ...
```

### 8. Monitor and Log
- Set up proper logging (not print statements)
- Use application monitoring (Sentry, New Relic)
- Monitor resource usage

### 9. Backup Strategy
- Regular database backups
- Model file versioning
- Disaster recovery plan

### 10. Update Dependencies
Regularly update dependencies to patch security vulnerabilities:
```bash
pip install --upgrade -r requirements.txt
```

## Example Production Configuration

### Using Gunicorn with systemd

Create `/etc/systemd/system/pantau-emas.service`:
```ini
[Unit]
Description=Pantau Emas Gold Price Prediction
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pantau_emas
Environment="FLASK_DEBUG=False"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/pantau-emas`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_DEBUG=False
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t pantau-emas .
docker run -p 5000:5000 -e FLASK_DEBUG=False pantau-emas
```
