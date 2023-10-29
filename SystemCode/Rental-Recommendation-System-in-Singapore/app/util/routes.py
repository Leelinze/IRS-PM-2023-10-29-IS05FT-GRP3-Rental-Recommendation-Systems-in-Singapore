from app.util import blueprint
from flask import render_template
from flask_login import login_required

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template("about.html")

@blueprint.route('/welcome')
@login_required
def welcome():
    # 这里返回 nav.html 的内容
    return render_template('welcome.html')

@blueprint.route('/nav')
def nav():
    # 这里返回 nav.html 的内容
    return render_template('nav.html')