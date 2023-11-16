from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response
from client.auth import auth_view


def startFlask(requestQ, dataQ):
    app = Flask(__name__)
    app.register_blueprint(auth_view)
    app.run()
