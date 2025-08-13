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
        title = soup.find("h1").get_text().strip().split("-")[0].strip()
    except Exception as e:
        logger.warning(f"Error finding title: {str(e)}")
        title = None
    finally:
        return title


def find_description(soup, logger):
    try:
        description_with_buttons = soup.find("div", class_="job-ad-body")
        # Remove buttons and other non-description text
        for tag in description_with_buttons.find_all(["button", "a", "iframe"]):
            tag.decompose()

        description = description_with_buttons.get_text(separator="\n", strip=True)
    except Exception as e:
        logger.warning(f"Error finding description: {str(e)}")
        description = None
    finally:
        return description

def find_state(soup, logger):
    try:
        state = None
    except Exception as e:
        logger.warning(f"Error finding state: {str(e)}")
        state = None
    finally:
        return state

def find_suburb(soup, logger):
    try:
        suburb = soup.find("p", class_="job-location").get_text().strip().split(":")[1].strip()
    except Exception as e:
        logger.warning(f"Error finding suburb: {str(e)}")
        suburb = None
    finally:
        return suburb         

def find_job_type(soup, logger):
    try:
        job_type = soup.find("p", class_="job-type").get_text().strip().strip()
    except Exception as e:
        logger.warning(f"Error finding job_type: {str(e)}")
        job_type = None
    finally:
        return job_type

def find_salary(soup, logger):
    try:
        salary = None
    except Exception as e:
        logger.warning(f"Error finding salary: {str(e)}")
        salary = None
    finally:
        return salary

def find_duration(soup, logger):
    try:
        duration = None
    except Exception as e:
        logger.warning(f"Error finding duration: {str(e)}")
        duration = None
    finally:
        return duration

def find_start_date(soup, logger):
    try:
        title = soup.find("p", class_="job-closing").get_text().strip().split(":")[1].strip()
    except Exception as e:
        logger.warning(f"Error finding title: {str(e)}")
        title = None
    finally:
        return title
    
def find_category(soup, logger):
    try:
        category = soup.find("p", class_="job-category").get_text().strip().split(":")[1].strip()
    except Exception as e:
        logger.warning(f"Error finding category: {str(e)}")
        category = None
    finally:
        return category