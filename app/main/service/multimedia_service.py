from app.main import db
from ..config import mailer
from app.main.service.generar_email import generateEmail_2


def enviar_mail(vendedor, prod, user):
    print("Enviar email")
    try:
        html_email = generateEmail_2(vendedor, prod, user)
        mailer.send(
            subject=vendedor.nick + 'Ha subido un nuevo producto',
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
