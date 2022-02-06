from flask import Blueprint, render_template, session, redirect, url_for
from . import db
from flask_login import login_required, current_user
from flask_socketio import SocketIO

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/waiting')
@login_required
def waiting():
    return render_template('waiting.html')

@main.route('/notInChat')
@login_required
def notInChat():
    session['inChat'] = False
    return redirect(url_for('main.index'))