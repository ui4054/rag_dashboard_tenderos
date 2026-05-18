import os
import duckdb
import pandas as pd
from dotenv import load_dotenv

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_CEREBRO = os.path.join(BASE_DIR, "01_cerebro")
DIR_EVIDENCIA = os.path.join(BASE_DIR, "02_evidencia")
DIR_MOTOR = os.path.join(BASE_DIR, "04_motor")

def ingesta_minimalista():
    print("--- INICIANDO INGESTA (PLAN D: DUCKDB FTS) ---")
    
    # 1. SQL (Datos Maestros)
    print("-> Configurando Evidencia SQL...")
    db_path = os.path.join(DIR_MOTOR, "investigacion_pura.db")
    con = duckdb.connect(db_path)
    csv_file = os.path.join(DIR_EVIDENCIA, "data_cleaned.csv")
    con.execute(f"CREATE OR REPLACE TABLE datos_maestros AS SELECT * FROM read_csv_auto('{csv_file}')")
    print(f"[OK] Tabla 'datos_maestros' creada.")

    # 2. CEREBRO TEÓRICO (DuckDB Full Text Search)
    print("-> Configurando Cerebro Teorico con DuckDB FTS...")
    
    # Cargar manuscrito
    tex_path = os.path.join(DIR_CEREBRO, "MANUSCRITO_INTEGRADO_IMRyD.tex")
    with open(tex_path, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    # Dividir en fragmentos lógicos (párrafos grandes)
    fragmentos = [f.strip() for f in texto.split('\n\n') if len(f.strip()) > 50]
    df_teoria = pd.DataFrame({'id': range(len(fragmentos)), 'contenido': fragmentos})
    
    # Crear tabla y habilitar FTS
    con.execute("CREATE OR REPLACE TABLE manuscrito_teorico (id INTEGER, contenido TEXT)")
    con.execute("INSERT INTO manuscrito_teorico SELECT * FROM df_teoria")
    
    # Instalar y cargar extensión FTS
    con.execute("INSTALL fts; LOAD fts;")
    con.execute("PRAGMA create_fts_index('manuscrito_teorico', 'id', 'contenido', overwrite=1)")
    
    # Crear la vista de oro
    print("-> Creando Vista de Oro (15 Dimensiones)...")
    from agente_maestro import AgenteMaestro
    agente = AgenteMaestro()
    agente.crear_vista_oro()
    
    print(f"[OK] {len(fragmentos)} fragmentos indexados en DuckDB (FTS activo).")
    print("\n--- INGESTA COMPLETADA ---")

if __name__ == "__main__":
    ingesta_minimalista()
