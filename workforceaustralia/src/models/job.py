from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    BigInteger,
    Text,
)
from src.models.base import Base


class Job(Base):
    __tablename__ = "workforceaustralia_jobs"

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    state = Column(String(255))
    suburb = Column(String(255))
    post_code = Column(String(255))
    creation_date = Column(DateTime)
    expiry_date = Column(DateTime)
    modified_date = Column(DateTime)
    salary_label = Column(String(255))
    industry_label = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    source_site = Column(String(255))
    is_external = Column(Boolean)
    is_new = Column(Boolean)
    score = Column(Float)
    category = Column(String(255))
    url = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    filtered = Column(String(255))
