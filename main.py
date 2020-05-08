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
    cmd = "SELECT customers.CustomerId, SUM(invoices.Total) as TotalSpent FROM customers JOIN invoices ON customers.CustomerId = invoices.CustomerId GROUP BY Customers.CustomerId;"
    c.execute(cmd)
    return c.fetchall()

@app.get('/sales')
def sales(category: str):
    res = customer_sales()
    return res
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

print(customer_sales())