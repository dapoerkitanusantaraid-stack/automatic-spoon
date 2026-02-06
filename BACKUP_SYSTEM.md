# 🔒 Backup System - Secure Cloud Backup with Consent

Sistem backup yang aman dan ethical untuk memungkinkan user backup data mereka sendiri dengan **explicit permission dan consent**.

## ✨ Key Features

### 🔐 Security
- ✅ **Explicit Consent Required** - User HARUS approve sebelum backup bisa berjalan
- ✅ **File Encryption** - Optional password-protected encryption dengan Fernet
- ✅ **Checksum Verification** - SHA256 checksum untuk verify integrity
- ✅ **Audit Logging** - Semua aktivitas tercatat dengan timestamp, IP, device info
- ✅ **Access Control** - Hanya customer sendiri yang bisa restore backup mereka

### 👤 Privacy First
- ✅ **User-Initiated** - Backup hanya dimulai oleh user sendiri
- ✅ **Transparent** - User tahu persis apa yang di-backup
- ✅ **Revocable** - User bisa disable backup kapan saja
- ✅ **No Sneaking** - Tidak ada background collection
- ✅ **Legal Compliance** - Sesuai GDPR, CCPA, dan regulasi privacy lainnya

### 📊 Full Audit Trail
- ✅ Who accessed backup
- ✅ When it was accessed  
- ✅ From which device/IP
- ✅ What action was performed
- ✅ Success or failure status

## 🏗️ System Architecture

### Database Tables

```
backup_permissions
├── id
├── customer_id (UNIQUE)
├── backup_enabled (boolean)
├── backup_types (JSON array)
├── consent_timestamp
├── consent_ip
└── consent_device

backups
├── id
├── customer_id
├── backup_name
├── created_timestamp
├── size_bytes
├── file_count
├── encrypted (boolean)
├── backup_types (JSON)
├── status
└── storage_path

backup_items
├── id
├── backup_id
├── file_name
├── file_type (photo|document|contact|settings)
├── file_size
├── encrypted
├── checksum (SHA256)
├── original_path
├── stored_path
└── metadata (JSON)

restore_history
├── id
├── backup_id
├── customer_id
├── restored_timestamp
├── restore_type
├── ip_address
├── device_info
└── success (boolean)

backup_audit_logs
├── id
├── customer_id
├── action (backup_created|backup_restored|backup_deleted|consent_given)
├── timestamp
├── ip_address
├── device_info
├── backup_id
└── details
```

## 📡 API Endpoints

### 1. Request Backup Permission
```bash
POST /backup/request-permission
{
  "customer_id": 123,
  "backup_types": ["photos", "documents", "contacts"],
  "ip_address": "192.168.1.1",
  "device_info": {...}
}

Response: {
  "status": "permission_requested",
  "message": "Backup permission request sent to customer",
  "requires_consent": true
}
```

### 2. Customer Approves Backup (Explicit Consent)
```bash
POST /backup/consent
{
  "customer_id": 123,
  "backup_types": ["photos", "documents"],
  "ip_address": "192.168.1.1",
  "device_info": {...}
}

Response: {
  "status": "success",
  "message": "Backup enabled",
  "backup_types": ["photos", "documents"],
  "enabled": true
}
```

### 3. Get Backup Permission Status
```bash
GET /backup/permission/{customer_id}

Response: {
  "customer_id": 123,
  "backup_enabled": true,
  "backup_types": ["photos", "documents"],
  "consent_timestamp": "2026-02-06T10:00:00",
  "consent_ip": "192.168.1.1"
}
```

### 4. Create Backup
```bash
POST /backup/create
{
  "customer_id": 123,
  "backup_name": "backup_20260206",
  "backup_types": ["photos"],
  "files": {
    "photos": [
      {
        "name": "photo1.jpg",
        "path": "/path/to/photo1.jpg",
        "metadata": {"size": 2048, "date": "2026-01-01"}
      }
    ]
  },
  "password": "user_password_optional",
  "ip_address": "192.168.1.1",
  "device_info": {...}
}

Response: {
  "status": "success",
  "backup_id": 42,
  "backup_name": "backup_20260206",
  "file_count": 150,
  "total_size": 524288000,
  "message": "Backup created successfully"
}
```

### 5. Get Backup List (Private)
```bash
GET /backup/list/{customer_id}

Response: {
  "customer_id": 123,
  "total": 3,
  "backups": [
    {
      "id": 42,
      "backup_name": "backup_20260206",
      "created_timestamp": "2026-02-06T10:00:00",
      "size_bytes": 524288000,
      "file_count": 150,
      "encrypted": true,
      "backup_types": ["photos"],
      "status": "completed"
    }
  ]
}
```

### 6. Restore Backup
```bash
POST /backup/restore
{
  "backup_id": 42,
  "customer_id": 123,
  "password": "user_password",
  "ip_address": "192.168.1.1",
  "device_info": {...}
}

Response: {
  "status": "success",
  "message": "Restored 150 files",
  "restore_folder": "restores/123/20260206_100500",
  "restored_count": 150
}
```

### 7. Get Audit Logs
```bash
GET /backup/audit/{customer_id}

Response: {
  "customer_id": 123,
  "total_logs": 42,
  "logs": [
    {
      "id": 1,
      "customer_id": 123,
      "action": "backup_created",
      "timestamp": "2026-02-06T10:00:00",
      "ip_address": "192.168.1.1",
      "device_info": {...},
      "backup_id": 42,
      "details": "Created backup with 150 files, 524288000 bytes"
    },
    {
      "id": 2,
      "customer_id": 123,
      "action": "backup_consent_given",
      "timestamp": "2026-02-06T09:50:00",
      "ip_address": "192.168.1.1",
      "device_info": {...}
    }
  ]
}
```

