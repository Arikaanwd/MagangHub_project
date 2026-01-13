from database import get_connection
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT id_user, username
        FROM users
        WHERE username=%s
          AND password_hash=%s
          AND is_active=1
    """, (username, hash_password(password)))

    user = cur.fetchone()
    conn.close()
    return user
