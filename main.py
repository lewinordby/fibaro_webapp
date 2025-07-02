from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import os

app = FastAPI()

def get_db_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.get("/temperatures")
async def get_temperatures():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT timestamp, temperature FROM temperatures ORDER BY timestamp DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Lag en liste med ordbøker og formater datetime som ISO-streng
        result = [{"timestamp": ts.isoformat(), "temperature": temp} for ts, temp in rows]

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
