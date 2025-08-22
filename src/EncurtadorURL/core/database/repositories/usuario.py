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

        return {"success": True, "message": "usuario criado com sucesso!"}

    except Exception as e:
        cur.close()
        conn.close()

        return {"success": False, "error": str(e)}

def get_users():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO;")
    return cur.fetchall()

def get_user(username):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT ID, USERNAME, EMAIL, PASSWORD_HASH FROM USUARIO WHERE USERNAME = '{username}';")
    return cur.fetchone()

def verify_password(username, password):
    user = get_user(username)

    if user == None:
        return None
    
    print(password)

    if verify_hash(password, user['password_hash']):
        return user
    
    return None