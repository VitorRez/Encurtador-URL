from ..connection import connect_to_db
from ..utils.create_code import generate_code

def create_short_url(original_url):
    conn = connect_to_db()
    cur = conn.cursor()

    try:
        short_code = generate_code()
        cur.execute(f"INSERT INTO SHORT_URL (SHORT_CODE, ORIGINAL_URL) VALUES('{short_code}', '{original_url}');")
        conn.commit()

        cur.close()
        conn.close()

        return {"success": True, "message": "url encurtado com sucesso!"}
    
    except Exception as e:
        cur.close()
        conn.close()

        return {"success": False, "error": str(e)}
    
def create_short_url_with_code(original_url, short_code):
    conn = connect_to_db()
    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO SHORT_URL (SHORT_CODE, ORIGINAL_URL) VALUES('{short_code}', '{original_url}');")
        conn.commit()

        cur.close()
        conn.close()

        return {"success": True, "message": "url encurtado com sucesso!"}
    
    except Exception as e:
        cur.close()
        conn.close()

        return {"success": False, "error": str(e)}
    
def get_short_urls():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT SHORT_CODE, ORIGINAL_URL, CLICKS FROM SHORT_URL;")
    return cur.fetchall()

def get_short_url_by_code(short_code):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT SHORT_CODE, ORIGINAL_URL, CLICKS FROM SHORT_URL WHERE SHORT_CODE = '{short_code}';")
    return cur.fetchone()

def get_short_url_by_url(original_url):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"SELECT SHORT_CODE, ORIGINAL_URL, CLICKS FROM ORIGINAL_URL WHERE SHORT_CODE = '{original_url}';")
    return cur.fetchone()

def update_click(short_code):
    conn = connect_to_db()
    cur = conn.cursor()

    try:
        cur.execute(f"UPDATE SHORT_URL SET clicks = clicks + 1 WHERE short_code = '{short_code}';")
        conn.commit()

        cur.close()
        conn.close()

        return {"success": True, "message": "Click registrado com sucesso!"}

    except Exception as e:
        cur.close()
        conn.close()

        return {"success": False, "error": str(e)}
