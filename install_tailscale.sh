#!/bin/bash
# Install Tailscale on Raspberry Pi

curl -fsSL https://tailscale.com/install.sh | sh

echo ""
echo "Installation complete!"
echo "Next step: Run 'sudo tailscale up' to authenticate"
