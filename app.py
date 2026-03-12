import sqlite3
import hashlib

# Conexão com banco
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

# Criação de tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    perfil TEXT NOT NULL,
    senha TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    minimo INTEGER NOT NULL
)
""")

# Função para criptografar senha
def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Exemplo de cadastro de usuário
def cadastrar_usuario(nome, perfil, senha):
    senha_hash = criptografar_senha(senha)
    cursor.execute("INSERT INTO usuarios (nome, perfil, senha) VALUES (?, ?, ?)",
                   (nome, perfil, senha_hash))
    conn.commit()

# Exemplo de cadastro de produto
def cadastrar_produto(nome, quantidade, minimo):
    cursor.execute("INSERT INTO produtos (nome, quantidade, minimo) VALUES (?, ?, ?)",
                   (nome, quantidade, minimo))
    conn.commit()

# Teste inicial
cadastrar_usuario("admin", "Administrador", "1234")
cadastrar_produto("Caneta", 100, 10)
