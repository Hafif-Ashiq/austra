import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from src.models.job import Job
from src.models.all_jobs import AllJobs
import datetime


class GoogleSheetsService:
    def __init__(self, spreadsheet_id: str, credentials_path: str, worksheet_name: str):
        self.creds = Credentials.from_service_account_file(
            credentials_path, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.client = gspread.authorize(self.creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)

        try:
            self.sheet = self.spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            self.sheet = self.spreadsheet.add_worksheet(
                title=worksheet_name, rows="1000", cols="26"
            )

    def upload_jobs(self, db: Session):
        jobs = db.query(Job).all()

        # Inspecte les colonnes du modèle Job
        mapper = inspect(Job)
        column_names = [column.key for column in mapper.columns]

        rows = [column_names]

        for job in jobs:
            row = []
            for column in column_names:
                value = getattr(job, column, "")
                if isinstance(value, datetime.datetime):
                    value = value.date().strftime("%Y-%m-%d")
                elif isinstance(value, datetime.date):
                    value = value.strftime("%Y-%m-%d")
                row.append(value)

            rows.append(row)

        self.sheet.clear()
        self.sheet.update("A1", rows)

    def upload_all(self, db: Session):

        all_jobs = db.query(AllJobs).all()

        mapper = inspect(AllJobs)
        column_names = [column.key for column in mapper.columns]

        # filter data (only keep the rows that are in the last 7 days)
        all_jobs = [
            job
            for job in all_jobs
            if job.publication_date
            >= datetime.datetime.now() - datetime.timedelta(days=7)
        ]

        # sort data by date then by url, then by salary (if salary is not None)

        all_jobs.sort(key=lambda x: (x.publication_date, x.url))

        rows = [column_names]

        for job in all_jobs:
            row = []
            for column in column_names:
                value = getattr(job, column, "")
                if isinstance(value, datetime.datetime):
                    value = value.date().strftime("%Y-%m-%d")
                elif isinstance(value, datetime.date):
                    value = value.strftime("%Y-%m-%d")
                row.append(value)

            rows.append(row)

        self.sheet.clear()
        self.sheet.update("A1", rows)
