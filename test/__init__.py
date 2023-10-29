
## Create and configure web application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

### Initialize flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = '6802382af0ed3106300a027b7441255c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_CSRF_IN_COOKIES'] = True

### SetUp flask extentions
db = SQLAlchemy(app)
jwt = JWTManager(app)
socketio = SocketIO(app)
bcrypt = Bcrypt(app)

## Import views
from test import views
