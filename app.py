from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from users import create_professor, get_professores, erase_professor, edit_professor, verify_login
from ponto import create_ponto, get_pontos, get_pontos_professor
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-longa-e-aleatoria' # deve ser alterada por questões de segurança

@app.route('/cadastrar-professor', methods=['POST']) # rota para criar um professor
def cadastrar_professor():
    email = request.form.get('email', '').strip().lower()
    nome = request.form.get('nome', '').strip().title()
    telefone = request.form.get('telefone', '').strip()
    coordenacao = request.form.get('coordenacao', '').strip()
    senha = request.form.get('senha', '')

    if not email or not nome or not telefone or not coordenacao or not senha:
        return "Todos os campos são obrigatórios", 400

    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres", 400

    try:
        create_professor(email, nome, telefone, coordenacao, senha)

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
    # Verifica se existe um professor autenticado
    if 'email' not in session:
        return "Usuário não autenticado", 401
    
    data_criacao = request.form.get('data_criacao', '').strip()
    status = request.form.get('status', '').strip()
    tipo_ponto = request.form.get('tipo_ponto', '').strip()
    
    if not data_criacao or not status or not tipo_ponto:
        return "Nem todos os campos foram preenchidos pelo servidor", 400
    
    criador = session['email']

    try:
        create_ponto(data_criacao, status, tipo_ponto, criador)
    except sqlite3.IntegrityError:
        return "Não foi possível criar o ponto"
    return '', 204

@app.route('/consultar-pontos', methods=['GET']) # caminho para consultar os pontos
def consultar_pontos():
    pontos = get_pontos()
    return jsonify(pontos)

# listas de mudanças de página

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        if verify_login(email, senha):
            session['email'] = email
            return redirect(url_for('baterponto'))

        return render_template(
            'login.html',
            erro="E-mail ou senha incorretos."
        )

    return render_template('login.html')

def usuario_logado(): # função que verifica se alguém está logado
    return 'email' in session


@app.route('/bater.ponto')
def baterponto():
    if not usuario_logado():
        return redirect(url_for('login'))

    return render_template('bater.ponto.html')

@app.route('/registros.usuario')
def registros():
    if 'email' not in session:
        return redirect(url_for('login'))

    pontos = get_pontos_professor(session['email'])

    for ponto in pontos:
        data_hora = (ponto['data_criacao'] or '').replace(',', '').strip()
        partes = data_hora.split(maxsplit=1)

        if len(partes) == 2:
            ponto['data'] = partes[0]
            ponto['hora'] = partes[1]
        else:
            ponto['data'] = ''
            ponto['hora'] = data_hora

    return render_template('registros.usuario.html', pontos=pontos)

@app.route('/gerenciar.professores')
def gerenciarprofessores():
    return render_template('gerenciar.professores.html')

@app.route('/lista.pontos.agente')
def listapontosagente():
    return render_template('lista.pontos.agente.html')

@app.route('/lista.pontos.coordenador')
def listapontoscoordenador():
    return render_template('lista.pontos.coordenador.html')

@app.route('/logout') # encerra a sessão
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
