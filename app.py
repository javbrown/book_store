from flask import Flask, render_template, request, redirect
from database_connection import *
from book_repo import *
from user_repo import *



# instantiate a Flask app object
app = Flask(__name__)

# NEW PART START


# Declares a route that listens for a GET request to the path /hello
# and a method to execute when that request comes in
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"

@app.route('/css', methods=['GET'])
def css():
    return render_template("css_practise.html")

@app.route('/books', methods=['GET'])
def get_books():
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  books = book_repo.all()
  return render_template("books.html", books=books)

@app.route('/books', methods=['POST'])
def create_book():
  connection = DatabaseConnection()
  connection.connect()
  book_repo = BookRepo(connection)
  book_details = request.form
  book = Book(title=book_details['title'], author=book_details['author'])
  book_repo.create(book)
  return redirect("/books")

@app.route('/users/new', methods=['GET'])
def create_user():
   return render_template("signup_form.html")

@app.route('/users', methods=['POST'])
def submit_form():
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

