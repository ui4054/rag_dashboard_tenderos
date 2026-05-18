import duckdb
import pandas as pd
from scipy.stats import chi2_contingency
import os

def df_to_markdown_table(df):
    cols = [""] + list(df.columns)
    header = "| " + " | ".join([str(c) for c in cols]) + " |\n"
    separator = "| " + " | ".join(["---"] * len(cols)) + " |\n"
    rows = ""
    for idx, row in df.iterrows():
        rows += "| " + str(idx) + " | " + " | ".join([str(x) for x in row]) + " |\n"
    return header + separator + rows

def generar_reporte_total():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "04_motor", "investigacion_pura.db")
    con = duckdb.connect(db_path, read_only=True)
    df = con.execute("SELECT * FROM datos_maestros").df()
    
    print("--- INICIANDO ANALITICA PURA (0 TOKENS) ---")
    
    reporte = "# REPORTE DE EVIDENCIA ESTADÍSTICA (AUTOMÁTICO)\n\n"
    
    # 1. Variables a cruzar
    cruces = [
        ('educacion', 'ingresos_mens'),
        ('edad', 'negocio_camara_comercio'),
        ('tipo_vivienda', 'negocio_estrato'),
        ('negocio_ubicacion', 'negocio_camara_comercio')
    ]
    
    for v1, v2 in cruces:
        print(f"-> Analizando {v1} vs {v2}...")
        reporte += f"## Cruce: {v1.upper()} vs {v2.upper()}\n\n"
        
        # Tabla de contingencia
        ct = pd.crosstab(df[v1], df[v2])
        reporte += "### Tabla de Frecuencias\n"
        reporte += df_to_markdown_table(ct) + "\n\n"
        
        # Prueba Chi-Cuadrado
        chi2, p, dof, ex = chi2_contingency(ct)
        reporte += f"- **Chi-Cuadrado:** {chi2:.2f}\n"
        reporte += f"- **P-Valor:** {p:.4f}\n"
        reporte += "- **Interpretación:** "
        reporte += "Significativo (H1)" if p < 0.05 else "No significativo (H0)"
        reporte += "\n\n---\n\n"

    # Guardar reporte
    output_path = os.path.join(base_dir, "REPORTE_EVIDENCIA_ESTADISTICA.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print(f"[OK] Reporte generado en: {output_path}")

if __name__ == "__main__":
    generar_reporte_total()
