from flask import Flask, Blueprint

app = Flask(__name__)

app.config['SERVER_NAME'] = 'flask.dev:5000'

bp = Blueprint('subdomain', __name__, subdomain="<user>")

app.register_blueprint(bp)

if __name__ == "__main__" :
    app.run()