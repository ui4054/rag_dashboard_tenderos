import duckdb

import sys
import os

def crear_arquitectura_vista():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    
    from agente_maestro import AgenteMaestro
    try:
        agente = AgenteMaestro()
        agente.crear_vista_oro()
        print("[OK] Vista 'vista_investigacion' (Capa de Oro 15 Dimensiones) creada exitosamente.")
        count = agente.con.execute("SELECT count(*) FROM vista_investigacion").fetchone()[0]
        print(f"[INFO] Registros disponibles en la vista: {count}")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la vista: {e}")

if __name__ == "__main__":
    crear_arquitectura_vista()
