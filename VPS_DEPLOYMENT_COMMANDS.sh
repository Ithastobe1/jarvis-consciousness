#!/bin/bash
# VPS Deployment Commands for Jarvis Consciousness
# Run these on the VPS (31.97.229.117) as root

# ============================================================================
# STEP 1: Download deployment script to VPS
# ============================================================================
# From your local machine:
# scp deploy.sh root@31.97.229.117:/tmp/
# ssh root@31.97.229.117 'bash /tmp/deploy.sh'

# ============================================================================
# STEP 2: If manual deployment needed, run these commands on VPS:
# ============================================================================

# SSH to VPS
ssh root@31.97.229.117

# Clone repo
mkdir -p /opt/jarvis-consciousness
cd /opt/jarvis-consciousness
git clone https://github.com/Ithastobe1/jarvis-consciousness.git .
cd /opt/jarvis-consciousness

# Install Python dependencies
pip3 install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/jarvis-consciousness.service > /dev/null << 'EOF'
[Unit]
Description=Jarvis Consciousness API
After=network.target
Wants=jarvis-consciousness.timer

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/jarvis-consciousness
ExecStart=/usr/bin/python3 -m jarvis_consciousness.api
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment="FLASK_ENV=production"

[Install]
WantedBy=multi-user.target
EOF

# Create data directories
mkdir -p /opt/jarvis-consciousness/data
chmod 755 /opt/jarvis-consciousness/data

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jarvis-consciousness
sudo systemctl start jarvis-consciousness

# ============================================================================
# STEP 3: Verify deployment
# ============================================================================

# Check service status
systemctl status jarvis-consciousness

# Check if running
curl http://localhost:5001/health

# Check logs
journalctl -u jarvis-consciousness -f

# ============================================================================
# STEP 4: Test endpoints
# ============================================================================

# Test briefing
curl http://localhost:5001/api/briefing | jq .

# Test family briefing
curl http://localhost:5001/api/family/briefing | jq .

# Test snapshot (for CC dashboard)
curl http://localhost:5001/api/snapshot | jq .

# ============================================================================
# STEP 5: Configure nginx reverse proxy (optional, for external access)
# ============================================================================

# Edit /etc/nginx/sites-available/jarvis-consciousness
sudo tee /etc/nginx/sites-available/jarvis-consciousness > /dev/null << 'EOF'
server {
    listen 5001;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/jarvis-consciousness /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# ============================================================================
# STEP 6: Verify external access
# ============================================================================

# From local machine:
curl http://31.97.229.117:5001/health

# ============================================================================
# All Done!
# ============================================================================

echo "✅ Jarvis Consciousness deployed to VPS"
echo "📍 API: http://31.97.229.117:5001"
echo "📍 Service: systemctl {status,restart,stop} jarvis-consciousness"
echo "📍 Logs: journalctl -u jarvis-consciousness -f"
