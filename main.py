from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psycopg2
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "fibaro_logs"),
    "user": os.getenv("DB_USER", "fibaro_logs_user"),
    "password": os.getenv("DB_PASS", "hsrB9suM6GeeqzJlaYqFiMqGVdZAIX2a"),
    "host": os.getenv("DB_HOST", "dpg-d1iggjer433s73aj7ol0-a.frankfurt-postgres.render.com"),
    "port": os.getenv("DB_PORT", 5432)
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT timestamp, temperature FROM temperature_logs ORDER BY timestamp DESC LIMIT 100")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        rows = []
        print("DB error:", e)

    return templates.TemplateResponse("index.html", {"request": request, "logs": rows})