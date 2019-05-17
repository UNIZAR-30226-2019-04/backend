import bs4
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
    url_token = "http://155.210.47.51:5000/user/" + user.public_id + "/confirmar_email/" + token.decode()
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
    foto1 = soup.find(id="picture_1")
    foto1['src'] = imagenes[0].path

    foto2 = soup.find(id="picture_2")
    foto2['src'] = imagenes[1].path

    tag_descrp = soup.find(id="descripcion")
    tag_descrp.string.replace_with(prod.descripcion)

    url_token = "http://telocam.com/producto/" + str(prod.id)
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)
