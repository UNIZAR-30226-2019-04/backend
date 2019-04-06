from app.main.model.categoria import Categoria
from .. import db


def insertar_categorias(data):
    categorias = data['nombres']
    for categoria in categorias:
        new_categoria = Categoria(
            nombre=categoria
        )
        save_changes(new_categoria)
    return {"Respuesta": "Return WIP, checkear manualmente si OK"}


def get_all_categorias():
    return Categoria.query.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
