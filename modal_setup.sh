#!/bin/bash

# Modal Workshop Setup Script
# Run this first to set up your Modal environment for the workshop

set -e  # Exit on any error

echo "Modal Workshop Setup"
echo "This script will prepare your computer for serverless ML deployment"
echo "============================================================"
echo ""

# Step 1: Check and install Modal
echo "Step 1: Checking Modal installation..."
if python3 -c "import modal" 2>/dev/null; then
    echo "Modal is already installed - ready to proceed"
else
    echo "Modal not found on your system - installing now..."
    echo "This may take a minute to download and install..."
    pip install modal
    echo "Modal installed successfully"
fi
echo ""

# Step 2: Check for optional environment file
echo "Step 2: Loading environment settings..."
if [ -f ".env.local" ]; then
    echo "Custom environment variables found in .env.local"
    echo "You can edit .env.local to customize app names and settings"
else
    echo "No .env.local file found - using default settings"
    echo "Everything will work fine with defaults - no config needed!"
fi
echo ""

# Step 3: Set up Modal authentication
echo "Step 3: Setting up Modal authentication..."
echo "This will open a browser window where you can:"
echo "1. Create a free Modal account (if you don't have one)"
echo "2. Authorize this computer to deploy to Modal"
echo "3. Get your authentication tokens"
echo ""

if modal setup; then
    echo "Modal authentication successful - you can now deploy models"
else
    echo "Modal setup failed"
    echo "Please run 'modal setup' manually in your terminal and try again"
    exit 1
fi
echo ""

# Step 4: Verify connection
echo "Step 4: Verifying Modal connection..."
if modal token get > /dev/null 2>&1; then
    echo "Modal connection verified - ready to deploy real models"
else
    echo "Modal connection test failed"
    echo "Try running 'modal setup' again or check your internet connection"
    exit 1
fi
echo ""

# Success message
echo "============================================================"
echo "Setup complete! Your system is ready for serverless ML deployment"
echo ""
echo "What you can do now:"
echo "1. Deploy to Modal cloud:  modal deploy sentiment_api.py"
echo "2. View in dashboard:      https://modal.com/apps"
echo ""
echo "After deployment, you'll get a URL to use your API!"
echo ""
echo "You're all set! Time to deploy your first AI model!"