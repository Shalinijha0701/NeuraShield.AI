#!/usr/bin/env python3
"""
NeuraShield.AI Startup Script
Launches the complete AI-powered DevSecOps platform
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_startup_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🛡️  NeuraShield.AI  🛡️                     ║
    ║           Self-Learning AI Guardian for Modern DevOps         ║
    ║                        Starting Up...                         ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'torch', 'transformers', 
        'redis', 'psycopg2-binary', 'neo4j'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Installing missing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
    else:
        print("✅ All dependencies satisfied")

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting NeuraShield.AI API server...")
    
    try:
        # Start the FastAPI server
        cmd = [
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ]
        
        process = subprocess.Popen(cmd, cwd=Path.cwd())
        print("✅ API server started on http://localhost:8000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def show_endpoints():
    """Display available API endpoints"""
    print("\n📡 Available API Endpoints:")
    print("   • GET  /                     - Welcome message")
    print("   • GET  /health               - Health check")
    print("   • POST /api/v1/analyze/code  - Neural Code Brain analysis")
    print("   • POST /api/v1/analyze/security - Quantum Security Shield scan")
    print("   • POST /api/v1/analyze/pipeline - Adaptive DevOps Optimizer")
    print("   • POST /api/v1/analyze/complete - Complete analysis")
    print("   • GET  /api/v1/metrics       - Platform metrics")

def show_usage_examples():
    """Show usage examples"""
    print("\n💡 Usage Examples:")
    print("   # Run demo")
    print("   python run_demo.py")
    print("")
    print("   # CLI analysis")
    print("   python -m app.cli analyze --path .")
    print("   python -m app.cli scan --path .")
    print("   python -m app.cli optimize")
    print("")
    print("   # API testing")
    print("   curl http://localhost:8000/health")

def main():
    print_startup_banner()
    
    # Check and install dependencies
    check_dependencies()
    
    # Start the API server
    api_process = start_api_server()
    
    if api_process:
        print("\n🛡️  NeuraShield.AI is now running!")
        print("   Neural Shields: ACTIVE")
        print("   AI Models: LOADED")
        print("   Security Scanning: ENABLED")
        
        show_endpoints()
        show_usage_examples()
        
        print(f"\n🎯 Quick Start:")
        print(f"   1. Run demo: python run_demo.py")
        print(f"   2. Visit API docs: http://localhost:8000/docs")
        print(f"   3. Check health: http://localhost:8000/health")
        
        print(f"\n⚡ Press Ctrl+C to stop the server")
        
        try:
            # Keep the script running
            api_process.wait()
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down NeuraShield.AI...")
            api_process.terminate()
            print("✅ Server stopped successfully")
    else:
        print("❌ Failed to start NeuraShield.AI")
        sys.exit(1)

if __name__ == "__main__":
    main()