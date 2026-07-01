import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

# Configuración de página
st.set_page_config(
    page_title="Calculadora de Pendiente 2D",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS premium personalizados
st.markdown("""
<style>
    /* Estilos generales */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Contenedor principal de métricas */
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    /* Estilo de las tarjetas de métricas */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        text-align: center;
        flex: 1;
        min-width: 200px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #6366f1;
        margin-bottom: 5px;
        font-family: 'Outfit', sans-serif;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* Subtítulo de tarjeta */
    .metric-sub {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 5px;
    }
    
    /* Contenedor de explicaciones */
    .math-explanation {
        background: rgba(99, 102, 241, 0.03);
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado Premium con gradiente
st.markdown("""
<div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 35px 25px; border-radius: 20px; margin-bottom: 30px; text-align: center; color: white; box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);">
    <h1 style="color: white; margin: 0; font-weight: 800; font-size: 2.6rem; letter-spacing: -0.03em; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        📐 Calculadora de Pendiente y Recta 2D
    </h1>
    <p style="margin: 12px 0 0 0; font-size: 1.15rem; opacity: 0.9; font-weight: 400; max-width: 700px; margin-left: auto; margin-right: auto;">
        Ingresa las coordenadas de dos puntos para analizar de forma interactiva su pendiente, ángulo de inclinación, ecuación de la recta y visualización geométrica.
    </p>
</div>
""", unsafe_allow_html=True)

# Barra lateral para entrada de datos
st.sidebar.markdown("""
<h2 style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1.4rem; color: #4f46e5; margin-bottom: 15px;">
    📍 Parámetros de Entrada
</h2>
""", unsafe_allow_html=True)

st.sidebar.subheader("Punto 1 $P_1(x_1, y_1)$")
col_p1_x, col_p1_y = st.sidebar.columns(2)
with col_p1_x:
    x1 = st.number_input("x₁", value=1.0, step=0.5, format="%.2f", key="x1")
with col_p1_y:
    y1 = st.number_input("y₁", value=2.0, step=0.5, format="%.2f", key="y1")

st.sidebar.markdown("---")

st.sidebar.subheader("Punto 2 $P_2(x_2, y_2)$")
col_p2_x, col_p2_y = st.sidebar.columns(2)
with col_p2_x:
    x2 = st.number_input("x₂", value=5.0, step=0.5, format="%.2f", key="x2")
with col_p2_y:
    y2 = st.number_input("y₂", value=5.0, step=0.5, format="%.2f", key="y2")

st.sidebar.markdown("---")

# Controles de visualización
st.sidebar.markdown("""
<h3 style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1.1rem; margin-bottom: 10px;">
    👁️ Opciones de Gráfico
</h3>
""", unsafe_allow_html=True)
show_triangle = st.sidebar.checkbox("Mostrar triángulo de pendiente (Δx, Δy)", value=True)
show_extended = st.sidebar.checkbox("Extender recta al infinito", value=True)
color_theme = st.sidebar.selectbox("Esquema de Color", ["Indigo / Morado", "Verde / Esmeralda", "Naranja / Rojo"])

# Mapeo de colores según el esquema
if color_theme == "Indigo / Morado":
    line_color = "#6366f1"
    point_color = "#4f46e5"
    run_color = "#8b5cf6"
    rise_color = "#ec4899"
elif color_theme == "Verde / Esmeralda":
    line_color = "#10b981"
    point_color = "#059669"
    run_color = "#3b82f6"
    rise_color = "#f59e0b"
else:
    line_color = "#ef4444"
    point_color = "#dc2626"
    run_color = "#10b981"
    rise_color = "#f59e0b"

# Cálculo de variables
dx = x2 - x1
dy = y2 - y1

is_same_point = (dx == 0 and dy == 0)
is_vertical = (dx == 0 and not is_same_point)
is_horizontal = (dy == 0 and not is_same_point)

# Inicializar variables de salida
slope = None
intercept = None
angle_deg = None

if is_same_point:
    status_msg = "Advertencia: Ambos puntos son iguales. No se puede definir una recta única."
    angle_deg = 0.0
elif is_vertical:
    status_msg = "Línea Vertical (Pendiente indefinida, división por cero)"
    angle_deg = 90.0 if dy > 0 else -90.0
else:
    slope = dy / dx
    intercept = y1 - slope * x1
    angle_rad = math.atan(slope)
    angle_deg = math.degrees(angle_rad)
    status_msg = "Operación exitosa"

# Diseño de la sección principal
# Sección de Métricas principales (Tarjetas personalizadas)
st.markdown("### 📊 Métricas Clave")

metric_html = "<div class='metric-container'>"

# Pendiente (m)
if is_same_point:
    val_m = "N/A"
    lbl_m = "Pendiente (m) - Indefinida"
    sub_m = "Puntos idénticos"
elif is_vertical:
    val_m = "∞"
    lbl_m = "Pendiente (m) - Indefinida"
    sub_m = "Recta vertical"
else:
    val_m = f"{slope:.4f}"
    # Mostrar fracción simplificada si es posible para mejorar experiencia
    try:
        from fractions import Fraction
        frac = Fraction(dy).limit_denominator() / Fraction(dx).limit_denominator()
        sub_m = f"Equivale a {frac}"
    except Exception:
        sub_m = f"Δy / Δx = {dy:.2f} / {dx:.2f}"
    lbl_m = "Pendiente (m)"

metric_html += f"""
<div class='metric-card'>
    <div class='metric-value'>{val_m}</div>
    <div class='metric-label'>{lbl_m}</div>
    <div class='metric-sub'>{sub_m}</div>
</div>
"""

# Ángulo (θ)
val_ang = f"{angle_deg:.2f}°"
sub_ang = "Ángulo con respecto al eje X"
metric_html += f"""
<div class='metric-card'>
    <div class='metric-value'>{val_ang}</div>
    <div class='metric-label'>Ángulo de Inclinación (θ)</div>
    <div class='metric-sub'>{sub_ang}</div>
</div>
"""

# Intersección en Y (b)
if is_same_point:
    val_b = "N/A"
    sub_b = "Sin recta"
elif is_vertical:
    val_b = "N/A"
    sub_b = f"No cruza Y (salvo si x={x1}=0)"
else:
    val_b = f"{intercept:.4f}"
    sub_b = f"Cruza Y en (0, {intercept:.2f})"

metric_html += f"""
<div class='metric-card'>
    <div class='metric-value'>{val_b}</div>
    <div class='metric-label'>Intersección con Y (b)</div>
    <div class='metric-sub'>{sub_b}</div>
</div>
"""

metric_html += "</div>"
st.markdown(metric_html, unsafe_allow_html=True)

# Layout de columnas para el gráfico y la explicación paso a paso
col_graph, col_explanation = st.columns([3, 2])

with col_graph:
    st.markdown("### 📈 Visualización Geométrica")
    
    # Crear figura Plotly
    fig = go.Figure()
    
    # Rango de ejes dinámico pero balanceado
    padding_x = max(2.0, abs(dx) * 0.4)
    padding_y = max(2.0, abs(dy) * 0.4)
    
    x_min = min(x1, x2) - padding_x
    x_max = max(x1, x2) + padding_x
    y_min = min(y1, y2) - padding_y
    y_max = max(y1, y2) + padding_y
    
    # Asegurar que el gráfico tenga cuadrícula simétrica y proporciones correctas
    # 1. Trazado de la recta extendida o segmento
    if not is_same_point:
        if is_vertical:
            # Línea vertical
            y_line = np.linspace(y_min - 2, y_max + 2, 100)
            x_line = np.full_like(y_line, x1)
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode="lines",
                line=dict(color=line_color, width=3, dash="dash" if show_extended else "solid"),
                name="Recta (Vertical)",
                hoverinfo="skip"
            ))
        else:
            # Línea con pendiente
            x_line = np.linspace(x_min - 2, x_max + 2, 200)
            y_line = slope * x_line + intercept
            
            # Solo graficar en el rango si no se extiende al infinito
            if not show_extended:
                x_line = np.linspace(min(x1, x2), max(x1, x2), 100)
                y_line = slope * x_line + intercept
                
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode="lines",
                line=dict(color=line_color, width=3, dash="solid" if not show_extended else "solid"),
                name="Recta y = mx + b" if not show_extended else "Recta (Extendida)",
                hoverinfo="skip"
            ))
            
    # 2. Dibujar triángulo rectángulo (Δx, Δy) para ilustrar la pendiente
    if show_triangle and not is_same_point and not is_vertical and not is_horizontal:
        # Vértice del ángulo recto
        x_corner = x2
        y_corner = y1
        
        # Segmento Avance (Δx): de (x1, y1) a (x2, y1)
        fig.add_trace(go.Scatter(
            x=[x1, x_corner], y=[y1, y_corner],
            mode="lines+text",
            line=dict(color=run_color, width=2.5, dash="dash"),
            text=["", f"Δx = {dx:.2f}"],
            textposition="bottom center",
            name="Avance (Δx)",
            hovertemplate=f"Avance (Δx): {dx:.2f}<extra></extra>"
        ))
        
        # Segmento Elevación (Δy): de (x2, y1) a (x2, y2)
        fig.add_trace(go.Scatter(
            x=[x_corner, x2], y=[y_corner, y2],
            mode="lines+text",
            line=dict(color=rise_color, width=2.5, dash="dash"),
            text=["", f"Δy = {dy:.2f}"],
            textposition="middle right",
            name="Elevación (Δy)",
            hovertemplate=f"Elevación (Δy): {dy:.2f}<extra></extra>"
        ))
        
    # 3. Dibujar los puntos P1 y P2
    fig.add_trace(go.Scatter(
        x=[x1], y=[y1],
        mode="markers+text",
        marker=dict(color=point_color, size=14, symbol="circle", line=dict(color="white", width=2)),
        text=["P₁"],
        textposition="top left",
        name="Punto P₁",
        hovertemplate=f"<b>P₁</b><br>X: {x1:.2f}<br>Y: {y1:.2f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=[x2], y=[y2],
        mode="markers+text",
        marker=dict(color=point_color, size=14, symbol="circle", line=dict(color="white", width=2)),
        text=["P₂"],
        textposition="bottom right",
        name="Punto P₂",
        hovertemplate=f"<b>P₂</b><br>X: {x2:.2f}<br>Y: {y2:.2f}<extra></extra>"
    ))
    
    # Configuración de diseño del gráfico (Premium)
    fig.update_layout(
        xaxis=dict(
            title="Eje X",
            gridcolor="rgba(128, 128, 128, 0.15)",
            zerolinecolor="rgba(128, 128, 128, 0.4)",
            zerolinewidth=1.5,
            range=[x_min, x_max]
        ),
        yaxis=dict(
            title="Eje Y",
            gridcolor="rgba(128, 128, 128, 0.15)",
            zerolinecolor="rgba(128, 128, 128, 0.4)",
            zerolinewidth=1.5,
            scaleanchor="x",  # Bloqueo de aspecto 1:1 para que la pendiente sea geométricamente real
            scaleratio=1,
            range=[y_min, y_max]
        ),
        margin=dict(l=40, r=40, t=20, b=40),
        hovermode="closest",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.1)"
        ),
        height=550,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    # Mostrar el gráfico interactivo
    st.plotly_chart(fig, use_container_width=True)

with col_explanation:
    st.markdown("### 📝 Desglose Matemático")
    
    explanation_box = st.container()
    with explanation_box:
        st.markdown(f"**Estado del Cálculo:** `{status_msg}`")
        
        # Sección de coordenadas
        st.markdown("#### 1. Identificación de coordenadas")
        st.latex(rf"P_1 = ({x1:.2f}, {y1:.2f}) \quad \text{{y}} \quad P_2 = ({x2:.2f}, {y2:.2f})")
        
        # Cambios en X e Y
        st.markdown("#### 2. Calcular los incrementos ($\Delta$)")
        st.latex(rf"\Delta x = x_2 - x_1 = {x2:.2f} - ({x1:.2f}) = {dx:.2f}")
        st.latex(rf"\Delta y = y_2 - y_1 = {y2:.2f} - ({y1:.2f}) = {dy:.2f}")
        
        # Cálculo de la pendiente
        st.markdown("#### 3. Fórmula de la Pendiente ($m$)")
        st.latex(r"m = \frac{\Delta y}{\Delta x} = \frac{y_2 - y_1}{x_2 - x_1}")
        
        if is_same_point:
            st.warning("Dado que $\Delta x = 0$ y $\Delta y = 0$, los puntos coinciden. No se puede calcular una pendiente ya que no hay una dirección de recta definida.")
        elif is_vertical:
            st.markdown("Sustituyendo los valores:")
            st.latex(rf"m = \frac{{{dy:.2f}}}{{0}} \implies \text{{Indefinido (División por Cero)}}")
            st.info("La recta es completamente vertical, paralela al eje Y. Su ecuación es:")
            st.latex(rf"x = {x1:.2f}")
        else:
            st.markdown("Sustituyendo los valores:")
            st.latex(rf"m = \frac{{{dy:.2f}}}{{{dx:.2f}}} = {slope:.4f}")
            
            # Ecuación de la recta
            st.markdown("#### 4. Ecuación de la Recta")
            st.markdown("**Forma Punto-Pendiente:**")
            st.latex(rf"y - y_1 = m(x - x_1)")
            st.latex(rf"y - {y1:.2f} = {slope:.4f}(x - {x1:.2f})")
            
            st.markdown("**Forma Pendiente-Intersección ($y = mx + b$):**")
            st.latex(rf"b = y_1 - m \cdot x_1 = {y1:.2f} - ({slope:.4f} \cdot {x1:.2f}) = {intercept:.4f}")
            
            sign_b = "+" if intercept >= 0 else "-"
            abs_b = abs(intercept)
            st.latex(rf"y = {slope:.4f}x {sign_b} {abs_b:.4f}")
            
        # Ángulo de inclinación
        st.markdown("#### 5. Ángulo de Inclinación ($\theta$)")
        if is_same_point:
            st.latex(r"\theta = 0^\circ")
        elif is_vertical:
            direction = "+" if dy > 0 else "-"
            st.latex(rf"\theta = \arctan\left(\frac{{{dy:.2f}}}{{0}}\right) \rightarrow {direction}90^\circ")
        else:
            st.latex(r"\theta = \arctan(m)")
            st.latex(rf"\theta = \arctan({slope:.4f}) \approx {math.atan(slope):.4f} \text{{ rad}}")
            st.latex(rf"\theta \approx {angle_deg:.2f}^\circ")

# Sección inferior informativa y didáctica
with st.expander("📚 Conceptos Clave e Interpretación de la Pendiente", expanded=False):
    st.markdown("""
    * **Pendiente Positiva ($m > 0$):** La recta sube de izquierda a derecha. El ángulo $\theta$ está en el rango $(0^\circ, 90^\circ)$.
    * **Pendiente Negativa ($m < 0$):** La recta baja de izquierda a derecha. El ángulo $\theta$ está en el rango $(-90^\circ, 0^\circ)$ o $(90^\circ, 180^\circ)$.
    * **Pendiente Cero ($m = 0$):** La recta es perfectamente horizontal (paralela al eje X). $\Delta y = 0$.
    * **Pendiente Indefinida ($m = \infty$):** La recta es perfectamente vertical (paralela al eje Y). $\Delta x = 0$.
    * **Interpretación Física ($\Delta y / \Delta x$):** La pendiente te dice cuántas unidades cambia la variable $Y$ por cada unidad que incrementa la variable $X$.
    """)
