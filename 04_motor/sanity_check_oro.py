import duckdb
import pandas as pd
import os

def run_sanity_check():
    db_path = r"c:\nubecita\OneDrive\Uniminuto\Investigacion_tenderos\RAG_CONSULTA\04_motor\investigacion_pura.db"
    con = duckdb.connect(db_path)
    
    print("--- SANITY CHECK: CAPA DE ORO ---")
    
    # 1. Verificar existencia de la vista
    try:
        views = con.execute("SELECT table_name FROM information_schema.views WHERE table_name = 'vista_investigacion'").fetchall()
        if views:
            print("[OK] Vista 'vista_investigacion' detectada.")
        else:
            print("[FAIL] Vista no encontrada.")
            return
    except Exception as e:
        print(f"[ERROR] Error al buscar vista: {e}")
        return

    # 2. Verificar Columnas "Bellas"
    df_cols = con.execute("SELECT * FROM vista_investigacion LIMIT 1").df()
    print(f"[INFO] Columnas detectadas: {list(df_cols.columns[:5])} ...")
    if "Nodo de Significancia" in df_cols.columns and "Ubicación Original" in df_cols.columns:
        print("[OK] Nomenclatura académica detectada.")
    else:
        print("[FAIL] La vista no tiene los nombres de columnas corregidos.")

    # 3. Verificar Mapeo de Barrios (Prueba de Fuego: Barrio Sabroso -> Nodo Lérida)
    test_mapping = con.execute("""
        SELECT "Nodo de Significancia", count(*) 
        FROM vista_investigacion 
        WHERE "Ubicación Original" ILIKE '%Sabroso%'
        GROUP BY 1
    """).df()
    
    if not test_mapping.empty:
        nodo = test_mapping["Nodo de Significancia"].iloc[0]
        if nodo == "Nodo Lérida":
            print(f"[OK] Mapeo inteligente exitoso: 'Sabroso' -> '{nodo}'.")
        else:
            print(f"[FAIL] 'Sabroso' mapeado incorrectamente a '{nodo}'.")
    else:
        print("[WARN] No se encontró el 'Barrio Sabroso' para la prueba de mapeo.")

    # 4. Verificar integridad de Mariquita
    test_mariquita = con.execute("""
        SELECT count(*) FROM vista_investigacion WHERE "Nodo de Significancia" = 'Nodo Mariquita'
    """).fetchone()[0]
    print(f"[INFO] Registros en Nodo Mariquita: {test_mariquita}")

    con.close()
    print("--- FIN DEL SANITY CHECK ---")

if __name__ == "__main__":
    run_sanity_check()
