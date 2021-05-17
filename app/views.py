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

# adding this line to overwrite the default login view from the above line
login_manager.login_view = "admin_login"

# creating user db model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    answers = db.Column(db.String(100))
    marks = db.Column(db.Integer)


    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password
        self.answers = ""
        self.marks = None
    
    # create a function to return username string
    def __repr__(self):
        return '<Name %r>' % self.id

# creating user db model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    # added in effort to make the admin login work
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

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
    username = StringField('admin username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('admin password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])
    remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message = "Username should be between 4 and 15 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message = "Password should be a minimum of 8 characters")])

class AssessmentForm(FlaskForm):
    ques1 = StringField('Covid is a caused by:')
    ques2 = StringField('Who are most likely to get affected?')
    ques3 = StringField('Common cold and covid-19 are the same.')
    ques4 = StringField('The virus is spread primarily through')
    ques5 = StringField('Where was covids first case detected?')
    ques6 = StringField('Which of the below options are most likely to be a symptom of Covid?')
    ques7 = StringField('Which of the following should we do to prevent transmission?')
    ques8 = StringField('When we are exposed to a covid patient, we are likely to show symptoms by')
    ques9 = StringField('If you show symptoms for Covid, you should')
    ques10 = StringField('Can vaccination lead to an increase in mutation of the virus?')


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
                return redirect(url_for('userfile'))
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
    form = AdminLoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin:
            if admin.password == form.password.data:
                # the force attribute is added in an effort to make the admin login work
                login_user(admin, remember=form.remember.data, force = True)
                print("reached")
                # return render_template("admin_dashboard.html")
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('admin_login'))
        
        else:
            flash("Admin account doesnt exist")
            return redirect(url_for("admin_login"))
    else:
        print("coming into the errors section")
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
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, answers = "",marks= None)
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

<<<<<<< HEAD
@app.route("/admin_dashboard", methods = ['GET', 'POST'])
def admin_dashboard():
    username_all = []
    print("entered admin dashboard view method")
    # added this line here instead of inside the else statement
=======
@app.route("/admin_dashboard", methods=['POST', 'GET'])


def admin_dashboard():
>>>>>>> eb862080345e03620f593b1646154db0713296e5
    if request.method == "POST":
        user_name = request.form.get('name')
        email_id = request.form.get('email')
        hashed_password = generate_password_hash(request.form.get('password'), method='sha256')

<<<<<<< HEAD
        new_user = User(username=user_name, email=email_id, password=hashed_password)
=======
        new_user = User(username=user_name, email=email_id, password=hashed_password, answers = "",marks = None)
>>>>>>> eb862080345e03620f593b1646154db0713296e5
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Newly added user ')
            return redirect(url_for('admin_dashboard'))
        except:
            flash('There was an error adding the user')
            return redirect(url_for('admin_dashboard'))

    
    else:
        # commented this out here and added above
        # username_all=[]
        user = User.query.all()
        for x in range(len(user)):
            username_all.append(user[x].username)
        return render_template('admin_dashboard.html', username_all=username_all)
    
    return render_template('admin_dashboard.html', username_all=username_all )

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


@app.route('/userfile')
@login_required
def userfile():
    return render_template("userfile.html",name=current_user.username)

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
      
    actual_answers = ['3','3','2','2','2','1','3','2','3','2']
    if request.method == 'POST':
        # user_answers = [request.form.get('question1'),request.form.get('question2'),request.form.get('question3'),request.form.get('question4')]
        user_answers = [form.ques1.data,form.ques2.data,form.ques3.data,form.ques4.data,form.ques5.data,form.ques6.data,form.ques7.data,form.ques8.data,form.ques9.data,form.ques10.data]
        tot = 0
        sep = "/"
        print(len(actual_answers))
        for i in range(len(actual_answers)):
            if(user_answers[i] == actual_answers[i]):
                tot += 1

        user_answer_concat = sep.join(user_answers)

        user_row = User.query.get(current_user.id)
        user_row.answers=user_answer_concat
        user_row.marks = tot
        db.session.add(user_row)
        db.session.commit()

        return redirect(url_for('submission'))
    return render_template("assessment.html" , form = form, name=current_user.username)



@app.route('/submission',methods=['GET','POST'])
@login_required
def submission():
    form = AssessmentForm()
    ques1 = 'Covid is caused by:'
    ques2 = 'Who are most likely to get affected?'
    ques3 = 'Common cold and covid-19 are the same.'
    ques4 = 'The virus is spread primarily through'
    ques5 = 'Where was covids first case detected?'
    ques6 = 'Which of the below options are most likely to be a symptom of Covid?'
    ques7 = 'Which of the following should we do to prevent transmission?'
    ques8 = 'When we are exposed to a covid patient, we are likely to show symptoms by'
    ques9 = 'If you show symptoms for Covid, you should'
    ques10 = 'Can vaccination lead to an increase in mutation of the virus?'

    questions=[ques1,ques2,ques3,ques4,ques5,ques6,ques7,ques8,ques9,ques10]

    user_row_subm = User.query.get(current_user.id)
    ans_string = user_row_subm.answers
    tot_marks = user_row_subm.marks
    print(tot_marks)
    ans = ans_string.split('/')
    if len(ans) == 1 and ans[0]=='':
        flash("You need to do the assessment before you can check the Submissions!!!")
        return redirect(url_for('assessment'))
    else:
        actual_answers = ['3','3','2','2','2','1','3','2','3','2']
        # print("_______")
        # print(len(actual_answers))
        # print("___")
        answer_correctness=[]
        for x in range(len(actual_answers)):
            # print("xvalues")
            # print (x)
            if(ans[x]==actual_answers[x]):
                
                answer_correctness.append('Correct')
            else:
                answer_correctness.append('In-correct')
        
        return render_template("submission.html",form = form, name=current_user.username,ans=answer_correctness, total = tot_marks, questions=questions)
        
    

        


@app.route('/progress')
@login_required
def progress():
    user_name = []
    user_answer = []
    user_marks=[]
    user_all = User.query.all()
    user_length = len(user_all)
    try:
        for i in range(len(user_all)):
            user_name.append(user_all[i].username) 
            
            # user_answer.append(user_all[i].answers)
            user_marks.append(user_all[i].marks)
            if None in user_marks:
                none_count = user_marks.count(None)
                len1 = len(user_marks) - none_count
                new_list = []
                for i in range(len(user_marks)):
                    if user_marks[i] != None:
                        new_list.append(user_marks[i])
                        
                user_average = sum(new_list)/len1
            else:
                user_average = sum(user_marks)/len(user_marks)
                unique_marks = set(user_marks)
                unique_marks = list(unique_marks)

                count = []
                for r in range(len(unique_marks)):
                    ct = unique_marks.count(unique_marks[r])
                    count = count.append(ct)
            return render_template("progressreport.html", name=current_user.username, user_name=user_name, user_length=user_length,user_avg = user_average, unique_marks=unique_marks,count=count)
    except ZeroDivisionError:
        flash("Re-directed to Assessment page!! Please contine with assessment to see progress...")
        return redirect(url_for("assessment"))

        
    
    
    # return render_template("progressreport.html", name=current_user.username)
    #return render_template("progressreport.html", name=current_user.username, user_name=user_name, user_length=user_length,user_avg = user_average)


