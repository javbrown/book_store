from playwright.sync_api import Page, expect
from database_connection import *
from user import *
from user_repo import *

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Books")

def test_get_all_books(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/books.sql")
    page.goto("http://127.0.0.1:5001/books")

    books = [
        ("The Gruffalo", "Julia Donaldson"),
        ("Ada Twist, Scientist", "Andrea Beaty"),
        ("The Girl Who Drank the Moon", "Kelly Barnhill"),
        ("Dragons in a Bag", "Zetta Elliott"),
    ]
    for title, author in books:
        expect(page.get_by_role('heading', name=title)).to_be_visible()
        expect(page.get_by_text(f'By {author}')).to_be_visible()

def test_books_form(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/books.sql")
    connection.execute("TRUNCATE TABLE users;")
    user_repo = UserRepo(connection)
    user = User('test', '1234')
    user_repo.save(user)

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_label("username").fill("test")
    page.get_by_label("password").fill("1234")
    page.get_by_role("button", name='login').click()
    page.goto("http://localhost:5001/books/new")
    page.get_by_label('Title').fill("Seires of unfortunate events")
    page.get_by_label("Author").fill("limmeny Snicket")
    page.get_by_role("button", name="Submit").click()

    books = page.locator('li')
    new_book = books.all_inner_texts()[-1]
    assert new_book == "Seires of unfortunate events\n\nBy limmeny Snicket\n\nX"


