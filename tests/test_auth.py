from playwright.sync_api import Page
from database_connection import DatabaseConnection

from app import app

def test_auth():
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")
    client = app.test_client()
    response = client.post("/sessions", data={
        'username': 'test',
        'password': '1234'
    })
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/books')

def test_auth_playwrite(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")
    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_label('username').fill('test')
    page.get_by_label('password').fill('1234')
    page.get_by_role('button', name='login').click()

    assert page.url == "http://127.0.0.1:5001/books"
    
