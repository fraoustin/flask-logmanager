from flask import Flask, request, current_app
from flask_logmanager import LogManager

app = Flask(__name__)
app.register_blueprint(LogManager(url_prefix="/api", ui_testing=True))


@app.route("/")
def hello():
    current_app.logger.error("error from hello")
    current_app.logger.info("info from hello")
    current_app.logger.debug("debug from hello")
    return "Hello World!"

@app.route("/error")
def warning():
    current_app.logger.error("error from warning")
    current_app.logger.info("info from warning")
    current_app.logger.debug("debug from warning")
    return "error", 400

@app.route('/search')
def search():
    current_app.logger.error("error from search")
    current_app.logger.info("info from search")
    current_app.logger.debug("debug from search")
    location = request.args.get('location')
    return  location

@app.route('/coucou/<location>')
def coucou(location=None):
    return  location

if __name__ == "__main__":
    app.run(port=8080)
