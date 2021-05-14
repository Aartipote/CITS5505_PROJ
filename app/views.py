from flask.globals import request
from app import app
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from app import db

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    answers = db.Column(db.String(100))

    # def __init__(self, username, email, password):
    #     self.id = id
    #     self.username = username
    #     self.email = email
    #     self.password = password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])
    remember = BooleanField('remember me')



class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])


class AssessmentForm(FlaskForm):
    ques1 = StringField('Vaccination can lead to an increase in mutation.')

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('login'))
        else:
            flash('Account not found. Please register')   
            return redirect(url_for('login')) 
    else:
        if(len(list(form.errors.values())) >0):
            flash(list(form.errors.values())[0][0])
            return redirect(url_for('login'))

        
        #return '<h1> Invalid username or password </h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        usernamecheck = User.query.filter_by(username = form.username.data).first()
        useremailcheck = User.query.filter_by(email = form.email.data).first()
        if not usernamecheck and not useremailcheck:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, answers = "")
            db.session.add(new_user)
            db.session.commit()

            flash('Your account has been created.....Go to login page')
            return redirect(url_for('signup'))
        else:
            flash("Account already exists. Please login.")
            return redirect(url_for("signup"))

    else:
        if(len(list(form.errors.values())) >0):
            flash(list(form.errors.values())[0][0])
            return redirect(url_for('signup'))

        
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    
    return render_template("signup.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base'))

@app.route('/aboutcovid')
@login_required
def aboutcovid():
    return render_template("aboutcovid.html", name=current_user.username)

@app.route('/safe_practices')
@login_required
def safe_practices():
    return render_template("safe_practices.html", name=current_user.username)

@app.route('/symptoms')
@login_required
def symptoms():
    return render_template("symptoms.html", name=current_user.username)

@app.route('/whattodo')
@login_required
def whattodo():
    return render_template("whattodo.html", name=current_user.username)


@app.route('/assessment',methods=['GET','POST'])
@login_required
def assessment():
    form = AssessmentForm()
    actual_answers = ['No','Virus','False','Sore throat']
    if request.method == 'POST':
        user_answers = [request.form.get('question1'),request.form.get('question2'),request.form.get('question3'),request.form.get('question4')]
        print(user_answers)
        total = 0
        for x in range(0,4):
            if(user_answers[x]==actual_answers[x]):
                total +=1
        print(total)
        sep = "/"
        user_answer_concat = sep.join(user_answers)
        print(user_answer_concat)
        user_row = User.query.get(current_user.id)
        user_row.answers=user_answer_concat
        db.session.add(user_row)
        db.session.commit()

        return redirect(url_for('submission'))
    return render_template("assessment.html" , name=current_user.username)


@app.route('/submission',methods=['GET'])
@login_required
def submission():

    return render_template("submission.html", name=current_user.username)

@app.route('/progress')
@login_required
def progress():
    return render_template("progressreport.html", name=current_user.username)


