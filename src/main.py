from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import os
import pandas as pd
import sqlite3 

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "database", "temperaturas.db"))
app = FastAPI()

# Modelo de dados
class TemperaturaPayload(BaseModel):
    temperatura: float

# Conexão com banco (exemplo com SQLite)
def salvar_temperatura(valor):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS temperatura (timestamp TEXT, valor REAL)")
    c.execute("INSERT INTO temperatura VALUES (?, ?)", (datetime.now().isoformat(), valor))
    conn.commit()
    conn.close()

@app.post("/temperatura")
async def receber_temperatura(payload: TemperaturaPayload):
    salvar_temperatura(payload.temperatura)
    return {"status": "ok"}

@app.get("/temperatura")
def listar_temperaturas():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM temperatura ORDER BY timestamp DESC LIMIT 100", conn)
    conn.close()
    return df.to_dict(orient="records")