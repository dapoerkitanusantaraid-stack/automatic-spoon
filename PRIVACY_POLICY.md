# 🔐 Security & Privacy Policy

**Complete transparency about how Project Server handles user data**

## Overview

Project Server adalah **privacy-first system** yang menempatkan:
- 🛡️ **User Privacy** sebagai prioritas utama
- 🔒 **Explicit Consent** untuk semua data collection
- 📋 **Full Transparency** via audit logs
- ⚖️ **Legal Compliance** dengan GDPR, CCPA, HIPAA

## What Data We Collect

### ✅ With Explicit User Consent:

1. **Device Information** (HANYA jika user approve)
   - Device type (iPhone, Android, etc)
   - Operating system & version
   - Screen resolution
   - Timezone
   - Browser/app version

2. **Backup Data** (HANYA selected types)
   - Photos (jika user backup "photos")
   - Documents (jika user backup "documents")
   - Contacts (jika user backup "contacts")
   - Settings (jika user backup "settings")

3. **Interaction Data** (for analytics)
   - Links clicked
   - Content viewed
   - Time spent (anonymized)
   - Platform used (Telegram, WhatsApp, web)

### ❌ What We DON'T Collect:

- ❌ Location data (without explicit permission)
- ❌ Camera/microphone access
- ❌ Phone calls or SMS
- ❌ Login credentials
- ❌ Passwords
- ❌ Browsing history
- ❌ App usage on other apps
- ❌ Financial data without consent

## Data Collection Methods

### 1️⃣ Explicit Request (Best Practice)
```
User sees dialog:
┌─────────────────────────────┐
│ Permission Request           │
├─────────────────────────────┤
│ App wants to:               │
│ ☐ Access your photos        │
│ ☐ Read your documents       │
│ ☐ View your contacts        │
│                             │
│ [Cancel]  [Approve]         │
└─────────────────────────────┘

Only if user clicks [Approve], data collection starts
```

### 2️⃣ SDK Integration (Transparent)
```javascript
// Mobile SDK shows what's being collected
ProjectServerSDK.init({
  trackingEnabled: true,  // User explicitly enables
  backupTypes: ['photos', 'documents'],  // User selects
  encryption: true  // Data encrypted by default
});
```

### 3️⃣ Enterprise Enrollment (Managed)
```
For businesses:
- IT admin configures backup policy
- Employees see clear notification
- Can opt-out individually
- Audit trail shows everything
```

## Data Usage

### ✅ How We Use Data:

1. **Backup & Recovery** (primary purpose)
   - Store user files securely
   - Encrypt at rest
   - Allow restore anytime
   - Delete on user request

2. **Analytics** (anonymous)
   - Popular content types
   - Platform usage stats
   - App performance metrics
   - Crash reports (bug fixes)

3. **Compliance** (legal requirement)
   - GDPR compliance
   - CCPA compliance
   - Law enforcement (with warrant only)
   - Fraud prevention

4. **Security** (protect users)
   - Detect malware
   - Prevent unauthorized access
   - Rate limit abuse
   - DDoS protection

### ❌ How We DON'T Use Data:

- ❌ Sell to third parties
- ❌ Share with advertisers
- ❌ Use for targeted ads
- ❌ Share with data brokers
- ❌ Use for government surveillance
- ❌ Use without explicit purpose
- ❌ Use beyond user consent scope

## Data Security

### Physical Security
```
☑️ Data centers with:
  - Armed guards
  - Biometric access
  - Surveillance 24/7
  - Fire suppression
  - Power redundancy
  - Network redundancy
  - Disaster backup systems
```

### Encryption
```
☑️ At Rest (storage):
  - AES-256 encryption
  - Fernet (industry standard)
  - User-derived keys
  - Hardware security modules (HSM)

☑️ In Transit (network):
  - TLS 1.3
  - Perfect forward secrecy
  - Certificate pinning
  - No plaintext ever

☑️ At Rest (deleted):
  - Secure wipe (DoD 5220.22-M)
  - Multiple passes overwrite
  - Physical destruction (sensitive)
```

### Access Controls
```
☑️ Authentication:
  - Multi-factor authentication (MFA)
  - Biometric login options
  - Hardware keys supported
  - Session management

☑️ Authorization:
  - Role-based access control (RBAC)
  - Only decrypt with user password
  - Admin cannot access user data
  - Least privilege principle

☑️ Audit Logging:
  - Every access logged
  - Timestamp + IP address
  - Device info recorded
  - Action details stored
  - Tamper detection
```

## Data Retention

### User Backup Files
```
Retention Policy:
- Active backup: Forever (until user deletes)
- Deleted by user: 30 days in trash
- Trash auto-delete: After 30 days
- Tax records: 7 years (if required)
- Compliance: As per regulations
```

### Audit Logs
```
Retention:
- Activity logs: 7 years
- Access logs: 1 year
- Error logs: 90 days
- Deleted items: 30 days recovery
```

### Analytics Data
```
Retention:
- Aggregated stats: Forever
- Individual tracking: 13 months
- Crash reports: Until fixed
- Personal identifiers: Not stored
```

## User Rights

### 1. Right to Access
```
Users can:
✅ Download all their data
✅ View backup list & size
✅ See audit trail
✅ Check device info collected
✅ Review consent history
```

**Request:** GET /user/{id}/export
**Response:** Zip file with all data

### 2. Right to Delete (Right to be Forgotten)
```
Users can:
✅ Delete individual files
✅ Delete entire backup
✅ Request data deletion
✅ Purge audit logs (after period)
✅ Disable backup entirely
```

