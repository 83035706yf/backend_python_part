from flask import Blueprint, jsonify

bp = Blueprint('test', __name__, url_prefix='/api')

@bp.route('/test', methods=['GET'])
def test():
    return jsonify(message="This is a test")