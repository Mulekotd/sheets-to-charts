from flask import Flask
from decouple import config

def create_app():
    app = Flask(__name__)
    app.secret_key = config('FLASK_SECRET_KEY')

    from app.routes.main import main_bp
    from app.routes.charts import charts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(charts_bp)

    return app
