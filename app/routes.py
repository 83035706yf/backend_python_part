from app import create_app
from app.controllers import study_plan_bp
from flask import current_app as app

def register_routes(app):
    app.register_blueprint(study_plan_bp)
    
    @app.route('/query/<topic_name>')
    def query_topic(topic_name):
        resources = app.neo4j_db.query_resources(topic_name)
        return {"resources": resources}