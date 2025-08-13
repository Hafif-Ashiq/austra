from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class CodeLabel(BaseModel):
    code: str
    label: Optional[str]


class JobResult(BaseModel):
    contractType: Optional[CodeLabel]
    creationDate: datetime
    description: str
    displayFromDate: datetime
    employerId: Optional[str]
    employerName: Optional[str]
    expiryDate: datetime
    howToApplyCode: Optional[str]
    industry: Optional[CodeLabel]
    isApplyOnlineJob: bool
    isExternalJob: bool
    isFavourite: bool
    isIndigenousJob: bool
    isNewJob: bool
    jobType: Optional[CodeLabel]
    latitude: Optional[float]
    location: Optional[CodeLabel]
    logoUrl: Optional[str]
    longitude: Optional[float]
    modifiedDate: datetime
    occupation: Optional[CodeLabel]
    organisation: Optional[CodeLabel]
    positionsAvailable: Optional[int]
    postCode: Optional[str]
    salary: Optional[CodeLabel]
    site: Optional[CodeLabel]
    state: Optional[str]
    suburb: Optional[str]
    tenure: Optional[CodeLabel]
    title: str
    vacancyId: int
    workType: Optional[CodeLabel]

    @validator("latitude", "longitude", pre=True)
    def parse_float(cls, v):
        if v is None or v == "":
            return None
        return float(v)


class ScoredResult(BaseModel):
    score: float
    result: JobResult


class JobAPIResponse(BaseModel):
    totalCount: int
    results: List[ScoredResult]
