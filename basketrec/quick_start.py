#!/usr/bin/env python3
"""
Quick start script for the Basket Recommendation System
"""

import os
import sys
import subprocess

def print_header():
    print("=" * 60)
    print("🚀 BASKET RECOMMENDATION SYSTEM - QUICK START")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔌 Testing database connection...")
    try:
        from database_config import DatabaseConfig
        db_config = DatabaseConfig()
        if db_config.test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def generate_sample_data():
    """Generate sample data if needed"""
    print("📊 Checking for sample data...")
    try:
        from database_config import DatabaseConfig
        db_config = DatabaseConfig()
        df = db_config.get_basket_data()
        
        if df is not None and len(df) > 0:
            print(f"✅ Found {len(df)} records in database")
            return True
        else:
            print("⚠️  No data found in database")
            return False
    except:
        print("⚠️  Could not check database for data")
        return False

def run_sample_data_generator():
    """Run the sample data generator"""
    print("🛒 Would you like to generate sample data?")
    choice = input("Enter 'y' to generate sample data, or 'n' to skip: ").strip().lower()
    
    if choice == 'y':
        try:
            subprocess.run([sys.executable, "sample_data_generator.py"])
            return True
        except Exception as e:
            print(f"❌ Error generating sample data: {e}")
            return False
    return False

def start_web_application():
    """Start the Streamlit web application"""
    print("🌐 Starting web application...")
    try:
        print("🚀 Opening Streamlit app in your browser...")
        print("📱 The app will be available at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print()
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Web application stopped")
    except Exception as e:
        print(f"❌ Error starting web application: {e}")

def main():
    print_header()
    
    # Step 1: Check Python version
    print("1️⃣ Checking Python version...")
    if not check_python_version():
        return
    print()
    
    # Step 2: Install dependencies
    print("2️⃣ Installing dependencies...")
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your internet connection and try again.")
        return
    print()
    
    # Step 3: Test database connection
    print("3️⃣ Testing database connection...")
    db_connected = test_database_connection()
    if not db_connected:
        print("⚠️  Database connection failed. You can still use the application with sample data.")
    print()
    
    # Step 4: Check for data
    print("4️⃣ Checking for data...")
    has_data = generate_sample_data()
    
    if not has_data:
        print("📊 No data found. Would you like to generate sample data?")
        if run_sample_data_generator():
            has_data = True
    
    if not has_data:
        print("⚠️  No data available. The application may not work properly.")
    print()
    
    # Step 5: Start application
    print("5️⃣ Starting application...")
    print("Choose your interface:")
    print("1. Web interface (recommended)")
    print("2. Command line interface")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            start_web_application()
            break
        elif choice == "2":
            print("🖥️  Starting CLI interface...")
            try:
                subprocess.run([sys.executable, "simple_cli.py"])
            except KeyboardInterrupt:
                print("\n👋 CLI application stopped")
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 