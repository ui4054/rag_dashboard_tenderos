import os
import duckdb
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(base_dir, "04_motor", "investigacion_pura.db")

print("====================================================")
print("   BANCO DE PRUEBAS SQL - MOTOR DE INVESTIGACION")
print("====================================================")

try:
    con = duckdb.connect(db_path, read_only=True)
    
    # 1. Verificar Vista
    print("\n[1] Verificando existencia de la vista...")
    res = con.execute("SELECT COUNT(*) FROM vista_investigacion").fetchone()
    print(f"    -> OK: La vista tiene {res[0]} registros.")
    
    # 2. Verificar Columnas Criticas
    print("\n[2] Verificando columnas de la Capa de Oro...")
    cols = con.execute("DESCRIBE vista_investigacion").df()
    print(cols[['column_name', 'column_type']])
    
    # 3. Prueba de Segmentacion
    print("\n[3] Prueba de Segmentacion por Nodo...")
    segmentos = con.execute('SELECT "Nodo de Significancia", COUNT(*) as Total FROM vista_investigacion GROUP BY 1').df()
    print(segmentos)
    
    print("\n[EXITO] El motor DuckDB esta vivo y la vista es correcta.")
    con.close()

except Exception as e:
    print(f"\n[ERROR] El motor de datos fallo: {e}")
