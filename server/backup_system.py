"""
Backup System - Secure Cloud Backup with User Consent
Fitur untuk memungkinkan user backup data mereka sendiri dengan permission eksplisit
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os
import json
from datetime import datetime
import hashlib
from pathlib import Path

# ======================== Models ========================

class BackupPermission(BaseModel):
    """Model untuk backup permission - user must consent"""
    customer_id: int
    backup_enabled: bool
    backup_types: List[str]  # ['photos', 'documents', 'contacts', 'settings']
    consent_timestamp: str
    consent_ip: str
    consent_device: str

class BackupItem(BaseModel):
    """Individual backup item"""
    file_name: str
    file_type: str  # 'photo', 'document', 'contact', 'message', 'settings'
    file_size: int
    encrypted: bool
    checksum: str
    backup_timestamp: str
    metadata: Optional[dict] = None

class BackupRestoreRequest(BaseModel):
    """Request to restore backup"""
    backup_id: int
    customer_id: int
    restore_type: str
    password: str  # Require password to restore

class BackupAuditLog(BaseModel):
    """Audit log untuk setiap backup action"""
    customer_id: int
    action: str  # 'backup_created', 'backup_restored', 'backup_deleted'
    timestamp: str
    ip_address: str
    device_info: dict
    backup_id: Optional[int] = None

# ======================== Database Setup ========================

def init_backup_db():
    """Initialize backup system database tables"""
    conn = sqlite3.connect('backup.db')
    c = conn.cursor()
    
    # Backup permissions table
    c.execute('''CREATE TABLE IF NOT EXISTS backup_permissions
                 (id INTEGER PRIMARY KEY,
                  customer_id INTEGER UNIQUE,
                  backup_enabled BOOLEAN,
                  backup_types TEXT,
                  consent_timestamp TEXT,
                  consent_ip TEXT,
                  consent_device TEXT,
                  FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    
    # Backups table
    c.execute('''CREATE TABLE IF NOT EXISTS backups
                 (id INTEGER PRIMARY KEY,
                  customer_id INTEGER,
                  backup_name TEXT,
                  created_timestamp TEXT,
                  size_bytes INTEGER,
                  file_count INTEGER,
                  encrypted BOOLEAN,
                  backup_types TEXT,
                  status TEXT,
                  storage_path TEXT,
                  FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    
    # Backup items table
    c.execute('''CREATE TABLE IF NOT EXISTS backup_items
                 (id INTEGER PRIMARY KEY,
                  backup_id INTEGER,
                  file_name TEXT,
                  file_type TEXT,
                  file_size INTEGER,
                  encrypted BOOLEAN,
                  checksum TEXT,
                  original_path TEXT,
                  stored_path TEXT,
                  metadata TEXT,
                  FOREIGN KEY(backup_id) REFERENCES backups(id))''')
    
    # Restore history table
    c.execute('''CREATE TABLE IF NOT EXISTS restore_history
                 (id INTEGER PRIMARY KEY,
                  backup_id INTEGER,
                  customer_id INTEGER,
                  restored_timestamp TEXT,
                  restore_type TEXT,
                  ip_address TEXT,
                  device_info TEXT,
                  success BOOLEAN,
                  FOREIGN KEY(backup_id) REFERENCES backups(id),
                  FOREIGN KEY(customer_id) REFERENCES customers(id))''')
    
    # Audit logs table
    c.execute('''CREATE TABLE IF NOT EXISTS backup_audit_logs
                 (id INTEGER PRIMARY KEY,
                  customer_id INTEGER,
                  action TEXT,
                  timestamp TEXT,
                  ip_address TEXT,
                  device_info TEXT,
                  backup_id INTEGER,
                  details TEXT,
                  FOREIGN KEY(customer_id) REFERENCES customers(id),
                  FOREIGN KEY(backup_id) REFERENCES backups(id))''')
    
    conn.commit()
    conn.close()

# ======================== Helper Functions ========================

def get_backup_db():
    """Get database connection"""
    conn = sqlite3.connect('backup.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_checksum(file_path: str) -> str:
    """Calculate SHA256 checksum of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def encrypt_file(file_path: str, password: str) -> str:
    """
    Encrypt file with password
    Note: Ini adalah contoh sederhana. Untuk production gunakan library encryption proper
    """
    try:
        from cryptography.fernet import Fernet
        import base64
        
        # Derive key from password
        password_bytes = password.encode()
        key = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', password_bytes, b'salt', 100000)[:32])
        
        cipher = Fernet(key)
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = cipher.encrypt(data)
        
        # Save encrypted file
        encrypted_path = file_path + '.encrypted'
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        return encrypted_path
    except Exception as e:
        print(f"Encryption error: {e}")
        return file_path

