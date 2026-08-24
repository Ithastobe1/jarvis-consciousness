#!/bin/bash
# ============================================================================
# JARVIS CONSCIOUSNESS — VPS DEPLOYMENT EXECUTION
# ============================================================================
# Run this script on your VPS to deploy Jarvis Consciousness
#
# Usage:
#   ssh root@31.97.229.117 'bash -s' < EXECUTE_DEPLOYMENT.sh
#
# Or copy to VPS and run:
#   scp EXECUTE_DEPLOYMENT.sh root@31.97.229.117:/tmp/
#   ssh root@31.97.229.117 'bash /tmp/EXECUTE_DEPLOYMENT.sh'
# ============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          🚀 JARVIS CONSCIOUSNESS VPS DEPLOYMENT                  ║"
echo "║                     Starting Now...                              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: Clone Repository
# ============================================================================

echo "📥 STEP 1: Cloning Jarvis Consciousness Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

INSTALL_DIR="/opt/jarvis-consciousness"
REPO_URL="https://github.com/Ithastobe1/jarvis-consciousness.git"

if [ -d "$INSTALL_DIR" ]; then
    echo "   ✓ Directory exists, pulling latest code..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "   ✓ Creating directory and cloning repo..."
    mkdir -p "$INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "   ✓ Repository ready at: $INSTALL_DIR"
echo ""

# ============================================================================
# STEP 2: Install Python Dependencies
# ============================================================================

echo "📦 STEP 2: Installing Python Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "   Checking Python version..."
python3 --version

echo "   Installing pip packages..."
pip3 install -r requirements.txt

echo "   ✓ Dependencies installed"
echo ""

# ============================================================================
# STEP 3: Create systemd Service
# ============================================================================

echo "⚙️  STEP 3: Creating Systemd Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SERVICE_FILE="/etc/systemd/system/jarvis-consciousness.service"

echo "   Creating: $SERVICE_FILE"

sudo tee "$SERVICE_FILE" > /dev/null << 'SERVICEEOF'
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
SERVICEEOF

echo "   ✓ Systemd service file created"
echo ""

# ============================================================================
# STEP 4: Create Data Directories
# ============================================================================

echo "📁 STEP 4: Creating Data Directories"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

mkdir -p "$INSTALL_DIR/data"
chmod 755 "$INSTALL_DIR/data"

echo "   ✓ Data directories created and permissions set"
echo ""

# ============================================================================
# STEP 5: Enable and Start Service
# ============================================================================

echo "🟢 STEP 5: Enabling and Starting Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "   Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "   Enabling service to start on boot..."
sudo systemctl enable jarvis-consciousness

echo "   Starting service..."
sudo systemctl start jarvis-consciousness

sleep 2

echo "   ✓ Service started"
echo ""

# ============================================================================
# STEP 6: Verify Service Status
# ============================================================================

echo "✓ STEP 6: Verifying Service Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

STATUS=$(systemctl is-active jarvis-consciousness)

if [ "$STATUS" = "active" ]; then
    echo "   ✅ Service is ACTIVE and RUNNING"
else
    echo "   ❌ Service status: $STATUS"
    echo "   Checking logs..."
    journalctl -u jarvis-consciousness -n 20
    exit 1
fi

echo ""

# ============================================================================
# STEP 7: Health Check
# ============================================================================

echo "🏥 STEP 7: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "   Waiting for API to start (up to 10 seconds)..."

for i in {1..10}; do
    if curl -s http://localhost:5001/health > /dev/null 2>&1; then
        echo "   ✅ API is responding on http://localhost:5001"
        break
    fi
    echo "   Attempt $i/10..."
    sleep 1
done

echo ""

# ============================================================================
# STEP 8: Test Endpoints
# ============================================================================

echo "🧪 STEP 8: Testing API Endpoints"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "   Testing: GET /health"
HEALTH=$(curl -s http://localhost:5001/health)
if echo "$HEALTH" | grep -q "ok"; then
    echo "   ✅ PASS"
else
    echo "   ❌ FAIL: $HEALTH"
fi

echo ""
echo "   Testing: GET /api/briefing"
BRIEFING=$(curl -s http://localhost:5001/api/briefing)
if echo "$BRIEFING" | grep -q "score"; then
    echo "   ✅ PASS - Briefing loading"
else
    echo "   ⚠️  Response: $(echo "$BRIEFING" | head -c 100)..."
fi

echo ""
echo "   Testing: GET /api/family/briefing"
FAMILY=$(curl -s http://localhost:5001/api/family/briefing)
if echo "$FAMILY" | grep -q "progress"; then
    echo "   ✅ PASS - Family briefing loading"
else
    echo "   ⚠️  Response: $(echo "$FAMILY" | head -c 100)..."
fi

echo ""

# ============================================================================
# STEP 9: Show Service Info
# ============================================================================

echo "📊 STEP 9: Service Information"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "   Service Name:    jarvis-consciousness"
echo "   Status:          $(systemctl is-active jarvis-consciousness)"
echo "   Enabled on Boot: $(systemctl is-enabled jarvis-consciousness)"
echo "   Install Dir:     $INSTALL_DIR"
echo "   Service File:    $SERVICE_FILE"
echo "   API Port:        5001"
echo "   API URL:         http://localhost:5001"
echo "   External URL:    http://31.97.229.117:5001"
echo ""

# ============================================================================
# STEP 10: Show Next Steps
# ============================================================================

echo "🎯 STEP 10: Next Steps"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "1. Verify API is accessible:"
echo "   curl http://31.97.229.117:5001/health"
echo ""
echo "2. Check service logs:"
echo "   journalctl -u jarvis-consciousness -f"
echo ""
echo "3. View recent logs:"
echo "   journalctl -u jarvis-consciousness -n 50"
echo ""
echo "4. Restart service (if needed):"
echo "   systemctl restart jarvis-consciousness"
echo ""
echo "5. Stop service:"
echo "   systemctl stop jarvis-consciousness"
echo ""

# ============================================================================
# DEPLOYMENT COMPLETE
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║  ✅ JARVIS CONSCIOUSNESS DEPLOYED SUCCESSFULLY                   ║"
echo "║                                                                    ║"
echo "║  🚀 API is live at: http://31.97.229.117:5001                    ║"
echo "║  📊 Dashboard:      http://31.97.229.117:5001/api/briefing       ║"
echo "║  👥 Family:         http://31.97.229.117:5001/api/family/briefing│"
echo "║                                                                    ║"
echo "║  Next: Wire Command Center & Telegram Bot                        ║"
echo "║        See CC_INTEGRATION_INSTRUCTIONS.md                        ║"
echo "║        See TELEGRAM_INTEGRATION_INSTRUCTIONS.md                  ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
