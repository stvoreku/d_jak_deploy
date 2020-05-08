from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status, Request
import sqlite3
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'
security = HTTPBasic()
app.sessions = {}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def customer_sales():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    cmd = "SELECT customers.CustomerId, customers.Email, customers.Phone, ROUND(SUM(invoices.Total),2) as Sum FROM customers JOIN invoices ON customers.CustomerId = invoices.CustomerId GROUP BY Customers.CustomerId ORDER BY -Sum;"
    c.execute(cmd)
    return c.fetchall()

def genres_sales():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    cmd = "SELECT genres.Name, COUNT(invoice_items.InvoiceId) as Sum FROM genres INNER JOIN tracks ON genres.GenreId = tracks.GenreId INNER JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId GROUP BY genres.GenreId ORDER BY -Sum;"
    c.execute(cmd)
    return c.fetchall()

@app.get('/sales')
def sales(category: str):
    STATS = {'customers':customer_sales, 'genres':genres_sales}
    if category not in STATS.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error':'no stats no cry'})
    res = STATS[category]
    return res
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

print(genres_sales())