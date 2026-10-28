from flask import Flask, render_template, request, redirect, session
from database_connection import *
from book_repo import *
from user_repo import *
from login_required import *
import hashlib


# instantiate a Flask app object
app = Flask(__name__)

# NEW PART START
app.secret_key = "some_really_secret_key"


# Declares a route that listens for a GET request to the path /hello
# and a method to execute when that request comes in
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/books', methods=['GET'])
def get_books():
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  books = book_repo.all()
  return render_template("books.html", books=books)

@app.route('/books/new', methods=["GET"])
def create_new_book():
   return render_template('new_book.html')



@app.route('/books', methods=['POST'])
@login_required
def create_book():
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  book_details = request.form
  book = Book(title=book_details['title'], author=book_details['author'])
  book_repo.create(book)
  return redirect("/books")

@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  book = book_repo.find_book(book_id)
  return render_template("book.html", book=book)

@app.route('/books/delete', methods=['POST'])
@login_required
def delete_book():
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  book_delete = request.form
  book_repo.delete(book_delete['id'])
  return redirect('/books')

@app.route('/users/new', methods=['GET'])
def create_user():
   return render_template("signup_form.html")

@app.route('/users', methods=['POST'])
def submit_form():
  connection = DatabaseConnection()
  connection.connect()
  user_repo = UserRepo(connection)
  user_details = request.form
  password = user_details['password']
  salt = '5gz'
  pwd_salt = password + salt
  hash = hashlib.sha256(pwd_salt.encode())
  user = User(username=user_details['username'], password=hash.hexdigest())
  user_repo.save(user)
  return redirect("/books")

@app.route('/sessions/new', methods=['GET'])
def login_user():
   return render_template("login_form.html")

@app.route('/sessions', methods=['POST'])
def check_user():
  connection = DatabaseConnection()
  connection.connect()
  user_repo = UserRepo(connection)
  check_user = request.form
  password = check_user['password']
  salt = '5gz'
  pwd_salt = password + salt
  hash = hashlib.sha256(pwd_salt.encode())
  user = user_repo.find_user(check_user['username'])
  print(hash.hexdigest())
  print(user.password)
  if user and hash.hexdigest() == user.password:
     session['user_id'] = user.id
     session['username'] = user.username
     return redirect('/books')
  else:
     return redirect('/session/new')
     

@app.route('/users', methods=['POST'])
def login():
  connection = DatabaseConnection()
  connection.connect()
  user_repo = UserRepo(connection)
  user_details = request.form
  user = User(username=user_details['username'], password=user_details['password'])
  user_repo.save(user)
  return redirect("/books")


@app.route('/authors', methods=['GET'])
def get_authors():
    return [
  {
    "name": "Julia Donaldson",
    "dob": "1948-09-16"
  },
  {
    "name": "Andrea Beaty",
    "dob": "1961-10-08"
  },
  {
    "name": "Kelly Barnhill",
    "dob": "1973-01-01"
  },
  {
    "name": "Zetta Elliott",
    "dob": "1979-11-11"
  }
]


# NEW PART END


# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001, debug=True)

