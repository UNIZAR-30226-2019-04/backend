import bs4

from app.main.config import URL_API
from app.main.model.multimedia import Multimedia


def load_preview(file):
    # load the file
    with open(file) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, features="lxml")
    return soup


def generateEmail(user, token):
    soup = load_preview("preview.html")
    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")
    # TODO: Cambiar a https cuando sea necesario
    url_token = URL_API + "/user/" + user.public_id + "/confirmar_email/" + token.decode()
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)


def generateEmail_2(vendedor, prod, user):
    soup = load_preview("mailProducto.html")
    tag_nombre = soup.find(id="titulo_prod")
    tag_nombre.string.replace_with(prod.titulo)

    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")

    tag_nombre = soup.find(id="introduccion_mail")
    tag_nombre.string.replace_with(vendedor.nick)

    imagenes = Multimedia.query.filter_by(producto=prod.id, tipo=False).all()
    if imagenes:
        foto1 = soup.find(id="picture_1")
        foto1['src'] = imagenes[0].path

        foto2 = soup.find(id="picture_2")
        foto2['src'] = imagenes[1].path

    tag_descrp = soup.find(id="descripcion")
    tag_descrp.string.replace_with(prod.descripcion)

    url_token = "https://telocam.com/#/ProductPage?idProd=" + str(prod.id)
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)


def generateEmail_3(user):
    soup = load_preview("report.html")
    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")
    tag_nombre = soup.find(id="introduccion_mail")
    tag_nombre.string.replace_with(user.nick)
    return str(soup)


def generateEmail_4(prod, user, session):
    soup = load_preview("ganaSubasta.html")
    tag_nombre = soup.find(id="titulo_prod")
    tag_nombre.string.replace_with(prod.titulo)

    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")

    tag_nombre = soup.find(id="prod_name")
    tag_nombre.string.replace_with(prod.titulo)

    imagenes = session.query(Multimedia).filter_by(producto=prod.id, tipo=False).all()
    if imagenes:
        foto1 = soup.find(id="picture_1")
        foto1['src'] = imagenes[0].path

        foto2 = soup.find(id="picture_2")
        foto2['src'] = imagenes[1].path

    tag_descrp = soup.find(id="descripcion")
    tag_descrp.string.replace_with(prod.descripcion)

    url_token = "https://telocam.com/#/ProductPage?idProd=" + str(prod.id)
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)


def generateEmail_5(prod, user, session):
    soup = load_preview("noPujas.html")

    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")

    tag_nombre = soup.find(id="prod_name")
    tag_nombre.string.replace_with(prod.titulo)

    url_token = "https://telocam.com/#/ProductPage?idProd=" + str(prod.id)
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)


def generateEmail_6(vendedor, prod, user,session):
    soup = load_preview("mailProducto.html")
    tag_nombre = soup.find(id="titulo_prod")
    tag_nombre.string.replace_with(prod.titulo)

    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user.nick + ", ")

    tag_nombre = soup.find(id="introduccion_mail")
    tag_nombre.string.replace_with(vendedor.nick)

    #imagenes = Multimedia.query.filter_by(producto=prod.id, tipo=False).all()
    imagenes = session.query(Multimedia).filter_by(producto=prod.id, tipo=False).all()
    if imagenes:
        foto1 = soup.find(id="picture_1")
        foto1['src'] = imagenes[0].path

        foto2 = soup.find(id="picture_2")
        try:
            foto2['src'] = imagenes[1].path
        except:
            foto2['src'] = "https://multimedia.telocam.com/producto/noimage.png"

    tag_descrp = soup.find(id="descripcion")
    tag_descrp.string.replace_with(prod.descripcion)

    url_token = "https://telocam.com/#/ProductPage?idProd=" + str(prod.id)
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)