### 8. Delete Backup
```bash
DELETE /backup/{backup_id}?customer_id=123

Response: {
  "status": "success",
  "message": "Backup berhasil dihapus"
}
```

## 🔑 Backup Types Supported

```python
backup_types = [
    "photos",      # Image files
    "documents",   # PDFs, DOCs, etc
    "contacts",    # Contact list
    "settings",    # App settings & preferences
    "messages",    # Chat messages (optional)
    "calendar",    # Calendar events
    "media"        # Audio files
]
```

## 🔐 Security Implementation

### 1. Permission System
```python
# User harus explicitly approve
def customer_consent_backup(customer_id, backup_types):
    # Only user dengan authenticated session bisa approve
    # Recorded in audit_logs dengan timestamp
    # Cannot be done by admin/third party
```

### 2. Encryption
```python
# Optional password-protected encryption
from cryptography.fernet import Fernet

# Files encrypted dengan Fernet (AES128)
# Key derived from user password dengan PBKDF2
# SHA256 checksum untuk integrity
```

### 3. Checksum Verification
```python
# SHA256 untuk verify file integrity
backup_file_checksum = SHA256(file_content)

# On restore, verify:
# checksum_match = SHA256(restored_file) == backup_checksum
```

### 4. Audit Trail
```
Setiap action dicatat:
- backup_created
- backup_restored  
- backup_deleted
- consent_given
- consent_revoked

Dengan:
- Timestamp
- IP Address
- Device Info
- User Agent
- Action Details
```

## 📱 Frontend Integration Example

```html
<!-- Request Backup -->
<button onclick="requestBackup()">Enable Backup</button>

<script>
async function requestBackup() {
  // Show permission dialog
  const response = await fetch('/backup/request-permission', {
    method: 'POST',
    body: JSON.stringify({
      customer_id: currentUser.id,
      backup_types: ['photos', 'documents'],
      device_info: getDeviceInfo()
    })
  });
}

// User clicks APPROVE button
async function approveBackup() {
  const response = await fetch('/backup/consent', {
    method: 'POST',
    body: JSON.stringify({
      customer_id: currentUser.id,
      backup_types: ['photos', 'documents'],
      device_info: getDeviceInfo()
    })
  });
  
  // Then create backup
  createBackup();
}

// Create backup
async function createBackup() {
  const response = await fetch('/backup/create', {
    method: 'POST',
    body: JSON.stringify({
      customer_id: currentUser.id,
      backup_name: `backup_${new Date().toISOString()}`,
      backup_types: ['photos'],
      files: {...},
      password: getUserPassword(),
      device_info: getDeviceInfo()
    })
  });
}
</script>
```

## 🛡️ Privacy Guarantees

### What We DO:
✅ Only backup what user explicitly selected  
✅ Encrypt files with user password  
✅ Store with GDPR compliance  
✅ Log all access & restore attempts  
✅ Allow user to delete anytime  
✅ Provide full transparency via audit logs  

### What We DON'T:
❌ Backup without explicit consent  
❌ Store login credentials  
❌ Track location without permission  
❌ Access camera/microphone  
❌ Sell data to third parties  
❌ Use for marketing without consent  
❌ Decrypt without user password  

## 📊 Use Cases

### 1. Personal Backup
```
User backs up:
- Photos & memories
- Important documents
- Contact list
```

### 2. Business Backup
```
Company backs up:
- Work documents
- Client files
- Project assets
```

### 3. Data Recovery
```
User lost phone?
- Restore from backup
- All data recovered
- Encrypted & safe
```

## 🔍 Compliance

### GDPR (European Union)
- ✅ Explicit consent required
- ✅ Right to access all data
- ✅ Right to delete (right to be forgotten)
- ✅ Data portability supported
- ✅ Privacy by design

### CCPA (California)
- ✅ Consumer right to know
- ✅ Consumer right to delete
- ✅ Consumer right to opt-out
- ✅ Non-disclosure of personal info

### HIPAA (Healthcare - if applicable)
- ✅ Encryption at rest & in transit
- ✅ Access controls & audit logs
- ✅ Business associate agreements
- ✅ Data integrity & authenticity

## 📋 Monitoring & Alerts

### Admin Dashboard Shows:
```
Backup Statistics:
- Total backups created
- Total storage used
- Backup success rate
- Most backed up file types

Security Monitoring:
- Failed restore attempts
- Unusual access patterns
- Large backup requests
- Geographic anomalies
```

## 🚨 Disaster Recovery

### If Backup Corrupted:
```
1. Checksum verification fails
2. Error logged to audit trail
3. User notified immediately
4. Multiple backups kept (versioning)
5. Previous version available
```

### If User Forgot Password:
```
1. No backdoor access
2. Must go through identity verification
3. Backup deleted (cannot decrypt)
4. User directed to create new backup
5. Process logged
```

## 💡 Best Practices

### For Users:
1. ✅ Use strong password if encrypting
2. ✅ Backup regularly (weekly/monthly)
3. ✅ Keep multiple backup versions
4. ✅ Review audit logs periodically
5. ✅ Delete old backups
6. ✅ Test restore before you need it

### For Administrators:
1. ✅ Monitor backup size trends
2. ✅ Check audit logs for anomalies
3. ✅ Ensure encryption enabled
4. ✅ Regular database backups
5. ✅ Implement data retention policy
6. ✅ Staff training on privacy

## 📞 Support

For users:
- How to enable backup
- How to restore files
- Password recovery
- Backup troubleshooting

For admins:
- Storage management
- User audit trail
- Compliance reports
- Security alerts

---

**Version**: 1.0
**Status**: Secure & Compliant ✅
**Last Updated**: February 6, 2026

🔐 **Privacy is a fundamental right. This system respects it.**
