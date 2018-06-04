# -*- coding: utf-8 -*-
"""
    #PyUIO
    ~~~~~~
    Flask and sqlite3.
"""
from datetime import datetime

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy

# create our little application :)
app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///pyuio.db',
    SQLALCHEMY_ECHO=False,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    SECRET_KEY='dev',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())


class Widgets(db.Model):
    __tablename__ = 'widgets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    url = db.Column(db.String)
    secret_key = db.Column(db.String)
    token = db.Column(db.String)

    def __init__(self, name, url, secret_key, token):
        self.name = name
        self.url = url
        self.secret_key = secret_key
        self.token = token


@app.route('/')
def show():
    widgets = Widgets.query.all()
    return render_template('pythonuio.jinja2', entries=widgets)


@app.route('/add', methods=['POST', 'GET'])
def add_widget():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Name is required', 'error')
        elif not request.form['url']:
            flash('URL is required', 'error')
        elif not request.form['secret_key']:
            flash('Secret Key is required', 'error')
        elif not request.form['token']:
            flash('Token is required', 'error')
        else:
            widget = Widgets(request.form['name'],
                             request.form['url'],
                             request.form['secret_key'],
                             request.form['token'])
            db.session.add(widget)
            db.session.commit()
            flash(u'Widget was successfully created')
            return redirect(url_for('show'))
        flash('Widget entry was successfully posted')
    return render_template('add_widget.jinja2')


if __name__ == '__main__':
    manager.run()
