from app import db



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())    
    url = db.Column(db.String())

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Pass(db.Model):
    __tablename__='pass'

    pw = db.Column(db.Integer, primary_key=True)

    def __init__(self,pw):
        self.pw = pw