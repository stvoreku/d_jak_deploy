from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status, Request
import sqlite3
from starlette.responses import RedirectResponse
from hashlib import sha256
from pydantic import BaseModel
import json
import secrets
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


def update_customer(customer_id, customer):
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    test_cmd = "SELECT COUNT(*) FROM customers WHERE CustomerId = ?"
    c.execute(test_cmd, (customer_id,))
    test_res = c.fetchone()
    print(test_res['COUNT(*)'])
    if test_res['COUNT(*)'] < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No Customer with given id"})
    upd_str = ''
    for key in customer.keys():
        upd_str += '{} = {},'.format(key, customer[key])
    upd_str = upd_str[:-1]
    cmd = "UPDATE customers SET {} WHERE CustomerId = ?".format(upd_str)
    print(cmd)
    c.execute(cmd, (customer_id,))
    cmd = "SELECT * FROM customers WHERE CustomerId = ?"
    c.execute(cmd, (customer_id, ))
    res = c.fetchone()
    return res

class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None

@app.put('/customers/{id}')
def customers(id: int, customer: Customer):
    res = update_customer(id, customer)
    return res


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}