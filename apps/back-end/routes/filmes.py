from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from data.filmes_mock import filmes
from schemas.filme_schema import FilmeSchema

filmes_bp = Blueprint("filmes", __name__)


@filmes_bp.route("/filmes", methods=["GET"])
def listar_filmes():
    """
    Lista todos os filmes
    ---
    tags:
      - Filmes
    responses:
      200:
        description: Lista de filmes
    """
    return jsonify(filmes)

# GET POR ID
@filmes_bp.route("/filmes/<int:id>", methods=["GET"])
def buscar_filme(id):
    """
    Busca filme por ID
    ---
    tags:
      - Filmes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Filme encontrado
    """
    for filme in filmes:
        if filme["id"] == id:
            return jsonify(filme)

    return jsonify({"erro": "Filme não encontrado"}), 404


@filmes_bp.route("/filmes", methods=["POST"])
def criar_filme():
    try:
        dados = request.json

        filme_validado = FilmeSchema(**dados)

        novo_filme = {
            "id": len(filmes) + 1,
            "nome": filme_validado.nome,
            "genero": filme_validado.genero
        }

        filmes.append(novo_filme)

        return jsonify({
            "mensagem": "Filme criado com sucesso",
            "filme": novo_filme
        }), 201

    except ValidationError as erro:
        return jsonify({
            "erro": erro.errors()
        }), 400