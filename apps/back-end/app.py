from flask import Flask, request
from flask_restx import Api, Resource, fields
from pydantic import BaseModel

app = Flask(__name__)

app.json.ensure_ascii = False

api = Api(
    app,
    version='1.0',
    title='API de Filmes',
    description='API para cadastro de filmes'
)

ns = api.namespace('filmes', description='Operações de filmes')


filme_model = api.model('Filme', {
    'nome': fields.String(required=True, description='Nome do filme'),
    'genero': fields.String(required=True, description='Gênero do filme')
})

filmes = [
    {"id": 1, "nome": "Interestelar", "genero": "Ficção"},
    {"id": 2, "nome": "Batman", "genero": "Ação"}
]

class FilmeModel(BaseModel):
    nome: str
    genero: str


@ns.route('/')
class FilmeLista(Resource):

    def get(self):
        return filmes

    @ns.expect(filme_model)
    def post(self):

        dados = request.json

        filme = FilmeModel(**dados)

        novo_filme = {
            "id": len(filmes) + 1,
            **filme.model_dump()
        }

        filmes.append(novo_filme)

        return {
            "mensagem": "Filme cadastrado",
            "filme": novo_filme
        }, 201


@ns.route('/<int:id>')
class Filme(Resource):

    @ns.doc(params={'id': 'ID do filme'})
    def get(self, id):

        for filme in filmes:
            if filme["id"] == id:
                return filme

        return {"erro": "Filme não encontrado"}, 404


if __name__ == '__main__':
    app.run(debug=True)