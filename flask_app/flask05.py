# FLASK Tutorial 5

#Imports
import os  #os is used to get environment variables IP & PORT
from flask import Flask  #Flask is the web app that we will customize
from flask import render_template, request, redirect, url_for
from database import db
from models import Note as Note
from models import User as User

app = Flask(__name__)  #Create an app

#Set name and location of database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#Bind SQLAlchemy db object to this Flask app
db.init_app(app)

#Setup models
with app.app_context():
    db.create_all()   #Run under the app context

# a_user = {'name': 'Emily', 'email': 'eruttenb@uncc.edu'}

# notes = {1: {'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
#         2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
#         3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}
#         }

@app.route('/')
@app.route('/index')
def index():
    #Get user from database
    a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()
    return render_template('index.html', user=a_user)


@app.route('/notes')
def get_notes():
    #Get user from database
    a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()
    #Get notes from database
    my_notes = db.session.query(Note).all()

    return render_template('notes.html', notes=my_notes, user=a_user)


@app.route('/notes/<note_id>')
def get_note(note_id):
    #Get user from database
    a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()
    #Get notes from database
    my_notes = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_notes , user=a_user)


@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    #Check method used for request
    if request.method == 'POST':
        #Get title data
        title = request.form['title']
        #Get note data
        text = request.form['noteText']
        #Get data stamp
        from datetime import date
        today = date.today()
        #Format date mm/dd/yyy
        today = today.strftime("%m-%d-%Y")
        #Get the last ID used and increment by 1
        #id = len(notes)+1
        #Create new note entry
        #notes[id] = {'title': title, 'text': text, 'date': today}
        new_record = Note(title, text, today)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        #GET request - show new note form
        #Retrieve user from database
        a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()
        return render_template('new.html', user=a_user)

@app.route('/notes/edit/<note_id>')
def update_note(note_id):
    #GET request - show new note form to edit note
    #retrieve user from database
    a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()

    #retrieve note from database
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('new.html', note=my_note, user=a_user)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000


