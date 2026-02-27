from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------- DATABASE ----------
def db():
    conn = sqlite3.connect("stylesense.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        skin TEXT)
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS clothes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        type TEXT,
        color TEXT,
        brand TEXT)
    """)

    conn.commit()
    conn.close()


create_tables()


# ---------- LOGIN PAGE ----------
@app.get("/")
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# ---------- REGISTER ----------
@app.post("/register")
async def register(
        username: str = Form(...),
        password: str = Form(...),
        skin: str = Form(...)
):
    conn = db()

    user = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if user:
        conn.close()
        return "User already exists"

    conn.execute(
        "INSERT INTO users VALUES(?,?,?)",
        (username, password, skin)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        f"/dashboard/{username}",
        status_code=303
    )


# ---------- LOGIN AUTH ----------
@app.post("/auth")
async def auth(
        username: str = Form(...),
        password: str = Form(...)
):
    conn = db()

    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    conn.close()

    if not user:
        return "❌ Wrong Username or Password"

    return RedirectResponse(
        f"/dashboard/{username}",
        status_code=303
    )


# ---------- DASHBOARD ----------
@app.get("/dashboard/{username}")
async def dashboard(request: Request, username: str):

    score = random.randint(50, 100)

    tips = [
        "Match shirt & shoes color",
        "Use neutral colors",
        "Add jackets for layering",
        "Avoid too many bright colors"
    ]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "score": score,
            "tips": tips
        }
    )


# ---------- ADD CLOTH ----------
@app.post("/add/{username}")
async def add(
        username: str,
        type: str = Form(...),
        color: str = Form(...),
        brand: str = Form(...)
):
    conn = db()

    conn.execute(
        "INSERT INTO clothes(username,type,color,brand) VALUES(?,?,?,?)",
        (username, type, color, brand)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(
        f"/dashboard/{username}",
        status_code=303
    )