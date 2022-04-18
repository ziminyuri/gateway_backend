import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_URL = os.getenv('POSTGRES_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ACCESS_LIFESPAN = {"hours": 1}
