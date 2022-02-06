from flask import Flask, render_template, Blueprint


chat = Blueprint('chat', __name__)

@chat.route('/chat')
def sessions():
    return render_template('chat.html')




