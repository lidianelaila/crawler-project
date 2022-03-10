#PARA RODAR ESSE ARQUIVO:
#export FLASK_APP=api.py
#set FLASK_APP=api.py
#flask run
import buscas

from flask import Flask,request,jsonify
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/<string:txt>",methods=["GET"])
def busca(txt):
    result = buscas.pesquisaPeso(txt)
    # print(result)
    return jsonify(result)

#RESULTADOS INTERESSANTES
#mortes por covid
#tecnologias novas
