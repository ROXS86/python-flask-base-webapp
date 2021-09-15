import os
from flask import Flask, render_template, json, request, redirect, url_for, flash
from flask_mail import Mail, Message
from datetime import datetime
from . import dbconnect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='facile',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # register the auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # config mail
    mail= Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'password_app'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    @app.route('/testmail')
    def testmail():
        msg = Message('Hello', sender='info@webapp.it', recipients=['email@gmail.com'])
        msg.html=render_template('email_system.html')
        mail.send(msg)
        return "Sent"

    return app
