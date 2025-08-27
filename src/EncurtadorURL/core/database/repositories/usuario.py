from ..connection import connect_to_db
from ..utils.hash import create_hash, verify_hash, verify_hash_with_hash

def create_user(username, email, password):
    conn = connect_to_db()
    cur = conn.cursor()

    p_hash = create_hash(password)
    
    try:
        cur.execute(f"INSERT INTO USUARIO (USERNAME, EMAIL, PASSWORD_HASH) VALUES ('{username}', '{email}', '{p_hash}');")
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Usuario criado com sucesso!"}

    except Exception as e:
        cur.close()
        conn.close()

        return {"error": "Email ou nome de usuário em uso."}

def get_users():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO;")
    return cur.fetchall()

def get_user_by_username(username):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO WHERE USERNAME = '{username}';")
    return cur.fetchone()

def get_user_by_email(email):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO WHERE EMAIL = '{email}';")
    return cur.fetchone()

def get_user_by_id(id):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO WHERE ID = '{id}';")
    return cur.fetchone()

def verify_password(email, password):
    user = get_user_by_email(email)

    if user == None:
        return None

    if verify_hash(password, user['password_hash']):
        return user
    
    return None

def update_user(user_id, username=None, email=None, password=None):
    conn = connect_to_db()
    cur = conn.cursor()

    updates = []
    values = []

    if username:
        updates.append("USERNAME = %s")
        values.append(username)
    
    if email:
        updates.append("EMAIL = %s")
        values.append(email)
    
    if password:
        p_hash = create_hash(password)
        updates.append("PASSWORD_HASH = %s")
        values.append(p_hash)

    if not updates:  # nada para atualizar
        cur.close()
        conn.close()
        return {"message": "Nenhuma alteração feita."}

    values.append(user_id)
    query = f"UPDATE USUARIO SET {', '.join(updates)} WHERE ID = %s"

    try:
        cur.execute(query, tuple(values))
        conn.commit()

        cur.close()
        conn.close()
        return {"message": "Usuário atualizado com sucesso!"}
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return {"error": str(e)}