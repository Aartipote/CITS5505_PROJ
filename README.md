# CITS5505_PROJ

#### Purpose of web application: 

This web application is based on the current pandemic COVID-19. The reason for selecting this topic is to develop a tool which helps user understand the current situation and tests their knowledge on it. 

The inspiration behind the project is to give users a bit more clarity about the recent chaos and also to see how much they know about the entire situation. There are learning modules provided for the user to educate themselves about the different aspects needed to be understood about Covid. Or directly, access the test. The assessment is a multiple choice question-answer system with a text box provided, where the user can answer with a number with the appropriate answer.

On submission, you will see how much the user got for the assessment along with the which questions being correctly answered or not. Direct navigation to the submission place on logging into the application will give the saved answers for the previous attempt. But if the user is new then he/she will get navigated to the assessment page.
The last page is the progress page which shows the number of users using the application and the average score of all of them.

#### Architecture of the Web Application:

The project on the highest level contains app.py, virtual environments folders and two python files of setupdatabase.py and run.py. As the file name suggests the run.py file makes the whole application run. The setupdatabase.py creates the database required for the users signing in or logging in and also hardcodes the admin to the database. There are two virtual environments env and flask. env is a virtual environment for running application on MacBook and flask is for a windows operating system. 

In app.py, the highest hierarchy is built to have static pages like CSS, JavaScript files and also images into static folder and html files in templates folder. Other than these files, the __init__.py configures and initializes the app and the database. The last python file, views.py has all the routes that are called to link the pages and create a flow for the entire application. They have even the codes to validate the user for login page and sign up pages and how it gets routed in each scenario. It also contains the database table schemas and majority of other modules like flask and bootstrap forms import codes. 

The HTML pages: The base.html and dashboard.html are the base pages for both the user login/sign up page and the user dashboard once you login respectively. Similarly, the admin_dashboard extends from admin_dashboard_base. They are created with the purpose to extend the navigation bar and the css to all the pages. 

#### Steps to launch the web application:

On terminal run: for activating the virtual enviornments.
Flask\Scripts\**activate**(for windows user) or source env/bin/**activate**(for mac user)
[Note: for deactivating environments after closing the applications use,
run flask\Scripts\**deactivate.bat**(for windows user) or **deactivate**(for mac user)  ]

#####	For running the entire application now:
For Windows:
SET FLASK_APP=run.py
SET FLASK_ENV=development
flask run

For Mac: 
export FLASK_APP=run.py
export FLASK_ENV=development
flask run

##### For troubleshooting problems with appdatabase.py:

Delete the database(appdatabase.db)
Then open the command line terminal and run the following set of codes:
 python setupdatabase.py
 python run.py

##### To build the application with new set of admins:

When only running application, it will take the hardcoded admins. So, for adding new admins edit the setupdatabase.py.
Delete the existing database, appdatabase.db 

Then open the command line terminal and run the following set of codes:
	python setupdatabase.py
	python run.py


#### Testing Performed:

We ran the entire code in Safari, Chrome and Edge. They ran successfully.
Admin page could add new user and they could login successfully.
Login page and Sign up page displayed flash messages when the user input doesnt meet the required criteria.
Flash messages are configured to display informative error messages to enhance user experience and application usability.

