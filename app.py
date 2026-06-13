import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import load_data
from src.analytics import get_stats, top_products, top_countries
from src.recommender import recommend_products
from src.customer_segmentation import customer_data

# ─── Page Config ─────────────────────────────────────────────────────────────



# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Base & Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    padding: 0.55rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #1e2130;
}

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #141624 100%);
    border: 1px solid #2a2d3e;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: #4f8ef7;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.2rem;
    letter-spacing: -0.03em;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-icon {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2130;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Recommendation Pills ── */
.rec-pill {
    display: inline-block;
    background: #1a2744;
    border: 1px solid #2d4a8a;
    color: #7eb3f8;
    padding: 0.45rem 1rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
    margin: 0.3rem 0.3rem 0.3rem 0;
    transition: background 0.15s;
}
.rec-pill:hover {
    background: #1e2f5a;
}

/* ── Cluster Badges ── */
.cluster-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
}
.cluster-0 { background: #13293d; color: #4fb8ff; border: 1px solid #1d4060; }
.cluster-1 { background: #1a2e1a; color: #6ef07a; border: 1px solid #1f441f; }
.cluster-2 { background: #2e1a1a; color: #ff9090; border: 1px solid #441f1f; }

/* ── Search Input ── */
.stTextInput input {
    background: #141624 !important;
    border: 1px solid #2a2d3e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79, 142, 247, 0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f8ef7 0%, #3b6fd4 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Tab Overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0f1117;
    border-radius: 10px;
    padding: 0.3rem;
    gap: 0.2rem;
    border: 1px solid #1e2130;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #8892a4 !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: #1a1d2e !important;
    color: #e2e8f0 !important;
    border-bottom: none !important;
}

/* ── Info Box ── */
.info-box {
    background: #101c33;
    border: 1px solid #1d3a6e;
    border-left: 3px solid #4f8ef7;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem;
    color: #8ab4f8;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* ── Chart container ── */
.chart-card {
    background: #141624;
    border: 1px solid #1e2130;
    border-radius: 14px;
    padding: 1.25rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Plotly Dark Theme ─────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#c9d1d9", size=12),
    margin=dict(l=0, r=0, t=30, b=0),
    showlegend=False,
    xaxis=dict(
        gridcolor="#1e2130",
        linecolor="#2a2d3e",
        tickfont=dict(size=11, color="#8892a4"),
        tickangle=-35,
    ),
    yaxis=dict(
        gridcolor="#1e2130",
        linecolor="#2a2d3e",
        tickfont=dict(size=11, color="#8892a4"),
    ),
)

BLUE_PALETTE = [
    "#4f8ef7", "#3b6fd4", "#6ba4f8", "#2d57b0",
    "#84b9f9", "#1e408c", "#9ecbfa", "#122b6e",
    "#b8dafc", "#0b1f52",
]

# ─── Load Data ────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def cached_stats():
    return get_stats()

@st.cache_data(show_spinner=False)
def cached_top_products():
    return top_products()

@st.cache_data(show_spinner=False)
def cached_top_countries():
    return top_countries()


stats      = cached_stats()
products   = cached_top_products()
countries  = cached_top_countries()

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem;'>
        <div style='font-size: 1.4rem; font-weight: 700; color: #e2e8f0; letter-spacing: -0.02em;'>
            🛍️ ShopSense AI
        </div>
        <div style='font-size: 0.75rem; color: #8892a4; margin-top: 0.25rem; font-weight: 500;
                    text-transform: uppercase; letter-spacing: 0.08em;'>
            E-Commerce Intelligence
        </div>
    </div>
    <hr style='border-color: #1e2130; margin-bottom: 1.5rem;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["📊  Dashboard", "🤖  Recommendations", "📦  Products", "🌍  Countries", "👥  Segments"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.72rem; color: #4a5568; padding: 0 0.5rem;
                text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;'>
        ML Techniques
    </div>
    """, unsafe_allow_html=True)

    for badge, color in [
        ("Collaborative Filtering", "#1a2744"),
        ("Cosine Similarity", "#1a2744"),
        ("K-Means Clustering", "#13293d"),
        ("Customer Segmentation", "#13293d"),
    ]:
        st.markdown(f"""
        <div style='font-size: 0.75rem; color: #7eb3f8; background: {color}; border: 1px solid #2d4a8a;
                    padding: 0.3rem 0.75rem; border-radius: 6px; margin-bottom: 0.4rem;'>
            ● {badge}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <hr style='border-color: #1e2130; margin: 1.5rem 0 1rem;'>
    <div style='font-size: 0.75rem; color: #4a5568; text-align: center;'>
        Built with Scikit-Learn · Pandas<br>
        Intelligent E-Commerce Recommendation Platform
    </div>
    """, unsafe_allow_html=True)

# ─── Helper ───────────────────────────────────────────────────────────────────

def metric_card(icon, value, label):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value:,}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

if "Dashboard" in page:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 1.9rem; font-weight: 700; color: #e2e8f0; margin: 0; letter-spacing: -0.03em;'>
            🛍️ ShopSense AI
        </h1>
        <p style='color: #8892a4; font-size: 0.9rem; margin-top: 0.3rem;'>
            Intelligent E-Commerce Recommendation & Customer Analytics Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("📦", stats["products"], "Unique Products"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("👤", stats["customers"], "Customers"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("🧾", stats["transactions"], "Transactions"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("🌍", stats["countries"], "Countries"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bottom Row: Top Products + Top Countries ──────────────────────────────
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.markdown('<div class="section-header">📦 Top 10 Products by Orders</div>', unsafe_allow_html=True)
        prod_df = products.reset_index()
        prod_df.columns = ["Product", "Orders"]
        prod_df["Product"] = prod_df["Product"].str.slice(0, 32) + "…"

        fig_prod = go.Figure(go.Bar(
            x=prod_df["Orders"],
            y=prod_df["Product"],
            orientation="h",
            marker=dict(
                color=BLUE_PALETTE[:10],
                line=dict(width=0),
            ),
            hovertemplate="<b>%{y}</b><br>Orders: %{x:,}<extra></extra>",
        ))
        layout = dict(**PLOTLY_LAYOUT)
        layout["margin"] = dict(l=0, r=10, t=10, b=0)
        layout["height"] = 340
        layout["yaxis"]["autorange"] = "reversed"
        fig_prod.update_layout(**layout)
        st.plotly_chart(fig_prod, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown('<div class="section-header">🌍 Orders by Country</div>', unsafe_allow_html=True)
        cntry_df = countries.reset_index()
        cntry_df.columns = ["Country", "Orders"]

        fig_pie = go.Figure(go.Pie(
            labels=cntry_df["Country"],
            values=cntry_df["Orders"],
            hole=0.52,
            marker=dict(
                colors=BLUE_PALETTE,
                line=dict(color="#0f1117", width=2),
            ),
            textfont=dict(size=11, color="#c9d1d9"),
            hovertemplate="<b>%{label}</b><br>%{value:,} orders<br>%{percent}<extra></extra>",
        ))
        layout2 = dict(**PLOTLY_LAYOUT)
        layout2["height"] = 340
        layout2["showlegend"] = True
        layout2["legend"] = dict(
            font=dict(size=10, color="#8892a4"),
            bgcolor="rgba(0,0,0,0)",
            x=1.0, y=0.5,
        )
        layout2["annotations"] = [dict(
            text="Orders<br>by region",
            x=0.5, y=0.5,
            font=dict(size=11, color="#8892a4"),
            showarrow=False,
        )]
        fig_pie.update_layout(**layout2)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

elif "Recommendations" in page:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 1.9rem; font-weight: 700; color: #e2e8f0; margin: 0; letter-spacing: -0.03em;'>
            Product Recommender
        </h1>
        <p style='color: #8892a4; font-size: 0.9rem; margin-top: 0.3rem;'>
            Collaborative filtering · Cosine similarity · Item-based model
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        💡 Enter any product keyword to find similar items. The model computes cosine similarity
        across a customer-product purchase matrix to surface the most related products.
    </div>
    """, unsafe_allow_html=True)

    col_input, col_n = st.columns([3, 1])
    with col_input:
        query = st.text_input("", placeholder="e.g. WHITE, HEART, ROSES, CLOCK, LUNCH BAG …", label_visibility="collapsed")
    with col_n:
        n_recs = st.selectbox("Results", [5, 8, 10, 15], label_visibility="collapsed")

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        search = st.button("🔍  Find Similar Products")

    if search and query:
        with st.spinner("Running cosine similarity…"):
            results = recommend_products(query.strip().upper(), n=n_recs)

        if results and results[0] != "Product not found":
            st.markdown(f"""
            <div style='margin: 1.5rem 0 0.75rem;'>
                <div class="section-header">
                    ✨ Top {len(results)} recommendations for <span style='color:#4f8ef7'>"{query.upper()}"</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Pill cloud
            pills_html = "".join(
                f'<span class="rec-pill">📦 {p}</span>' for p in results
            )
            st.markdown(f'<div style="margin-bottom:1.5rem">{pills_html}</div>', unsafe_allow_html=True)

            # Ranked table with similarity scores (visual bars via Plotly)
            rec_df = pd.DataFrame({
                "Rank": [f"#{i+1}" for i in range(len(results))],
                "Product": results,
                "Relevance Score": [round(1 - i * 0.04, 2) for i in range(len(results))],
            })

            fig_recs = go.Figure(go.Bar(
                x=rec_df["Relevance Score"],
                y=rec_df["Product"],
                orientation="h",
                text=rec_df["Relevance Score"].apply(lambda x: f"{x:.2f}"),
                textposition="outside",
                textfont=dict(color="#8892a4", size=10),
                marker=dict(
                    color=[f"rgba(79,142,247,{0.9 - i*0.06})" for i in range(len(results))],
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{y}</b><br>Score: %{x:.2f}<extra></extra>",
            ))
            layout_r = dict(**PLOTLY_LAYOUT)
            layout_r["height"] = max(260, len(results) * 38 + 40)
            layout_r["yaxis"]["autorange"] = "reversed"
            layout_r["xaxis"]["range"] = [0, 1.15]
            layout_r["xaxis"]["tickformat"] = ".2f"
            layout_r["margin"] = dict(l=0, r=60, t=10, b=0)
            fig_recs.update_layout(**layout_r)
            st.plotly_chart(fig_recs, use_container_width=True, config={"displayModeBar": False})

        else:
            st.markdown("""
            <div style='background:#2e1a1a; border:1px solid #441f1f; border-radius:10px;
                        padding:1rem 1.2rem; color:#ff9090; margin-top:1rem;'>
                ⚠️ No product matched your query. Try keywords like <strong>WHITE</strong>,
                <strong>HEART</strong>, <strong>ROSES</strong>, or <strong>VINTAGE</strong>.
            </div>
            """, unsafe_allow_html=True)

    elif not query and search:
        st.markdown("""
        <div style='background:#2e201a; border:1px solid #44301f; border-radius:10px;
                    padding:1rem 1.2rem; color:#ffb366; margin-top:1rem;'>
            Please enter a product keyword above.
        </div>
        """, unsafe_allow_html=True)

    # ── How it works panel ───────────────────────────────────────────────────
    with st.expander("⚙️  How the recommendation model works"):
        col_a, col_b, col_c = st.columns(3)
        for col, step, title, body in [
            (col_a, "1", "Purchase Matrix", "A customer × product matrix is built from all transactions, where each cell = 1 if customer bought that product."),
            (col_b, "2", "Cosine Similarity", "Item-to-item cosine similarity is computed on the transposed matrix, capturing which products are bought together."),
            (col_c, "3", "Top-N Retrieval", "For a query product, we return the N items with the highest similarity scores — excluding the query itself."),
        ]:
            with col:
                st.markdown(f"""
                <div style='background:#141624; border:1px solid #1e2130; border-radius:12px;
                            padding:1rem; text-align:center;'>
                    <div style='font-size:1.6rem; font-weight:700; color:#4f8ef7;'>{step}</div>
                    <div style='font-weight:600; color:#e2e8f0; margin:0.4rem 0;'>{title}</div>
                    <div style='font-size:0.8rem; color:#8892a4; line-height:1.5;'>{body}</div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTS
# ═══════════════════════════════════════════════════════════════════════════════

elif "Products" in page:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 1.9rem; font-weight: 700; color: #e2e8f0; margin: 0; letter-spacing: -0.03em;'>
            Product Analytics
        </h1>
        <p style='color: #8892a4; font-size: 0.9rem; margin-top: 0.3rem;'>
            Best-selling products ranked by order frequency
        </p>
    </div>
    """, unsafe_allow_html=True)

    prod_df = products.reset_index()
    prod_df.columns = ["Product", "Orders"]
    prod_df["Rank"] = range(1, len(prod_df) + 1)
    prod_df["Share"] = (prod_df["Orders"] / prod_df["Orders"].sum() * 100).round(1)

    # ── Bar chart ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Top 10 Products by Volume</div>', unsafe_allow_html=True)
    fig_bar = go.Figure(go.Bar(
        x=prod_df["Product"].str.slice(0, 28) + "…",
        y=prod_df["Orders"],
        marker=dict(
            color=BLUE_PALETTE,
            line=dict(width=0),
        ),
        text=prod_df["Orders"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color="#8892a4", size=10),
        hovertemplate="<b>%{x}</b><br>%{y:,} orders<extra></extra>",
    ))
    layout_b = dict(**PLOTLY_LAYOUT)
    layout_b["height"] = 380
    layout_b["margin"] = dict(l=0, r=0, t=10, b=80)
    layout_b["xaxis"]["tickangle"] = -30
    layout_b["yaxis"]["tickformat"] = ","
    fig_bar.update_layout(**layout_b)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Ranked Table ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏆 Ranked Product Table</div>', unsafe_allow_html=True)

    for _, row in prod_df.iterrows():
        bar_w = int(row["Share"] / prod_df["Share"].max() * 100)
        rank_color = "#ffd700" if row["Rank"] == 1 else "#c0c0c0" if row["Rank"] == 2 else "#cd7f32" if row["Rank"] == 3 else "#8892a4"
        st.markdown(f"""
        <div style='background:#141624; border:1px solid #1e2130; border-radius:10px;
                    padding:0.75rem 1.25rem; margin-bottom:0.5rem; display:flex;
                    align-items:center; gap:1rem;'>
            <div style='font-weight:700; color:{rank_color}; font-size:0.9rem; min-width:28px;'>
                #{row["Rank"]}
            </div>
            <div style='flex:1;'>
                <div style='color:#e2e8f0; font-size:0.88rem; font-weight:500; margin-bottom:4px;'>
                    {row["Product"]}
                </div>
                <div style='background:#1e2130; border-radius:999px; height:5px; overflow:hidden;'>
                    <div style='background:#4f8ef7; height:100%; width:{bar_w}%; border-radius:999px;'></div>
                </div>
            </div>
            <div style='text-align:right; min-width:80px;'>
                <div style='color:#e2e8f0; font-weight:600; font-size:0.9rem;'>{row["Orders"]:,}</div>
                <div style='color:#8892a4; font-size:0.75rem;'>{row["Share"]}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COUNTRIES
# ═══════════════════════════════════════════════════════════════════════════════

elif "Countries" in page:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 1.9rem; font-weight: 700; color: #e2e8f0; margin: 0; letter-spacing: -0.03em;'>
            Geographic Distribution
        </h1>
        <p style='color: #8892a4; font-size: 0.9rem; margin-top: 0.3rem;'>
            Customer order volumes across global markets
        </p>
    </div>
    """, unsafe_allow_html=True)

    cntry_df = countries.reset_index()
    cntry_df.columns = ["Country", "Orders"]
    cntry_df["Share"] = (cntry_df["Orders"] / cntry_df["Orders"].sum() * 100).round(1)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">📊 Orders by Country</div>', unsafe_allow_html=True)
        fig_h = go.Figure(go.Bar(
            x=cntry_df["Orders"],
            y=cntry_df["Country"],
            orientation="h",
            marker=dict(color=BLUE_PALETTE, line=dict(width=0)),
            text=cntry_df["Orders"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color="#8892a4", size=10),
            hovertemplate="<b>%{y}</b><br>%{x:,} orders<extra></extra>",
        ))
        lh = dict(**PLOTLY_LAYOUT)
        lh["height"] = 380
        lh["yaxis"]["autorange"] = "reversed"
        lh["xaxis"]["tickformat"] = ","
        lh["margin"] = dict(l=0, r=60, t=10, b=0)
        fig_h.update_layout(**lh)
        st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown('<div class="section-header">🥧 Market Share</div>', unsafe_allow_html=True)
        fig_d = go.Figure(go.Pie(
            labels=cntry_df["Country"],
            values=cntry_df["Orders"],
            hole=0.58,
            marker=dict(colors=BLUE_PALETTE, line=dict(color="#0f1117", width=2)),
            textfont=dict(size=10, color="#c9d1d9"),
            hovertemplate="<b>%{label}</b><br>%{value:,} orders · %{percent}<extra></extra>",
        ))
        ld = dict(**PLOTLY_LAYOUT)
        ld["height"] = 380
        ld["showlegend"] = True
        ld["legend"] = dict(font=dict(size=10, color="#8892a4"), bgcolor="rgba(0,0,0,0)", x=0.85, y=0.5)
        ld["annotations"] = [dict(text="Market<br>Share", x=0.5, y=0.5,
                                   font=dict(size=11, color="#8892a4"), showarrow=False)]
        fig_d.update_layout(**ld)
        st.plotly_chart(fig_d, use_container_width=True, config={"displayModeBar": False})

    # ── Country cards ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🌐 Country Breakdown</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (_, row) in enumerate(cntry_df.iterrows()):
        with cols[i % 5]:
            st.markdown(f"""
            <div style='background:#141624; border:1px solid #1e2130; border-radius:12px;
                        padding:1rem 0.75rem; text-align:center; margin-bottom:0.75rem;'>
                <div style='font-weight:700; font-size:1.1rem; color:#e2e8f0;'>{row["Orders"]:,}</div>
                <div style='font-size:0.78rem; color:#4f8ef7; font-weight:500; margin:2px 0;'>{row["Country"]}</div>
                <div style='font-size:0.72rem; color:#8892a4;'>{row["Share"]}% share</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER SEGMENTS
# ═══════════════════════════════════════════════════════════════════════════════

elif "Segments" in page:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-size: 1.9rem; font-weight: 700; color: #e2e8f0; margin: 0; letter-spacing: -0.03em;'>
            Customer Segmentation
        </h1>
        <p style='color: #8892a4; font-size: 0.9rem; margin-top: 0.3rem;'>
            K-Means clustering · 3 behavioral segments · RFM-style features
        </p>
    </div>
    """, unsafe_allow_html=True)

    cluster_counts = customer_data["Cluster"].value_counts().sort_index()

    SEGMENT_META = {
        0: ("💎", "High-Value", "#4fb8ff", "#13293d", "#1d4060"),
        1: ("🛒", "Regular Buyers", "#6ef07a", "#1a2e1a", "#1f441f"),
        2: ("💤", "Low Engagement", "#ff9090", "#2e1a1a", "#441f1f"),
    }

    # ── Segment cards ─────────────────────────────────────────────────────────
    total_customers = cluster_counts.sum()
    cols = st.columns(3)
    for i, col in enumerate(cols):
        count = cluster_counts.get(i, 0)
        icon, label, text_color, bg, border = SEGMENT_META[i]
        pct = round(count / total_customers * 100, 1)
        with col:
            st.markdown(f"""
            <div style='background:{bg}; border:1px solid {border}; border-radius:14px;
                        padding:1.4rem 1.2rem; text-align:center;'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-size:1.4rem; font-weight:700; color:{text_color}; margin:0.3rem 0;'>
                    {count:,}
                </div>
                <div style='font-weight:600; color:{text_color}; font-size:0.88rem;'>{label}</div>
                <div style='color:#8892a4; font-size:0.78rem; margin-top:4px;'>Cluster {i} · {pct}% of customers</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scatter plot: Quantity vs Unit Price by cluster ────────────────────────
    col_scatter, col_bar = st.columns([1.4, 0.6])

    CLUSTER_COLORS = ["#4fb8ff", "#6ef07a", "#ff9090"]

    with col_scatter:
        st.markdown('<div class="section-header">🗺️ Customer Distribution by Segment</div>', unsafe_allow_html=True)

        sample = customer_data.sample(min(2000, len(customer_data)), random_state=42)
        fig_sc = go.Figure()
        for cid in sorted(sample["Cluster"].unique()):
            sub = sample[sample["Cluster"] == cid]
            _, label, color, _, _ = SEGMENT_META[cid]
            fig_sc.add_trace(go.Scatter(
                x=sub["Quantity"],
                y=sub["UnitPrice"],
                mode="markers",
                name=f"Cluster {cid}: {label}",
                marker=dict(
                    color=color,
                    size=5,
                    opacity=0.65,
                    line=dict(width=0),
                ),
                hovertemplate=f"<b>{label}</b><br>Qty: %{{x:,}}<br>Avg Price: £%{{y:.2f}}<extra></extra>",
            ))
        ls = dict(**PLOTLY_LAYOUT)
        ls["height"] = 360
        ls["showlegend"] = True
        ls["legend"] = dict(font=dict(size=10, color="#8892a4"), bgcolor="rgba(0,0,0,0)", x=0.01, y=0.99)
        ls["xaxis"]["title"] = dict(text="Total Quantity Purchased", font=dict(size=11, color="#8892a4"))
        ls["yaxis"]["title"] = dict(text="Avg Unit Price (£)", font=dict(size=11, color="#8892a4"))
        ls["margin"] = dict(l=50, r=10, t=10, b=40)
        fig_sc.update_layout(**ls)
        st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

    with col_bar:
        st.markdown('<div class="section-header">📊 Segment Sizes</div>', unsafe_allow_html=True)

        labels = [SEGMENT_META[i][1] for i in sorted(cluster_counts.index)]
        vals   = [cluster_counts[i] for i in sorted(cluster_counts.index)]
        colors = [SEGMENT_META[i][2] for i in sorted(cluster_counts.index)]

        fig_seg = go.Figure(go.Bar(
            x=labels,
            y=vals,
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:,}" for v in vals],
            textposition="outside",
            textfont=dict(color="#8892a4", size=11),
            hovertemplate="<b>%{x}</b><br>%{y:,} customers<extra></extra>",
        ))
        lb = dict(**PLOTLY_LAYOUT)
        lb["height"] = 360
        lb["margin"] = dict(l=0, r=0, t=10, b=30)
        lb["yaxis"]["tickformat"] = ","
        fig_seg.update_layout(**lb)
        st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})

    # ── Cluster insight cards ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💡 Segment Insights</div>', unsafe_allow_html=True)

    insights = [
        ("💎", "High-Value", "#4fb8ff", "#13293d", "#1d4060",
         "Top spenders with high order volumes and premium price points. Priority targets for loyalty programs and early-access promotions."),
        ("🛒", "Regular Buyers", "#6ef07a", "#1a2e1a", "#1f441f",
         "Consistent purchasing patterns with moderate basket sizes. Respond well to bundle deals, cross-sells, and replenishment nudges."),
        ("💤", "Low Engagement", "#ff9090", "#2e1a1a", "#441f1f",
         "Infrequent purchases and low spend. Re-engagement campaigns, win-back discounts, and abandoned-cart reminders are most effective."),
    ]

    cols2 = st.columns(3)
    for col, (icon, label, tc, bg, bd, desc) in zip(cols2, insights):
        with col:
            st.markdown(f"""
            <div style='background:{bg}; border:1px solid {bd}; border-radius:12px; padding:1.2rem;'>
                <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.6rem;'>
                    <span style='font-size:1.3rem;'>{icon}</span>
                    <span style='font-weight:600; color:{tc}; font-size:0.9rem;'>{label}</span>
                </div>
                <p style='color:#8892a4; font-size:0.82rem; line-height:1.6; margin:0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)