from agente_maestro import AgenteMaestro
import time

def ejecutar_banco():
    agente = AgenteMaestro()
    pruebas = [
        "¿Cuántos tenderos hay por género en la muestra total?",
        "Resume la metodología y los objetivos principales del estudio según el manuscrito.",
        "Cruza el nivel educativo con el promedio de ingresos y explica si hay una relación lógica."
    ]
    
    df_f = agente.con.execute("SELECT * FROM vista_investigacion").df()
    vector = agente.obtener_vector_critico(df_f)
    datos_texto = f"MUESTRA TOTAL N={len(df_f)}."
    
    print("--- INICIANDO BANCO DE PRUEBAS MINIMALISTA ---")
    
    for i, q in enumerate(pruebas):
        start = time.time()
        print(f"\nPRUEBA {i+1}: {q}")
        generador = agente.interpretar_hallazgo(q, datos_texto, vector_critico=vector)
        respuesta = "".join(list(generador))
        end = time.time()
        
        print(f"Tiempo: {end-start:.2f}s")
        print(f"Respuesta:\n{respuesta}\n")
        print("-" * 50)

    print("\n--- PRUEBAS FINALIZADAS ---")

if __name__ == "__main__":
    ejecutar_banco()
