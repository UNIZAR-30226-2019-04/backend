import bs4


def load_preview():
    # load the file
    with open("preview.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)
    return soup


def generateEmail(user, token):
    soup = load_preview()
    tag_nombre = soup.find(id="nombre_usuario")
    tag_nombre.string.replace_with("Hola " + user + ", ")
    url_token = "https://155.210.47.51/confirm?token=" + token
    button = soup.find(id="button")
    button['href'] = url_token
    a_token = soup.find(id="url_token")
    a_token['href'] = url_token
    a_token.string.replace_with(url_token)

    return str(soup)
