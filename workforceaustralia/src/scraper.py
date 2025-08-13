from urllib.parse import quote
import json
from src.services.openai_service import OpenAIService
from src.webdriver.fetch_cloudscraper import Driver
from src.schemas.api_result import JobAPIResponse
from src.models.base import SessionLocal
from src.services.pydantic_to_job import pydantic_to_job
from src.models.job import Job
from src.services.google_sheets_service import GoogleSheetsService
from src.services.job_to_all_jobs import job_to_all_jobs
import os, dotenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.models.all_jobs import AllJobs
from datetime import datetime, timedelta, date

dotenv.load_dotenv()

CATEGORIES = [
    "No experience",
    "Warehouse",
    "Cleaning",
    "Cleaner",
    "Labourer",
    "Pick",
    "Packer",
    "Process worker",
    "Farm hand",
    "Picking",
    "Fruit picking",
    "Grower",
    "Packing",
    "Roadhouse",
    "Housekeeping",
    "Hospitality",
]


class WorkforceaustraliaScraper:
    """
    Workforce Australia scraper class.
    This class is responsible for scraping job listings from the Workforce Australia website.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Workforce Australia scraper.
        """
        super().__init__(*args, **kwargs)

    def get_last_scrape_date(self, db: Session, category: str) -> date:
        """
        Get the last scrape date for a specific category.
        Returns the creation_date of the most recent job for this category.
        If no jobs exist, returns a default date (7 days ago).
        """
        last_job = (
            db.query(Job)
            .filter(Job.category == category)
            .order_by(Job.creation_date.desc())
            .first()
        )

        if last_job and last_job.creation_date:
            print(f"Last scrape for '{category}': {last_job.creation_date}")
            return last_job.creation_date.date()
        else:
            # If no previous jobs, use 7 days ago as default
            default_date = datetime.now() - timedelta(days=7)
            print(f"No previous jobs for '{category}', using default: {default_date}")
            return default_date.date()

    def scrape(self):
        """
        Scrape job listings from the Workforce Australia website.
        """
        # Implement the scraping logic here
        url = (
            lambda cat, page: f"https://www.workforceaustralia.gov.au/api/v1/global/vacancies/?searchText={quote(cat)}&sort=DateAddedDescending&pageNumber={page}&pageSize=100"
        )
        for category in CATEGORIES:
            print(f"Scraping category: {category}")
            page = 1
            results = []
            db = SessionLocal()
            last_scrape_date = self.get_last_scrape_date(db, category)
            while True:
                print(f"URL: {url(category, page)}")
                print(f"Page: {page}")
                driver = Driver()
                str_data = driver.page(url(category, page))
                json_data = json.loads(str_data)
                if json_data["results"] == []:
                    break

                # Since results are sorted by date, break when we find an old job
                should_break = False
                filtered_results = []
                for result in json_data["results"]:
                    # Handle datetime parsing with or without microseconds
                    creation_date = result["result"]["creationDate"]
                    try:
                        # Try with microseconds first
                        post_date = datetime.strptime(
                            creation_date, "%Y-%m-%dT%H:%M:%S.%f"
                        ).date()
                    except ValueError:
                        # If that fails, try without microseconds
                        post_date = datetime.strptime(
                            creation_date, "%Y-%m-%dT%H:%M:%S"
                        ).date()

                    if post_date <= last_scrape_date:
                        print(
                            f"Found job from {post_date} <= last scrape {last_scrape_date}, stopping"
                        )
                        should_break = True
                        break
                    filtered_results.append(result)

                results.extend(filtered_results)

                if should_break:
                    break

                page += 1
            data = JobAPIResponse(results=results, totalCount=len(results))
            print(f"Data: {len(data.results)}")
            db = SessionLocal()

            for result in data.results:
                job = pydantic_to_job(result, category)
                exists = db.query(Job).filter_by(vacancy_id=job.vacancy_id).first()
                if not exists:
                    db.add(job)
                    db.commit()
                    db.refresh(job)
            db.close()

        self.filter_jobs()

        self.save_in_sheets()
        self.save_in_db_all()
        self.save_in_sheets_all()

    def save_in_sheets(self):
        db = SessionLocal()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

        service = GoogleSheetsService(
            spreadsheet_id, credentials_path, "workforceaustralia"
        )
        service.upload_jobs(db)

    def save_in_db_all(self):
        db: Session = SessionLocal()
        jobs = db.query(Job).all()
        for job in jobs:
            all_job_data = job_to_all_jobs(job)
            existing = db.query(AllJobs).filter_by(url=all_job_data.url).first()
            if existing:
                db.delete(existing)
                db.commit()
            print(f"\n\n\n{all_job_data.filtered}\n\n\n")
            db.add(all_job_data)
            db.commit()
        print("All jobs saved or updated in AllJobs table.")

    def save_in_sheets_all(self):
        db = SessionLocal()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

        service = GoogleSheetsService(spreadsheet_id, credentials_path, "all")
        service.upload_all(db)

    def filter_jobs(self):
        db = SessionLocal()
        jobs = db.query(Job).all()
        api_key = os.getenv("OPENAI_API_KEY")
        service = OpenAIService(api_key)
        for job in jobs:
            if job.filtered in ["yes", "no", "maybe"]:
                print(f"Job {job.url} already filtered, skipping.")
                continue
            filtered = service.test_job(job)
            job.filtered = filtered
            db.add(job)
            db.commit()
