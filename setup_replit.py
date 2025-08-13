#!/usr/bin/env python3
"""
Replit Setup Script for Austra Job Scraping Project
This script sets up the environment specifically for Replit hosting.
"""

import os
import sys
import subprocess
import time
import signal
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_postgres():
    """Start PostgreSQL service and create database"""
    try:
        print("🗄️  Starting PostgreSQL...")
        
        # Start PostgreSQL service
        subprocess.run(["pg_ctl", "-D", "/home/runner/.local/share/postgresql/data", "start"], 
                      check=True, capture_output=True)
        
        # Wait for PostgreSQL to be ready
        time.sleep(3)
        
        print("✅ PostgreSQL started successfully")
        
        # Create database
        create_database()
        
    except Exception as e:
        print(f"⚠️  PostgreSQL setup warning: {e}")
        print("Continuing with setup...")

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
            print(f"📝 Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully!")
        else:
            print(f"✅ Database '{db_name}' already exists.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️  Database creation warning: {e}")
        print("Continuing with setup...")

def install_dependencies():
    """Install Python dependencies for all projects"""
    projects = ["agrilabour", "apgworkforce", "costagroup", "workforceaustralia"]
    
    for project in projects:
        print(f"\n📦 Installing dependencies for {project}...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{project}/requirements.txt"], 
                                  check=True, capture_output=True, text=True)
            print(f"✅ Dependencies installed for {project}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning installing dependencies for {project}: {e}")
            print(f"Error output: {e.stderr}")

def setup_chrome_environment():
    """Set up Chrome environment variables for Selenium"""
    # Set Chrome binary path for Nix environment
    chrome_path = "/nix/store/*/bin/chromium"
    chromedriver_path = "/nix/store/*/bin/chromedriver"
    
    # Find actual paths
    try:
        chrome_result = subprocess.run(["which", "chromium"], capture_output=True, text=True)
        if chrome_result.returncode == 0:
            os.environ["CHROME_BIN"] = chrome_result.stdout.strip()
            print(f"✅ Chrome binary found: {os.environ['CHROME_BIN']}")
    except:
        pass
    
    try:
        chromedriver_result = subprocess.run(["which", "chromedriver"], capture_output=True, text=True)
        if chromedriver_result.returncode == 0:
            os.environ["CHROMEDRIVER_PATH"] = chromedriver_result.stdout.strip()
            print(f"✅ ChromeDriver found: {os.environ['CHROMEDRIVER_PATH']}")
    except:
        pass

def create_env_file():
    """Create a .env file with Replit-specific settings"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("\n📝 Creating .env file for Replit...")
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

# Selenium Configuration
USE_REMOTE_SELENIUM=false
CHROME_BIN=/nix/store/*/bin/chromium
CHROMEDRIVER_PATH=/nix/store/*/bin/chromedriver
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created for Replit. Please update it with your actual values.")
    else:
        print("✅ .env file already exists.")

def create_main_entry():
    """Create a main entry point for Replit"""
    main_content = '''#!/usr/bin/env python3
"""
Main entry point for Austra Job Scraping Project on Replit
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("🚀 Austra Job Scraping Project")
    print("=" * 40)
    print("Available scrapers:")
    print("1. agrilabour")
    print("2. apgworkforce")
    print("3. costagroup")
    print("4. workforceaustralia")
    print()
    
    choice = input("Enter the number of the scraper to run (1-4): ").strip()
    
    scrapers = {
        "1": "agrilabour",
        "2": "apgworkforce", 
        "3": "costagroup",
        "4": "workforceaustralia"
    }
    
    if choice in scrapers:
        scraper = scrapers[choice]
        print(f"\\n🔄 Starting {scraper} scraper...")
        
        # Change to scraper directory and run
        os.chdir(scraper)
        os.system(f"python main.py")
    else:
        print("❌ Invalid choice. Please enter a number between 1-4.")

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w") as f:
        f.write(main_content)
    print("✅ Main entry point created")

def main():
    print("🚀 Setting up Austra Job Scraping Project for Replit")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Set up Chrome environment
    setup_chrome_environment()
    
    # Install dependencies
    print("\n📦 Installing Python dependencies...")
    install_dependencies()
    
    # Set up PostgreSQL
    print("\n🗄️  Setting up PostgreSQL...")
    setup_postgres()
    
    # Create main entry point
    create_main_entry()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your actual credentials")
    print("2. Click 'Run' to start the application")
    print("3. Choose which scraper to run from the menu")
    print("\n🔧 Environment ready for Replit hosting!")

if __name__ == "__main__":
    main() 