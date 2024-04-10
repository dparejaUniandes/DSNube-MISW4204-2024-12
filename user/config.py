import os
from dotenv import load_dotenv

load_dotenv()
OUR_HOST=os.getenv("DB_HOST", "127.0.0.1")
OUR_DB=os.getenv("DB_DB", "fpv_db")
OUR_USER=os.getenv("POSTGRES_USER", "postgres")
OUR_PORT=os.getenv("DB_PORT", "5432")
OUR_PW=os.getenv("POSTGRES_PASSWORD", "postgres")
OUR_JWTSECRET=os.getenv("JWT_SECRET_KEY", "secret-key")

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(OUR_USER, OUR_PW, OUR_HOST, OUR_PORT, OUR_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = OUR_JWTSECRET

