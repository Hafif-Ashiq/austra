#!/usr/bin/env python3
"""
Local Development Setup Script
This script helps set up the local development environment for the Austra job scraping project.
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        db_name = os.getenv("DB_NAME", "austra_jobs")
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        print("Please make sure PostgreSQL is running and credentials are correct.")

def install_dependencies():
    """Install Python dependencies for all projects"""
    projects = ["agrilabour", "apgworkforce", "costagroup", "workforceaustralia"]
    
    for project in projects:
        print(f"\nInstalling dependencies for {project}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{project}/requirements.txt"], 
                         check=True, capture_output=True, text=True)
            print(f"✓ Dependencies installed for {project}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing dependencies for {project}: {e}")
            print(f"Error output: {e.stderr}")

def create_env_file():
    """Create a sample .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("\nCreating sample .env file...")
        env_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=austra_jobs
DB_USER=postgres
DB_PASSWORD=password

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Selenium Configuration (optional - for apgworkforce)
USE_REMOTE_SELENIUM=false
SELENIUM_URL=http://localhost:4444/wd/hub
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✓ Sample .env file created. Please update it with your actual values.")
    else:
        print("✓ .env file already exists.")

def main():
    print("🚀 Setting up Austra Job Scraping Project for Local Development")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    print("\n📦 Installing Python dependencies...")
    install_dependencies()
    
    # Create database
    print("\n🗄️  Setting up database...")
    create_database()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your actual credentials")
    print("2. Make sure PostgreSQL is running on localhost:5432")
    print("3. For apgworkforce (Selenium):")
    print("   - Install Chrome browser for Selenium support")
    print("   - The webdriver-manager will handle ChromeDriver automatically")
    print("4. Run any scraper: python agrilabour/main.py")
    print("\n🔧 No Docker required - everything runs locally!")

if __name__ == "__main__":
    main() 