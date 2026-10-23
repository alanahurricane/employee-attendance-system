from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/lista.pontos.agentes')
def listapontosagentes():
    return render_template('lista.pontos.agentes.html')

@app.route('/lista.pontos.coordenador')
def listapontoscoordenador():
    return render_template('lista.pontos.coordenador.html')

if __name__ == '__main__':
    app.run(debug=True)