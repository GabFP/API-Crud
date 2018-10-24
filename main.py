from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from BDconection import BD
import pyodbc
import CRUD
import time


app = Flask(__name__)
CORS(app)
server = 'server-blackbird.database.windows.net'
user = 'mbonesso@server-blackbird'
senha = '@Math628438'
nomebd = 'BlackBird_DB'


@app.route('/', methods=['POST', 'GET'])
def index():
    return "http://178.128.75.3:5000/login/"


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if 'login_token' in request.cookies:
        return "já está logado"
    else:
        try:
            bd = BD(server, user, senha, nomebd)
        except pyodbc.OperationalError:
            return "não conectou com o BD"
        try:
            content = request.get_json()
        except TypeError:
            return "não identificou json"
        ra = content['ra']
        rasenha = content['senha']
        local = content['login']
        try:
            lido = CRUD.readpessoa(bd, ra)
        except UnboundLocalError:
            return "ra não encontrado"
        if rasenha == lido["senha"]:
            if local == "web":
                response = current_app.make_response("sucesso")
                response.set_cookie('login_token', value=f'{lido["senha"]+ra+local}', expires=time.time() + 30 * 60)
                return response
            else:
                response = current_app.make_response("sucesso")
                response.set_cookie('login_token', value=f'{lido["senha"]+ra}', expires=time.time()+30*60)
                return response
        else:
            return "senha ou ra errados"


@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    if 'login_token' in request.cookies:
        response = current_app.make_response("sucesso")
        response.set_cookie('login_token', value='', expires=0)
        return response
    else:
        return "não estava logado"


@app.route('/create/<tabela>/', methods=['POST', 'GET'])
def create(tabela):
    if 'login_token' in request.cookie and 'web' in request.cookie['login_token']:
        try:
            bd = BD(server, user, senha, nomebd)
        except pyodbc.OperationalError:
            return "não conectou com o BD"
        if tabela == 'evento':
            try:
                content = request.get_json()
            except TypeError:
                return "não identificou json"
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
            try:
                content = request.get_json()
            except TypeError:
                return "não identificou json"

            titulo = content["titulo"]
            descricao = content["descricao"]
            CRUD.createcategoria_atividade(bd, id, titulo, descricao)

            return "criado"
        else:
            return "tabela não encontrada", 404
    else:
        return "não logado"


@app.route("/read/<tabela>/", methods=['POST', 'GET'])
def read(tabela):
    if 'login_token' in request.cookies:
        try:
            bd = BD(server, user, senha, nomebd)
        except pyodbc.OperationalError:
            return "não conectou com o BD"
        if tabela == "evento":
            lido = CRUD.readevento(bd)
            return jsonify(lido)
        elif tabela == "pessoa":
            try:
                content = request.get_json()
            except TypeError:
                return "não identificou json"
            lido = CRUD.readpessoa(bd, content["ra"])
            return jsonify(lido)
        elif tabela == "categoria_atividade":
            lido = CRUD.readcategoria_atividade(bd)
            return jsonify(lido)
        else:
            return "tabela não encontrada", 404
    else:
        return "não logado"


@app.route("/update/<tabela>/", methods=['POST', 'GET'])
def update(tabela):
    if 'login_token' in request.cookies:
        try:
            bd = BD(server, user, senha, nomebd)
        except pyodbc.OperationalError:
            return "não conectou com o BD"
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
    else:
        return "não logado"


@app.route("/delete/<tabela>/", methods=['POST', 'GET'])
def delete(tabela):
    if 'login_token' in request.cookies:
        try:
            bd = BD(server, user, senha, nomebd)
        except pyodbc.OperationalError:
            return "não conectou com o BD"
        if tabela == "evento":
            con = request.get_json()
            CRUD.deletaevento(bd, con["id"])
            return "deletado"
        else:
            return "tabela não encontrada", 404
    else:
        return "não logado"


if __name__ == "__main__":
    app.run()
