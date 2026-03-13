from db_config import conectar

def cadastrar_produto(nome, descricao, quantidade, estoque_minimo, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produto (nome, descricao, quantidade, estoque_minimo, preco)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, descricao, quantidade, estoque_minimo, preco))
    conn.commit()
    conn.close()
