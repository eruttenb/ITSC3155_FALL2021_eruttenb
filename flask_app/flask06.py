# FLASK Tutorial 6

# Imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template, request, redirect, url_for, session
from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm, LoginForm
import bcrypt

app = Flask(__name__)  # Create an app

# Set name and location of database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure secret key that will be used by the app to secure session data
app.config['SECRET_KEY'] = 'SE3155'

# Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()  # Run under the app context


# a_user = {'name': 'Emily', 'email': 'eruttenb@uncc.edu'}

# notes = {1: {'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
#         2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
#         3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}
#         }

@app.route('/')
@app.route('/index')
def index():
    # Check if a user is saved in session
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template('index.html')


@app.route('/notes')
def get_notes():
    # Check if user is saved in session
    if session.get('user'):
        # Retrieve notes from database
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        # Redirect user to login view
        return redirect(url_for('login'))


@app.route('/notes/<note_id>')
def get_note(note_id):
    # Get user from database
    a_user = db.session.query(User).filter_by(email='eruttenb@uncc.edu').one()
    # Get notes from database
    my_notes = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_notes, user=a_user)


@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    # Check if user is saved in session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get title data
            title = request.form['title']
            # Get note data
            text = request.form['noteText']
            # Get data stamp
            from datetime import date
            today = date.today()
            # Format date mm/dd/yyy
            today = today.strftime("%m-%d-%Y")
            # Get the last ID used and increment by 1
            # id = len(notes)+1
            # Create new note entry
            # notes[id] = {'title': title, 'text': text, 'date': today}
            new_record = Note(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note form
            return render_template('new.html', user=session['user'])
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('login'))


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # Check if user is saved in session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get title data
            title = request.form['title']
            # Get note data
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).one()
            # Update note data
            note.title = title
            note.text = text
            # Update note in db
            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note form to edit note
            # Retrieve note from database
            my_note = db.session.query(Note).filter_by(id=note_id).one()
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('login'))


@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    # Check if a user is saved in session
    if session.get('user'):
        # Retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        # User is not in session, so redirect to login
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # Something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # Validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # We know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # User exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # Password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # Render view
            return redirect(url_for('get_notes'))

        # Password check failed
        # Set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # Form did not validate or GET request
        return render_template("login.html", form=login_form)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000
