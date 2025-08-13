from src.models.all_jobs import AllJobs
from src.models.job import Job

def job_to_all_jobs(job: Job):
    """
    Convert a Job instance to an AllJobs instance.
    
    Args:
        job (Job): The Job instance to convert.
    
    Returns:
        AllJobs: The converted AllJobs instance.
    """
    return AllJobs(
        publication_date=job.created_at,
        job_title=job.title,
        state=job.state,
        city=job.suburb,
        income=job.salary,
        duration=job.duration,
        url=job.url,
        filtered=job.filtered

    )