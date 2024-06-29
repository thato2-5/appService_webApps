from flask import Flask, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from webforms import SearchForm, RegistrationForm, LoginForm, NoteForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "Development Key"

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

#Users Table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable = False, unique = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    # User Can Have Many Posts 
    todos = db.relationship('Todo', backref='todo')

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email= email

#Todo list Table
class Todo(db.Model):
    date_time = datetime.now()
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
    date = db.Column(db.String, default = date_time.strftime("%d/%m/%Y "))
    time = db.Column(db.String, default = date_time.strftime("%I:%M   %p"))
    # Foreign Key To Link Users (refer to primary key of the user)
    todo_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, todo_id):
         self.title = title
         self.description = description
         self.todo_id = todo_id

# Flask_Login Part
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Load current user
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

#View function for home page
@app.route('/')
def index():
    return render_template('index.html')

#View function to register new user
@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form = form)

#view function for user registration
@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password1.data, "sha256")
        user = Users(name, username, password, email)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added')
        except IntegrityError:
            db.session.rollback()
            flash('Error: Username or Email or Password already exists in the database')
            return render_template('register.html', form = form)
        return render_template('success.html', name = name, username = username, email = email, password = password)
    else:
        flash('Please fill the required fields correctly!')
        return render_template('register.html', form = form)

#View function to create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("Login Succesfull!!")
				return render_template('loginSuccess.html')
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("That User Doesn't Exist! Try Again...")
	return render_template('login.html', form=form)

#View function to create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return render_template('index.html')

#View Function to add note
@app.route('/addNote', methods=['GET', 'POST'])
@login_required
def add_note() :
    form = NoteForm()
    if form.validate_on_submit():
        poster = current_user.id
        title = form.title.data
        description = form.description.data 
        todo_id = poster
        note = Todo(title = title, description = description, todo_id = todo_id)
        # Clear The Form
        form.title.data = ''
        form.description.data = ''
		# Add note data to database
        db.session.add(note)
        db.session.commit()

		# Return a Message
        flash("Note added successfully!")
	# Redirect to the webpage
    return render_template("add_note.html", form = form)

#View function to perform search
@app.route('/search')
@login_required
def search():
    form = SearchForm()
    return render_template('newSearch.html', form = form)

#View function for searcg results
@app.route('/searchResult', methods = ['GET', 'POST'])
def searchResult():
    form = SearchForm()
    todos = Todo.query
    if form.validate_on_submit():
        search = form.search.data
        todos = todos.filter(Todo.description.like('%' + search + '%'))
        todos = todos.order_by(Todo.title).all()

        return render_template('search.html', form=form, search=search, todos = todos)

@app.route('/todos/<int:id>')
def todo(id):
	todo = Todo.query.get_or_404(id)
	return render_template('note.html', todo = todo)

@app.route('/notes')
def notes():
	# Grab all the todos from the database
	todos = Todo.query.order_by(Todo.date_added)
	return render_template("notes.html", todos = todos)

@app.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
	todos = Todo.query.get_or_404(id)
	form = NoteForm()
	if form.validate_on_submit():
		todos.title = form.title.data
		todos.description = form.description.data
		# Update Database
		db.session.add(todos)
		db.session.commit()
		flash("Note Has Been Updated!")
		return render_template('note.html', id=todos.id)
	
	if current_user.id == todo.todo_id:
		form.title.data = todos.title
		form.description.data = todos.description
		return render_template('edit_note.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Note...")
		todos = Todo.query.order_by(Todo.date)
		return render_template("notes.html", todos=todos)

@app.route('/notes/delete/<int:id>')
@login_required
def delete_note(id):
	note_to_delete = Todo.query.get_or_404(id)
	id = current_user.id
	if id == note_to_delete.todo.id:
		try:
			db.session.delete(note_to_delete)
			db.session.commit()

			#Message
			flash("Note Deleted!")

			# Grab all the todos from the database
			todos = Todo.query.order_by(Todo.date)
			return render_template("notes.html", todos = todos)

		except:
			# Return an error message
			flash("Whoops! There was a problem deleting note, try again...")

			# Grab all the posts from the database
			todos = Todo.query.order_by(Todo.date)
			return render_template("notes.html", todos = todos)
	else:
		#Message
		flash("You Aren't Authorized To Delete That Note!")

		# Grab all the notes from the database
		todos = Todo.query.order_by(Todo.date)
		return render_template("notes.html", todos = todos)


#Create our databases and run application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)