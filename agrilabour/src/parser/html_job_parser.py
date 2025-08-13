import os, sys, logging, re
from bs4 import BeautifulSoup
from src.models.job import Job
from datetime import date




def html_job_parser(html_content, url):
    logger = logging.getLogger("HtmlParserUrl")    
    soup = BeautifulSoup(str(html_content), 'html.parser')
    # title description state suburb job_type salary duration start_date

    title = find_title(soup, logger)
    description = find_description(soup, logger)
    state = find_state(soup, logger)
    suburb = find_suburb(soup, logger)
    job_type = find_job_type(soup, logger)
    salary = find_salary(soup, logger)
    duration = find_duration(soup, logger)
    start_date = find_start_date(soup, logger)
    job = Job(
        title=title,
        description=description,
        state=state,
        suburb=suburb,
        job_type=job_type,
        salary=salary,
        duration=duration,
        start_date=start_date,
        created_at=date.today().isoformat(),
        url=url
    )
    return job



def find_title(soup, logger):
    try:
        title = soup.find("div", class_="job-detail-top").find("h2").get_text().strip().split(" - ")[0].strip()
    except Exception as e:
        logger.warning(f"Error finding title: {str(e)}")
        title = None
    finally:
        return title


def find_description(soup, logger):
    try:
        description = soup.find("div", class_="job-detail-bottom").get_text().strip()
    except Exception as e:
        logger.warning(f"Error finding description: {str(e)}")
        description = None
    finally:
        return description

def find_state(soup, logger):
    try:
        state = soup.find("div", class_="job-detail-top").find("h2").get_text().strip().split(",")[-1].strip()
    except Exception as e:
        logger.warning(f"Error finding state: {str(e)}")
        state = None
    finally:
        return state

def find_suburb(soup, logger):
    try:
        suburb = soup.find("div", class_="job-detail-top").find("h2").get_text().strip().split(" - ")[1].split(",")[0].strip()
    except Exception as e:
        logger.warning(f"Error finding suburb: {str(e)}")
        suburb = None
    finally:
        return suburb         

def find_job_type(soup, logger):
    try:
        job_type = "casual"
    except Exception as e:
        logger.warning(f"Error finding job_type: {str(e)}")
        job_type = None
    finally:
        return job_type

def find_salary(soup, logger):
    try:
        salary = soup.find("li", string=lambda text: text and "per hour" in text).get_text().strip()
    except Exception as e:
        logger.warning(f"Error finding salary: {str(e)}")
        salary = None
    finally:
        return salary

def find_duration(soup, logger):
    try:
        duration = soup.find("li", string=lambda text: text and "Duration:" in text).get_text().strip().split(":")[-1].strip()
    except Exception as e:
        logger.warning(f"Error finding duration: {str(e)}")
        duration = None
    finally:
        return duration

def find_start_date(soup, logger):
    try:
        title = soup.find("li", string=lambda text: text and "Start:" in text).get_text().strip().split(":")[-1].strip()
    except Exception as e:
        logger.warning(f"Error finding title: {str(e)}")
        title = None
    finally:
        return title