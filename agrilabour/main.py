from src.scraper import Scraper
from setup_logger import setup_logger
import time
from src.models.base import Base, engine
from src.models.job import Job  # important pour que la classe soit enregistrée



def main():
    setup_logger("scraper", log_to_stdout=True, level="DEBUG")
    setup_logger("webdriver", log_to_stdout=True, level="DEBUG")
    time.sleep(5)
    Base.metadata.create_all(bind=engine)
    scraper = Scraper()
    scraper.scrape()
    return



if __name__ == "__main__":
    main()