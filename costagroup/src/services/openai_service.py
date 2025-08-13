from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from src.models.job import Job
from src.models.all_jobs import AllJobs
import datetime

prompt = """
You are an expert in job screening for travelers. Your goal is to evaluate whether a job offer in Australia is suitable for a backpacker on a Working Holiday Visa, looking for temporary work.

SALARY/HOURLY RATE RULES:
- AUTOMATICALLY REJECT any job offering over $80,000 annual salary or over $60 per hour
- AUTOMATICALLY ACCEPT any job offering under $35 per hour (respond "yes")

REQUIRED KEYWORDS (if any of these are present, the job should be accepted):
No experience, Warehouse, Cleaning, Cleaner, Labourer, Pick, Packer, Process worker, Factory, Traffic controller, Kitchen hand, Unskilled, General hand, Farm hand, Picking, Fruit picking, Grower, Packing, Roadhouse, Housekeeping, Hospitality

EXCLUSION KEYWORDS (if any of these are present, the job should be rejected):
Senior, Experienced, Manager, Managers, Director, Supervisor

EVALUATION PROCESS:
1. First check salary/hourly rate - apply automatic rules above
2. Check for exclusion keywords - if found, respond "no"
3. Check for required keywords - if found, respond "yes"
4. For remaining jobs, evaluate if suitable for backpacker profile (manual, low-skilled, temporary work in farming, hospitality, cleaning, warehouse, construction, etc.)

Analyze the job offer below and reply with only one word, chosen from the following:

yes – the job clearly fits a backpacker profile
no – the job is not suitable for a backpacker  
maybe – the job might be suitable, but some important information is missing or unclear

Do not include any other words, explanation, or formatting in your answer.

Here is the job offer:

"""


class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def test_job(self, job: Job):
        # This method is a placeholder for testing job data with OpenAI
        # You can implement your logic here to interact with OpenAI's API

        try:
            description = job.description or ""
            if not description:
                return "no"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n Title: {job.title}\n\n Salary: {job.salary if job.salary else 'N/A'}\n\nDescription: {description}",
                    },
                ],
            )
            result = response.choices[0].message.content
            print(result)
            if result in ["yes", "no", "maybe"]:
                print(f"Job {job.url} result: {result}")
                return result
            else:
                print(f"Job {job.url} result: unexpected response {result}")
                return "error"
        except Exception as e:
            print(f"Error processing job {job.url}: {e}")
            return "error"
