from flask import render_template, url_for
from beluxis import app 


@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/perfil/<usuario>')
def perfil(usuario: str):
    return render_template("perfil.html", usuario=usuario)

@app.route('/produtos')
def produtos():
    return render_template("produtos.html")

@app.route('/contato')
def contato():
    return render_template("contato.html")

