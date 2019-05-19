from sqlalchemy import text

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.reporteUsuario import ReporteUsuario
from app.main.service.generar_email import generateEmail_3
from ..config import mailer


def save_new_reporte(data):
    user = Usuario.query.filter_by(public_id=data['reportado']).first()
    if user:
        query = "SELECT MAX(id) FROM reporte_usuario"
        result = db.engine.execute(text(query))
        d, a = {}, []
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        ind = a[0]['max']
        if ind is None:
            ind = 0
        ind += 1
        new_reporte = ReporteUsuario(
            id=ind,
            descripcion=data['descripcion'],
            tipoReporte=data['tipoReporte'],
            reportado=user.id
        )
        save_changes(new_reporte)
        reportes = ReporteUsuario.query.filter_by(reportado=user.id).all()
        if len(reportes) % 3 == 0:
            enviar_mail(user)
        response_object = {
            'status': 'success',
            'message': 'Usuario reportado',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe'
        }
        return response_object, 404


# TODO:
def enviar_mail(user):
    print("Enviar email")
    try:
        html_email = generateEmail_3(user)
        mailer.send(
            subject='Notificacion de reporte',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[user.email]
        )
        response_object = {
            'status': 'success',
            'message': 'Successfully sent.',
        }
        print(response_object)
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        print(response_object, e)
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
