import sqlite3
from sqlalchemy import Column, Integer, String
from flask import Flask, flash, render_template, request, session, url_for, redirect
from flask_session import Session
from flask import g
from flask_sqlalchemy import SQLAlchemy

#create a Flask instance in your main module or in the __init__.py
# configure application
app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///appraisal.db'
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


@app.before_request
def before_request():
    g.db = sqlite3.connect("appraisal.db")



@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
        
        
        
class InfoPersonal(db.Model):
    __tablename__ = 'infoPersonal'
    empID = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    designation = db.Column(db.Text)
    
    def __init__(self,email,firstName,lastName,designation):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.designation = designation



class InfoTask(db.Model):
    __tablename__ = 'infoTask'
    id = db.Column(db.Integer, primary_key=True)
    empID = db.Column(db.Text)
    source = db.Column(db.Text)
    reportedTo = db.Column(db.Text)
    description = db.Column(db.Text)
    weightage = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    rating = db.Column(db.Text)
    
    def __init__(self, empID, source, reportedTo, description, weightage, duration, rating):
        self.empID = empID
        self.source = source
        self.reportedTo = reportedTo
        self.description = description
        self.weightage = weightage
        self.duration = duration
        self.rating = rating
        
        

@app.route("/")
def prac3():
    #list all employees details in table from db
    list_table = InfoPersonal.query.all()
    #print(list_table)
    #print(type(list_table))
    return render_template("prac3.html", rows=list_table)



def get_infoPersonal():
    emp_id = request.args.get('id')
    list_personal =InfoPersonal.query.filter(InfoPersonal.empID == emp_id)
    return list_personal
    
    
    
def get_infoTask():
    emp_id = request.args.get('id')
    print("aaaaaaaa" + emp_id)
    list_tasks = InfoTask.query.filter(InfoTask.empID == emp_id)
    print(list_tasks)
    return list_tasks

    

@app.route('/prac4', methods=["GET"])
def get_details():
    emp_id = request.args.get('id')
    list_personal = get_infoPersonal()
    list_tasks = get_infoTask()
    return render_template('prac4.html', row_tasks = list_tasks, row_personal = list_personal,empID=emp_id)


    
@app.route('/prac4', methods=["POST"])
def submit_infoTask():
    
    # The request is POST with some data, get POST data and validate it. The form data is available in request.
    # form dictionary. Stripping it to remove leading and trailing whitespaces
    source = request.form['source'].strip()
    description = request.form['description'].strip()
    reportedTo = request.form['reportto'].strip()
    duration = request.form['duration'].strip()
    weightage = request.form['weightage'].strip()
    rating = request.form['rating'].strip()
    print(type(weightage))
    
    #creating an string with error alert
    error =""
    # Check if all the fields are non-empty and raise an error otherwise
    if source=='' or description=='' or reportedTo=='' or duration=='' or weightage=='' or rating=='' :
        error = "Please enter all the fields."
        list_tasks = get_infoTask()
        list_personal = get_infoPersonal()
        print(error)
        # Render the form template with the error messages
        return render_template('prac4.html', errors=error, row_personal = list_personal, row_tasks = list_tasks)
        
    empID = request.args.get('id')
    print(empID)
    xyz = InfoTask(empID, source, reportedTo, description, weightage, duration, rating)
    db.session.add(xyz)
    db.session.commit()
    list_tasks = get_infoTask()
    list_personal = get_infoPersonal()
    return render_template('prac4.html',row_personal = list_personal, row_tasks = list_tasks, empID= empID)
