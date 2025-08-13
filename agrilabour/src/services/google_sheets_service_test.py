import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from src.models.job import Job

class GoogleSheetsServiceTest:
    def __init__(self, spreadsheet_id: str, credentials_path: str, worksheet_name: str):
        self.creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

    def upload_jobs(self, db: Session):
        self.sheet.update("A1", [["Hello world 👋"]])
