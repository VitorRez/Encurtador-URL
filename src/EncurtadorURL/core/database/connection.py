import psycopg2
from psycopg2.extras import RealDictCursor
from .config_db import DB_CONFIG

def connect_to_db():
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        cursor_factory=RealDictCursor
    )