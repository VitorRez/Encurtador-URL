from EncurtadorURL.core.database.utils.hash import *
from database.connection import *
import psycopg2

conn = connect_to_db()
cur = conn.cursor()

p_hash = create_hash('senha')

cur.execute(f"INSERT INTO USUARIO (USERNAME, EMAIL, PASSWORD_HASH) VALUES ('usuario', 'email', '{p_hash}');")
conn.commit()

cur.close()
conn.close()