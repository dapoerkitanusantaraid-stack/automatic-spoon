# 🚀 Production Deployment Guide

**Complete guide to deploying Project Server to production**

## Pre-Deployment Checklist

### Security Review
- [ ] All API endpoints require authentication
- [ ] HTTPS/TLS 1.3 enabled
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CSRF tokens implemented
- [ ] Security headers set
- [ ] Sensitive data not logged
- [ ] Encryption working correctly

### Database Preparation
- [ ] Run database initialization scripts
- [ ] Create backup database tables
- [ ] Set up database indexes
- [ ] Verify foreign key constraints
- [ ] Test backup/restore flow
- [ ] Verify encryption/decryption
- [ ] Test audit logging

### Environment Configuration
- [ ] `.env` file created with all secrets
- [ ] Database URLs configured
- [ ] API keys for Telegram/WhatsApp added
- [ ] JWT secret generated (32+ bytes)
- [ ] Encryption salt generated
- [ ] CORS origins configured
- [ ] Rate limiting thresholds set
- [ ] Email service configured (for notifications)

### Application Testing
- [ ] Unit tests passing (100% for critical paths)
- [ ] Integration tests passing
- [ ] Content CRUD working
- [ ] Customer management working
- [ ] Backup creation & restore working
- [ ] Permission system working
- [ ] Telegram bot responding
- [ ] WhatsApp bot responding
- [ ] Admin dashboard accessible
- [ ] Analytics endpoint working

## Step 1: Infrastructure Setup

### Option A: Self-Hosted (VPS)

#### Server Requirements
```
Ubuntu 22.04 LTS or 24.04 LTS
├─ CPU: 2+ cores (4 recommended)
├─ RAM: 4GB minimum (8GB recommended)
├─ Storage: 50GB minimum (for backups)
├─ Bandwidth: 10 Mbps+
└─ Network: Static IP address
```

#### Initial Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx (reverse proxy)
sudo apt install -y nginx certbot python3-certbot-nginx

# Create application directory
sudo mkdir -p /opt/project-server
sudo chown $USER:$USER /opt/project-server
cd /opt/project-server
```

### Option B: Cloud Platform (Recommended)

#### Railway.app (Most Beginner-Friendly)
```
1. Create account at railway.app
2. Connect GitHub repository
3. Configure environment variables
4. Deploy (automatic from git push)
5. Database automatically created
6. SSL included
7. Cost: ~$5-50/month depending on usage
```

#### Heroku (Legacy but stable)
```
1. Create account at heroku.com
2. Install Heroku CLI
3. heroku login
4. heroku create project-server
5. heroku config:set TELEGRAM_TOKEN=...
6. git push heroku main
7. Cost: ~$50+/month
```

#### AWS (Most Control)
```
1. Create EC2 instance (t3.medium)
2. RDS for PostgreSQL database
3. S3 for backup storage
4. CloudFront for CDN
5. Route53 for DNS
6. Application Load Balancer
7. Cost: $50-500+/month
```

#### DigitalOcean (Good Balance)
```
1. Create droplet ($6-24/month)
2. Use DigitalOcean Spaces for storage
3. DigitalOcean Database (PostgreSQL)
4. App Platform for auto-scaling
5. Cost: $12-100+/month
```

## Step 2: Environment Setup

### Create `.env` File

```bash
# Create secure .env file
nano /opt/project-server/.env

# Add all configuration
```

```env
# ============ CORE SETTINGS ============
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secure-32-byte-random-key-here-min-32-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# ============ DATABASE ============
DATABASE_URL=sqlite:///./data.db
BACKUP_DATABASE_URL=sqlite:///./backup.db
# OR for PostgreSQL (better for production)
# DATABASE_URL=postgresql://user:password@localhost/project_server
# BACKUP_DATABASE_URL=postgresql://user:password@localhost/project_server_backup

# ============ ENCRYPTION ============
ENCRYPTION_SALT=your-32-byte-random-salt-here
ENCRYPTION_PASSWORD=strong-password-for-backups

# ============ TELEGRAM ============
TELEGRAM_TOKEN=your-telegram-bot-token
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/telegram/webhook

