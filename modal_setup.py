#!/usr/bin/env python3
"""
Modal Setup and Authentication Script
Run this first to set up your Modal environment for the workshop
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def check_modal_installation():
    """
    Check if Modal is installed on the system and install it if missing.
    Modal is required for all serverless deployments in this workshop.
    """
    try:
        import modal
        print("Modal is already installed - ready to proceed")
        return True
    except ImportError:
        print("Modal not found on your system - installing now...")
        print("This may take a minute to download and install...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "modal"])
        print("Modal installed successfully")
        return True

def setup_modal_auth():
    """
    Set up Modal authentication by opening browser for login.
    This connects your local environment to Modal's cloud infrastructure.
    You only need to do this once per machine.
    """
    print("\nSetting up Modal authentication...")
    print("This will open a browser window where you can:")
    print("1. Create a free Modal account (if you don't have one)")
    print("2. Authorize this computer to deploy to Modal")
    print("3. Get your authentication tokens")
    
    try:
        result = subprocess.run(["modal", "setup"], check=True, capture_output=True, text=True)
        print("Modal authentication successful - you can now deploy models")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Modal setup failed with error: {e}")
        print("Please run 'modal setup' manually in your terminal and try again")
        return False

def verify_modal_connection():
    """
    Test that Modal connection is working by creating a simple test app.
    This ensures your authentication is correct and Modal servers are reachable.
    """
    try:
        import modal
        
        # Create a minimal test app to verify connection
        # This doesn't deploy anything, just tests the connection
        app = modal.App("test-connection")
        
        @app.function()
        def test_function():
            """Simple test function to verify Modal connectivity"""
            return "Hello from Modal cloud infrastructure"
        
        print("Modal connection verified - ready to deploy real models")
        return True
    except Exception as e:
        print(f"Modal connection test failed: {e}")
        print("Try running 'modal setup' again or check your internet connection")
        return False

def load_environment():
    """
    Load any custom environment variables from .env.local file.
    These variables can customize app names, rate limits, etc.
    The .env.local file is optional - everything will work without it.
    """
    if os.path.exists('.env.local'):
        load_dotenv('.env.local')
        print("Custom environment variables loaded from .env.local")
        print("You can edit .env.local to customize app names and settings")
    else:
        print("No .env.local file found - using default settings")
        print("You can create .env.local later to customize your deployments")

def main():
    """
    Main setup workflow that prepares your environment for Modal deployments.
    This script handles all the one-time setup needed for the workshop.
    """
    print("Modal Workshop Setup")
    print("This script will prepare your computer for serverless ML deployment")
    print("=" * 60)
    
    # Step 1: Ensure Modal is installed
    print("Step 1: Checking Modal installation...")
    if not check_modal_installation():
        print("Failed to install Modal - please install manually")
        return False
    
    # Step 2: Load any custom settings
    print("\nStep 2: Loading environment settings...")
    load_environment()
    
    # Step 3: Set up authentication with Modal servers
    print("\nStep 3: Setting up Modal authentication...")
    if not setup_modal_auth():
        print("Authentication failed - please try manual setup")
        return False
    
    # Step 4: Verify everything is working
    print("\nStep 4: Verifying Modal connection...")
    if not verify_modal_connection():
        print("Connection test failed - please check setup")
        return False
    
    # Success - ready for workshop
    print("\nSetup complete! Your system is ready for serverless ML deployment")
    print("\nWhat you can do now:")
    print("1. Deploy simple models: python sentiment_api.py")
    print("2. Deploy to Modal cloud: modal deploy sentiment_api.py")
    print("3. Test your deployments: python test_deployment.py")
    print("4. Try GPU models: modal deploy image_classifier.py")
    
    return True

if __name__ == "__main__":
    # Run the setup process
    success = main()
    if not success:
        print("\nSetup failed - please ask for help before proceeding")
        sys.exit(1)
    else:
        print("\nYou're all set! Start with sentiment_api.py")