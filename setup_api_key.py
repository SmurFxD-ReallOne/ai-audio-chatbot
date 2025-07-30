#!/usr/bin/env python3
"""
Setup script for AI Audio Chatbot
This script helps you set up your Cohere API key
"""

import os

def create_env_file():
    """Create .env file with the API key"""
    api_key = "oXvDi3bg3i74s3y73wEB3cbbpSF7n7D8mXikMnZO"
    
    env_content = f"COHERE_API_KEY={api_key}\n"
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print(f"📝 API Key configured: {api_key[:10]}...{api_key[-10:]}")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'cohere', 'speechrecognition', 
        'pyaudio', 'gtts', 'playsound', 'python-dotenv', 'requests', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed!")
        return True

def main():
    print("🎤 AI Audio Chatbot Setup")
    print("=" * 40)
    
    # Create .env file
    print("\n1. Setting up API key...")
    if create_env_file():
        print("   ✅ API key configured successfully!")
    else:
        print("   ❌ Failed to configure API key")
        return
    
    # Check dependencies
    print("\n2. Checking dependencies...")
    if check_dependencies():
        print("   ✅ All dependencies are ready!")
    else:
        print("   ⚠️  Some dependencies are missing")
        print("   💡 Run: pip install -r requirements.txt")
    
    print("\n" + "=" * 40)
    print("🚀 Setup complete! You can now run the chatbot:")
    print("   python app.py")
    print("   or double-click run.bat (Windows)")
    print("\n🌐 Open your browser to: http://localhost:5000")

if __name__ == "__main__":
    main() 