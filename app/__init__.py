from flask import Flask

from app import config


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = config.SECRET_KEY


from app import api, context_processors, db, signals, views


db.init_db()
