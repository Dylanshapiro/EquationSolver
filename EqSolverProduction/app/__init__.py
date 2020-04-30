from flask import Flask


app = Flask(__name__)

# blueprint for main route of app
from app.routes.mainRoutes import main as main_blueprint
app.register_blueprint(main_blueprint)

