Flask-logmanager
================

Manage level log of your flask application

Generate one logger by rule and add REST api for manager each logger


Installation
------------

::

    pip install flask-logmanager
        
Or

::

    git clone https://github.com/fraoustin/flask-logmanager.git
    cd flask-logmanager
    python setup.py install

Usage
-----

::

    from flask import Flask, request, current_app
    from flask_logmanager import LogManager

    app = Flask(__name__)
    app.register_blueprint(LogManager(url_prefix="/api", ui_testing=True))


    @app.route("/testone")
    def testOne():
        current_app.logger.error("error from testOne")
        current_app.logger.info("info from testOne")
        current_app.logger.debug("debug from testOne")
        return "Hello testOne!"

    @app.route("/testtwo")
    def testTwo():
        current_app.logger.error("error from testTwo")
        current_app.logger.info("info from testTwo")
        current_app.logger.debug("debug from testTwo")
        return "Hello testOne!"


    if __name__ == "__main__":
        app.run(port=8080)   #TODO


You can change level log of /testone on http://127.0.0.1:8080/api/ui

If you want change level in your application

::

    from flask_logmanager import get_logger_by_rule
    import logging

    get_logger_by_rule('/testone').setLevel(logging.DEBUG)

