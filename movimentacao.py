from db_config import conectar

def movimentar_produto(id_produto, tipo, quantidade, id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    if tipo == "ENTRADA":
        cursor.execute("UPDATE produto SET quantidade = quantidade + %s WHERE id_produto=%s",
                       (quantidade, id_produto))
    else:
        cursor.execute("UPDATE produto SET quantidade = quantidade - %s WHERE id_produto=%s",
                       (quantidade, id_produto))

    cursor.execute("""
        INSERT INTO movimentacao (id_produto, tipo, quantidade, id_usuario)
        VALUES (%s, %s, %s, %s)
    """, (id_produto, tipo, quantidade, id_usuario))

    conn.commit()
    conn.close()
