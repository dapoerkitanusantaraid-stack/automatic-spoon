#!/usr/bin/env bash
# Setup basic firewall (ufw) and fail2ban for Ubuntu-based servers
# Run as root or with sudo.

set -euo pipefail

echo "==> Installing ufw and fail2ban"
apt-get update
apt-get install -y ufw fail2ban

echo "==> Resetting ufw to default deny incoming"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

echo "==> Allow SSH (port 22) and HTTP/HTTPS"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Add any application-specific ports here, e.g., for monitoring
# ufw allow 3000/tcp   # grafana

echo "==> Enabling ufw"
ufw --force enable

echo "==> Configuring fail2ban basic jail"
cat > /etc/fail2ban/jail.d/project-server.local <<'EOF'
[sshd]
enabled = true
port    = ssh
filter  = sshd
logpath = /var/log/auth.log
maxretry = 5

[nginx-http-auth]
enabled = true
port    = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 6
EOF

systemctl restart fail2ban

echo "Firewall and fail2ban configured. Verify with: ufw status verbose && systemctl status fail2ban"
