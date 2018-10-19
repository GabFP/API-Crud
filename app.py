from flask import Flask, jsonify, request
from BDconection import BD
import CRUD
app = Flask(__name__)

server = 'server-blackbird.database.windows.net'
user = 'mbonesso'
senha = '@Math628438'
nomebd = 'BlackBird_DB'

bd = BD(server, user, senha, nomebd)


@app.route('/', methods=['POST', 'GET'])
def index():
    return "teste"


@app.route('/create/<tabela>/', methods=['POST', 'GET'])
def create(tabela):
    if tabela == 'evento':
        content = request.get_json()
        titulo = content['titulo']
        categoria_atividade = "SELECT id from dbo.categoria_atividade WHERE id='{}'".format(
            content['categoria_atividade'])
        descricao = content['descricao']
        palestrante = content['palestrante']
        data = content['data']
        horario = content['horario']
        duracao = content['duracao']
        local = content['local']
        quantidade_vagas = content['quantidade_vagas']
        info_complementar = content['info_complementar']
        token_evento = 0
        encerrado = 0
        CRUD.crearevento(bd, titulo, categoria_atividade, descricao, palestrante, data, horario, duracao, local,
                         quantidade_vagas, info_complementar, token_evento, encerrado)
        return "criado"
    elif tabela == "categoria_atividade":
        content = request.get_json()

        titulo = content["titulo"]
        descricao = content["descricao"]
        CRUD.createcategoria_atividade(bd, id, titulo, descricao)

        return "criado"
    else:
        return "tabela não encontrada", 404


@app.route("/read/<tabela>/", methods=['POST', 'GET'])
def read(tabela):
    if tabela == "evento":
        lido = CRUD.readevento(bd)

        return jsonify(lido)

    elif tabela == "pessoa":
        content = request.get_json()
        lido = CRUD.readpessoa(bd, content["ra"])

        return jsonify(lido)

    elif tabela == "categoria_atividade":
        lido = CRUD.readcategoria_atividade(bd)

        return jsonify(lido)

    else:
        return "tabela não encontrada", 404


@app.route("/update/<tabela>/", methods=['POST', 'GET'])
def update(tabela):
    if tabela == "evento":
        con = request.get_json()
        token_evento = con["data"]+con["id"]
        CRUD.updateevento(bd, con["id"], con["titulo"], con["descricao"], con["palestrante"],
                          con["data"], con["horario"], con["duracao"], con["local"],
                          con["quantidade_vagas"], con["info_complementar"],
                          token_evento, con["encerrado"])
        return "atualizado"
    else:
        return "tabela não encontrada", 404


@app.route("/delete/<tabela>/", methods=['POST', 'GET'])
def delete(tabela):
    if tabela == "evento":
        con = request.get_json()
        CRUD.deletaevento(bd, con["id"])
        return "deletado"
    else:
        return "tabela não encontrada", 404


if __name__ == "__main__":
    app.run(debug=True)