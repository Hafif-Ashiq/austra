from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, BigInteger, Text
from src.models.base import Base

class Job(Base):
    __tablename__ = "agrilabour_jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    state = Column(String(255))
    suburb = Column(String(255))
    job_type = Column(String(255))
    salary = Column(String(255))
    duration = Column(String(255))
    start_date = Column(String(255))
    url = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    filtered = Column(String(255))

    def __repr__(self):
        return (
            f"<Job(id={self.id}, title='{self.title}', state='{self.state}', "
            f"suburb='{self.suburb}', job_type='{self.job_type}', salary='{self.salary}', "
            f"start_date={self.start_date})>"
            f" description='{self.description}...'>"
        )
    
