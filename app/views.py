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

# creating user db model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    answers = db.Column(db.String(100))

    # create a function to return username string
    def __repr__(self):
        return '<Name %r>' % self.id

# creating user db model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

    # def __init__(self, username, email, password):
    #     self.id = id
    #     self.username = username
    #     self.email = email
    #     self.password = password

# admin1 = Admin(username="aarti", password="aarti123")
# admin2 = Admin(username="reshma", password="reshma123")

# db.session.add(admin1)
# db.session.commit()

# db.session.add(admin2)
# db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])
    remember = BooleanField('remember me')

class AdminLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])


class AssessmentForm(FlaskForm):
    ques1 = 'Vaccination can lead to an increase in mutation.'
    ques2 = 'Common cold is the same as Covid-19.'
    ques4 = 'Which symptom do we see most likely when we are infected by COVID-19?'
    ques3 = 'Common cold is the same as Covid-19.'

    questions = [ques1,ques2,ques3,ques4]

@app.route("/")
def base():
    return render_template("home.html")

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


@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin:
            if admin.password == form.password.data:
                login_user(admin, remember=form.remember.data)
                # return render_template("admin_dashboard.html")
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('admin_login'))
        
        else:
            flash("Admin account doesnt exist")
            return redirect(url_for("admin_login"))
    else:
        if(len(list(form.errors.values())) >0):
            flash(list(form.errors.values())[0][0])
            return redirect(url_for('admin_login'))

        
        # return "<h1>" + form.username.data + "<h1>" + form.password.data

    return render_template("admin_login.html", form=form)    

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

@app.route("/admin_dashboard", methods=['POST', 'GET'])
@login_required
# def admin_dashboard():
#     username_all=[]
#     user = User.query.all()
#     for x in range(len(user)):

#         username_all.append(user[x].username)

#    ,username_all=username_all
def end_user():
    if request.method == "POST":
        user_name = request.form.get('name')
        email_id = request.form.get('email')
        hashed_password = generate_password_hash(request.form.get('password'), method='sha256')

        new_user = User(username=user_name, email=email_id, password=hashed_password, answers = "")
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/admin_dashboard')
        except:
            flash('There was an error adding the user')
            return redirect(url_for('/admin_dashboard'))

    else:
        username_all=[]
        user = User.query.all()
        for x in range(len(user)):
            username_all.append(user[x].username)
        return render_template('admin_dashboard.html', username_all=username_all)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')

@app.route('/admin_logout')
@login_required
def admin_logout():
    logout_user()
    return render_template('home.html')

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
    ques1 = 'Vaccination can lead to an increase in mutation.'
    ques2 = 'Covid-19 is a'
    ques3 = 'Common cold is the same as Covid-19.'
    ques4 = 'Which symptom do we see most likely when we are infected by COVID-19?'
    
    questions = [ques1,ques2,ques3,ques4]

    

    actual_answers = ['No','Virus','False','Sore throat']
    if request.method == 'POST':
        user_answers = [request.form.get('question1'),request.form.get('question2'),request.form.get('question3'),request.form.get('question4')]
        sep = "/"

            

        user_answer_concat = sep.join(user_answers)

        user_row = User.query.get(current_user.id)
        user_row.answers=user_answer_concat
        db.session.add(user_row)
        db.session.commit()

        return redirect(url_for('submission'))
    return render_template("assessment.html" , name=current_user.username,questions=questions)



@app.route('/submission',methods=['GET','POST'])
@login_required
def submission():
    form = AssessmentForm()

    ques1 = 'Vaccination can lead to an increase in mutation.'
    ques2 = 'Covid-19 is a'
    ques3 = 'Common cold is the same as Covid-19.'
    ques4 = 'Which symptom do we see most likely when we are infected by COVID-19?'
    

    questions = [ques1,ques2,ques3,ques4]

    user_row_subm = User.query.get(current_user.id)
    ans_string = user_row_subm.answers
    ans = ans_string.split('/')
    if len(ans) == 1 and ans[0]=='':
        flash("You need to do the assessment before you can check the Submissions!!!")
        return redirect(url_for('assessment'))
    else:
        actual_answers = ['No','Virus','False','Sore throat']
        tot_value = 0
        answer_correctness=[]
        for x in range(len(actual_answers)):
            if(ans[x]==actual_answers[x]):
                tot_value +=1
                answer_correctness.append('Correct')
            else:
                answer_correctness.append('In-correct')
        
        return render_template("submission.html",form = form, name=current_user.username,ans=answer_correctness, total = tot_value, questions=questions)

        


@app.route('/progress')
@login_required
def progress():
    return render_template("progressreport.html", name=current_user.username)


