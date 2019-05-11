import uuid

from flask import request
from flask_restplus import Resource
import os

from app.main.model.producto import Producto
from app.main.model.multimedia import Multimedia
from app.main.util.dto import MultimediaDto
from app.main.service.multimedia_service import get_multimedia, save_changes

api = MultimediaDto.api

UPLOAD_FOLDER = '/var/www/html/producto/'
#UPLOAD_FOLDER = '/srv/http/'
SERVER_ROUTE = 'http://155.210.47.51:10080'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}


@api.route('/')
class MultimediaGet(Resource):
    @api.expect(MultimediaDto.multimedia)
    @api.response(200, 'OK.')
    def get(self):
        """Devuelve la lista de imágenes."""

        return get_multimedia()


@api.route('/<id_producto>')
class MultimediaPost(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    def post(self, id_producto):
        """Sube una imagen"""

        # check if the post request has the file part
        if 'file' not in request.files:
            return ({'status': 'fail', 'error': 'no file'}), 400
        data = request.json
        # check if product exists
        """
        if 'producto' not in data:
            return ({'status': 'fail', 'error': 'need product id'}), 400
        id_producto = data['producto']
        """
        if Producto.query.filter_by(id=id_producto, borrado=False).first():
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
                    return ({'status': 'success', 'message': 'Archivo subido correctamente',
                             "data": [{"path": SERVER_ROUTE + file_path}]}), 200
                return ({'status': 'fail', 'error': 'extension not allowed'}), 400
            return ({'status': 'fail', 'error': 'file not allowed'}), 400
        return ({'status': 'fail', 'error': 'product not found'}), 400
