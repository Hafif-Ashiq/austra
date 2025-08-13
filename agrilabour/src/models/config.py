from dotenv import load_dotenv

load_dotenv()
import os


DATABASE = {
    "USER": os.getenv("DB_USER", "postgres"),
    "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
    "HOST": os.getenv("DB_HOST", "localhost"),
    "PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "austra_jobs"),
}

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE['USER']}:{DATABASE['PASSWORD']}"
    f"@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"
)
