import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent.joinpath('.env.test')
load_dotenv(env_path)


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
