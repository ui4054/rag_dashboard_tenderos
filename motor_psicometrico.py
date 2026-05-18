import pandas as pd
import duckdb

import os

# Mapeo de nombres técnicos a nombres formales para el manuscrito
MAPEO_LABELS = {
    'likert_autonomo': 'Autonomía',
    'likert_oportunidad': 'Oportunidad',
    'likert_ideas': 'Creatividad',
    'likert_adaptabilidad': 'Resiliencia',
    'likert_iniciativa': 'Iniciativa',
    'likert_riesgo_recursos': 'Riesgo',
    'likert_equipo': 'Trabajo en Equipo',
    'likert_administracion': 'Gestión Adm.'
}

def generar_matriz_psicometrica():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "04_motor", "investigacion_pura.db")
    con = duckdb.connect(db_path, read_only=True)
    df = con.execute("SELECT * FROM datos_maestros").df()
    
    # 2. Filtrar Likerts y renombrar
    likert_cols = [c for c in df.columns if 'likert_' in c]
    data_likert = df[likert_cols].fillna(3)
    data_likert = data_likert.rename(columns=MAPEO_LABELS)
    
    # 3. Calcular Correlación
    corr_matrix = data_likert.corr()
    
    # 4. Guardar Matriz
    output_path = os.path.join(base_dir, "MATRIZ_CORRELACION_LICKERT.csv")
    corr_matrix.to_csv(output_path)
    print(f"[OK] Matriz generada con etiquetas formales en: {output_path}")

if __name__ == "__main__":
    generar_matriz_psicometrica()
