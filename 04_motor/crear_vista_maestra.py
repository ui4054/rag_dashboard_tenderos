import duckdb

def crear_arquitectura_vista():
    db_path = r"c:\nubecita\OneDrive\Uniminuto\Investigacion_tenderos\RAG_CONSULTA\04_motor\investigacion_pura.db"
    con = duckdb.connect(db_path)
    
    # SQL para crear la vista con la lógica de significancia del manuscrito
    sql_view = """
    CREATE OR REPLACE VIEW vista_investigacion AS 
    SELECT *,
           CASE 
                WHEN negocio_ubicacion = 'Lérida' THEN 'Nodo Lérida'
                WHEN negocio_ubicacion = 'Mariquita' THEN 'Nodo Mariquita'
                WHEN negocio_ubicacion = 'Armero Guayabal' THEN 'Nodo Armero Guayabal'
                ELSE 'Nodo Otros (Robustez)'
           END as nodo_significancia
    FROM datos_maestros
    """
    
    try:
        con.execute(sql_view)
        print("[OK] Vista 'vista_investigacion' creada exitosamente.")
        # Verificación rápida
        count = con.execute("SELECT count(*) FROM vista_investigacion").fetchone()[0]
        print(f"[INFO] Registros disponibles en la vista: {count}")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la vista: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    crear_arquitectura_vista()
