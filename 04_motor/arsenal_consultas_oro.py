import duckdb
import pandas as pd
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(base_dir, "04_motor", "investigacion_pura.db")

def ejecutar_arsenal():
    con = duckdb.connect(db_path, read_only=True)
    print("\n" + "="*60)
    print("   ARSENAL DE VALIDACION: CAPA DE ORO (VISTA INVESTIGACION)")
    print("="*60)

    consultas = {
        "1. DISTRIBUCION TERRITORIAL (TABLA 1)": 
            'SELECT "Nodo de Significancia", COUNT(*) as N, ROUND(COUNT(*) * 100.0 / 535, 2) as "%" FROM vista_investigacion GROUP BY 1 ORDER BY N DESC',
        
        "2. ANALISIS DE FORMALIZACION X NODO": 
            'SELECT "Nodo de Significancia", "Formalización", COUNT(*) as Cantidad FROM vista_investigacion GROUP BY 1, 2 ORDER BY 1',
        
        "3. PERFIL PSICOMETRICO MAESTRO (LIKERT)": 
            'SELECT "Nodo de Significancia", ROUND(AVG("Resiliencia"),2) as Resil, ROUND(AVG("Autonomía"),2) as Auton, ROUND(AVG("Creatividad"),2) as Creat FROM vista_investigacion GROUP BY 1',
        
        "4. CRUCE ANTIGÜEDAD VS FORMALIZACION": 
            'SELECT "Antigüedad del Negocio", "Formalización", COUNT(*) FROM vista_investigacion GROUP BY 1, 2 ORDER BY 1'
    }

    for titulo, sql in consultas.items():
        print(f"\n>>> {titulo}")
        try:
            df = con.execute(sql).df()
            print(df.to_string(index=False))
            print("-" * 30)
        except Exception as e:
            print(f"Error en consulta: {e}")

    con.close()

if __name__ == "__main__":
    ejecutar_arsenal()
