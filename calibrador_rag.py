import time
import pandas as pd
import sys
from agente_maestro import AgenteMaestro

def generar_banco_40():
    nodos = ["Lérida", "Mariquita", "Armero Guayabal"]
    dimensiones = ["Resiliencia", "Autonomía", "Gestión del Riesgo", "Creatividad", "Aprender del Error"]
    grupos_edad = ["18 a 25 años", "36 a 45 años", "Más de 65 años"]
    educacion = ["Secundaria", "Pregrado", "Postgrado"]
    
    banco = []
    # 1-15: Geografía
    for n in nodos:
        for d in dimensiones:
            banco.append({"q": f"Manifestación de {d} en {n}", "f": {"Nodo de Significancia": f"Nodo {n}"}})
    # 16-30: Edad
    for e in grupos_edad:
        for d in dimensiones:
            banco.append({"q": f"Desafíos de {d} en {e}", "f": {"Rango de Edad": e}})
    # 31-40: Educación y Formalización
    for ed in educacion:
        banco.append({"q": f"Impacto de la educación {ed} en la resiliencia", "f": {"Nivel Educativo": ed}})
    banco.append({"q": "Resiliencia en Formalizados", "f": {"Formalización": "Formalizado"}})
    banco.append({"q": "Resiliencia en No Formalizados", "f": {"Formalización": "No Formalizado"}})
    
    # Rellenar hasta 40 con combinaciones de Estrato si es necesario
    while len(banco) < 40:
        banco.append({"q": f"Dinámica de emprendimiento en Estrato {len(banco)-30}", "f": {"Estrato": str(len(banco)-30)}})
        
    return banco[:40]

def ejecutar_estres(start=31, end=40):
    try:
        agente = AgenteMaestro()
        banco = generar_banco_40()
        print(f"START: CALIBRANDO LOTE FINAL {start} A {end}")
        
        for i in range(start-1, end):
            if i >= len(banco): break
            test = banco[i]
            print(f"\n--- PRUEBA {i+1} ---")
            col = list(test['f'].keys())[0]
            val = list(test['f'].values())[0]
            
            try:
                query = f'SELECT * FROM vista_investigacion WHERE "{col}" = ?'
                df_f = agente.con.execute(query, [val]).df()
                payload = f"DATOS (N={len(df_f)}): {df_f.describe().to_string()}"
                
                inicio = time.time()
                respuesta = ""
                for chunk in agente.interpretar_hallazgo(test['q'], payload):
                    respuesta += chunk
                fin = time.time()
                
                print(f"Q: {test['q']}")
                print(f"IA: {respuesta[:200]}...")
                print(f"TIME: {fin-inicio:.2f}s")
            except Exception as e:
                print(f"ERR: {e}")
    except Exception as e:
        print(f"FATAL: {e}")

if __name__ == "__main__":
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 31
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    ejecutar_estres(s, e)
