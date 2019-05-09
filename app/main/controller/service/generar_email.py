import bs4


def load_preview():
    # load the file
    with open("preview.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, features="lxml")
    return soup


def generateEmail(user, token):
    soup = load_preview()
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
