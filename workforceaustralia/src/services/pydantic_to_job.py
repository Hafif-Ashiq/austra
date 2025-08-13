from datetime import datetime
from src.models.job import Job  # Assure-toi que ce chemin est correct
from src.schemas.api_result import (
    JobResult,
)  # ou adapte selon où sont tes modèles Pydantic


def pydantic_to_job(scored_result: JobResult, category: str) -> Job:
    job_data = scored_result.result
    return Job(
        vacancy_id=job_data.vacancyId,
        title=job_data.title,
        description=job_data.description,
        state=job_data.state,
        suburb=job_data.suburb,
        post_code=job_data.postCode,
        creation_date=job_data.creationDate,
        expiry_date=job_data.expiryDate,
        modified_date=job_data.modifiedDate,
        salary_label=job_data.salary.label if job_data.salary else None,
        industry_label=job_data.industry.label if job_data.industry else None,
        latitude=job_data.latitude,
        longitude=job_data.longitude,
        source_site=job_data.site.label if job_data.site else None,
        is_external=job_data.isExternalJob,
        is_new=job_data.isNewJob,
        score=scored_result.score,
        url=f"https://www.workforceaustralia.gov.au/individuals/jobs/details/{job_data.vacancyId}",
        created_at=datetime.utcnow(),
        category=category,
    )
