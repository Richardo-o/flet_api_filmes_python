from pydantic import BaseModel

class FilmeSchema(BaseModel):
    nome: str
    genero: str