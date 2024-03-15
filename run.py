from app import create_app
# import logging

# logging.basicConfig(filename='error.log', level=logging.ERROR)
# logging.getLogger('flask_cors').level = logging.DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(port=5086)
