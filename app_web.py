import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agente_maestro import AgenteMaestro

# ── CONFIGURACION ──────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Tenderos - Norte del Tolima",
    layout="wide"
)

# CSS MINIMO: solo afecta elementos 100% nuestros (sem, cards)
# No tocamos selectores internos de Streamlit
st.markdown("""
<style>
/* Texto blanco solo en sidebar, sin tocar SVGs */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span:not([data-testid]),
[data-testid="stSidebar"] small { color: #ffffff !important; }

/* Celda de consulta personalizada */
textarea {
    background-color: #ffffff !important;
    color: #0284c7 !important;
    font-weight: 500 !important;
    border: 2px solid #0284c7 !important;
    border-radius: 8px !important;
}
textarea::placeholder { color: #93c5fd !important; }

.sem-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 14px;
    border-radius: 6px;
    margin-bottom: 5px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #1e293b;
}
.sem-v { background: #f0fdf4; border-left: 4px solid #22c55e; }
.sem-a { background: #fefce8; border-left: 4px solid #eab308; }
.sem-r { background: #fef2f2; border-left: 4px solid #ef4444; }
.sem-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 8px;
    flex-shrink: 0;
}
.card-rojo {
    background: linear-gradient(135deg, #fef2f2, #fff1f2);
    border-radius: 10px;
    padding: 16px;
    border-left: 4px solid #ef4444;
    margin-bottom: 8px;
}
.card-verde {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border-radius: 10px;
    padding: 16px;
    border-left: 4px solid #22c55e;
    margin-bottom: 8px;
}
.card-label {
    margin: 0;
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.card-value-rojo  { margin: 4px 0 0 0; font-size: 2rem; font-weight: 800; color: #dc2626; }
.card-value-verde { margin: 4px 0 0 0; font-size: 2rem; font-weight: 800; color: #16a34a; }
.card-sub  { margin: 2px 0 0 0; font-size: 0.8rem; color: #64748b; }
</style>
""", unsafe_allow_html=True)

# ── DATOS ──────────────────────────────────────────────────
PSIC_COLS = [
    "Autonomia", "Oportunidad", "Creatividad", "Resiliencia", "Iniciativa",
    "Gestion Riesgo", "Trabajo Equipo", "Gestion Adm.", "Aprender del Error",
    "Analisis FODA", "Comunicacion", "Perfil de Riesgo", "Pensamiento Creativo",
    "Autonomia en Tareas", "Motivacion"
]

PSIC_COLS_DB = [
    "Autonom\u00eda", "Oportunidad", "Creatividad", "Resiliencia", "Iniciativa",
    "Gesti\u00f3n Riesgo", "Trabajo Equipo", "Gesti\u00f3n Adm.", "Aprender del Error",
    "An\u00e1lisis FODA", "Comunicaci\u00f3n", "Perfil de Riesgo", "Pensamiento Creativo",
    "Autonom\u00eda en Tareas", "Motivaci\u00f3n"
]

@st.cache_resource
def load_agent():
    return AgenteMaestro()

agente = load_agent()
agente.crear_vista_oro()
df_raw = agente.con.execute("SELECT * FROM vista_investigacion").df()
total_n = len(df_raw)

# ── SIDEBAR ─────────────────────────────────────────────────
# Sin expanders: filtros directos con subheaders nativos
st.sidebar.title("RAG Consulta")
st.sidebar.caption("Motor: Gemini 2.5 Flash Lite")
st.sidebar.divider()

