from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    nombre = db.Column(db.String(20),unique=False,nullable=False)
    apellido = db.Column(db.String(20),unique=False,nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


        

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre":self.nombre,
            "apellido":self.apellido,
            "username":self.username
            # do not serialize the password, its a security breach
        }

class Actividades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.String(100), unique=True, nullable=False)
    distancia = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20),db.ForeignKey("user.email"))
    emocion = db.Column(db.String(20),unique=False,nullable=False) 
    relacion = db.relationship("User")