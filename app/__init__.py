from flask import Flask, Blueprint
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from .utils import transform_study_plan
from database.neo4j_database import Neo4jDatabase

def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8088", "supports_credentials": True}})
    app.config.from_object('config')

    # Initialize Neo4j Database
    app.neo4j_db = Neo4jDatabase()  # Store as part of app context

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)  # Create API with blueprint
    app.register_blueprint(api_bp)  # Register blueprint

    # Set up Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        '/swagger',
        '/static/swagger.json',
        config={
            'app_name': "Sciencetopia API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

    from .routes import register_routes
    register_routes(app)

    return app