def decrypt_file(encrypted_path: str, password: str) -> str:
    """Decrypt file with password"""
    try:
        from cryptography.fernet import Fernet
        import base64
        
        password_bytes = password.encode()
        key = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', password_bytes, b'salt', 100000)[:32])
        
        cipher = Fernet(key)
        
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Save decrypted file
        decrypted_path = encrypted_path.replace('.encrypted', '.decrypted')
        with open(decrypted_path, 'wb') as f:
            f.write(decrypted_data)
        
        return decrypted_path
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def log_audit_action(customer_id: int, action: str, ip_address: str, device_info: dict, 
                     backup_id: int = None, details: str = None):
    """Log backup action untuk audit trail"""
    conn = get_backup_db()
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO backup_audit_logs
                     (customer_id, action, timestamp, ip_address, device_info, backup_id, details)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (customer_id, action, datetime.now().isoformat(), ip_address,
                   json.dumps(device_info), backup_id, details))
        conn.commit()
        print(f"✅ Audit logged: {action}")
    except Exception as e:
        print(f"Error logging audit: {e}")
    finally:
        conn.close()

# ======================== Backup System Functions ========================

def request_backup_permission(customer_id: int, backup_types: List[str], 
                             ip_address: str, device_info: dict) -> dict:
    """
    Request backup permission dari customer
    Customer HARUS explicitly consent sebelum backup bisa diaktifkan
    """
    conn = get_backup_db()
    c = conn.cursor()
    
    try:
        # Check if permission already exists
        c.execute('SELECT id FROM backup_permissions WHERE customer_id = ?', (customer_id,))
        existing = c.fetchone()
        
        if existing:
            c.execute('''UPDATE backup_permissions 
                         SET backup_enabled=0, backup_types=?, consent_timestamp=?
                         WHERE customer_id=?''',
                      (json.dumps(backup_types), datetime.now().isoformat(), customer_id))
        else:
            c.execute('''INSERT INTO backup_permissions
                         (customer_id, backup_enabled, backup_types, consent_timestamp, consent_ip, consent_device)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (customer_id, False, json.dumps(backup_types), datetime.now().isoformat(),
                       ip_address, json.dumps(device_info)))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "permission_requested",
            "message": f"Backup permission request sent to customer {customer_id}",
            "requires_consent": True
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def customer_consent_backup(customer_id: int, backup_types: List[str], 
                           ip_address: str, device_info: dict) -> dict:
    """
    Customer EXPLICITLY consent untuk backup
    Ini harus dilakukan oleh user sendiri, bukan admin
    """
    conn = get_backup_db()
    c = conn.cursor()
    
    try:
        c.execute('''UPDATE backup_permissions 
                     SET backup_enabled=1, backup_types=?, consent_timestamp=?
                     WHERE customer_id=?''',
                  (json.dumps(backup_types), datetime.now().isoformat(), customer_id))
        
        conn.commit()
        
        # Log consent action
        log_audit_action(customer_id, "backup_consent_given", ip_address, device_info)
        
        conn.close()
        
        return {
            "status": "success",
            "message": f"Backup enabled for customer {customer_id}",
            "backup_types": backup_types,
            "enabled": True
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_backup_permission(customer_id: int) -> dict:
    """Get backup permission status untuk customer"""
    conn = get_backup_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM backup_permissions WHERE customer_id = ?', (customer_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        permission = dict(row)
        permission['backup_types'] = json.loads(permission['backup_types'])
        return permission
    else:
        return {
            "customer_id": customer_id,
            "backup_enabled": False,
            "backup_types": [],
            "message": "No backup permission set"
        }

def create_backup(customer_id: int, backup_name: str, backup_types: List[str],
                 sample_files: dict, password: str, ip_address: str, device_info: dict) -> int:
    """
    Create backup untuk customer
    Hanya backup file yang telah di-consent oleh user
    """
    # Check permission terlebih dahulu
    permission = get_backup_permission(customer_id)
    if not permission['backup_enabled']:
        return {"status": "error", "message": "Backup not enabled for this customer"}
    
    # Verify backup_types yang diminta sesuai dengan yang di-consent
    allowed_types = permission['backup_types']
    for btype in backup_types:
        if btype not in allowed_types:
            return {"status": "error", "message": f"Backup type '{btype}' not in consent"}
    
    conn = get_backup_db()
    c = conn.cursor()
    
    try:
        # Create backup record
        backup_folder = f"backups/{customer_id}/{backup_name}"
        os.makedirs(backup_folder, exist_ok=True)
        
        total_size = 0
        file_count = 0
        
        # Process each file type
        for file_type, files in sample_files.items():
            if file_type not in backup_types:
                continue
            
            for file_info in files:
                try:
                    # Encrypt file jika password diberikan
                    if password and len(password) > 0:
                        stored_path = encrypt_file(file_info['path'], password)
                        encrypted = True
                    else:
                        stored_path = file_info['path']
                        encrypted = False
                    
                    # Calculate checksum
                    checksum = calculate_checksum(stored_path)
                    file_size = os.path.getsize(stored_path)
                    
                    total_size += file_size
                    file_count += 1
                    
                    # Store file metadata
                    c.execute('''INSERT INTO backup_items
                                 (backup_id, file_name, file_type, file_size, encrypted, checksum, original_path, stored_path, metadata)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (None, file_info['name'], file_type, file_size, encrypted, checksum,
                               file_info['path'], stored_path, json.dumps(file_info.get('metadata', {}))))
                    
                except Exception as e:
                    print(f"Error backing up {file_info['name']}: {e}")
                    continue
        
        # Insert backup record
        c.execute('''INSERT INTO backups
                     (customer_id, backup_name, created_timestamp, size_bytes, file_count, 
                      encrypted, backup_types, status, storage_path)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (customer_id, backup_name, datetime.now().isoformat(), total_size, file_count,
                   len(password) > 0, json.dumps(backup_types), 'completed', backup_folder))
        
        backup_id = c.lastrowid
        conn.commit()
        
        # Log action
        log_audit_action(customer_id, "backup_created", ip_address, device_info, backup_id,
                        f"Created backup with {file_count} files, {total_size} bytes")
        
        conn.close()
        
        return {
            "status": "success",
            "backup_id": backup_id,
            "backup_name": backup_name,
            "file_count": file_count,
            "total_size": total_size,
            "message": f"Backup created successfully"
        }
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

def get_backup_list(customer_id: int) -> List[dict]:
    """Get semua backup untuk customer"""
    conn = get_backup_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM backups WHERE customer_id = ? ORDER BY created_timestamp DESC', 
              (customer_id,))
    backups = [dict(row) for row in c.fetchall()]
    
    for backup in backups:
        backup['backup_types'] = json.loads(backup['backup_types'])
    
    conn.close()
    return backups

def restore_backup(backup_id: int, customer_id: int, password: str = None,
                  ip_address: str = None, device_info: dict = None) -> dict:
    """
    Restore backup untuk customer
    Hanya customer sendiri yang bisa restore backup mereka sendiri
    """
    conn = get_backup_db()
    c = conn.cursor()
    
    # Verify backup belongs to customer
    c.execute('SELECT * FROM backups WHERE id = ? AND customer_id = ?', (backup_id, customer_id))
    backup = c.fetchone()
    
    if not backup:
        conn.close()
        return {"status": "error", "message": "Backup not found or does not belong to this customer"}
    
    backup_dict = dict(backup)
    
    # Get backup items
    c.execute('SELECT * FROM backup_items WHERE backup_id = ?', (backup_id,))
    items = [dict(row) for row in c.fetchall()]
    
    try:
        restored_count = 0
        restore_folder = f"restores/{customer_id}/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(restore_folder, exist_ok=True)
        
        for item in items:
            try:
                # Decrypt if needed
                if item['encrypted']:
                    if not password:
                        continue  # Skip encrypted files without password
                    
                    restored_path = decrypt_file(item['stored_path'], password)
                    if not restored_path:
                        continue
                else:
                    # Copy file
                    import shutil
                    restored_path = f"{restore_folder}/{item['file_name']}"
                    shutil.copy(item['stored_path'], restored_path)
                
                # Verify checksum
                current_checksum = calculate_checksum(restored_path)
                if current_checksum != item['checksum']:
                    print(f"Checksum mismatch for {item['file_name']}")
                    continue
                
                restored_count += 1
                
            except Exception as e:
                print(f"Error restoring {item['file_name']}: {e}")
                continue
        
        # Log restore action
        log_audit_action(customer_id, "backup_restored", ip_address, device_info, backup_id,
                        f"Restored {restored_count} files from backup")
        
        # Record restore in history
        c.execute('''INSERT INTO restore_history
                     (backup_id, customer_id, restored_timestamp, restore_type, ip_address, device_info, success)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (backup_id, customer_id, datetime.now().isoformat(), "full_restore",
                   ip_address, json.dumps(device_info), restored_count > 0))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": f"Restored {restored_count} files",
            "restore_folder": restore_folder,
            "restored_count": restored_count
        }
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}

def get_audit_logs(customer_id: int, limit: int = 100) -> List[dict]:
    """Get audit logs untuk customer backup activities"""
    conn = get_backup_db()
    c = conn.cursor()
    
    c.execute('''SELECT * FROM backup_audit_logs 
                 WHERE customer_id = ? 
                 ORDER BY timestamp DESC LIMIT ?''', (customer_id, limit))
    
    logs = [dict(row) for row in c.fetchall()]
    
    for log in logs:
        if log['device_info']:
            log['device_info'] = json.loads(log['device_info'])
    
    conn.close()
    return logs

# ======================== Export Functions ========================

if __name__ == "__main__":
    init_backup_db()
    print("✅ Backup system initialized")
