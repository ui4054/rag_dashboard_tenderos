import os
import duckdb
import json
import pandas as pd
from dotenv import load_dotenv

# Integración Gemini (Cloud) + Local Search (Plan D - DuckDB FTS)
from langchain_google_genai import ChatGoogleGenerativeAI

class AgenteMaestro:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, "04_motor", "investigacion_pura.db")
        
        # Configuración Gemini
        load_dotenv(os.path.join(self.base_dir, ".env"))
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

        # 1. Configurar LLM (Gemini)
        # Usamos el modelo especificado por el usuario
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite", 
            google_api_key=self.api_key,
            temperature=0.1
        )
            
        # 2. Conexión a Datos (Plan D: Búsqueda Local Robusta)
        self.con = duckdb.connect(self.db_path, read_only=False)

    def crear_vista_oro(self):
        # VISTA DE ORO DEFINITIVA (Mapeo 1:1 con app_web.py)
        sql_view = """
        CREATE OR REPLACE VIEW vista_investigacion AS 
        SELECT 
            id,
            negocio_ubicacion as "Ubicación Original",
            CASE 
                WHEN negocio_ubicacion ILIKE '%Lérida%' OR negocio_ubicacion ILIKE '%Lerida%' OR negocio_ubicacion ILIKE '%Sabroso%' OR negocio_ubicacion ILIKE '%brisas%' OR negocio_ubicacion ILIKE '%reposo%' OR negocio_ubicacion ILIKE '%protecho%' OR negocio_ubicacion ILIKE '%Paz%' OR negocio_ubicacion ILIKE '%Resurgir%' OR negocio_ubicacion ILIKE '%Ciuadela%' OR negocio_ubicacion ILIKE '%jardin%' OR negocio_ubicacion ILIKE '%Aleman%' OR negocio_ubicacion ILIKE '%Galan%' OR negocio_ubicacion ILIKE '%Adraofasa%' OR negocio_ubicacion ILIKE '%Mango%' OR negocio_ubicacion ILIKE '%Candelaria%' THEN 'Nodo Lérida'
                WHEN negocio_ubicacion ILIKE '%Mariquita%' THEN 'Nodo Mariquita'
                WHEN negocio_ubicacion ILIKE '%Armero%' THEN 'Nodo Armero Guayabal'
                ELSE 'Nodo Otros'
            END as "Nodo de Significancia",
            CASE 
                WHEN CAST(negocio_camara_comercio AS VARCHAR) IN ('1', 'Si', 'Con Cámara de Comercio') THEN 'Formalizado'
                ELSE 'No Formalizado'
            END as "Formalización",
            educacion as "Nivel Educativo",
            TRIM(edad) as "Rango de Edad",
            ingresos_mens as "Ingresos Mensuales",
            personas_cargo as "Carga Familiar",
            negocio_antiguedad as "Antigüedad del Negocio",
            negocio_estrato as "Estrato",
            tipo_vivienda as "Tipo de Vivienda",
            -- 15 DIMENSIONES PSICOMÉTRICAS
            COALESCE(TRY_CAST(likert_autonomo AS INT), 3) as "Autonomía",
            COALESCE(TRY_CAST(likert_oportunidad AS INT), 3) as "Oportunidad",
            COALESCE(TRY_CAST(likert_ideas AS INT), 3) as "Creatividad",
            COALESCE(TRY_CAST(likert_adaptabilidad AS INT), 3) as "Resiliencia",
            COALESCE(TRY_CAST(likert_iniciativa AS INT), 3) as "Iniciativa",
            COALESCE(TRY_CAST(likert_riesgo_recursos AS INT), 3) as "Gestión Riesgo",
            COALESCE(TRY_CAST(likert_equipo AS INT), 3) as "Trabajo Equipo",
            COALESCE(TRY_CAST(likert_administracion AS INT), 3) as "Gestión Adm.",
            COALESCE(TRY_CAST(likert_aprendizaje_error AS INT), 3) as "Aprender del Error",
            COALESCE(TRY_CAST(likert_debil_fortaleza AS INT), 3) as "Análisis FODA",
            COALESCE(TRY_CAST(likert_comunicacion AS INT), 3) as "Comunicación",
            COALESCE(TRY_CAST(likert_riesgo_predisposicion AS INT), 3) as "Perfil de Riesgo",
            COALESCE(TRY_CAST(likert_creatividad AS INT), 3) as "Pensamiento Creativo",
            COALESCE(TRY_CAST(likert_autonomo_tareas AS INT), 3) as "Autonomía en Tareas",
            COALESCE(TRY_CAST(likert_motivacion AS INT), 3) as "Motivación"
        FROM datos_maestros
        """
        self.con.execute(sql_view)

    def obtener_vector_critico(self, df):
        """Genera una radiografía completa de la muestra filtrada."""
        if df.empty: return "Sin datos para análisis."
        
        total_poblacion = self.con.execute("SELECT COUNT(*) FROM vista_investigacion").fetchone()[0]
        n = len(df)
        cobertura = (n / total_poblacion * 100) if total_poblacion > 0 else 0
        
        def get_dist(col):
            dist = df[col].value_counts(normalize=True).head(3) * 100
            return ", ".join([f"{k}: {v:.1f}%" for k, v in dist.to_dict().items()])

        psic_cols = ["Autonomía", "Oportunidad", "Creatividad", "Resiliencia", "Iniciativa", 
                     "Gestión Riesgo", "Trabajo Equipo", "Gestión Adm.", "Aprender del Error", 
                     "Análisis FODA", "Comunicación", "Perfil de Riesgo", "Pensamiento Creativo", 
                     "Autonomía en Tareas", "Motivación"]
        
        promedios_psic = df[psic_cols].mean().to_dict()
        psic_str = ", ".join([f"{k}: {v:.2f}" for k, v in promedios_psic.items()])

        df_eval = df.copy()
        df_eval['score_total'] = df_eval[psic_cols].mean(axis=1)
        exito = df_eval.loc[df_eval['score_total'].idxmax()]
        critico = df_eval.loc[df_eval['score_total'].idxmin()]

        return f"""
        --- RADIOGRAFÍA DE MUESTRA ({n} de {total_poblacion}) ---
        [DEMOGRAFÍA]: {get_dist("Tipo de Vivienda")}, {get_dist("Nivel Educativo")}
        [NEGOCIO]: {get_dist("Ingresos Mensuales")}, {get_dist("Formalización")}
        [PSICOMETRÍA]: {psic_str}
        [CASOS]: Éxito (ID {exito['id']}), Crítico (ID {critico['id']})
        """

    def analizar_hipercubo_dinamico(self, df, flags):
        """Genera el diccionario de picos y valles para Resiliencia y Perfil de Riesgo."""
        if df.empty: return {}
        
        # 1. Identificar dimensiones activas para el cubo
        dimensiones = [d for d, activa in flags.items() if activa]
        if not dimensiones:
            # Si no hay filtros, usamos el Nodo como dimensión base mínima
            dimensiones = ["Nodo de Significancia"]
            
        # 2. Cálculo del Cubo (Medidas: Resiliencia y Perfil de Riesgo)
        medidas = ["Resiliencia", "Perfil de Riesgo"]
        cubo = df.groupby(dimensiones)[medidas].agg(['mean', 'count']).reset_index()
        
        # Aplanar columnas después de agg multidimensional
        cubo.columns = [('_'.join(col).strip('_') if isinstance(col, tuple) else col) for col in cubo.columns]
        
        # 3. Cálculo de Representatividad por Nodo
        totales_nodo = df.groupby('Nodo de Significancia').size().to_dict()
        def get_repr(row):
            # Si el Nodo está en las dimensiones, lo usamos. Si no, usamos el total de la muestra.
            nodo = row.get('Nodo de Significancia')
            count_col = 'Resiliencia_count'
            if nodo and nodo in totales_nodo:
                return (row[count_col] / totales_nodo[nodo]) * 100
            return (row[count_col] / len(df)) * 100

        cubo['repr'] = cubo.apply(get_repr, axis=1)
        
        # 4. Identificar Picos y Valles
        pico_res = cubo.loc[cubo['Resiliencia_mean'].idxmax()].to_dict()
        valle_res = cubo.loc[cubo['Resiliencia_mean'].idxmin()].to_dict()
        pico_riesgo = cubo.loc[cubo['Perfil de Riesgo_mean'].idxmax()].to_dict()
        
        return {
            "pico_resiliencia": pico_res,
            "valle_resiliencia": valle_res,
            "pico_riesgo": pico_riesgo,
            "dimensiones": dimensiones,
            "n_muestral": len(df)
        }

    def buscar_teoria(self, consulta, k=2):
        """Búsqueda de teoría usando el motor FTS de DuckDB (Plan D - Sin Vectores)."""
        try:
            # Búsqueda por palabras clave con BM25 (Motor interno DuckDB)
            sql = f"""
            SELECT contenido 
            FROM manuscrito_teorico 
            WHERE fts_main_manuscrito_teorico.match_bm25(id, ?) > 0
            LIMIT {k}
            """
            res = self.con.execute(sql, [consulta]).fetchall()
            return "\n".join([r[0] for r in res])
        except Exception as e:
            # Fallback simple si FTS falla: búsqueda LIKE
            sql_like = "SELECT contenido FROM manuscrito_teorico WHERE contenido ILIKE ? LIMIT 1"
            res = self.con.execute(sql_like, [f"%{consulta}%"]).fetchall()
            return res[0][0] if res else "No se encontró teoría específica para este hallazgo."

    def interpretar_hallazgo(self, consigna, datos_texto, vector_critico="", motor="Gemini", hipercubo=None):
        try:
            # 1. Recuperar Teoría (Búsqueda Robusta DuckDB)
            # Si hay hipercubo, usamos el 'valle' para potenciar la búsqueda
            if hipercubo and 'valle_resiliencia' in hipercubo:
                v = hipercubo['valle_resiliencia']
                terminos_potenciados = f"{consigna} {v.get('Formalización','')} {v.get('Nodo de Significancia','')}"
                teoria = self.buscar_teoria(terminos_potenciados)
            else:
                teoria = self.buscar_teoria(consigna)

            # 2. Prompt Unificado con Hipercubo (Renombrado internamente para la IA como Núcleo de Análisis)
            hiper_str = ""
            if hipercubo:
                hiper_str = f"\nNÚCLEO DE ANÁLISIS (PICOS Y VALLES):\n{json.dumps(hipercubo, indent=2, ensure_ascii=False)}"

            prompt = f"""Actúa como Experto Senior en Investigación Social y Análisis Cuantitativo.
            
            CONSIGNA: {consigna}
            
            DATOS DE LA MUESTRA:
            {vector_critico}
            {datos_texto}
            {hiper_str}
            
            BASE TEÓRICA RELEVANTE:
            {teoria}
            
            INSTRUCCIÓN: Genera un análisis ejecutivo siguiendo la lógica de Dato, Contraste y Relevancia, pero integrándolo en prosa fluida, profesional y natural.
            El 'Núcleo de Análisis' te indica los extremos y su representatividad; úsalos para validar si el hallazgo es un caso aislado o un patrón representativo.
            
            REGLAS ESTRICTAS DE MANUAL DE ESTILO Y REDACCIÓN:
            1. CONFIDENCIALIDAD: Para custodiar la propiedad intelectual del modelo combinatorio, NUNCA utilices la palabra 'hipercubo' o 'cubo'. Al hacer referencia a los picos y valles, debes llamarlo estrictamente 'núcleo de análisis'.
            2. PROHIBICIÓN DE ETIQUETAS Y SINTAXIS MARKDOWN: NUNCA utilices asteriscos de negrita (** o *), ni viñetas, ni corchetes como [PSICOMETRÍA] o [NEGOCIO]. En su lugar, utiliza frases introductorias elegantes y continuas (ejemplo: 'Análisis de la Gestión Administrativa:').
            3. PROHIBICIÓN DE SINTAXIS LATEX: NUNCA utilices símbolos de dólar ($) ni notación LaTeX para fórmulas o estadísticos. Redacta las cifras y métricas directamente en texto plano limpio (ejemplo: 'OR = 4.64, p = 0.006').
            4. CONECTORES NARRATIVOS FORMALES: NUNCA uses etiquetas aisladas como 'Dato:', 'Contraste:' o 'Relevancia:'. En su lugar, enlaza los conceptos con conectores fluidos como: 'Con respecto a los datos observados en la muestra:', 'Al contrastar con el marco referencial del estudio:', e 'Implicación analítica:'.
            5. APERTURA DIRECTA: NUNCA incluyas títulos generales, saludos ni frases de introducción como 'Interpretación Q1'. Inicia en el primer párrafo directamente con el análisis formal."""

            for chunk in self.llm.stream(prompt):
                yield chunk.content

        except Exception as e:
            yield f"Error en la interpretación: {str(e)}"