st.sidebar.subheader("Nodo Territorial")
f_nodo = st.sidebar.multiselect(
    "Seleccionar nodos",
    options=sorted(df_raw["Nodo de Significancia"].unique()),
    default=df_raw["Nodo de Significancia"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Formalizacion")
f_formal = st.sidebar.multiselect(
    "Seleccionar estado",
    options=sorted(df_raw["Formalizaci\u00f3n"].unique()),
    default=df_raw["Formalizaci\u00f3n"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Rango de Edad")
f_edad = st.sidebar.multiselect(
    "Seleccionar edades",
    options=sorted(df_raw["Rango de Edad"].unique()),
    default=df_raw["Rango de Edad"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Nivel Educativo")
f_educ = st.sidebar.multiselect(
    "Seleccionar educacion",
    options=sorted(df_raw["Nivel Educativo"].unique()),
    default=df_raw["Nivel Educativo"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Estrato")
f_estrato = st.sidebar.multiselect(
    "Seleccionar estrato",
    options=sorted(df_raw["Estrato"].unique()),
    default=df_raw["Estrato"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Antiguedad del Negocio")
f_antig = st.sidebar.multiselect(
    "Seleccionar antiguedad",
    options=sorted(df_raw["Antig\u00fcedad del Negocio"].unique()),
    default=df_raw["Antig\u00fcedad del Negocio"].unique(),
    label_visibility="collapsed"
)

st.sidebar.subheader("Tipo de Vivienda")
f_vivienda = st.sidebar.multiselect(
    "Seleccionar vivienda",
    options=sorted(df_raw["Tipo de Vivienda"].unique()),
    default=df_raw["Tipo de Vivienda"].unique(),
    label_visibility="collapsed"
)

motor_id = "Gemini"

# ── FILTRADO ────────────────────────────────────────────────
df_f = df_raw[
    (df_raw["Nodo de Significancia"].isin(f_nodo)) &
    (df_raw["Formalizaci\u00f3n"].isin(f_formal)) &
    (df_raw["Rango de Edad"].isin(f_edad)) &
    (df_raw["Nivel Educativo"].isin(f_educ)) &
    (df_raw["Estrato"].isin(f_estrato)) &
    (df_raw["Antig\u00fcedad del Negocio"].isin(f_antig)) &
    (df_raw["Tipo de Vivienda"].isin(f_vivienda))
]

# ── HEADER ──────────────────────────────────────────────────
st.title("Analisis Exploratorio - Tenderos Norte del Tolima")
st.caption("Lerida, Mariquita, Armero Guayabal, Casabianca, Honda, Ambalema, Falan, Fresno, Venadillo")
st.divider()

# ── FILA KPI: METRICA + GAUGES ──────────────────────────────
n_filtrado = len(df_f)
perc_formal = (len(df_f[df_f["Formalizaci\u00f3n"]=="Formalizado"]) / n_filtrado * 100) if n_filtrado > 0 else 0
res_media   = df_f["Resiliencia"].mean() if n_filtrado > 0 else 0
riesgo_media = df_f["Perfil de Riesgo"].mean() if n_filtrado > 0 else 0

def gauge(valor, titulo, rango_max, sufijo=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        number={"suffix": sufijo, "font": {"size": 34, "color": "#0f172a"}},
        title={"text": titulo, "font": {"size": 12, "color": "#64748b"}},
        gauge={
            "axis": {"range": [0, rango_max], "tickfont": {"size": 9}},
            "bar": {"color": "#0284c7", "thickness": 0.3},
            "bgcolor": "#f8fafc",
            "borderwidth": 0,
            "steps": [
                {"range": [0, rango_max * 0.4], "color": "#fef2f2"},
                {"range": [rango_max * 0.4, rango_max * 0.7], "color": "#fefce8"},
                {"range": [rango_max * 0.7, rango_max], "color": "#f0fdf4"},
            ],
        }
    ))
    fig.update_layout(
        height=190,
        margin=dict(l=15, r=15, t=35, b=5),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Muestra Filtrada", f"{n_filtrado}", delta=f"de {total_n} total")
    st.metric("Formalizacion", f"{perc_formal:.1f}%")
with kpi2:
    st.plotly_chart(gauge(res_media, "RESILIENCIA", 5), use_container_width=True)
with kpi3:
    st.plotly_chart(gauge(riesgo_media, "PERFIL DE RIESGO", 5), use_container_width=True)
with kpi4:
    st.plotly_chart(gauge(perc_formal, "FORMALIZACION %", 100, "%"), use_container_width=True)

st.divider()

# ── SEMAFORO ────────────────────────────────────────────────
if n_filtrado > 0:
    with st.expander("Semaforo Psicometrico - 15 Dimensiones", expanded=False):
        medias_db = df_f[PSIC_COLS_DB].mean()
        medias_db.index = PSIC_COLS
        medias = medias_db.sort_values(ascending=False)
        media_global = medias.mean()

        col_a, col_b, col_c = st.columns(3)
        items = list(medias.items())
        for col_idx, col in enumerate([col_a, col_b, col_c]):
            with col:
                for dim, val in items[col_idx*5 : (col_idx+1)*5]:
                    if val >= media_global + 0.1:
                        clase, color = "sem-v", "#22c55e"
                    elif val >= media_global - 0.1:
                        clase, color = "sem-a", "#eab308"
                    else:
                        clase, color = "sem-r", "#ef4444"
                    st.markdown(
                        f'<div class="{clase} sem-row">'
                        f'<span><span class="sem-dot" style="background:{color};"></span>{dim}</span>'
                        f'<strong>{val:.2f}</strong></div>',
                        unsafe_allow_html=True
                    )

# ── BARRAS DEMOGRAFICAS ─────────────────────────────────────
st.subheader("Distribucion Demografica")
H = 260
c1, c2, c3 = st.columns(3)
with c1:
    st.plotly_chart(
        px.bar(df_f.groupby("Rango de Edad").size().reset_index(name="n"),
               x="Rango de Edad", y="n", title="Edad", height=H,
               color_discrete_sequence=["#0284c7"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )
with c2:
    st.plotly_chart(
        px.bar(df_f.groupby("Nivel Educativo").size().reset_index(name="n"),
               x="Nivel Educativo", y="n", title="Educacion", height=H,
               color_discrete_sequence=["#0ea5e9"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )
with c3:
    st.plotly_chart(
        px.bar(df_f.groupby("Antig\u00fcedad del Negocio").size().reset_index(name="n"),
               x="Antig\u00fcedad del Negocio", y="n", title="Antiguedad", height=H,
               color_discrete_sequence=["#38bdf8"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )

c4, c5, c6 = st.columns(3)
with c4:
    st.plotly_chart(
        px.bar(df_f.groupby("Ingresos Mensuales").size().reset_index(name="n"),
               x="Ingresos Mensuales", y="n", title="Ingresos", height=H,
               color_discrete_sequence=["#7dd3fc"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )
with c5:
    st.plotly_chart(
        px.bar(df_f.groupby("Carga Familiar").size().reset_index(name="n"),
               x="Carga Familiar", y="n", title="Carga Familiar", height=H,
               color_discrete_sequence=["#0284c7"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )
with c6:
    st.plotly_chart(
        px.bar(df_f.groupby("Estrato").size().reset_index(name="n"),
               x="Estrato", y="n", title="Estrato", height=H,
               color_discrete_sequence=["#0ea5e9"]).update_layout(
                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                   xaxis_title="", yaxis_title=""),
        use_container_width=True
    )

# ── PESTANAS ────────────────────────────────────────────────
st.divider()
t1, t2, t3, t4 = st.tabs(["Visualizacion", "Interpretacion IA", "Datos", "Diccionario"])

with t1:
    col_a, col_b = st.columns(2)
    with col_a:
        df_l = df_f[PSIC_COLS_DB].mean().reset_index()
        df_l.columns = ["Dim", "Val"]
        df_l["Dim"] = PSIC_COLS
        fig_rad = px.line_polar(df_l, r="Val", theta="Dim", line_close=True,
                                title="Perfil Psicometrico (Radar)")
        fig_rad.update_traces(fill="toself", fillcolor="rgba(2,132,199,0.12)",
                               line_color="#0284c7", line_width=2)
        fig_rad.update_layout(
            polar=dict(radialaxis=dict(range=[1,5], tickfont=dict(size=9))),
            paper_bgcolor="rgba(0,0,0,0)", title_font=dict(size=13)
        )
        st.plotly_chart(fig_rad, use_container_width=True)
    with col_b:
        df_p = df_f.groupby(["Nodo de Significancia", "Formalizaci\u00f3n"]).size().reset_index(name="n")
        fig_nodo = px.bar(df_p, x="Nodo de Significancia", y="n",
                          color="Formalizaci\u00f3n", barmode="group",
                          title="Formalizacion por Nodo",
                          color_discrete_map={"Formalizado":"#22c55e","No Formalizado":"#f97316"})
        fig_nodo.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_nodo, use_container_width=True)

    st.subheader("Mapa de Calor de Correlaciones")
    if n_filtrado > 5:
        corr = df_f[PSIC_COLS_DB].corr()
        corr.index = PSIC_COLS
        corr.columns = PSIC_COLS
        fig_h = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", height=680)
        fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_h, use_container_width=True)

with t2:
    st.subheader("Interpretacion de Metricas")

    flags = {
        "Formalizaci\u00f3n": len(f_formal) < len(df_raw["Formalizaci\u00f3n"].unique()),
        "Nodo de Significancia": len(f_nodo) < len(df_raw["Nodo de Significancia"].unique()),
        "Rango de Edad": len(f_edad) < len(df_raw["Rango de Edad"].unique()),
        "Nivel Educativo": len(f_educ) < len(df_raw["Nivel Educativo"].unique()),
        "Estrato": len(f_estrato) < len(df_raw["Estrato"].unique()),
        "Antig\u00fcedad del Negocio": len(f_antig) < len(df_raw["Antig\u00fcedad del Negocio"].unique())
    }

    hipercubo = agente.analizar_hipercubo_dinamico(df_f, flags)

    if hipercubo:
        st.subheader("Diagnostico del Hipercubo")
        h1, h2 = st.columns(2)
        with h1:
            v = hipercubo["valle_resiliencia"]
            segmento = " | ".join([f"{d}: {v.get(d,'N/A')}" for d in hipercubo["dimensiones"]])
            st.markdown(f"""<div class="card-rojo">
                <p class="card-label">VALLE DE RESILIENCIA</p>
                <p class="card-value-rojo">{v["Resiliencia_mean"]:.2f}</p>
                <p class="card-sub">{segmento}</p>
            </div>""", unsafe_allow_html=True)
        with h2:
            p = hipercubo["pico_riesgo"]
            segmento_p = " | ".join([f"{d}: {p.get(d,'N/A')}" for d in hipercubo["dimensiones"]])
            st.markdown(f"""<div class="card-verde">
                <p class="card-label">PICO DE RIESGO</p>
                <p class="card-value-verde">{p["Perfil de Riesgo_mean"]:.2f}</p>
                <p class="card-sub">{segmento_p}</p>
            </div>""", unsafe_allow_html=True)

    st.divider()

    if st.button("Ejecutar Sintesis Priorizada", type="primary"):
        if n_filtrado > 0:
            with st.spinner("Analizando..."):
                means = df_f[PSIC_COLS_DB].mean()
                means.index = PSIC_COLS
                means = means.sort_values(ascending=False)
                payload = f"N={n_filtrado}. Picos: {means.head(3).to_dict()}. Valles: {means.tail(3).to_dict()}"
                vector  = agente.obtener_vector_critico(df_f)
                st.write_stream(agente.interpretar_hallazgo(
                    "resiliencia y riesgo", payload, vector,
                    motor=motor_id, hipercubo=hipercubo))
        else:
            st.warning("Sin datos en el filtro actual.")

    st.divider()
    user_prompt = st.text_area("Consulta personalizada", placeholder="Ejemplo: Analiza por que los tenderos formalizados tienen mayor resiliencia...")
    if st.button("Ejecutar Consulta"):
        if user_prompt and n_filtrado > 0:
            with st.spinner("Procesando..."):
                means = df_f[PSIC_COLS_DB].mean()
                means.index = PSIC_COLS
                payload = f"N={n_filtrado}. DATOS: {means.to_dict()}."
                vector  = agente.obtener_vector_critico(df_f)
                st.write_stream(agente.interpretar_hallazgo(
                    user_prompt, payload, vector,
                    motor=motor_id, hipercubo=hipercubo))
        elif not user_prompt:
            st.error("Escribe una consigna primero.")
        else:
            st.warning("Sin datos en el filtro actual.")

with t3:
    st.subheader("Explorador de Microdatos")
    st.dataframe(
        df_f.drop(columns=["Ubicación Original"], errors="ignore"),
        use_container_width=True, height=600
    )
    st.download_button(
        "Descargar CSV",
        df_f.to_csv(index=False).encode("utf-8"),
        file_name="muestra_filtrada.csv",
        mime="text/csv"
    )

with t4:
    st.subheader("Ficha Tecnica - Representatividad Muestral")
    st.markdown("""
| Municipio        | Universo (N) | Muestra (n) | Cobertura | Margen Error |
|:-----------------|:---:|:---:|:---:|:---:|
| Lerida           | 40  | 29  | 72.5% | +/- 9.1%  |
| Mariquita        | 126 | 18  | 14.3% | +/- 21.7% |
| Armero Guayabal  | 44  | 11  | 25.0% | +/- 26.3% |
| Casabianca       | 13  | 5   | 38.5% | +/- 35.0% |
| Honda            | 101 | 4   | 4.0%  | +/- 48.0% |
| Ambalema         | 22  | 1   | 4.5%  | +/- 96.0% |
| Falan            | 22  | 1   | 4.5%  | +/- 96.0% |
| Fresno           | 49  | 1   | 2.0%  | +/- 96.0% |
| Venadillo        | 66  | 1   | 1.5%  | +/- 96.0% |
| **TOTAL**        | **483** | **71** | **14.7%** | **+/- 10.5%** |
    """)
    st.divider()
    st.subheader("Glosario de Dimensiones Psicometricas")
    st.info("Escala Likert 1-5, donde 5 es el nivel mas alto de competencia autopercibida.")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("""
**Orientacion Emprendedora**
- Autonomia: Decisiones independientes sin supervision.
- Iniciativa: Proactividad ante la competencia.
- Creatividad: Soluciones novedosas para el negocio.
- Oportunidad: Deteccion de ventajas en el mercado.
- Motivacion: Impulso interno de crecimiento.

**Gestion Estrategica**
- Gestion Adm.: Control de procesos internos.
- Analisis FODA: Reconocimiento de fortalezas y amenazas.
- Gestion Riesgo: Manejo de incertidumbre financiera.
        """)
    with g2:
        st.markdown("""
**Capital Humano y Resiliencia**
- Resiliencia: Adaptacion ante crisis economicas.
- Aprender del Error: Transformar fallos en aprendizaje.
- Comunicacion: Eficacia con proveedores y clientes.
- Trabajo Equipo: Colaboracion con actores locales.

**Enfoque Operativo**
- Perfil de Riesgo: Disposicion a riesgos calculados.
- Pensamiento Creativo: Logica creativa en tareas diarias.
- Autonomia en Tareas: Independencia en ejecucion operativa.
        """)
