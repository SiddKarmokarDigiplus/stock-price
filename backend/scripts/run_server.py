#!/usr/bin/env python3
"""
Server startup script with better error handling and port management
"""

import os
import sys
import socket
from datetime import datetime

def check_port(port, host='0.0.0.0'):
    """Check if a port is available on the specified host interface."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
        except OSError:
            return False

def find_free_port(start_port=5000, host='0.0.0.0'):
    """Find a free port starting from start_port on specified host."""
    port = start_port
    while port < start_port + 100:
        if check_port(port, host=host):
            return port
        port += 1
    raise RuntimeError("Could not find a free port")

def check_virtual_environment():
    """Check if running in a virtual environment"""
    import sys
    import os
    
    # Check if we're in a virtual environment
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    
    if not in_venv:
        print("⚠️  WARNING: Not running in a virtual environment!")
        print("   Best practice: Create and activate a virtual environment:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   source venv/bin/activate  # macOS/Linux")
        print("")
    
    return in_venv

def main():
    """Main server startup function"""
    print("=" * 60)
    print("🚀 Live Stock Price API Server")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    # Check virtual environment
    check_virtual_environment()
    
    # Check if required packages are installed
    try:
        import flask
        import yfinance
        import pandas
        import requests
        print("✓ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Install with: pip install -r requirements.txt")
        print("Make sure virtual environment is activated!")
        sys.exit(1)
    
    # Determine host and port availability
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    if not check_port(port, host=host):
        print(f"⚠️  Port {port} on {host} is busy, finding free port...")
        port = find_free_port(port, host=host)
        print(f"✓ Using port {port}")
    else:
        print(f"✓ Port {port} on {host} is available")
    
    # Set environment variables
    os.environ['PORT'] = str(port)
    
    print(f"🌐 Server will start at: http://localhost:{port}")
    print(f"📊 Health check: http://localhost:{port}/health")
    print(f"💰 Live price API: http://localhost:{port}/live_price?symbol=AAPL")
    print("=" * 60)
    print("Starting server...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Import and run the Flask app
        from main import app
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
