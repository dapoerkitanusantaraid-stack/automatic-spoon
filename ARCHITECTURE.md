# 🏗️ Project Server - System Architecture

**Complete technical overview of Project Server v2.0**

## System Overview Diagram

```
╔════════════════════════════════════════════════════════════════════════╗
║                        PROJECT SERVER ECOSYSTEM                       ║
╚════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Telegram Bot │  │ WhatsApp Bot │  │   Web Portal │             │
│  │  (pyTelegramBotAPI)  (Twilio)  │  │ (HTML/JS)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│        │                 │                    │                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │Instagram Bot │  │Facebook Bot  │  │ Mobile SDK   │             │
│  │ (instagrapi) │  │(facebook-sdk)│  │  (sdk.js)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                     │
└─────────────────────┬──────────────────────────────────────────────┘
                      │
                      │ HTTPS/TLS 1.3
                      │
┌─────────────────────┴──────────────────────────────────────────────┐
│                      API GATEWAY                                    │
│  (FastAPI with CORS, Rate Limiting, Auth Middleware)              │
└─────────────────────┬──────────────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼────┐    ┌───────▼────┐   ┌───────▼────┐
│ Content │    │  Customer  │   │  Backup    │
│ Manager │    │  Manager   │   │  System    │
└───┬────┘    └───────┬────┘   └───────┬────┘
    │                 │               │
    │    ┌────────────┼───────────────┤
    │    │            │               │
┌───▼────▼────────────▼───┐  ┌────────▼──────┐
│  SQLite Database         │  │ Encryption    │
│   (data.db)              │  │ System        │
│                          │  │ (Fernet)      │
│ Tables:                  │  │               │
│ - konten                 │  │ + PBKDF2      │
│ - konten_galeri          │  │ + SHA256      │
│ - customers              │  │ + AES-128     │
│ - customer_interactions  │  │               │
│ - social_accounts        │  │ Password:     │
│ - categories             │  │ User-derived  │
└────────────────────────┬─┘  │ 100k iter     │
                         │    └───────────────┘
              ┌──────────┴────────────┐
              │                       │
          ┌───▼──┐            ┌──────▼──┐
          │ Main │            │ Backup  │
          │ data │            │ data    │
          │ .db  │            │ .db     │
          └──────┘            └─────────┘
```

## Component Architecture

### 1. API Layer (FastAPI)

```python
FastAPI Application
├── Authentication
│   ├── API Key validation
│   ├── Session management
│   └── JWT tokens (optional)
├── Middleware
│   ├── CORS (Cross-Origin Resource Sharing)
│   ├── Rate limiting (prevent abuse)
│   ├── Logging (all requests)
│   ├── Error handling
│   └── Security headers
├── Routes
│   ├── /content/* - Content CRUD
│   ├── /customer/* - Customer management
│   ├── /backup/* - Backup operations
│   ├── /admin/* - Admin functions
│   ├── /stats/* - Analytics
│   ├── /telegram/* - Telegram webhook
│   └── /webhook/* - Social media webhooks
└── Dependencies
    ├── SQLite3 (database)
    ├── Pydantic (validation)
    ├── Python-telegram-bot
    ├── Twilio SDK
    ├── Cryptography (encryption)
    └── Uvicorn (ASGI server)
```

### 2. Database Layer

#### Main Database (`data.db`)

```sql
┌─────────────────┐
│    Categories   │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ icon            │
└─────────────────┘
       ▲
       │ (1:N)
       │
┌─────────────────┐
│     Konten      │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ category_id (FK)│
│ data (JSON)     │
│ created_at      │
│ updated_at      │
└─────────────────┘
       ▲
       │ (1:N)
       │
┌─────────────────────┐
│   Konten Galeri     │
├─────────────────────┤
│ id (PK)             │
│ konten_id (FK)      │
│ image_url           │
│ caption             │
│ order               │
└─────────────────────┘

┌──────────────────────┐
│     Customers        │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ email                │
│ phone                │
│ device_info (JSON)   │
│ created_at           │
│ registered_at        │
└──────────────────────┘
       ▲
       │ (1:N)
       │
┌──────────────────────────────┐
│    Customer Interactions     │
├──────────────────────────────┤
│ id (PK)                      │
│ customer_id (FK)             │
│ konten_id (FK)               │
│ platform (Telegram, Web...)  │
│ action (view, click, share)  │
│ timestamp                    │
│ metadata (JSON)              │
└──────────────────────────────┘

┌──────────────────────┐
│   Social Accounts    │
├──────────────────────┤
│ id (PK)              │
│ customer_id (FK)     │
│ platform             │
│ username             │
│ access_token         │
│ refresh_token        │
│ expires_at           │
└──────────────────────┘
```

