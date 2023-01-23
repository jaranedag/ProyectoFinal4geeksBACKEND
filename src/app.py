"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/signup", methods=["POST"])  
def signup():
  body = request.get_json()
  username = body["username"]
  email = body["email"]
  password = body["password"]
  nombre = body ["nombre"]
  apellido = body ["apellido"]

  user = User(username=username,email=email,password=password,nombre=nombre,apellido=apellido,is_active=True)
  db.session.add(user)
  db.session.commit()
  
  return jsonify({"email":email,
  "password":password,"nombre":nombre,"apellido":apellido})

@app.route('/login', methods=['POST'])
def login():
      #usuario contraseña :D
      
      body = request.get_json()
      if "email" not in body:
        return "falta email", 400
      if "pass" not in body:
        return "falta contraseña", 400
      
      #validar datos
      #almacenar datos
      #mensaje de estado
      user = User.query.filter_by(email=body["email"],password =body["pass"]).first()
      if(user):
        #otorgar permisos
        expira = datetime.timedelta(minutes=1)
        access = create_access_token(identity=body,expires_delta=expira)
        return jsonify({
           "token": access

        }), 200
      else:
        return "datos incorrectos"  
@app.route('/user', methods=['GET','POST'])
def handle_hello():
    #cuando es un get conseguiremos todos los usuarios 
    if request.method =='GET':
        all_people = User.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
    
        return jsonify(all_people), 200
    
    else:
        body = request.get_json() # obtener el request body de la solicitud
        if body is None:
            return "The request body is null", 400
        if 'email' not in body:
            return 'Especificar email', 400
        if 'password' not in body:
            return 'Especificar password',400
        #estoy consultando si existe alguien con el email que mande en la api y consigo la primera coincidencia
        onePeople = User.query.filter_by(email=body["email"]).first()
        if onePeople:
            if (onePeople.password == body["password"] ):
                #CUANDO VALIDAMOS LA PASSWORD CREAREMOS EL TOKEN
                expira = datetime.timedelta(minutes=2)
                access_token = create_access_token(identity=onePeople.email, expires_delta=expira)
                data = {
                    "info_user": onePeople.serialize(),
                    "token": access_token,
                    "expires": expira.total_seconds()
                }
                return(jsonify(data))
            else:
                return(jsonify({"mensaje":False}))
        else:
            return(jsonify({"mensaje":"mail no se encuentra registrado"}))        
@app.route("/private",methods=["GET"])
@jwt_required()
def privada():
    identidad = get_jwt_identity()
    return identidad
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
