import hashlib
from db_config import conectar

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_login(login, senha):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE login=%s AND senha=%s",
                   (login, criptografar_senha(senha)))
    usuario = cursor.fetchone()
    conn.close()
    return usuario
