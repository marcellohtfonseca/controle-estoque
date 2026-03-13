import tkinter as tk
from tkinter import messagebox
from db_config import conectar
import hashlib

# Função para criptografar senha
def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para validar login
def validar_login(login, senha):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE login=%s AND senha=%s",
                   (login, criptografar_senha(senha)))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Função para cadastrar produto
def cadastrar_produto(nome, descricao, quantidade, estoque_minimo, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produto (nome, descricao, quantidade, estoque_minimo, preco)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, descricao, quantidade, estoque_minimo, preco))
    conn.commit()
    conn.close()
    
# Função para movimentar produto
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

# Função para cadastrar usuário (somente admin)
def cadastrar_usuario(nome, login, senha, perfil):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuario (nome, login, senha, perfil)
        VALUES (%s, %s, %s, %s)
    """, (nome, login, criptografar_senha(senha), perfil.upper()))
    conn.commit()
    conn.close()

# ---------------- INTERFACE ----------------

# Tela de Login
def tela_login():
    def tentar_login():
        usuario = validar_login(entry_login.get(), entry_senha.get())
        if usuario:
            perfil = usuario['perfil'].upper()
            messagebox.showinfo("Sucesso", f"Bem-vindo {usuario['nome']}! Perfil: {perfil}")
            root.destroy()
            tela_menu(usuario)
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos")

    root = tk.Tk()
    root.title("Login - Controle de Estoque")

    tk.Label(root, text="Login:").pack()
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Senha:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    tk.Button(root, text="Entrar", command=tentar_login).pack()

    root.mainloop()

# Tela Menu Principal
def tela_menu(usuario):
    menu = tk.Tk()
    menu.title("Menu Principal")

    tk.Label(menu, text=f"Usuário: {usuario['nome']} ({usuario['perfil'].upper()})").pack()

    tk.Button(menu, text="Cadastrar Produto", command=tela_cadastro_produto).pack()
    tk.Button(menu, text="Movimentar Estoque", command=lambda: tela_movimentacao(usuario)).pack()
    tk.Button(menu, text="Listar Estoque", command=tela_listar_estoque).pack()

    # Somente ADMIN pode cadastrar novos usuários
    if usuario['perfil'].upper() == 'ADMIN':
        tk.Button(menu, text="Cadastrar Usuário", command=tela_cadastro_usuario).pack()

    menu.mainloop()

# Tela Cadastro de Produto
def tela_cadastro_produto():
    def salvar():
        try:
            cadastrar_produto(entry_nome.get(), entry_desc.get(),
                              int(entry_qtd.get()), int(entry_min.get()), float(entry_preco.get()))
            messagebox.showinfo("Sucesso", "Produto cadastrado!")
            cadastro.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade, mínimo e preço devem ser números!")

    cadastro = tk.Tk()
    cadastro.title("Cadastro de Produto")

    tk.Label(cadastro, text="Nome:").pack()
    entry_nome = tk.Entry(cadastro); entry_nome.pack()

    tk.Label(cadastro, text="Descrição:").pack()
    entry_desc = tk.Entry(cadastro); entry_desc.pack()

    tk.Label(cadastro, text="Quantidade:").pack()
    entry_qtd = tk.Entry(cadastro); entry_qtd.pack()

    tk.Label(cadastro, text="Estoque mínimo:").pack()
    entry_min = tk.Entry(cadastro); entry_min.pack()

    tk.Label(cadastro, text="Preço:").pack()
    entry_preco = tk.Entry(cadastro); entry_preco.pack()

    tk.Button(cadastro, text="Salvar", command=salvar).pack()

    cadastro.mainloop()

# Tela Movimentação
def tela_movimentacao(usuario):
    def salvar_mov():
        try:
            movimentar_produto(int(entry_id.get()), var_tipo.get(),
                               int(entry_qtd.get()), usuario['id_usuario'])
            messagebox.showinfo("Sucesso", "Movimentação registrada!")
            mov.destroy()
        except ValueError:
            messagebox.showerror("Erro", "ID e quantidade devem ser números!")

    mov = tk.Tk()
    mov.title("Movimentação de Estoque")

    tk.Label(mov, text="ID Produto:").pack()
    entry_id = tk.Entry(mov); entry_id.pack()

    tk.Label(mov, text="Tipo:").pack()
    var_tipo = tk.StringVar(value="ENTRADA")
    tk.Radiobutton(mov, text="Entrada", variable=var_tipo, value="ENTRADA").pack()
    tk.Radiobutton(mov, text="Saída", variable=var_tipo, value="SAIDA").pack()

    tk.Label(mov, text="Quantidade:").pack()
    entry_qtd = tk.Entry(mov); entry_qtd.pack()

    tk.Button(mov, text="Salvar", command=salvar_mov).pack()

    mov.mainloop()

# Tela Listagem de Estoque
def tela_listar_estoque():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produto")
    produtos = cursor.fetchall()
    conn.close()

    lista = tk.Tk()
    lista.title("Estoque Atual")

    for p in produtos:
        cor = "red" if p['quantidade'] < p['estoque_minimo'] else "black"
        tk.Label(lista, text=f"{p['id_produto']} - {p['nome']} | Qtd: {p['quantidade']}", fg=cor).pack()

    lista.mainloop()

# Tela Cadastro de Usuário (somente admin)
def tela_cadastro_usuario():
    def salvar_usuario():
        try:
            cadastrar_usuario(entry_nome.get(), entry_login.get(),
                              entry_senha.get(), var_perfil.get())
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            cadastro.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")

    cadastro = tk.Tk()
    cadastro.title("Cadastro de Usuário")

    tk.Label(cadastro, text="Nome:").pack()
    entry_nome = tk.Entry(cadastro); entry_nome.pack()

    tk.Label(cadastro, text="Login:").pack()
    entry_login = tk.Entry(cadastro); entry_login.pack()

    tk.Label(cadastro, text="Senha:").pack()
    entry_senha = tk.Entry(cadastro, show="*"); entry_senha.pack()

    tk.Label(cadastro, text="Perfil:").pack()
    var_perfil = tk.StringVar(value="COMUM")
    tk.Radiobutton(cadastro, text="Administrador", variable=var_perfil, value="ADMIN").pack()
    tk.Radiobutton(cadastro, text="Comum", variable=var_perfil, value="COMUM").pack()

    tk.Button(cadastro, text="Salvar", command=salvar_usuario).pack()

    cadastro.mainloop()

# Iniciar aplicação
tela_login()