**Request:** DELETE /backup/{id}
**Note:** Immediate deletion, secure wipe

### 3. Right to Data Portability
```
Users can:
✅ Export data in standard format (JSON, CSV)
✅ Download encrypted backup
✅ Move to another service
✅ Keep copy of everything
```

**Format:** Standard JSON/CSV/ZIP

### 4. Right to Opt-Out
```
Users can:
✅ Disable backup anytime
✅ Stop data collection
✅ Opt-out of analytics
✅ Withdraw consent
✅ No penalties for opting out
```

**Request:** POST /backup/revoke-consent

### 5. Right to Explanation
```
Users get:
✅ Clear privacy policy
✅ Plain language explanation
✅ Examples of data use
✅ Data flow diagrams
✅ FAQ & support
```

## Legal Compliance

### GDPR (General Data Protection Regulation)
**Applies to: EU residents**

```
✅ Lawful basis: Explicit consent
✅ Transparency: Clear policies
✅ Minimum data: Only necessary
✅ Purpose limitation: No misuse
✅ Security: Encryption + access control
✅ Breach notification: Within 72 hours
✅ DPA: Data Protection Assessment
✅ Rights: All 8 rights provided
```

### CCPA (California Consumer Privacy Act)
**Applies to: California residents**

```
✅ Right to know: Access all data
✅ Right to delete: Data deletion
✅ Right to opt-out: Stop selling
✅ Right to not discriminate: Fair treatment
✅ Non-selling policy: Never sold
✅ Accessibility: WCAG compliant
```

### HIPAA (Health Insurance Portability)
**Applies to: Healthcare data**

```
✅ Encryption: Required for backup
✅ Access controls: Strict ACLs
✅ Audit logs: Comprehensive logging
✅ Business associates: BAA agreement
✅ Breach notification: Required
✅ Data integrity: Checksum verification
```

### LGPD (Brazil Lei Geral de Proteção de Dados)
**Applies to: Brazilian residents**

```
✅ Legal basis: User consent
✅ Purpose specification: Clear use
✅ Transparency: Full disclosure
✅ Delete right: Data deletion
✅ Data sharing: Limited only
✅ Security: Industry standard encryption
```

## Incident Response

### What Happens if Data Breach?

```
1. IMMEDIATE (within 1 hour):
   ✓ Isolate affected systems
   ✓ Stop ongoing breach
   ✓ Preserve evidence
   ✓ Notify incident response team

2. SHORT TERM (within 24 hours):
   ✓ Investigate scope
   ✓ Identify affected users
   ✓ Determine root cause
   ✓ Begin remediation

3. MEDIUM TERM (within 72 hours):
   ✓ Notify all affected users
   ✓ Notify regulators (if required)
   ✓ Provide credit monitoring (if personal data)
   ✓ Launch external audit

4. LONG TERM (ongoing):
   ✓ Implement fixes
   ✓ Enhance security
   ✓ Update policies
   ✓ Provide support to affected users
```

## Third Party Sharing

### Who We Share Data With

```
✅ Backup storage providers:
   - Amazon AWS (data centers)
   - Encrypted end-to-end
   - Data Processing Agreement (DPA)

✅ CDN providers:
   - CloudFlare (website acceleration)
   - Cached content only (no personal data)
   - DPA signed

✅ Analytics services:
   - Aggregated data only
   - No personal identifiers
   - Anonymized statistics

✅ Legal compliance:
   - Law enforcement (warrants only)
   - Government agencies (if required by law)
   - Court orders (judges only)
   - Subpoenas (with legal process)

❌ We DON'T share with:
   - Advertisers
   - Data brokers
   - Marketing companies
   - Social media networks
   - Anyone without legal requirement
```

## Children's Privacy (COPPA)

### Under 13 years old

```
✅ Special protections:
  - Parental consent required
  - No marketing emails
  - Limited data collection
  - No personalized ads
  - Account deletion easy
  - Clear language policies
```

### 13-17 years old (Teens)

```
✅ Age-appropriate:
  - Clear privacy controls
  - Easy opt-out
  - Transparent practices
  - Parent override available
```

## Transparency Reports

### What We Publish

```
Quarterly Reports:
├─ Government requests
│  ├─ Number of requests
│  ├─ Requests granted/denied
│  └─ Data category
├─ DMCA takedowns
├─ Content removals
├─ Security updates
└─ Privacy incidents (if any)

Annual Reports:
├─ Data protection stats
├─ User rights requests
├─ GDPR/CCPA compliance
├─ Security investments
└─ Policy updates
```

## Questions & Concerns?

### Support Channels

```
Email: privacy@yourdomain.com (response within 48 hours)
Phone: +1-XXX-XXX-XXXX (business hours)
Web: https://yourdomain.com/privacy/contact
Physical Address: [Office Address]
```

### Data Protection Officer

```
For GDPR inquiries:
DPO: [Name]
Email: dpo@yourdomain.com
Phone: [Phone]
```

---

**Last Updated**: February 6, 2026
**Version**: 1.0
**Status**: Active ✅

---

## Summary

🛡️ **We are committed to:**
- ✅ Privacy as a fundamental right
- ✅ Transparent data practices
- ✅ Strong encryption & security
- ✅ User control over data
- ✅ Legal compliance (GDPR, CCPA, HIPAA)
- ✅ Regular security audits
- ✅ Honest communication
- ✅ Your trust

**If you use Project Server, your privacy is protected. Period.**
