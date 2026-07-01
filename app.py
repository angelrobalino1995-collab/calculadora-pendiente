import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

# ───────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Calculadora de Pendiente 3D",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ───────────────────────────────────────────────────
# CSS PREMIUM
# ───────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Outfit', sans-serif; }

    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin-bottom: 24px;
    }

    .metric-card {
        background: rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        backdrop-filter: blur(6px);
        text-align: center;
        flex: 1;
        min-width: 180px;
        transition: all 0.28s cubic-bezier(0.4,0,0.2,1);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(99,102,241,0.18);
        border-color: rgba(99,102,241,0.55);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #818cf8;
        margin-bottom: 4px;
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }

    .metric-label {
        font-size: 0.78rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    .metric-sub {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 5px;
    }

    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
    }

    .badge-ok { background: rgba(16,185,129,0.15); color: #34d399; }
    .badge-warn { background: rgba(245,158,11,0.15); color: #fbbf24; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────────
# ENCABEZADO
# ───────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #3730a3 0%, #6d28d9 60%, #be185d 100%);
            padding: 36px 28px; border-radius: 22px; margin-bottom: 28px;
            text-align: center; color: white;
            box-shadow: 0 14px 30px -6px rgba(109,40,217,0.45);">
    <h1 style="color:white; margin:0; font-weight:800; font-size:2.5rem;
               letter-spacing:-0.03em; text-shadow: 0 2px 6px rgba(0,0,0,0.18);">
        📐 Calculadora de Pendiente en el Espacio 3D
    </h1>
    <p style="margin:14px 0 0; font-size:1.1rem; opacity:0.88; max-width:750px;
              margin-left:auto; margin-right:auto;">
        Ingresa las coordenadas de dos puntos en el espacio
        <em>P₁(x₁,y₁,z₁)</em> y <em>P₂(x₂,y₂,z₂)</em> para analizar el
        vector dirección, ángulos de inclinación, pendientes proyectadas y
        la ecuación paramétrica de la recta.
    </p>
</div>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────────
# SIDEBAR – ENTRADAS
# ───────────────────────────────────────────────────
st.sidebar.markdown("""
<h2 style="font-family:'Outfit',sans-serif; font-weight:700; font-size:1.35rem;
           color:#818cf8; margin-bottom:12px;">📍 Puntos en el Espacio</h2>
""", unsafe_allow_html=True)

st.sidebar.subheader("Punto 1  P₁(x₁, y₁, z₁)")
c1a, c1b, c1c = st.sidebar.columns(3)
with c1a: x1 = st.number_input("x₁", value=1.0, step=0.5, format="%.2f", key="x1")
with c1b: y1 = st.number_input("y₁", value=2.0, step=0.5, format="%.2f", key="y1")
with c1c: z1 = st.number_input("z₁", value=0.0, step=0.5, format="%.2f", key="z1")

st.sidebar.markdown("---")

st.sidebar.subheader("Punto 2  P₂(x₂, y₂, z₂)")
c2a, c2b, c2c = st.sidebar.columns(3)
with c2a: x2 = st.number_input("x₂", value=4.0, step=0.5, format="%.2f", key="x2")
with c2b: y2 = st.number_input("y₂", value=6.0, step=0.5, format="%.2f", key="y2")
with c2c: z2 = st.number_input("z₂", value=3.0, step=0.5, format="%.2f", key="z2")

st.sidebar.markdown("---")

st.sidebar.markdown("""
<h3 style="font-family:'Outfit',sans-serif; font-weight:600; font-size:1.05rem; margin-bottom:8px;">
    👁️ Visualización
</h3>
""", unsafe_allow_html=True)
show_triangle = st.sidebar.checkbox("Proyecciones ortogonales (Δx, Δy, Δz)", value=True)
show_extended = st.sidebar.checkbox("Extender recta más allá de los puntos", value=True)
color_theme   = st.sidebar.selectbox("Esquema de color",
    ["Violeta / Rosa", "Cian / Verde", "Naranja / Amarillo"])

# Paleta de colores
if color_theme == "Violeta / Rosa":
    lc, pc, dx_c, dy_c, dz_c = "#818cf8", "#6d28d9", "#a78bfa", "#f472b6", "#34d399"
elif color_theme == "Cian / Verde":
    lc, pc, dx_c, dy_c, dz_c = "#22d3ee", "#0e7490", "#38bdf8", "#4ade80", "#facc15"
else:
    lc, pc, dx_c, dy_c, dz_c = "#fb923c", "#b45309", "#fbbf24", "#ef4444", "#a3e635"

# ───────────────────────────────────────────────────
# CÁLCULOS MATEMÁTICOS
# ───────────────────────────────────────────────────
dx = x2 - x1
dy = y2 - y1
dz = z2 - z1

is_same = (dx == 0 and dy == 0 and dz == 0)

# Módulo del vector dirección (longitud del segmento)
length = math.sqrt(dx**2 + dy**2 + dz**2) if not is_same else 0.0

# Cosenos directores (ángulos con cada eje)
if not is_same:
    cos_alpha = dx / length          # ángulo con eje X
    cos_beta  = dy / length          # ángulo con eje Y
    cos_gamma = dz / length          # ángulo con eje Z
    alpha = math.degrees(math.acos(max(-1.0, min(1.0, cos_alpha))))
    beta  = math.degrees(math.acos(max(-1.0, min(1.0, cos_beta))))
    gamma = math.degrees(math.acos(max(-1.0, min(1.0, cos_gamma))))
else:
    cos_alpha = cos_beta = cos_gamma = 0.0
    alpha = beta = gamma = 0.0

# Pendientes proyectadas (pendiente 2D en cada plano coordenado)
slope_xy = dy / dx      if dx != 0 else None   # plano XY
slope_xz = dz / dx      if dx != 0 else None   # plano XZ
slope_yz = dz / dy      if dy != 0 else None   # plano YZ

# ───────────────────────────────────────────────────
# MÉTRICAS CLAVE
# ───────────────────────────────────────────────────
st.markdown("### 📊 Métricas Clave")

def fmt_slope(s):
    return f"{s:.4f}" if s is not None else "∞"

def fmt_angle(a):
    return f"{a:.2f}°"

metric_html = "<div class='metric-container'>"

cards = [
    ("length", f"{length:.4f}", "Distancia |P₁P₂|", "Módulo del vector dirección"),
    ("alpha",  fmt_angle(alpha),  "Ángulo α (con eje X)", f"cos α = {cos_alpha:.4f}"),
    ("beta",   fmt_angle(beta),   "Ángulo β (con eje Y)", f"cos β = {cos_beta:.4f}"),
    ("gamma",  fmt_angle(gamma),  "Ángulo γ (con eje Z)", f"cos γ = {cos_gamma:.4f}"),
    ("mxy",  fmt_slope(slope_xy), "Pendiente m_XY",       "Proyección plano XY"),
    ("mxz",  fmt_slope(slope_xz), "Pendiente m_XZ",       "Proyección plano XZ"),
    ("myz",  fmt_slope(slope_yz), "Pendiente m_YZ",       "Proyección plano YZ"),
]

for _, val, label, sub in cards:
    metric_html += f"""
<div class='metric-card'>
    <div class='metric-value'>{val}</div>
    <div class='metric-label'>{label}</div>
    <div class='metric-sub'>{sub}</div>
</div>"""

metric_html += "</div>"
st.markdown(metric_html, unsafe_allow_html=True)

# ───────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ───────────────────────────────────────────────────
col_graph, col_math = st.columns([3, 2])

# ── GRÁFICO 3D ──────────────────────────────────────
with col_graph:
    st.markdown("### 🌐 Visualización Geométrica 3D")

    if is_same:
        st.warning("Los dos puntos son idénticos. No se puede trazar una recta.")
    else:
        fig = go.Figure()

        # Parámetro t para extender la recta
        t_range = np.linspace(-0.5 if show_extended else 0,
                               1.5 if show_extended else 1, 200)
        line_x = x1 + t_range * dx
        line_y = y1 + t_range * dy
        line_z = z1 + t_range * dz

        # ── Recta principal ──
        fig.add_trace(go.Scatter3d(
            x=line_x, y=line_y, z=line_z,
            mode="lines",
            line=dict(color=lc, width=5),
            name="Recta 3D",
            hoverinfo="skip"
        ))

        # ── Proyecciones ortogonales (triángulo 3D) ──
        if show_triangle:
            # Proyección sobre plano XY (z constante = z1)
            fig.add_trace(go.Scatter3d(
                x=[x1, x2, x2], y=[y1, y2, y2], z=[z1, z1, z2],
                mode="lines",
                line=dict(color=dx_c, width=3, dash="dash"),
                name=f"Δx={dx:.2f}  |  Δy={dy:.2f}  |  Δz={dz:.2f}",
            ))
            # Aristas auxiliares del paralelepípedo
            for xs,ys,zs,xe,ye,ze,col,nm in [
                (x1, y1, z1, x2, y1, z1, dx_c, f"Δx = {dx:.2f}"),
                (x2, y1, z1, x2, y2, z1, dy_c, f"Δy = {dy:.2f}"),
                (x2, y2, z1, x2, y2, z2, dz_c, f"Δz = {dz:.2f}"),
            ]:
                fig.add_trace(go.Scatter3d(
                    x=[xs,xe], y=[ys,ye], z=[zs,ze],
                    mode="lines+text",
                    line=dict(color=col, width=3, dash="dot"),
                    name=nm, showlegend=True,
                    text=["", nm],
                    textposition="middle right",
                ))

        # ── Puntos P1 y P2 ──
        for xi, yi, zi, lbl in [(x1,y1,z1,"P₁"), (x2,y2,z2,"P₂")]:
            fig.add_trace(go.Scatter3d(
                x=[xi], y=[yi], z=[zi],
                mode="markers+text",
                marker=dict(size=9, color=pc, line=dict(color="white", width=2)),
                text=[lbl], textposition="top center",
                name=lbl,
                hovertemplate=f"<b>{lbl}</b><br>x={xi:.2f}<br>y={yi:.2f}<br>z={zi:.2f}<extra></extra>"
            ))

        fig.update_layout(
            scene=dict(
                xaxis=dict(title="X", gridcolor="rgba(128,128,128,0.15)",
                           backgroundcolor="rgba(0,0,0,0)", showbackground=False),
                yaxis=dict(title="Y", gridcolor="rgba(128,128,128,0.15)",
                           backgroundcolor="rgba(0,0,0,0)", showbackground=False),
                zaxis=dict(title="Z", gridcolor="rgba(128,128,128,0.15)",
                           backgroundcolor="rgba(0,0,0,0)", showbackground=False),
                bgcolor="rgba(0,0,0,0)",
                camera=dict(eye=dict(x=1.6, y=1.4, z=1.0))
            ),
            margin=dict(l=0, r=0, t=10, b=0),
            height=560,
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                yanchor="top", y=0.97,
                xanchor="left", x=0.01,
                bgcolor="rgba(20,20,30,0.5)",
                bordercolor="rgba(255,255,255,0.08)",
                borderwidth=1,
            )
        )

        st.plotly_chart(fig, use_container_width=True)

# ── DESGLOSE MATEMÁTICO ──────────────────────────────
with col_math:
    st.markdown("### 📝 Desglose Matemático")

    if is_same:
        st.error("Los puntos son idénticos — no hay recta ni vector definido.")
    else:
        # 1. Puntos
        st.markdown("#### 1. Puntos en el espacio")
        st.latex(rf"P_1 = ({x1:.2f},\; {y1:.2f},\; {z1:.2f})")
        st.latex(rf"P_2 = ({x2:.2f},\; {y2:.2f},\; {z2:.2f})")

        # 2. Vector dirección
        st.markdown("#### 2. Vector Dirección $\overrightarrow{d}$")
        st.latex(rf"\vec{{d}} = P_2 - P_1 = ({dx:.2f},\; {dy:.2f},\; {dz:.2f})")

        # 3. Módulo
        st.markdown("#### 3. Módulo del Vector (distancia)")
        st.latex(r"|\vec{d}| = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2}")
        st.latex(rf"= \sqrt{{{dx:.2f}^2 + {dy:.2f}^2 + {dz:.2f}^2}} = {length:.4f}")

        # 4. Cosenos directores
        st.markdown("#### 4. Cosenos Directores y Ángulos")
        st.latex(r"\cos\alpha = \frac{\Delta x}{|\vec{d}|},\quad"
                 r"\cos\beta = \frac{\Delta y}{|\vec{d}|},\quad"
                 r"\cos\gamma = \frac{\Delta z}{|\vec{d}|}")
        st.latex(rf"\alpha = {alpha:.2f}^\circ,\quad"
                 rf"\beta = {beta:.2f}^\circ,\quad"
                 rf"\gamma = {gamma:.2f}^\circ")

        # 5. Pendientes proyectadas
        st.markdown("#### 5. Pendientes Proyectadas")
        if slope_xy is not None:
            st.latex(rf"m_{{XY}} = \frac{{\Delta y}}{{\Delta x}} = \frac{{{dy:.2f}}}{{{dx:.2f}}} = {slope_xy:.4f}")
        else:
            st.info("$m_{XY}$: Indefinida (Δx = 0 → recta vertical en plano XY)")

        if slope_xz is not None:
            st.latex(rf"m_{{XZ}} = \frac{{\Delta z}}{{\Delta x}} = \frac{{{dz:.2f}}}{{{dx:.2f}}} = {slope_xz:.4f}")
        else:
            st.info("$m_{XZ}$: Indefinida (Δx = 0 → recta vertical en plano XZ)")

        if slope_yz is not None:
            st.latex(rf"m_{{YZ}} = \frac{{\Delta z}}{{\Delta y}} = \frac{{{dz:.2f}}}{{{dy:.2f}}} = {slope_yz:.4f}")
        else:
            st.info("$m_{YZ}$: Indefinida (Δy = 0 → recta vertical en plano YZ)")

        # 6. Ecuación paramétrica
        st.markdown("#### 6. Ecuación Paramétrica de la Recta")
        st.latex(r"\begin{cases}"
                 rf"x = {x1:.2f} + {dx:.2f}\,t \\"
                 rf"y = {y1:.2f} + {dy:.2f}\,t \\"
                 rf"z = {z1:.2f} + {dz:.2f}\,t"
                 r"\end{cases}")
        st.caption("Donde t = 0 → P₁ y t = 1 → P₂")

        # 7. Ecuación simétrica (si todos los deltas son distintos de cero)
        if dx != 0 and dy != 0 and dz != 0:
            st.markdown("#### 7. Ecuación Simétrica (Cartesiana)")
            st.latex(rf"\frac{{x - {x1:.2f}}}{{{dx:.2f}}} = "
                     rf"\frac{{y - {y1:.2f}}}{{{dy:.2f}}} = "
                     rf"\frac{{z - {z1:.2f}}}{{{dz:.2f}}}")

# ── SECCIÓN EDUCATIVA ────────────────────────────────
with st.expander("📚 Conceptos Clave: Rectas en el Espacio 3D", expanded=False):
    st.markdown("""
| Concepto | Fórmula | Descripción |
|---|---|---|
| **Vector dirección** | $\\vec{d} = (\\Delta x, \\Delta y, \\Delta z)$ | Indica la dirección de la recta |
| **Distancia** | $\\|\\vec{d}\\| = \\sqrt{\\Delta x^2+\\Delta y^2+\\Delta z^2}$ | Longitud del segmento |
| **Coseno director α** | $\\cos\\alpha = \\Delta x / \\|\\vec{d}\\|$ | Ángulo con eje X |
| **Coseno director β** | $\\cos\\beta = \\Delta y / \\|\\vec{d}\\|$ | Ángulo con eje Y |
| **Coseno director γ** | $\\cos\\gamma = \\Delta z / \\|\\vec{d}\\|$ | Ángulo con eje Z |
| **Propiedad** | $\\cos^2\\alpha+\\cos^2\\beta+\\cos^2\\gamma = 1$ | Identidad de cosenos directores |
| **Pendiente $m_{XY}$** | $\\Delta y/\\Delta x$ | Pendiente en la proyección sobre el plano XY |
| **Pendiente $m_{XZ}$** | $\\Delta z/\\Delta x$ | Pendiente en la proyección sobre el plano XZ |
| **Pendiente $m_{YZ}$** | $\\Delta z/\\Delta y$ | Pendiente en la proyección sobre el plano YZ |

> 💡 **Nota:** En el espacio 3D no existe una sola "pendiente"; hay tres pendientes proyectadas y
> tres ángulos directores. El vector dirección $\\vec{d}$ es la generalización completa del concepto de pendiente.
""")
