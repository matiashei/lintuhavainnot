from flask import Flask
import config

app = Flask(__name__)
app.secret_key = config.secret_key

from routes import main_routes, item_routes, user_routes