from src.webdriver.fetch_selenium import Driver
from src.models.base import SessionLocal
from src.parser.html_url_parser import html_url_parser
from src.parser.html_job_parser import html_job_parser
from src.models.job import Job
from src.services.google_sheets_service import GoogleSheetsService
from src.services.job_to_all_jobs import job_to_all_jobs
from src.services.openai_service import OpenAIService
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.models.all_jobs import AllJobs
import os, dotenv

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


class Scraper:
    """
    Workforce Australia scraper class.
    This class is responsible for scraping job listings from the Workforce Australia website.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Workforce Australia scraper.
        """
        super().__init__(*args, **kwargs)

    def scrape(self):
        """
        Scrape job listings from the Workforce Australia website.
        """
        list_product_urls = self.find_urls()
        print(f"Found {len(list_product_urls)} job URLs")

        self.scrap_jobs_and_save_in_db(list_product_urls)

        self.filter_jobs()

        self.save_in_sheets()

        self.save_in_db_all()

        self.save_in_sheets_all()

    def find_urls(self):
        main_page_url = f"https://www.apgworkforce.com.au/job-search"
        list_product_urls = []
        print(f"URL: {main_page_url}")
        try:
            driver = Driver()
            list_page_html = driver.page_url(main_page_url)
            print(f"Found {len(list_page_html)} pages to scrape")
            for i in range(len(list_page_html)):
                list_product_urls_page = html_url_parser(list_page_html[i])
                list_product_urls.extend(list_product_urls_page)
                print(f"Found {len(list_product_urls_page)} job URLs on page {i}")
        except Exception as e:
            print(f"Error scraping page : {e}")
        print(f"Total job URLs found: {len(list_product_urls)}")
        return list_product_urls

    def scrap_jobs_and_save_in_db(self, list_product_urls):
        db = SessionLocal()
        for data_url in list_product_urls:
            try:
                print(f"Scraping job URL: {data_url['url']}")
                driver = Driver()
                exists = db.query(Job).filter_by(url=data_url["url"]).first()

                if exists:
                    print(
                        f"Job {data_url['url']} already exists in the database, skipping."
                    )
                    continue

                str_data = driver.page(data_url["url"])
                job = html_job_parser(str_data, data_url["url"])
                print(job)
                if job:

                    exists = db.query(Job).filter_by(url=job.url).first()
                    db.add(job)
                    db.commit()
                    print(f"Job {job.url} added to the database.")
            except Exception as e:
                print(f"Error scraping job URL {data_url['url']}: {e}")

    def save_in_sheets(self):
        db = SessionLocal()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

        service = GoogleSheetsService(spreadsheet_id, credentials_path, "apgworkforce")
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