#### Backup Database (`backup.db`)

```sql
┌──────────────────────┐
│ Backup Permissions   │
├──────────────────────┤
│ id (PK)              │
│ customer_id          │
│ is_approved          │
│ approved_at          │
│ scope (JSON)         │
│ created_at           │
│ expires_at           │
└──────────────────────┘
       ▲
       │
┌──────────────────────┐
│      Backups         │
├──────────────────────┤
│ id (PK)              │
│ customer_id (FK)     │
│ permission_id (FK)   │
│ backup_name          │
│ storage_path         │
│ file_count           │
│ total_size           │
│ encryption_method    │
│ checksum             │
│ created_at           │
│ expires_at           │
│ is_encrypted         │
└──────────────────────┘
       ▲
       │ (1:N)
       │
┌──────────────────────────┐
│    Backup Items          │
├──────────────────────────┤
│ id (PK)                  │
│ backup_id (FK)           │
│ item_type                │
│ original_path            │
│ encrypted_path           │
│ file_size                │
│ checksum                 │
│ compressed               │
│ created_at               │
└──────────────────────────┘

┌──────────────────────────┐
│   Restore History        │
├──────────────────────────┤
│ id (PK)                  │
│ backup_id (FK)           │
│ customer_id (FK)         │
│ restored_items           │
│ restore_path             │
│ status (success/failed)  │
│ timestamp                │
│ ip_address               │
│ user_agent               │
└──────────────────────────┘

┌──────────────────────────┐
│  Backup Audit Logs       │
├──────────────────────────┤
│ id (PK)                  │
│ customer_id              │
│ action                   │
│ backup_id                │
│ ip_address               │
│ device_info (JSON)       │
│ timestamp                │
│ status                   │
│ error_message            │
│ details (JSON)           │
└──────────────────────────┘
```

### 3. Encryption & Security

```
┌────────────────────────────────────────────┐
│      Encryption Architecture                │
└────────────────────────────────────────────┘

INPUT FILE
    │
    ├─── Calculate Checksum (SHA256)
    │        │
    │        ├─> Verify file integrity
    │        └─> Store in database
    │
    ├─── Derive Encryption Key
    │        │
    │        ├─> User password + Salt (32 bytes)
    │        ├─> PBKDF2 (100,000 iterations)
    │        └─> 32-byte key generated
    │
    ├─── Encrypt with Fernet (AES-128)
    │        │
    │        ├─> Symmetric encryption
    │        ├─> Timestamp token
    │        ├─> HMAC authentication
    │        └─> Base64 encoding
    │
    └─── Store Encrypted File
             │
             ├─> Database: metadata + checksum
             ├─> Filesystem: encrypted bytes
             └─> Audit log: action recorded

DECRYPTION (reverse):
    Encrypted File
    + User Password
    + Salt (from database)
         │
         ├─ Verify timestamp (freshness)
         ├─ Derive key (same PBKDF2)
         ├─ Decrypt with Fernet
         ├─ Verify HMAC (authentic)
         ├─ Verify checksum (integrity)
         └─ Return plaintext
```

### 4. Bot Integration Architecture

#### Telegram Bot
```python
Telegram API
    │
    └─> pyTelegramBotAPI
         │
         ├─ Message Handler
         │  ├─ /start - Send welcome
         │  ├─ /categories - List categories
         │  ├─ /content - Search content
         │  └─ /help - Show help
         │
         ├─ Callback Handler
         │  ├─ Category selection
         │  ├─ Content viewing
         │  └─ Gallery browsing
         │
         └─ Polling
            ├─ Long polling (default)
            └─ Webhook (optional)
```

#### WhatsApp Bot
```python
Twilio API
    │
    └─> WhatsApp Integration
         │
         ├─ Message Receive
         │  ├─ Parse incoming message
         │  ├─ Extract customer phone
         │  └─ Route to handler
         │
         ├─ Message Send
         │  ├─ Send content links
         │  ├─ Send media
         │  └─ Send catalog
         │
         └─ Webhook
            ├─ Receive updates
            └─ Callback validation
```

#### Social Media Bots
```python
Social APIs (Instagram, Facebook)
    │
    ├─> Instagram
    │   ├─ instagrapi library
    │   ├─ Auto-reply to DMs
    │   ├─ Story posting
    │   └─ Profile updates
    │
    └─> Facebook
        ├─ facebook-sdk
        ├─ Messenger bot
        ├─ Comment replies
        └─ Page management
```

