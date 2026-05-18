import sys
import os
import pandas as pd
import scipy.stats as stats
from typing import Dict, Any, List

# Subimos 3 niveles desde app/services.py para llegar a RAG_CONSULTA
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from agente_maestro import AgenteMaestro
from app.schemas import FiltrosRequest, BivariadoRequest

class RagService:
    def __init__(self):
        self.agente = AgenteMaestro()
        self.agente.crear_vista_oro()
        self.df_raw = self.agente.con.execute("SELECT * FROM vista_investigacion").df()
        self.total_n = len(self.df_raw)
        
        self.psic_cols = [
            "Autonomía", "Oportunidad", "Creatividad", "Resiliencia", "Iniciativa",
            "Gestión Riesgo", "Trabajo Equipo", "Gestión Adm.", "Aprender del Error",
            "Análisis FODA", "Comunicación", "Perfil de Riesgo", "Pensamiento Creativo",
            "Autonomía en Tareas", "Motivación"
        ]

    def aplicar_filtros(self, req: FiltrosRequest) -> pd.DataFrame:
        df = self.df_raw.copy()
        
        if req.nodos and len(req.nodos) > 0:
            df = df[df["Nodo de Significancia"].isin(req.nodos)]
        if req.formalizacion and len(req.formalizacion) > 0:
            df = df[df["Formalización"].isin(req.formalizacion)]
        if req.rango_edad and len(req.rango_edad) > 0:
            df = df[df["Rango de Edad"].isin(req.rango_edad)]
        if req.nivel_educativo and len(req.nivel_educativo) > 0:
            df = df[df["Nivel Educativo"].isin(req.nivel_educativo)]
        if req.estrato and len(req.estrato) > 0:
            df = df[df["Estrato"].isin(req.estrato)]
        if req.antiguedad_negocio and len(req.antiguedad_negocio) > 0:
            df = df[df["Antigüedad del Negocio"].isin(req.antiguedad_negocio)]
        if req.tipo_vivienda and len(req.tipo_vivienda) > 0:
            df = df[df["Tipo de Vivienda"].isin(req.tipo_vivienda)]
            
        return df

    def obtener_opciones_filtros(self) -> Dict[str, List[str]]:
        return {
            "nodos": sorted(self.df_raw["Nodo de Significancia"].dropna().unique().tolist()),
            "formalizacion": sorted(self.df_raw["Formalización"].dropna().unique().tolist()),
            "rango_edad": sorted(self.df_raw["Rango de Edad"].dropna().unique().tolist()),
            "nivel_educativo": sorted(self.df_raw["Nivel Educativo"].dropna().unique().tolist()),
            "estrato": sorted(self.df_raw["Estrato"].dropna().unique().tolist()),
            "antiguedad_negocio": sorted(self.df_raw["Antigüedad del Negocio"].dropna().unique().tolist()),
            "tipo_vivienda": sorted(self.df_raw["Tipo de Vivienda"].dropna().unique().tolist())
        }

    def obtener_kpis(self, req: FiltrosRequest) -> Dict[str, Any]:
        df_f = self.aplicar_filtros(req)
        n_filtrado = len(df_f)
        
        if n_filtrado == 0:
            return {
                "muestra_filtrada": 0,
                "total_muestra": self.total_n,
                "perc_formalizacion": 0.0,
                "resiliencia_media": 0.0,
                "riesgo_media": 0.0,
                "promedios_psicometricos": {}
            }
            
        formalizados = len(df_f[df_f["Formalización"] == "Formalizado"])
        perc_formal = (formalizados / n_filtrado) * 100
        res_media = df_f["Resiliencia"].mean()
        riesgo_media = df_f["Perfil de Riesgo"].mean()
        
        promedios_psic = df_f[self.psic_cols].mean().round(2).to_dict()
        
        # Demografías para gráficos
        dist_edad = df_f["Rango de Edad"].value_counts().to_dict()
        dist_educ = df_f["Nivel Educativo"].value_counts().to_dict()
        dist_estrato = df_f["Estrato"].value_counts().to_dict()
        dist_ingresos = df_f["Ingresos Mensuales"].value_counts().to_dict()
        dist_nodo = df_f["Nodo de Significancia"].value_counts().to_dict()
        
        # Banderas de filtrado para el hipercubo
        flags = {
            "Formalización": len(req.formalizacion) > 0 and len(req.formalizacion) < len(self.df_raw["Formalización"].unique()),
            "Nodo de Significancia": len(req.nodos) > 0 and len(req.nodos) < len(self.df_raw["Nodo de Significancia"].unique()),
            "Rango de Edad": len(req.rango_edad) > 0 and len(req.rango_edad) < len(self.df_raw["Rango de Edad"].unique()),
            "Nivel Educativo": len(req.nivel_educativo) > 0 and len(req.nivel_educativo) < len(self.df_raw["Nivel Educativo"].unique()),
            "Estrato": len(req.estrato) > 0 and len(req.estrato) < len(self.df_raw["Estrato"].unique()),
            "Antigüedad del Negocio": len(req.antiguedad_negocio) > 0 and len(req.antiguedad_negocio) < len(self.df_raw["Antigüedad del Negocio"].unique())
        }
        hipercubo = self.agente.analizar_hipercubo_dinamico(df_f, flags)
        
        # Matriz de Correlación de Spearman (Rho) de las 15 dimensiones psicométricas (Mapeo de Cruce)
        # Spearman es el estadígrafo correcto para datos ordinales tipo Likert (1-5)
        matriz_corr = {}
        if n_filtrado > 1:
            corr_df = df_f[self.psic_cols].corr(method='spearman').round(2).fillna(0)
            matriz_corr = corr_df.to_dict()
        
        return {
            "muestra_filtrada": n_filtrado,
            "total_muestra": self.total_n,
            "perc_formalizacion": round(perc_formal, 1),
            "resiliencia_media": round(res_media, 2),
            "riesgo_media": round(riesgo_media, 2),
            "promedios_psicometricos": promedios_psic,
            "distribucion_demografica": {
                "edad": dist_edad,
                "educacion": dist_educ,
                "estrato": dist_estrato,
                "ingresos": dist_ingresos,
                "nodo": dist_nodo
            },
            "hipercubo": hipercubo,
            "matriz_correlacion": matriz_corr
        }

    def ejecutar_consulta_rag(self, consigna: str, req: FiltrosRequest) -> Dict[str, Any]:
        df_f = self.aplicar_filtros(req)
        n_filtrado = len(df_f)
        
        if n_filtrado == 0:
            return {"respuesta": "No hay datos en la muestra filtrada para realizar el análisis."}
            
        # Determinar banderas de filtros activos
        flags = {
            "Formalización": len(req.formalizacion) > 0 and len(req.formalizacion) < len(self.df_raw["Formalización"].unique()),
            "Nodo de Significancia": len(req.nodos) > 0 and len(req.nodos) < len(self.df_raw["Nodo de Significancia"].unique()),
            "Rango de Edad": len(req.rango_edad) > 0 and len(req.rango_edad) < len(self.df_raw["Rango de Edad"].unique()),
            "Nivel Educativo": len(req.nivel_educativo) > 0 and len(req.nivel_educativo) < len(self.df_raw["Nivel Educativo"].unique()),
            "Estrato": len(req.estrato) > 0 and len(req.estrato) < len(self.df_raw["Estrato"].unique()),
            "Antigüedad del Negocio": len(req.antiguedad_negocio) > 0 and len(req.antiguedad_negocio) < len(self.df_raw["Antigüedad del Negocio"].unique())
        }
        
        hipercubo = self.agente.analizar_hipercubo_dinamico(df_f, flags)
        vector = self.agente.obtener_vector_critico(df_f)
        
        promedios = df_f[self.psic_cols].mean().round(2)
        payload_datos = f"MUESTRA N={n_filtrado}. PROMEDIOS PSICOMÉTRICOS: {promedios.to_dict()}."
        
        generador = self.agente.interpretar_hallazgo(
            consigna=consigna,
            datos_texto=payload_datos,
            vector_critico=vector,
            motor="Gemini",
            hipercubo=hipercubo
        )
        
        respuesta_completa = "".join(list(generador))
        
        return {
            "respuesta": respuesta_completa,
            "hipercubo": hipercubo
        }

    def calcular_bivariado(self, req: BivariadoRequest) -> Dict[str, Any]:
        df_f = self.aplicar_filtros(req.filtros)
        n_muestral = len(df_f)
        
        if n_muestral < 3:
            return {
                "error": "Muestra insuficiente para regresión y prueba de hipótesis (mínimo N=3)",
                "n_muestral": n_muestral
            }
            
        if req.dim1 not in self.psic_cols or req.dim2 not in self.psic_cols:
            return {"error": "Dimensiones especificadas no son válidas."}
            
        x = df_f[req.dim1]
        y = df_f[req.dim2]
        
        # Rho de Spearman: correlación de rangos, apropiada para escalas Likert (ordinales)
        rho_spearman, p_value_spearman = stats.spearmanr(x, y)
        
        # Mantenemos la regresión OLS para la ecuación de la recta y la pendiente interpretativa
        slope, intercept, _, _, std_err = stats.linregress(x, y)
        
        # Puntos crudos para el diagrama de dispersión (scatter)
        puntos = [{"x": float(px), "y": float(py)} for px, py in zip(x.tolist(), y.tolist())]
        
        return {
            "dim1": req.dim1,
            "dim2": req.dim2,
            "n_muestral": n_muestral,
            "rho_spearman": round(rho_spearman, 4),
            "r_squared": round(rho_spearman**2, 4),
            "p_value": round(p_value_spearman, 5),
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "std_err": round(std_err, 4),
            "ecuacion": f"y = {round(slope, 3)}x + {round(intercept, 3)}",
            "puntos": puntos
        }

    def exportar_microdatos(self, req: FiltrosRequest) -> Dict[str, Any]:
        df_f = self.aplicar_filtros(req)
        # Excluimos columnas binarias internas o irrelevantes si es necesario
        df_clean = df_f.drop(columns=["Ubicación Original"], errors="ignore")
        
        # Generamos CSV en memoria
        csv_data = df_clean.to_csv(index=False)
        
        # Generamos JSON de las primeras 100 filas para previsualización rápida en web sin colapsar el DOM
        filas_preview = df_clean.head(100).fillna("").to_dict(orient="records")
        columnas = list(df_clean.columns)
        
        return {
            "total_filas": len(df_clean),
            "columnas": columnas,
            "preview": filas_preview,
            "csv_raw": csv_data
        }
