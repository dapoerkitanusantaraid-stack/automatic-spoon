"""
Backup System - Usage Examples
Contoh-contoh penggunaan backup system dengan ethical approach
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

# ============== EXAMPLE 1: Request Backup Permission ==============

def example_request_backup_permission():
    """
    Step 1: Request permission dari user
    User akan melihat dialog: "App minta izin backup untuk:"
    """
    print("\n1️⃣  REQUEST BACKUP PERMISSION")
    print("="*50)
    
    customer_id = 1
    backup_types = ["photos", "documents", "contacts"]
    
    data = {
        "customer_id": customer_id,
        "backup_types": backup_types,
        "ip_address": "192.168.1.100",
        "device_info": {
            "device": "iPhone 14",
            "os": "iOS 17.0",
            "app_version": "1.0.0"
        }
    }
    
    response = requests.post(f"{API_BASE}/backup/request-permission", json=data)
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Requires Consent: {result['requires_consent']}")
    print("\n✅ Permission request sent to user")
    print("⏳ Waiting for user to approve...")
    

# ============== EXAMPLE 2: User Approves Backup ==============

def example_user_approve_backup():
    """
    Step 2: User clicks APPROVE in dialog
    Hanya bisa dilakukan oleh user sendiri dengan authenticated session
    """
    print("\n2️⃣  USER APPROVES BACKUP")
    print("="*50)
    
    customer_id = 1
    backup_types = ["photos", "documents", "contacts"]
    
    data = {
        "customer_id": customer_id,
        "backup_types": backup_types,
        "ip_address": "192.168.1.100",
        "device_info": {
            "device": "iPhone 14",
            "os": "iOS 17.0",
            "app_version": "1.0.0"
        }
    }
    
    response = requests.post(f"{API_BASE}/backup/consent", json=data)
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Backup Types Approved: {', '.join(result['backup_types'])}")
    print(f"Enabled: {result['enabled']}")
    print("\n✅ User consent recorded")
    print("✅ Backup system now enabled for this user")


# ============== EXAMPLE 3: Check Permission Status ==============

def example_check_permission():
    """
    Check apakah user sudah enable backup
    """
    print("\n3️⃣  CHECK PERMISSION STATUS")
    print("="*50)
    
    customer_id = 1
    
    response = requests.get(f"{API_BASE}/backup/permission/{customer_id}")
    result = response.json()
    
    print(f"Customer ID: {result['customer_id']}")
    print(f"Backup Enabled: {result['backup_enabled']}")
    print(f"Backup Types: {', '.join(result['backup_types'])}")
    print(f"Consent Given: {result['consent_timestamp']}")
    print(f"Consent IP: {result['consent_ip']}")
    
    if result['backup_enabled']:
        print("\n✅ User has enabled backup - safe to proceed")
    else:
        print("\n⚠️  User has NOT enabled backup - cannot backup")


# ============== EXAMPLE 4: Create Backup ==============

def example_create_backup():
    """
    Step 3: Create backup
    Hanya jika user telah approve
    """
    print("\n4️⃣  CREATE BACKUP")
    print("="*50)
    
    customer_id = 1
    
    # Sample files to backup
    sample_files = {
        "photos": [
            {
                "name": "photo_001.jpg",
                "path": "/tmp/photo_001.jpg",
                "metadata": {
                    "date_taken": "2026-01-15",
                    "location": "New York",
                    "size": 2048576
                }
            },
            {
                "name": "photo_002.jpg",
                "path": "/tmp/photo_002.jpg",
                "metadata": {
                    "date_taken": "2026-01-20",
                    "size": 3145728
                }
            }
        ],
        "documents": [
            {
                "name": "resume.pdf",
                "path": "/tmp/resume.pdf",
                "metadata": {
                    "file_type": "pdf",
                    "size": 1024000
                }
            },
            {
                "name": "contract.docx",
                "path": "/tmp/contract.docx",
                "metadata": {
                    "file_type": "document",
                    "size": 512000
                }
            }
        ]
    }
    
    data = {
        "customer_id": customer_id,
        "backup_name": f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "backup_types": ["photos", "documents"],
        "files": sample_files,
        "password": "user_strong_password_123",  # User buat password sendiri
        "ip_address": "192.168.1.100",
        "device_info": {
            "device": "iPhone 14",
            "os": "iOS 17.0",
            "app_version": "1.0.0"
        }
    }
    
    response = requests.post(f"{API_BASE}/backup/create", json=data)
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Backup ID: {result['backup_id']}")
    print(f"Backup Name: {result['backup_name']}")
    print(f"Files Backed Up: {result['file_count']}")
    print(f"Total Size: {result['total_size']:,} bytes ({result['total_size']/1024/1024:.2f} MB)")
    print(f"Message: {result['message']}")
    print("\n✅ Backup created successfully")
    print(f"💾 Encrypted & stored securely")
    
    return result['backup_id']


# ============== EXAMPLE 5: Get Backup List ==============

def example_get_backup_list():
    """
    List semua backup untuk user (private)
    Hanya user bisa lihat backup mereka sendiri
    """
    print("\n5️⃣  GET BACKUP LIST")
    print("="*50)
    
    customer_id = 1
    
    response = requests.get(f"{API_BASE}/backup/list/{customer_id}")
    result = response.json()
    
    print(f"Customer ID: {result['customer_id']}")
    print(f"Total Backups: {result['total']}")
    print()
    
    for backup in result['backups']:
        print(f"📦 Backup ID: {backup['id']}")
        print(f"   Name: {backup['backup_name']}")
        print(f"   Created: {backup['created_timestamp']}")
        print(f"   Files: {backup['file_count']}")
        print(f"   Size: {backup['size_bytes']:,} bytes")
        print(f"   Encrypted: {'🔐 Yes' if backup['encrypted'] else '❌ No'}")
        print(f"   Status: {backup['status']}")
        print()


# ============== EXAMPLE 6: Restore Backup ==============

def example_restore_backup():
    """
    Step 4: Restore backup
    User perlu password untuk restore (extra security)
    """
    print("\n6️⃣  RESTORE BACKUP")
    print("="*50)
    
    backup_id = 1
    customer_id = 1
    
    data = {
        "backup_id": backup_id,
        "customer_id": customer_id,
        "password": "user_strong_password_123",  # User harus masukkan password
        "ip_address": "192.168.1.100",
        "device_info": {
            "device": "iPhone 14",
            "os": "iOS 17.0",
            "app_version": "1.0.0"
        }
    }
    
    response = requests.post(f"{API_BASE}/backup/restore", json=data)
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Restored Files: {result['restored_count']}")
    print(f"Restore Folder: {result['restore_folder']}")
    print(f"Message: {result['message']}")
    print("\n✅ Backup restored successfully")
    print(f"📁 Files available in: {result['restore_folder']}")


# ============== EXAMPLE 7: View Audit Logs ==============

def example_view_audit_logs():
    """
    View semua aktivitas backup
    User bisa lihat kapan backup dibuat/di-restore
    User bisa lihat dari device mana
    """
    print("\n7️⃣  VIEW AUDIT LOGS")
    print("="*50)
    
    customer_id = 1
    
    response = requests.get(f"{API_BASE}/backup/audit/{customer_id}")
    result = response.json()
    
    print(f"Customer ID: {result['customer_id']}")
    print(f"Total Log Entries: {result['total_logs']}")
    print()
    print("📋 ACTIVITY HISTORY:")
    print("-"*50)
    
    for log in result['logs']:
        action = log['action'].upper().replace('_', ' ')
        timestamp = log['timestamp']
        ip = log['ip_address']
        device = log['device_info'].get('device', 'Unknown') if log['device_info'] else 'Unknown'
        
        print(f"\n✓ {action}")
        print(f"  Time: {timestamp}")
        print(f"  IP: {ip}")
        print(f"  Device: {device}")
        if log.get('details'):
            print(f"  Details: {log['details']}")


# ============== EXAMPLE 8: Delete Backup ==============

def example_delete_backup():
    """
    User bisa delete backup kapan saja
    """
    print("\n8️⃣  DELETE BACKUP")
    print("="*50)
    
    backup_id = 1
    customer_id = 1
    
    response = requests.delete(
        f"{API_BASE}/backup/{backup_id}",
        params={"customer_id": customer_id}
    )
    result = response.json()
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print("\n✅ Backup deleted permanently")
    print("🔒 Data will be securely wiped from storage")


# ============== EXAMPLE 9: Privacy Best Practices ==============

def example_privacy_best_practices():
    """
    Best practices untuk privacy-respecting backup
    """
    print("\n9️⃣  PRIVACY BEST PRACTICES")
    print("="*50)
    
    best_practices = {
        "For Users": [
            "✅ Enable backup for important files only",
            "✅ Use strong password for encryption",
            "✅ Review backup audit logs regularly",
            "✅ Delete old backups you don't need",
            "✅ Test restore process before emergency",
            "✅ Keep password in secure password manager"
        ],
        "For Administrators": [
            "✅ Never backup without explicit consent",
            "✅ Show permission dialog clearly",
            "✅ Log all backup activities",
            "✅ Encrypt at rest & in transit",
            "✅ Regular security audits",
            "✅ Comply with GDPR/CCPA/HIPAA",
            "✅ Allow users to delete anytime",
            "✅ Provide data portability"
        ],
        "For Apps": [
            "✅ Show clear permission dialog",
            "✅ Only backup selected types",
            "✅ Encrypt with user password",
            "✅ Provide restore confirmation",
            "✅ Show audit trail to user",
            "✅ Handle errors gracefully"
        ]
    }
    
    for category, practices in best_practices.items():
        print(f"\n{category}:")
        for practice in practices:
            print(f"  {practice}")


# ============== EXAMPLE 10: Compliance Report ==============

def example_compliance_report():
    """
    Generate compliance report
    """
    print("\n🔟 COMPLIANCE REPORT")
    print("="*50)
    
    compliance_checklist = {
        "GDPR Compliance (EU)": {
            "Explicit Consent": "✅ Required before backup",
            "Right to Access": "✅ Available via API",
            "Right to Delete": "✅ Delete endpoint provided",
            "Data Portability": "✅ Export format supported",
            "Privacy by Design": "✅ Default encrypted"
        },
        "CCPA Compliance (California)": {
            "Right to Know": "✅ Audit logs show all access",
            "Right to Delete": "✅ Backup deletion supported",
            "Right to Opt-Out": "✅ Can disable backup",
            "Non-Selling": "✅ Data never sold"
        },
        "Security": {
            "Encryption": "✅ Fernet (AES-128)",
            "Password": "✅ PBKDF2 derived key",
            "Integrity": "✅ SHA256 checksum",
            "Audit Trail": "✅ Full logging + IP tracking",
            "Access Control": "✅ User-only restore"
        },
        "Privacy": {
            "Consent": "✅ Explicit user approval",
            "Transparency": "✅ Users know what's backed up",
            "Minimal Data": "✅ Only what user selected",
            "User Control": "✅ Can delete anytime",
            "No Tracking": "✅ No hidden background backup"
        }
    }
    
    for category, items in compliance_checklist.items():
        print(f"\n{category}:")
        for item, status in items.items():
            print(f"  {item}: {status}")


# ============== RUN EXAMPLES ==============

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📚 BACKUP SYSTEM - USAGE EXAMPLES")
    print("="*60)
    print("\nThese examples show ethical & compliant backup usage")
    print("✅ User consent required")
    print("✅ Transparent operations")
    print("✅ Full audit trail")
    print("✅ Privacy-first design")
    
    # Uncomment untuk run examples
    # example_request_backup_permission()
    # example_user_approve_backup()
    # example_check_permission()
    # backup_id = example_create_backup()
    # example_get_backup_list()
    # example_restore_backup()
    # example_view_audit_logs()
    # example_delete_backup()
    # example_privacy_best_practices()
    # example_compliance_report()
    
    print("\n" + "="*60)
    print("Uncomment functions to run examples")
    print("="*60)