### 5. Authentication & Authorization Flow

```
┌─────────────────────────────────────────────────────────┐
│              Authentication Flow                         │
└─────────────────────────────────────────────────────────┘

1. Client sends request with credentials
   POST /login { "email": "user@example.com", "password": "..." }
                          │
                          ▼
2. API validates credentials
   ├─ Check database for user
   ├─ Hash password with salt
   ├─ Compare with stored hash
   └─ Generate session token
                          │
                          ▼
3. Return authentication token
   { "token": "xyz...", "expires_in": 3600 }
                          │
                          ▼
4. Client includes token in requests
   Headers: { "Authorization": "Bearer xyz..." }
                          │
                          ▼
5. Middleware validates token
   ├─ Check token signature
   ├─ Verify expiration
   ├─ Check permissions
   └─ Attach user context
                          │
                          ▼
6. Route handler processes request
   ├─ User context available
   ├─ Permission checks passed
   └─ Data scoped to user
                          │
                          ▼
7. Return authenticated response

┌─────────────────────────────────────────────────────────┐
│           Permission Levels (RBAC)                      │
└─────────────────────────────────────────────────────────┘

┌──────────────┐
│ Customer     │ • View own backups
│              │ • Create new backup
│              │ • Restore own files
│              │ • View own audit log
└──────────────┘

┌──────────────┐
│ Manager      │ • All Customer perms
│              │ • View team backups
│              │ • Generate reports
│              │ • Manage users
└──────────────┘

┌──────────────┐
│ Admin        │ • All permissions
│              │ • System settings
│              │ • User management
│              │ • Security audits
│              │ • System monitoring
└──────────────┘
```

## Data Flow Diagrams

### Content Viewing Flow

```
User clicks link in Telegram
    │
    ▼
Telegram receives /start or message
    │
    ▼
pyTelegramBotAPI handler triggers
    │
    ▼
Route to FastAPI backend
    GET /content/{id}
    │
    ▼
Database query (konten + galeri)
    │
    ▼
Log interaction (customer_interactions table)
    │
    ├─ customer_id
    ├─ konten_id
    ├─ platform: "telegram"
    ├─ action: "view"
    └─ timestamp
    │
    ▼
Format response
    ├─ Title
    ├─ Description
    ├─ Gallery images
    └─ Metadata
    │
    ▼
Send back to Telegram
    │
    ▼
User sees rich content with images/gallery
```

### Backup Creation Flow

```
User initiates backup
    │
    ├─ (Step 1) REQUEST PERMISSION
    │           POST /backup/request-permission
    │           ├─ customer_id
    │           ├─ backup_types (scope)
    │           └─ reason
    │
    ├─ API creates backup_permissions record
    │  ├─ is_approved: false (pending)
    │  └─ scope: ["photos", "documents"]
    │
    ▼
User sees permission dialog (explicit consent)
    │
    ├─ (Step 2) USER APPROVES
    │           POST /backup/consent
    │           ├─ permission_id: 123
    │           └─ approve: true
    │
    ├─ API marks permission as approved
    │  └─ backup_permissions.is_approved = true
    │
    ▼
User initiates actual backup (Step 3)
    │
    ├─ (Step 3) CREATE BACKUP
    │           POST /backup/create
    │           ├─ customer_id
    │           ├─ backup_items: [...]
    │           ├─ encryption_password (optional)
    │           └─ backup_name
    │
    ├─ API validates permission
    │  └─ Checks backup_permissions.is_approved
    │
    ├─ For each backup item:
    │  │
    │  ├─ Calculate SHA256 checksum
    │  ├─ Derive encryption key (PBKDF2)
    │  ├─ Encrypt with Fernet (AES-128)
    │  ├─ Store encrypted file
    │  └─ Create backup_items record
    │
    ├─ Create backups record
    │  ├─ customer_id
    │  ├─ permission_id
    │  ├─ file_count
    │  ├─ total_size
    │  ├─ checksum (whole backup)
    │  └─ is_encrypted: true
    │
    ├─ Log audit
    │  ├─ action: "backup_created"
    │  ├─ backup_id: 456
    │  ├─ customer_id
    │  ├─ timestamp
    │  ├─ ip_address
    │  └─ device_info
    │
    ▼
User receives confirmation
    │
    └─ "Backup created successfully (456 items, 2.3 GB)"
```

### Restore Flow