# ============ WHATSAPP / TWILIO ============
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_NUMBER=+14155552671

# ============ INSTAGRAM ============
INSTAGRAM_USERNAME=your-instagram-username
INSTAGRAM_PASSWORD=your-instagram-password

# ============ FACEBOOK ============
FACEBOOK_ACCESS_TOKEN=your-facebook-token
FACEBOOK_PAGE_ID=your-page-id

# ============ SECURITY ============
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
MAX_UPLOAD_SIZE_MB=500
PASSWORD_MIN_LENGTH=12

# ============ EMAIL (for notifications) ============
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
NOTIFICATION_EMAIL=alerts@yourdomain.com

# ============ BACKUP SETTINGS ============
BACKUP_RETENTION_DAYS=365
AUTO_BACKUP_ENABLED=false
BACKUP_SCHEDULE_HOUR=2
BACKUP_SCHEDULE_MINUTE=0

# ============ MONITORING ============
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
LOG_LEVEL=INFO

# ============ API KEYS ============
ADMIN_API_KEY=admin-api-key-for-automation
```

### Generate Secure Strings

```bash
# Generate SECRET_KEY (32+ bytes)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_SALT (32 bytes)
python3 -c "import os; print(os.urandom(32).hex())"

# Example output:
# SECRET_KEY: AbCdEfGhIjKlMnOpQrStUvWxYz1234567890ABCDE
# SALT: a3f5b7c9e2d4f6h8j0k2m4n6p8q0s2t4v6w8x0y2z4
```

## Step 3: Database Migration

### SQLite (Development/Small Scale)

```bash
# Copy database files to production
scp data.db user@server:/opt/project-server/
scp backup.db user@server:/opt/project-server/

# Set permissions
ssh user@server
chmod 600 /opt/project-server/data.db
chmod 600 /opt/project-server/backup.db
```

### PostgreSQL (Production Recommended)

```bash
# On production server
sudo apt install postgresql postgresql-contrib

# Create databases
sudo -u postgres psql

postgres=# CREATE USER project_server WITH PASSWORD 'secure-password-here';
postgres=# ALTER ROLE project_server SET client_encoding TO 'utf8';
postgres=# ALTER ROLE project_server SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE project_server SET timezone TO 'UTC';
postgres=# CREATE DATABASE project_server OWNER project_server;
postgres=# CREATE DATABASE project_server_backup OWNER project_server;
postgres=# GRANT ALL PRIVILEGES ON DATABASE project_server TO project_server;
postgres=# GRANT ALL PRIVILEGES ON DATABASE project_server_backup TO project_server;
postgres=# \q

# Run migrations (in Docker container)
docker-compose exec api python init_database.py
```

## Step 4: Docker Setup

### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: project_server_api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data.db
      - BACKUP_DATABASE_URL=sqlite:///./backup.db
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "10"
    networks:
      - project_server

  nginx:
    image: nginx:latest
    container_name: project_server_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./static:/usr/share/nginx/html:ro
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - project_server

  postgres:
    image: postgres:15-alpine
    container_name: project_server_db
    environment:
      POSTGRES_DB: project_server
      POSTGRES_USER: project_server
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - project_server
    # Uncomment if using PostgreSQL
    # ports:
    #   - "5432:5432"

volumes:
  postgres_data:

networks:
  project_server:
    driver: bridge
```

### Create `nginx.conf`

```nginx
http {
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/h;

    # Upstream API server
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Rate limiting
        limit_req zone=api_limit burst=20 nodelay;

        # Proxy settings
        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 30s;
            proxy_connect_timeout 5s;
        }

        # Static files
        location /static/ {
            alias /usr/share/nginx/html/;
            expires 30d;
        }

        # Health check endpoint
        location /health {
            access_log off;
            proxy_pass http://api;
        }
    }
}

events {
    worker_connections 1024;
}
```

## Step 5: SSL/TLS Certificate

### Using Let's Encrypt (Free)

