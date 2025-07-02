from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT timestamp, temperature FROM temperatures ORDER BY timestamp DESC LIMIT 100")
        rows_raw = cur.fetchall()
        cur.close()
        conn.close()

        # Konverter datetime til streng (ISO-format)
        rows = [(ts.isoformat(), temp) for ts, temp in rows_raw]

        return templates.TemplateResponse("index.html", {"request": request, "rows": rows})
    except Exception as e:
        return HTMLResponse(f"<h1>Database error: {e}</h1>", status_code=500)