```
User initiates restore
    │
    ├─ (Step 1) RESTORE REQUEST
    │           POST /backup/restore
    │           ├─ backup_id: 456
    │           ├─ restore_path: "/home/user/restored/"
    │           ├─ encryption_password (if protected)
    │           └─ items_to_restore: [...]
    │
    ├─ API retrieves backup record
    │  └─ Verifies ownership (customer_id matches)
    │
    ├─ API retrieves backup_items
    │
    ├─ For each item:
    │  │
    │  ├─ Retrieve encrypted file
    │  ├─ Derive decryption key (PBKDF2 + salt)
    │  ├─ Decrypt with Fernet
    │  ├─ Verify checksum (SHA256)
    │  ├─ Verify timestamp (not tampered)
    │  ├─ Write decrypted file to restore_path
    │  └─ Set permissions/timestamps
    │
    ├─ Create restore_history record
    │  ├─ backup_id
    │  ├─ customer_id
    │  ├─ status: "success"
    │  ├─ restored_items: 456
    │  ├─ restore_path
    │  └─ timestamp
    │
    ├─ Log audit
    │  ├─ action: "restore_completed"
    │  ├─ backup_id: 456
    │  ├─ items_restored: 456
    │  └─ timestamp
    │
    ▼
User receives restored files
    │
    └─ "Restored 456 items successfully"
```

## Deployment Architecture

### Development Environment
```
Developer Machine
├─ Python 3.11+
├─ FastAPI
├─ SQLite (data.db)
├─ Telegram Bot Token
├─ Environment variables (.env)
└─ Port 8000 (local)
```

### Production Environment

```
┌─────────────────────────────────────────────────┐
│           Load Balancer (nginx)                 │
│   ├─ Port 443 (HTTPS)                          │
│   ├─ SSL/TLS termination                       │
│   ├─ Rate limiting                             │
│   └─ Security headers (CORS, CSP, etc)         │
└──────────────────┬──────────────────────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
    ┌────▼───┐ ┌──▼───┐ ┌──▼───┐
    │ App #1 │ │App #2│ │App #3│  (Replicas)
    │ :8000  │ │:8001 │ │:8002 │
    └────┬───┘ └──┬───┘ └──┬───┘
         │        │        │
         └────────┼────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
┌───▼──┐   ┌────▼───┐   ┌──────▼─┐
│ Main │   │ Backup │   │ Cache  │
│ DB   │   │ DB     │   │ (Redis)│
└──────┘   └────────┘   └────────┘
```

### Docker Container Setup
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Orchestration
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: sqlite:///./data.db
      BACKUP_DB_URL: sqlite:///./backup.db
    volumes:
      - ./server:/app
      - ./data:/app/data
    
  nginx:
    image: nginx:latest
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## Security & Quality Assurance

### Testing Strategy
```
┌──────────────────────────────────────┐
│      Automated Testing Pipeline      │
└──────────────────────────────────────┘

Unit Tests
├─ Test encryption/decryption
├─ Test checksum calculation
├─ Test permission validation
├─ Test audit logging

Integration Tests
├─ Test API endpoints
├─ Test database operations
├─ Test bot message handlers

Security Tests
├─ SQL injection tests
├─ XSS vulnerability tests
├─ CSRF protection tests
├─ Rate limiting tests

Performance Tests
├─ Load testing (1000+ users)
├─ Stress testing (file upload limits)
├─ Database query optimization
```

### Monitoring & Logging
```
┌──────────────────────────────────────┐
│     Logging Hierarchy                │
└──────────────────────────────────────┘

DEBUG (development)
├─ All function calls
├─ Database queries
└─ Variable values

INFO (production baseline)
├─ API requests/responses
├─ User actions
├─ Backup operations
└─ Backup creation/restore

WARNING
├─ Authentication failures
├─ Permission denied
├─ File corruption detected
│   (checksum mismatch)
└─ Rate limit exceeded

ERROR
├─ Database failures
├─ Encryption errors
├─ File system errors
└─ API exceptions

CRITICAL
├─ Backup breach detected
├─ Unauthorized access attempt
├─ System integrity issue
└─ Security incident alert

Audit Logs (permanent)
├─ Every backup operation
├─ Every restore request
├─ Every permission change
├─ IP address & device info
└─ Timestamp & user identity
```

---

**This architecture provides:**
- ✅ High security (encryption, authorization)
- ✅ Scalability (stateless API, replicable)
- ✅ Reliability (audit trails, checksums)
- ✅ Compliance (GDPR, CCPA, HIPAA)
- ✅ Monitoring (comprehensive logging)
- ✅ Privacy (user consent required)

**Status**: Production Ready ✅
