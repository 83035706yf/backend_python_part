from app import create_app
from app.controllers import study_plan_bp
from app.controllers import test_bp

def register_routes(app):
    app.register_blueprint(study_plan_bp)
    app.register_blueprint(test_bp)
