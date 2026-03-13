import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="marceloko",
        database="estoque"
    )

# Teste da conexão
if __name__ == "__main__":
    try:
        conn = conectar()
        print("Conexão com MySQL realizada com sucesso!")
        conn.close()
    except Exception as e:
        print("Erro na conexão:", e)
