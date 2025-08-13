# Austra Job Scraping - Local Development Setup

This guide will help you set up the Austra job scraping project to run locally without any Docker containers.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **PostgreSQL** installed and running locally
3. **Chrome browser** (for apgworkforce Selenium scraping)
4. **Git** (to clone the repository)

## Quick Setup

### 1. Run the Setup Script

```bash
python setup_local.py
```

This script will:
- Create a sample `.env` file
- Install all Python dependencies
- Create the PostgreSQL database

### 2. Configure Environment Variables

Edit the `.env` file with your actual credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=austra_jobs
DB_USER=postgres
DB_PASSWORD=your_password

# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Selenium Configuration (optional)
USE_REMOTE_SELENIUM=false
SELENIUM_URL=http://localhost:4444/wd/hub
```

### 3. PostgreSQL Setup

Make sure PostgreSQL is running and accessible:

```bash
# On Windows (if using PostgreSQL installer)
# PostgreSQL should start automatically as a service

# On macOS (if using Homebrew)
brew services start postgresql

# On Linux (Ubuntu/Debian)
sudo systemctl start postgresql
```

Create a database user (if needed):
```sql
CREATE USER postgres WITH PASSWORD 'your_password';
ALTER USER postgres WITH SUPERUSER;
```

## Running the Scrapers

### Option 1: Local Chrome WebDriver (Recommended for apgworkforce)

The apgworkforce scraper will automatically use your local Chrome browser:

```bash
cd apgworkforce
python main.py
```

### Option 2: Manual ChromeDriver Setup (Alternative for apgworkforce)

If webdriver-manager doesn't work:

1. Download ChromeDriver manually from: https://chromedriver.chromium.org/
2. Add it to your system PATH
3. Run the scraper:
```bash
cd apgworkforce
python main.py
```

### Other Scrapers

All other scrapers can run directly without Selenium:

```bash
# Agrilabour
cd agrilabour
python main.py

# Costagroup
cd costagroup
python main.py

# Workforce Australia
cd workforceaustralia
python main.py
```

## Project Structure

```
austra/
├── agrilabour/          # Agrilabour scraper
├── apgworkforce/        # APG Workforce scraper (uses Selenium)
├── costagroup/          # Costa Group scraper
├── workforceaustralia/  # Workforce Australia scraper
├── docker-compose.yml   # Reference only (not used)
├── setup_local.py       # Local development setup script
├── .env                 # Environment variables
└── credentials.json     # Google Sheets credentials
```

## Troubleshooting

### Database Connection Issues

1. **Check PostgreSQL is running:**
   ```bash
   # Windows
   services.msc  # Look for PostgreSQL service
   
   # macOS/Linux
   ps aux | grep postgres
   ```

2. **Test connection:**
   ```bash
   psql -h localhost -U postgres -d austra_jobs
   ```

3. **Check credentials in .env file**

### Selenium Issues (apgworkforce)

1. **Chrome not found:**
   - Make sure Chrome is installed
   - The webdriver-manager will automatically download the correct ChromeDriver

2. **Permission issues:**
   - Run as administrator (Windows)
   - Check file permissions (macOS/Linux)

3. **Use remote Selenium:**
   - Start the container: `docker-compose up selenium`
   - Set `USE_REMOTE_SELENIUM=true` in .env

### Dependencies Issues

If you encounter dependency conflicts:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r agrilabour/requirements.txt
pip install -r apgworkforce/requirements.txt
pip install -r costagroup/requirements.txt
pip install -r workforceaustralia/requirements.txt
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `austra_jobs` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `password` |
| `CHROME_BIN` | Chrome binary path | Auto-detected |
| `CHROMEDRIVER_PATH` | ChromeDriver path | Auto-detected |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | Google Sheets ID | Required |
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Path to credentials file | `credentials.json` |
| `OPENAI_API_KEY` | OpenAI API key | Required |

## Development Notes

- All scrapers use SQLAlchemy with PostgreSQL
- Database tables are created automatically on first run
- Logs are written to stdout and files in each project directory
- Each scraper can be run independently
- The setup script handles most configuration automatically 