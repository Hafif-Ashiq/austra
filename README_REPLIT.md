# Austra Job Scraping - Replit Deployment

This guide will help you deploy the Austra job scraping project on Replit using Nix.

## Quick Start

1. **Fork/Import this repository to Replit**
2. **Click "Run"** - the setup script will automatically:
   - Install all dependencies
   - Set up PostgreSQL
   - Configure Chrome/Selenium for the Nix environment
   - Create the main application

3. **Update the `.env` file** with your credentials:
   ```env
   # Google Sheets Configuration
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
   GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Upload your `credentials.json`** file to the root directory

5. **Run the application** and choose which scraper to execute

## Environment Setup

### Nix Configuration
The project uses Nix for dependency management:

- **Python 3.9** with pip and virtualenv
- **PostgreSQL 15** for database
- **Chromium** and **ChromeDriver** for Selenium
- **Node.js 18** and **Yarn** (if needed)

### Automatic Setup
The `setup_replit.py` script handles:
- PostgreSQL service startup
- Database creation
- Python dependency installation
- Chrome environment configuration
- Main application creation

## Running Scrapers

### Interactive Mode
Click "Run" and choose from the menu:
1. **agrilabour** - Agrilabour job scraper
2. **apgworkforce** - APG Workforce scraper (uses Selenium)
3. **costagroup** - Costa Group scraper
4. **workforceaustralia** - Workforce Australia scraper

### Direct Execution
You can also run scrapers directly:
```bash
cd agrilabour
python main.py
```

## Database Configuration

The project automatically:
- Starts PostgreSQL service
- Creates `austra_jobs` database
- Uses default credentials (can be overridden in `.env`)

Default database settings:
- Host: `localhost`
- Port: `5432`
- Database: `austra_jobs`
- User: `postgres`
- Password: `password`

## Selenium Configuration (apgworkforce)

The apgworkforce scraper automatically detects and uses:
1. **Nix Chromium** binary
2. **Nix ChromeDriver** 
3. **webdriver-manager** as fallback
4. **System Chrome** as final fallback

No manual Chrome installation required!

## File Structure

```
austra/
├── agrilabour/          # Agrilabour scraper
├── apgworkforce/        # APG Workforce scraper (Selenium)
├── costagroup/          # Costa Group scraper
├── workforceaustralia/  # Workforce Australia scraper
├── replit.nix          # Nix dependencies
├── .replit             # Replit configuration
├── setup_replit.py     # Replit setup script
├── main.py             # Main entry point (auto-generated)
├── .env                # Environment variables
└── credentials.json    # Google Sheets credentials
```

## Environment Variables

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
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Credentials file | `credentials.json` |
| `OPENAI_API_KEY` | OpenAI API key | Required |

## Troubleshooting

### PostgreSQL Issues
- The setup script automatically starts PostgreSQL
- If you see connection errors, wait a few seconds for the service to start
- Check the console output for any setup warnings

### Selenium Issues
- Chrome and ChromeDriver are automatically installed via Nix
- The setup script configures environment variables
- Multiple fallback methods ensure compatibility

### Dependency Issues
- All dependencies are installed automatically
- If you see import errors, check the console output
- You can manually install: `pip install -r [project]/requirements.txt`

### Credentials Issues
- Make sure `credentials.json` is uploaded to the root directory
- Verify your Google Sheets ID and OpenAI API key in `.env`
- Check that the Google Sheets service account has proper permissions

## Advantages of Replit + Nix

✅ **No Docker required** - Everything runs natively
✅ **Automatic dependency management** - Nix handles all system dependencies
✅ **Consistent environment** - Same setup across all Replit instances
✅ **Easy deployment** - Just fork and run
✅ **Built-in database** - PostgreSQL included
✅ **Chrome support** - Selenium works out of the box
✅ **Free hosting** - Replit provides free hosting for this type of project

## Monitoring and Logs

- All scrapers write logs to stdout (visible in Replit console)
- Database operations are logged
- Selenium operations include detailed debugging information
- Error messages are clearly displayed

## Security Notes

- Keep your `.env` file private (don't commit it to public repos)
- Use environment variables for sensitive data
- The `credentials.json` file should be kept secure
- Consider using Replit's Secrets feature for API keys

## Performance

- Replit provides adequate resources for web scraping
- PostgreSQL runs locally for fast database access
- Chrome runs in headless mode for efficiency
- Each scraper can be run independently

The project is now fully optimized for Replit hosting with no Docker dependencies! 