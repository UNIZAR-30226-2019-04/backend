import uuid

from flask import request
from flask_restplus import Resource
import os

from app.main.config import URL_MULTIMEDIA
from app.main.model.producto import Producto
from app.main.model.multimedia import Multimedia
from app.main.model.usuario import Usuario
from app.main.model.seguir import Seguir
from app.main.util.dto import MultimediaDto
from app.main.service.multimedia_service import save_changes, enviar_mail

api = MultimediaDto.api

UPLOAD_FOLDER = '/var/www/html/producto/'
#UPLOAD_FOLDER = '/srv/http/'
SERVER_ROUTE = URL_MULTIMEDIA + '/producto/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}


@api.route('/')
class MultimediaGet(Resource):
    @api.response(200, 'OK.')
    @api.marshal_list_with(MultimediaDto.multimedia, envelope='data')
    def get(self):
        """Devuelve la lista de imágenes."""

        # Parámetros opcionales:
        producto = request.args.get('producto', default=None, type=int)

        if producto is None:
            return Multimedia.query.all()
        else:
            return Multimedia.query.filter_by(producto=producto).all()


@api.route('/<id_producto>')
class MultimediaPost(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    def post(self, id_producto):
        """Sube una imagen"""

        # check if the post request has the file part
        if 'file' not in request.files:
            return ({'status': 'fail', 'error': 'no file'}), 400

        # check if product exists
        prod = Producto.query.filter_by(id=id_producto, borrado=False).first()
        if prod:
            file = request.files['file']
            if file and '.' in file.filename:
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                if file_extension in ALLOWED_EXTENSIONS:
                    file_path = str(uuid.uuid4()) + '.' + file_extension  # Random image path
                    file.save(os.path.join(UPLOAD_FOLDER, file_path))
                    new_multimedia = Multimedia(
                        path=SERVER_ROUTE + file_path,
                        tipo=file_extension == "mp4",
                        producto=id_producto
                    )
                    save_changes(new_multimedia)
                    if len(Multimedia.query.filter_by(producto=id_producto).all()) == 2:
                        vendedor = Usuario.query.filter_by(id=prod.vendedor).first()
                        seguidores_id = Seguir.query.filter_by(seguido=vendedor.id).all()
                        for seguidor_id in seguidores_id:
                            seguidor = Usuario.query.filter_by(id=seguidor_id).first()
                            enviar_mail(vendedor, prod, seguidor)
                    return ({'status': 'success', 'message': 'Archivo subido correctamente',
                             "data": [{"path": SERVER_ROUTE + file_path}]}), 200
                return ({'status': 'fail', 'error': 'extension not allowed'}), 400
            return ({'status': 'fail', 'error': 'file not allowed'}), 400
        return ({'status': 'fail', 'error': 'product not found'}), 400