```bash
# On server with root access
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Verify installation
sudo certbot certificates

# Copy to Docker volume
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/project-server/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/project-server/ssl/key.pem
sudo chmod 644 /opt/project-server/ssl/*

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Using CloudFlare (Free)

```
1. Add domain to CloudFlare (free plan)
2. Set nameservers to CloudFlare
3. Enable "Flexible SSL" or "Full SSL"
4. CloudFlare handles certificate automatically
5. Cheaper and better DDoS protection
```

## Step 6: Deploy Application

### Deploy with Docker Compose

```bash
# On production server
cd /opt/project-server

# Pull latest code (if using git)
git pull origin main

# Build and start containers
docker-compose build
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Test API
curl https://yourdomain.com/health
```

### Health Check

```bash
# Test API is running
curl -s https://yourdomain.com/health | jq '.'

# Expected response:
# {
#   "status": "ok",
#   "version": "2.0.0",
#   "database": "connected"
# }
```

## Step 7: Monitoring & Maintenance

### Set Up Monitoring

#### Prometheus + Grafana
```yaml
# docker-compose.yml additions
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

#### Log Aggregation (ELK Stack)
```bash
# Elasticsearch for log storage
# Logstash for log processing
# Kibana for visualization
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Daily backup script

BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d)

# Backup database
docker exec project_server_db pg_dump project_server > $BACKUP_DIR/db_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

# Upload to S3
aws s3 cp $BACKUP_DIR/db_$DATE.sql.gz s3://your-backup-bucket/

echo "Backup completed: db_$DATE.sql.gz"
```

### Schedule with Cron

```bash
# Run backup daily at 2 AM
crontab -e

# Add line:
0 2 * * * /opt/project-server/backup.sh
```

## Step 8: Post-Deployment

### Verify Setup

```bash
# Test API endpoints
curl https://yourdomain.com/docs

# Test content creation
curl -X POST https://yourdomain.com/content \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","category":"General"}'

# Test backup system
curl https://yourdomain.com/backup/list/1

# Test Telegram
curl -X POST https://yourdomain.com/telegram/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id":123}'
```

### Configure Firebase/Push Notifications

```python
# server/notifications.py
from firebase_admin import messaging

def send_notification(device_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=device_token
    )
    response = messaging.send(message)
    return response
```

### Set Up Database Backups

```bash
# Automated PostgreSQL backups to S3
aws s3 sync /backups s3://your-backup-bucket/ --delete
```

## Troubleshooting

### Container Won't Start
```bash
docker logs project_server_api
docker inspect project_server_api
```

### Can't Connect to Database
```bash
docker-compose exec api python -c "import sqlite3; sqlite3.connect('data.db').close()"
```

### High Memory Usage
```bash
# Check which process uses memory
docker stats

# Limit memory in docker-compose.yml
services:
  api:
    mem_limit: 1g
    memswap_limit: 1g
```

### SSL Certificate Error
```bash
# Verify certificate
openssl s_client -connect yourdomain.com:443

# Check expiration
certbot certificates

# Renew manually
certbot renew --dry-run
```

## Production Checklist ✅

### Before Going Live
- [ ] Domain name registered
- [ ] SSL certificate installed
- [ ] Database backups configured
- [ ] Monitoring set up
- [ ] Admin user created
- [ ] Telegram bot token added
- [ ] WhatsApp credentials configured
- [ ] CORS origins correct
- [ ] Rate limiting set
- [ ] Email notifications working
- [ ] Backup system tested (create + restore)
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Compliance verified (GDPR/CCPA)
- [ ] Documentation updated
- [ ] Support contact configured
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] Status page created
- [ ] Automated backups running

### Day 1 After Launch
- [ ] Monitor error logs
- [ ] Check database growth
- [ ] Verify backup creation
- [ ] Test restore functionality
- [ ] Confirm email notifications
- [ ] Announce publicly
- [ ] Set up status page

### Weekly Maintenance
- [ ] Review security logs
- [ ] Check backup integrity
- [ ] Verify certificate renewal
- [ ] Monitor disk space
- [ ] Check application updates

### Monthly Maintenance
- [ ] Full security audit
- [ ] Database optimization
- [ ] Disaster recovery drill
- [ ] Update dependencies
- [ ] Review compliance reports

---

**Your Project Server is now production-ready! 🚀**

For support: support@yourdomain.com
For security issues: security@yourdomain.com
