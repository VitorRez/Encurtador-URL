from EncurtadorURL.core.database.utils.hash import *
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='urldb',
    user='euufsj',
    password='euufsj'
)

cur = conn.cursor()

p_hash = create_hash('3684deug')

cur.execute(f"INSERT INTO USUARIO (USERNAME, EMAIL, PASSWORD_HASH) VALUES ('Vitor', 'vitorez2002@gmail.com', '{p_hash}');")
conn.commit()

cur.close()
conn.close()