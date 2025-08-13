from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, BigInteger, Text
from src.models.base import Base

class AllJobs(Base):
    __tablename__ = "all_jobs"

    id = Column(Integer, primary_key=True)
    publication_date = Column(DateTime, nullable=False)
    job_title = Column(String(255))
    state = Column(Text)
    city = Column(String(255))
    income = Column(String(255))
    duration = Column(String(255))
    url = Column(String(255), unique=True)
    filtered = Column(String(255))

    def __repr__(self):
        return (
            f"<AllJobs(publication_date={self.publication_date}, job_title='{self.job_title}', "
            f"state='{self.state}', city='{self.city}', income='{self.income}', "
            f"duration='{self.duration}', url='{self.url}')>"
        )