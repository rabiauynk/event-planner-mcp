#!/usr/bin/env python3
"""
Simple startup script for the Event Planner MCP
"""
import sys
import os

def main():
    """Main entry point"""
    try:
        print("Starting Event Planner MCP...")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        
        # Check if required modules are available
        try:
            import flask
            print(f"Flask version: {flask.__version__}")
        except ImportError:
            print("ERROR: Flask not installed")
            return 1
            
        try:
            import requests
            print(f"Requests available")
        except ImportError:
            print("ERROR: Requests not installed")
            return 1
        
        # Import and run the app
        from app import app
        
        # Get configuration
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') != 'production'
        
        print(f"Starting server on port {port}")
        print(f"Debug mode: {debug}")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except Exception as e:
        print(f"ERROR: Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
