#!/bin/bash

# Alpha Sign HTTP Service Installation Script
# This script installs the HTTP service as a systemd service

set -e

# Configuration
SERVICE_NAME="alphasign-http"
SERVICE_USER="alphasign"
INSTALL_DIR="/opt/alphasign"
LOG_DIR="/var/log"
SERVICE_FILE="alphasign-http.service"

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "Windows detected. Please use install_http_service_windows.bat instead."
    echo "Or run the service manually:"
    echo "  python alphasign_http_service.py --host 0.0.0.0 --port 8888"
    exit 1
fi

echo "Installing Alpha Sign HTTP Service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Create service user
if ! id "$SERVICE_USER" &>/dev/null; then
    echo "Creating service user: $SERVICE_USER"
    useradd --system --no-create-home --shell /bin/false "$SERVICE_USER"
else
    echo "Service user $SERVICE_USER already exists"
fi

# Create installation directory
echo "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
chown "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

# Copy service files
echo "Installing service files..."
cp alphasign_http_service.py "$INSTALL_DIR/"
cp -r alphasign "$INSTALL_DIR/"
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Create log directory
echo "Creating log directory: $LOG_DIR"
mkdir -p "$LOG_DIR"
touch "$LOG_DIR/alphasign-http.log"
chown "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR/alphasign-http.log"

# Install systemd service
echo "Installing systemd service..."
cp "$SERVICE_FILE" "/etc/systemd/system/"
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

# Set permissions
chmod +x "$INSTALL_DIR/alphasign_http_service.py"

echo "Installation complete!"
echo ""
echo "To start the service:"
echo "  sudo systemctl start $SERVICE_NAME"
echo ""
echo "To check status:"
echo "  sudo systemctl status $SERVICE_NAME"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "To test the service:"
echo "  curl 'http://localhost:8888/AlphaSign?msg=Hello%20World'"
echo ""
echo "Service will start automatically on boot."
