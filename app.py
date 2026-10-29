from flask import Flask, render_template, request, redirect, url_for, jsonify # usa flask pra poder navegar nas páginas e no banco de dados
from users import create_professor, get_professores
import sqlite3
app = Flask(__name__)


@app.route ('/cadastrar-professor', methods=['POST']) # rota para cadastrar o professor
def cadastrar_professor ():
    nome = request.form.get('nome', '').strip().title()
    email = request.form.get('email', '').strip().lower()
    telefone = request.form.get('telefone', '').strip()
    coordenacao = request.form.get('coordenacao', '').strip()

    if not nome or not email or not telefone or not coordenacao:
        return "Todos os campos são obrigatórios", 400

    try:
        create_professor(nome, email, telefone, coordenacao)

    except sqlite3.IntegrityError:
        return "Não foi possível cadastrar. Verifique se o e-mail já existe", 400

    return redirect(url_for('gerenciarprofessores'))


@app.route ('/consultar-professor', methods=['GET']) # rota para consultar cadastro do professor
def consultar_professor ():
    return jsonify(get_professores())


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
