import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings

def connect_to_db():
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DATABASE,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        cursor_factory=RealDictCursor
    )