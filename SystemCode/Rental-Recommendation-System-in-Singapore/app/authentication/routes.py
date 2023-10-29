from flask import render_template, request, redirect, url_for,flash,jsonify
from flask_login import current_user

from flask_login import login_user, current_user

from app.extension import db,bcrypt
from app.authentication import blueprint
from app.authentication.form import LoginForm,SignupForm
# from app.authentication.models import User


@blueprint.route('/login',methods=['Get','POST'])
def login():
    form =LoginForm()
    return render_template('login.html',form=form)
@blueprint.route('/signup', methods=['POST','GET'])
def signup():
    # 这里返回 nav.html 的内容
    userform = SignupForm()
    return render_template('sign-up.html',form=userform)

@blueprint.route('/collect_data', methods=['POST'])
def collect_data():
    from app.authentication.models import User
    form= SignupForm()
    if form.validate_on_submit():
        print("-----------start query test:house-----------")
        user = User.query.filter_by(userID=1).first()
        print(user.userName) 
        username = form.username.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data
        print(username,password,confirmPassword)
        if password == confirmPassword:
            user = User.query.filter_by(userName=username).first()
            User.query.filter_by(userName=username).delete()
            db.session.commit()
            if user:
                flash('Username already exists.', category='error')
                return redirect(url_for('signup'))
            else:
                try:
                    user = User(userName=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
                    db.session.add(user)
                    db.session.commit()
                    print("User added successfully")
                    user = User.query.filter_by(userName=username).first()
                    if user:
                        print("New user ID:", user.userID)
                    else:
                        print("User added but not found")
                except Exception as e:
                    print("Error adding user:", str(e))
                    db.session.rollback()
            return redirect(url_for('authentication_blueprint.login'))
        else:
            return redirect(url_for('authentication_blueprint.signup'))
    return redirect(url_for('authentication_blueprint.login'))

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    title = 'User sign up'
    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data

        password = bcrypt.generate_password_hash(form.password.data)

        user = User(name=name, username=username, password=password)

        db.session.add(user)

        db.session.commit()

        flash('Successfully registered!', category='success')
        return redirect(url_for('home'))
    return render_template('sign-up.html', form=form, title=title, signup=True)
# users={'admmin':'admin666','hola':'holly'}
@blueprint.route('/submit_login', methods=['Get','POST'])
def submit_login():
    from app.authentication.models import User
    from app.services.DataProcessing import df_to_amenities,get_ratings
    # username = loginForm.username.data
    # password = loginForm.password.data
    username = request.form.get('Username')
    password = request.form.get('Password')
    error = None

    print(username,password)
    user = User.query.filter_by(userName=username).first()
    if user:
        
        print("User found:", user.userName)
        print("Stored password hash:", user.password)
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'result': 'success', 'message': 'Welcome!'})
        else:
            #return 'login'
            return jsonify({'result': 'error', 'message': 'Wrong password. Please try again.'})
    else:
        print("No such user")
        return jsonify({'result': 'error', 'message': 'No such username. Please sign up first.'})
        #return 'login'
