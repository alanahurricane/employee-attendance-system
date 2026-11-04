from flask import Flask, render_template, request, redirect, url_for, jsonify # usa flask pra poder navegar nas páginas e no banco de dados
from users import create_professor, get_professores, erase_professor, edit_professor
from ponto import create_ponto, get_pontos
import sqlite3
app = Flask(__name__)


@app.route ('/cadastrar-professor', methods=['POST']) # rota para cadastrar o professor
def cadastrar_professor ():
    email = request.form.get('email', '').strip().lower()
    nome = request.form.get('nome', '').strip().title()
    telefone = request.form.get('telefone', '').strip()
    coordenacao = request.form.get('coordenacao', '').strip()

    if not nome or not email or not telefone or not coordenacao:
        return "Todos os campos são obrigatórios", 400

    try:
        create_professor(email, nome, telefone, coordenacao)

    except sqlite3.IntegrityError:
        return "Não foi possível cadastrar. Verifique se o e-mail já existe", 400

    return redirect(url_for('gerenciarprofessores'))

@app.route ('/consultar-professor', methods=['GET']) # rota para consultar cadastro do professor
def consultar_professor ():
    return jsonify(get_professores())


@app.route('/editar-professor', methods=['POST']) # rota para editar o cadastro do professor
def editar_professor():
    email_antigo = request.form.get('email_antigo', '').strip().lower() # identifica o email antigo que será substituído
    email = request.form.get('email', '').strip().lower() # novo email a ser armazenado
    nome = request.form.get('nome', '').strip().title()
    telefone = request.form.get('telefone', '').strip()
    coordenacao = request.form.get('coordenacao', '').strip()

    if not email_antigo or not email or not nome or not telefone or not coordenacao:
        return "Todos os campos são obrigatórios", 400

    try:
        edit_professor(email_antigo, email, nome, telefone, coordenacao)

    except sqlite3.IntegrityError:
        return "Não foi possível editar. Verifique se o e-mail já existe.", 400

    return '', 204


@app.route('/excluir-professor', methods=['POST'])  # rota para excluir professor selecionado
def excluir_professor():
    email = request.form.get('email', '').strip().lower()

    if not email:
        return "E-mail não informado", 400

    erase_professor(email)

    return '', 204

@app.route ('/create-ponto', methods=['POST']) # rota para criar ponto
def cadastrar_ponto ():
    data_criacao = request.form.get('data_criacao', '').strip()
    status = request.form.get('status', '').strip()
    tipo_ponto = request.form.get('tipo_ponto', '').strip()
    
    if not data_criacao or not status or not tipo_ponto:
        return "Nem todos os campos foram preenchidos pelo servidor", 400

    try:
        create_ponto(data_criacao, status, tipo_ponto)
    except sqlite3.IntegrityError:
        return "Não foi possível criar o ponto"
    return '', 204

@app.route('/consultar-pontos', methods=['GET']) # caminho para consultar os pontos
def consultar_pontos():
    pontos = get_pontos()
    return jsonify(pontos)

# listas de mudanças de página
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/bater.ponto')
def baterponto():
    return render_template('bater.ponto.html')

@app.route('/registros.usuario')
def registros():
    return render_template('registros.usuario.html')

@app.route('/gerenciar.professores')
def gerenciarprofessores():
    return render_template('gerenciar.professores.html')

@app.route('/lista.pontos.agente')
def listapontosagente():
    return render_template('lista.pontos.agente.html')

@app.route('/lista.pontos.coordenador')
def listapontoscoordenador():
    return render_template('lista.pontos.coordenador.html')

if __name__ == '__main__':
    app.run(debug=True)
