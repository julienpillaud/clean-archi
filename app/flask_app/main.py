from flask import Flask

from app.flask_app.blueprints import items
from app.repository.dependencies import repository_provider

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config["repository_provider"] = repository_provider
app.register_blueprint(items.blueprint)
