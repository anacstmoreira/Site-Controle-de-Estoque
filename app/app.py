import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import NotFound

import database

app = Flask(__name__)
#Chave q o Flask usa pras mensagens flash
app.secret_key = os.urandom(24)

@app.route("/")
def pagina_inicial():
    #Essa linha pega o texto digitado na busca da URL, remove espaços extras, e, se não tiver nada, define como vazio
    termo = request.args.get("pesquisa", "").strip()
    itens = database.obter_itens(termo if termo else None)
    return render_template("index.html", itens=itens)

@app.route("/novo")
def novo_item():
    #Pega o proximo id desponivel, ocorre no arquivo database pra organizar melhor
    proximo_id = database.proximo_id_disponivel()
    return render_template("novo.html", proximo_id=proximo_id)

@app.route("/adicionar", methods=["POST"])
def adicionar_item():
    #Isso é um tratamento de erro pra caso o id ja exista no banco de dados
    try:
        id_novo = int(request.form["id"])
    except ValueError:
        flash("ID inválido.", "erro")
        return redirect(url_for("novo_item"))

    nome_novo = request.form["nome"]
    marca_nova = request.form["marca"]
    descricao_nova = request.form["descricao"]

    #Tratamento pra quantidade
    try:
        quantidade_nova = int(request.form["quantidade"])
    except ValueError:
        flash("Quantidade inválida. Use apenas números inteiros.", "erro")
        return redirect(url_for("novo_item"))

    #Tratamento pra preço
    try:
        preco_novo = float(request.form["preco"].replace(",", "."))
    except ValueError:
        flash("Preço inválido. Use apenas números e ponto ou vírgula.", "erro")
        return redirect(url_for("novo_item"))

    #Abaixo são limitadores e/ou condiçoes para os atributos
    if id_novo < 0:
        flash("O ID não pode ser negativo", "erro")
        return redirect(url_for("novo_item"))

    if len(nome_novo) > 40:
        flash("Máximo de caracteres para marca é 100.", "erro")
        return redirect(url_for("novo_item"))

    if len(marca_nova) > 40:
        flash("Máximo de caracteres para marca é 100.", "erro")
        return redirect(url_for("novo_item"))

    if len(descricao_nova) > 200:
        flash("Máximo de caracteres para descrição é 100.", "erro")
        return redirect(url_for("novo_item"))

    if quantidade_nova < 0:
        flash("Quantidade não pode ser negativa.", "erro")
        return redirect(url_for("novo_item"))
    elif quantidade_nova > 9999999999:
        flash("Quantidade é muito alta.", "erro")
        return redirect(url_for("novo_item"))

    if preco_novo < 0:
        flash("Preço deve ser maior ou igual a zero.", "erro")
        return redirect(url_for("novo_item"))
    elif preco_novo > 9999999999:
        flash("Preço é muito alto.", "erro")
        return redirect(url_for("novo_item"))

    if database.existe_item(id_novo):
        flash("Já existe um item com esse ID.", "erro")
        return redirect(url_for("novo_item"))

    database.inserir_item(id_novo, nome_novo, marca_nova, descricao_nova, quantidade_nova, preco_novo)

    flash("Item adicionado com sucesso!", "sucesso")
    return redirect(url_for("pagina_inicial"))

#Exclusao de item pelo id, o id é procurado no banco de dados e após excluir voltamos pra pagina principal(recarrega a pagina)
@app.route("/excluir/<id_item>")
def excluir_item(id_item):
    #Isso serve para mostrar mensagem de erro para caso tentem acessar id invalidos pela rota
    if not id_item.isdigit():
        flash("ID inválido.", "erro")
        return redirect(url_for("pagina_inicial"))

    id_item = int(id_item)

    if not database.existe_item(id_item):
        flash("Esse ID não existe.", "erro")
        return redirect(url_for("pagina_inicial"))

    database.excluir_item(id_item)
    flash("Item excluído com sucesso.", "sucesso")
    return redirect(url_for("pagina_inicial"))


#Redireciona o usuario pra pagina de ediçao caso o item exista com base no id
@app.route("/editar/<id_item>")
def mostrar_edicao_form(id_item):
    #Isso serve para mostrar mensagem de erro para caso tentem acessar id invalidos pela rota
    if not id_item.isdigit():
        flash("ID inválido.", "erro")
        return redirect(url_for("pagina_inicial"))

    item = database.buscar_item(id_item)
    if item:
        return render_template("editar.html", item=item)
    else:
        flash("Item não encontrado.", "erro")
        return redirect(url_for("pagina_inicial"))

#Aqui é feito a atualização do item
@app.route("/atualizar/<int:id_item>", methods=["POST"])
def atualizar_item(id_item):
    nome_novo = request.form["nome"]
    marca_nova = request.form["marca"]
    descricao_nova = request.form["descricao"]
    quantidade_nova = int(request.form["quantidade"])
    preco_novo = float(request.form["preco"])

    database.atualizar_item_bd(id_item, nome_novo, marca_nova, descricao_nova, quantidade_nova, preco_novo)

    flash("Item atualizado com sucesso!", "sucesso")
    return redirect(url_for("pagina_inicial"))

if __name__ == "__main__":
    database.criar_tabela()
    app.run(debug=True, port=5000)
