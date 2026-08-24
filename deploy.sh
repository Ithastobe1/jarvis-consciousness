#!/bin/bash
# Jarvis Consciousness Deployment Script
# Deploys to VPS as systemd service

set -e

echo "🚀 Jarvis Consciousness Deployment"
echo "===================================="

# Configuration
REPO_URL="https://github.com/Ithastobe1/jarvis-consciousness.git"
INSTALL_DIR="/opt/jarvis-consciousness"
SERVICE_NAME="jarvis-consciousness"
SERVICE_PORT="5001"
USER="www-data"

# Step 1: Clone repo
echo "📥 Cloning repository..."
if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Step 2: Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Step 3: Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/jarvis-consciousness.service > /dev/null << EOF
[Unit]
Description=Jarvis Consciousness API
After=network.target
Wants=jarvis-consciousness.timer

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 -m jarvis_consciousness.api
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment="FLASK_ENV=production"

[Install]
WantedBy=multi-user.target
EOF

# Step 4: Create data directories
echo "📁 Creating data directories..."
mkdir -p "$INSTALL_DIR/data"
chmod 755 "$INSTALL_DIR/data"

# Step 5: Enable and start service
echo "🟢 Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable jarvis-consciousness
sudo systemctl start jarvis-consciousness

# Step 6: Verify service
echo "✓ Verifying service..."
sleep 2
if sudo systemctl is-active --quiet jarvis-consciousness; then
    echo "✅ Service is running"
else
    echo "❌ Service failed to start"
    sudo systemctl status jarvis-consciousness
    exit 1
fi

# Step 7: Health check
echo "🏥 Health check..."
if curl -s http://localhost:$SERVICE_PORT/health > /dev/null; then
    echo "✅ API is healthy"
else
    echo "⚠️  API not responding yet, but service is running"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📍 API URL: http://localhost:$SERVICE_PORT"
echo "📍 Service: systemctl {status,restart,stop} jarvis-consciousness"
echo "📍 Logs: journalctl -u jarvis-consciousness -f"
echo ""
echo "Next steps:"
echo "1. Verify service: curl http://localhost:$SERVICE_PORT/health"
echo "2. Wire to Command Center (see DEPLOYMENT.md)"
echo "3. Wire to Telegram bot (see DEPLOYMENT.md)"
echo "4. Enable webhooks (see DEPLOYMENT.md)"
