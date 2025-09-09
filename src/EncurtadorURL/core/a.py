from EncurtadorURL.core.database.utils.hash import *
from database.connection import *
import psycopg2

conn = connect_to_db()
cur = conn.cursor()

username = 'usuario'
email = 'email'
password = 'senha'

p_hash = create_hash(password)

cur.execute(
    "SELECT COUNT(*) FROM USUARIO WHERE USERNAME = %s OR EMAIL = %s;",
    (username, email)
)
count = cur.fetchone()[0]

if count > 0:
    print("Usuário já existe no banco de dados.")
else:
    cur.execute(
        "INSERT INTO USUARIO (USERNAME, EMAIL, PASSWORD_HASH) VALUES (%s, %s, %s);",
        (username, email, p_hash)
    )
    conn.commit()
    print("Usuário cadastrado com sucesso!")

cur.close()
conn.close()
