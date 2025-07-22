import sqlite3

BANCO_DE_DADOS = "itens.db"

def conectar():
    conexao = sqlite3.connect(BANCO_DE_DADOS)
    conexao.row_factory = sqlite3.Row
    return conexao

#Cria a tabela se ela não existir
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens(
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        marca TEXT,
        descricao TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco DOUBLE NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()

def obter_itens(filtro_nome=None):
    conexao = conectar()
    cursor = conexao.cursor()
    #Esse filtro é pra pesquisa exibir os itens que correspondem ao que ele pesquisou
    if filtro_nome:
        cursor.execute("SELECT * FROM itens WHERE nome LIKE ?", (f"%{filtro_nome}%",))
    else:
        cursor.execute("SELECT * FROM itens")
    itens = cursor.fetchall()
    conexao.close()
    #Aqui tem a formataçao de todos os atributos do item, assim o preço unitario e total ficam formatados em reais
    itens_formatados = []
    for item in itens:
        preco = item['preco']
        quantidade = item['quantidade']
        total = preco * quantidade
        itens_formatados.append({
            "id": item["id"],
            "nome": item["nome"],
            "marca": item["marca"],
            "descricao": item["descricao"],
            "quantidade": quantidade,
            "preco": f"R$ {preco:.2f}".replace(".", ","),
            "preco_total": f"R$ {total:.2f}".replace(".", ",")
        })
    return itens_formatados

def buscar_item(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM itens WHERE id = ?", (id_item,))
    item = cursor.fetchone()
    conexao.close()
    return item

def existe_item(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM itens WHERE id = ?", (id_item,))
    #Verifica se a consulta retornou algum registro
    existe = cursor.fetchone() is not None
    conexao.close()
    return existe

def inserir_item(id_item, nome, marca, descricao, quantidade, preco):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO itens (id, nome, marca, descricao, quantidade, preco) VALUES (?, ?, ?, ?, ?, ?)",
        (id_item, nome, marca, descricao, quantidade, preco)
    )
    conexao.commit()
    conexao.close()

def atualizar_item_bd(id_item, nome, marca, descricao, quantidade, preco):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE itens SET nome = ?, marca = ?, descricao = ?, quantidade = ?, preco = ? WHERE id = ?",
        (nome, marca, descricao, quantidade, preco, id_item)
    )
    conexao.commit()
    conexao.close()

def excluir_item(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM itens WHERE id = ?", (id_item,))
    conexao.commit()
    conexao.close()

def proximo_id_disponivel():
    conexao = conectar()
    cursor = conexao.cursor()
    #Busca todos os ids da tabela 'itens', ordenados
    cursor.execute("SELECT id FROM itens ORDER BY id")
    #Pega todos os ids e armazena em uma lista
    ids = [row["id"] for row in cursor.fetchall()]
    conexao.close()
    #Começa verificando o próximo id possível a partir do 1
    proximo = 1
    for id_atual in ids:
        if id_atual == proximo:
            proximo += 1
        else:
            break
    return proximo
