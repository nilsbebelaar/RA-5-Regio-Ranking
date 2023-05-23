from flask import Flask
from flask_basicauth import BasicAuth
from flask_apscheduler import APScheduler

basic_auth = BasicAuth()
scheduler = APScheduler()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.url_map.strict_slashes = False

    basic_auth.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        from app import routes
        app.register_blueprint(routes.blueprint)
        
        return app