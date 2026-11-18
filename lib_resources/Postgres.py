import pg8000
import pandas as pd
import json
import os

def BD_Manager():
    ruta_json = "credentials/credentials_sql.json"
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            host = datos["host"]
            database = datos["database"]
            user = datos["user"]
            password = datos["password"]
    
    else:
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
    try:
        conn = pg8000.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        query = "SELECT * FROM rpa_logs ORDER BY fecha_hora DESC"
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    except Exception as e:
        print(f"Error de conexión: {e}")
        return pd.DataFrame()