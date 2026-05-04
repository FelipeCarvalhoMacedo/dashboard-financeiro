import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilo ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background-color: #0d0f14; }
[data-testid="stAppViewContainer"] { background-color: #0d0f14; }
[data-testid="stHeader"] { background-color: #0d0f14; }

/* Remove padding interno q causava scrollbar */
[data-testid="stPlotlyChart"] > div { overflow: hidden !important; }
[data-testid="stPlotlyChart"] {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    overflow: hidden;
}

/* KPI cards */
.kpi-card {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 20px;
}
.kpi-label { font-size: 10px; color: #7a829a; text-transform: uppercase; letter-spacing: .07em; margin-bottom: 8px; }
.kpi-val   { font-size: 24px; font-weight: 500; color: #f0f2f8; line-height: 1; margin-bottom: 4px; }
.kpi-sub   { font-size: 11px; color: #7a829a; }

/* Filter card */
.filter-card {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px 20px 8px;
    margin-bottom: 8px;
}
.filter-label {
    font-size: 10px; font-weight: 600; letter-spacing: .1em;
    text-transform: uppercase; color: #7a829a; margin-bottom: 6px;
}

/* Multiselect styling */
[data-testid="stMultiSelect"] > div > div {
    background: #242838 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #f0f2f8 !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(79,142,247,0.2) !important;
    border: 1px solid rgba(79,142,247,0.4) !important;
    border-radius: 6px !important;
    color: #4f8ef7 !important;
}

.section-title {
    font-size: 10px; font-weight: 600; letter-spacing: .12em;
    text-transform: uppercase; color: #7a829a; margin: 20px 0 10px;
    border-bottom: 1px solid rgba(255,255,255,0.07); padding-bottom: 8px;
}
h1 { font-family: 'DM Serif Display', serif !important; color: #f0f2f8 !important; }
h1 em { color: #4f8ef7 !important; font-style: italic; }

/* Button reset */
[data-testid="stButton"] button {
    background: rgba(247,96,79,0.12) !important;
    border: 1px solid rgba(247,96,79,0.3) !important;
    border-radius: 8px !important;
    color: #f7604f !important;
    font-size: 12px !important;
    padding: 6px 16px !important;
    width: 100%;
}
[data-testid="stButton"] button:hover {
    background: rgba(247,96,79,0.22) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = {
        'Mês':      ['Jan/25','Fev/25','Mar/25','Abr/25','Mai/25','Jun/25',
                     'Jul/25','Ago/25','Set/25','Dez/25','Jan/26','Fev/26','Mar/26','Abr/26'],
        'Ano':      [2025,2025,2025,2025,2025,2025,2025,2025,2025,2025,2026,2026,2026,2026],
        'MêsNum':   [1,2,3,4,5,6,7,8,9,12,1,2,3,4],
        'Receita':  [1219176.6,1266955.59,1161315.92,1291845.83,1219985.68,1213612.69,
                     1311490.14,1220322.12,1280506.9,1617184.76,1195579.62,1182451.99,1233783.23,1200783.23],
        'Despesa':  [978720.98,1063173.08,932060.48,887393.96,973646.15,948208.93,
                     1077979.11,999233.1,1027861.47,1205541.18,964423.27,986375.26,969895.22,964388.47],
        'Resultado':[240455.62,203782.51,229255.44,404451.87,246339.53,265403.76,
                     233511.03,221089.02,252645.43,411643.58,231156.35,196076.73,263888.01,236394.76],
        'Prov_IR':  [137382.23,137382.23,145855.73,148012.97,154662.20,162626.40,
                     165686.13,161280.53,168822.96,208629.70,166865.69,159689.26,178013.22,166793.22],
        'Contabil': [841338.75,925790.85,917193.02,784047.51,732731.76,785382.53,
                     782836.81,838418.57,858662.33,996881.48,797557.58,826686.00,791882.00,797595.25],
    }
    df = pd.DataFrame(data)
    df['Margem_%'] = (df['Resultado'] / df['Receita'] * 100).round(1)
    return df

df_full = load_data()

MESES_LABEL = {1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',
               6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',
               11:'Novembro',12:'Dezembro'}
meses_disponiveis = sorted(df_full['MêsNum'].unique())
anos_disponiveis  = sorted(df_full['Ano'].unique())

# ── HEADER ─────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h1>Dashboard <em>Financeiro</em></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7a829a;font-size:13px;margin-top:-10px'>Administradora de Imóveis · Jan/2025 – Abr/2026 · Lucro Presumido</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""
    <div class='kpi-card' style='border-top:2px solid #2ecf8e;text-align:right;margin-top:8px'>
        <div class='kpi-label'>Resultado Acumulado Total</div>
        <div class='kpi-val' style='color:#2ecf8e'>R$ {df_full['Resultado'].sum()/1e6:.2f}M</div>
        <div class='kpi-sub'>14 meses · todos os períodos</div>
    </div>""", unsafe_allow_html=True)

# ── FILTROS ────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>🎛️ Filtros</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='filter-card'>", unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([2, 3, 1])

    with fc1:
        st.markdown("<div class='filter-label'>Ano</div>", unsafe_allow_html=True)
        anos_sel = st.multiselect(
            label="ano", options=anos_disponiveis,
            default=anos_disponiveis,
            format_func=lambda x: str(x),
            label_visibility="collapsed"
        )

    with fc2:
        st.markdown("<div class='filter-label'>Mês</div>", unsafe_allow_html=True)
        meses_sel = st.multiselect(
            label="mes", options=meses_disponiveis,
            default=meses_disponiveis,
            format_func=lambda x: MESES_LABEL[x],
            label_visibility="collapsed"
        )

    with fc3:
        st.markdown("<div class='filter-label'>Limpar</div>", unsafe_allow_html=True)
        if st.button("↺ Resetar"):
            anos_sel  = anos_disponiveis
            meses_sel = meses_disponiveis
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Aplicar filtro
if not anos_sel:  anos_sel  = anos_disponiveis
if not meses_sel: meses_sel = meses_disponiveis

df = df_full[
    df_full['Ano'].isin(anos_sel) &
    df_full['MêsNum'].isin(meses_sel)
].copy()

n_meses = len(df)

# ── KPIs ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Indicadores do Período Selecionado</div>", unsafe_allow_html=True)

def kpi(col, label, val, sub, color):
    col.markdown(f"""
    <div class='kpi-card' style='border-top:2px solid {color}'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-val'>{val}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
if n_meses > 0:
    idx_max = df['Resultado'].idxmax()
    kpi(k1,"Receita média/mês",    f"R$ {df['Receita'].mean()/1e6:.2f}M",   f"{n_meses} mês(es)","#4f8ef7")
    kpi(k2,"Despesa média/mês",    f"R$ {df['Despesa'].mean()/1e3:.0f}K",   "incl. provisão I.R.","#f7604f")
    kpi(k3,"Resultado médio/mês",  f"R$ {df['Resultado'].mean()/1e3:.0f}K", "após I.R. e Juliana","#2ecf8e")
    kpi(k4,"Margem líquida média", f"{df['Margem_%'].mean():.1f}%",         "resultado / receita","#9b6dff")
    kpi(k5,"Melhor mês",           df.loc[idx_max,'Mês'],                   f"R$ {df.loc[idx_max,'Resultado']/1e3:.0f}K","#f5a623")
else:
    st.warning("Nenhum período selecionado. Ajuste os filtros acima.")

st.markdown("<br>", unsafe_allow_html=True)

# ── GRÁFICO PRINCIPAL ──────────────────────────────────────────────────────────
LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='#1a1e2a',
    font=dict(color='#7a829a', family='DM Sans', size=11),
    margin=dict(l=12, r=12, t=36, b=12),
)

if n_meses > 0:
    st.markdown("<div class='section-title'>Receita, Despesa e Resultado mensal</div>", unsafe_allow_html=True)
    fig_main = make_subplots(specs=[[{"secondary_y": True}]])
    fig_main.add_trace(go.Bar(
        name='Receita', x=df['Mês'], y=df['Receita'],
        marker_color='rgba(79,142,247,0.25)', marker_line_color='#4f8ef7', marker_line_width=1.5
    ), secondary_y=False)
    fig_main.add_trace(go.Bar(
        name='Despesa', x=df['Mês'], y=df['Despesa'],
        marker_color='rgba(247,96,79,0.2)', marker_line_color='#f7604f', marker_line_width=1.5
    ), secondary_y=False)
    fig_main.add_trace(go.Scatter(
        name='Resultado', x=df['Mês'], y=df['Resultado'],
        line=dict(color='#2ecf8e', width=2.5),
        fill='tozeroy', fillcolor='rgba(46,207,142,0.06)',
        mode='lines+markers', marker=dict(size=6, color='#2ecf8e')
    ), secondary_y=True)
    fig_main.update_layout(
        barmode='group', height=340,
        legend=dict(orientation='h', yanchor='bottom', y=1.01, font=dict(size=11)),
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickangle=-40),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
        yaxis2=dict(gridcolor='rgba(0,0,0,0)', tickformat=',.0f', tickprefix='R$'),
        **LAYOUT
    )
    st.plotly_chart(fig_main, use_container_width=True)

    # ── MARGEM + COMPARATIVO ───────────────────────────────────────────────────
    col_m, col_c = st.columns(2)
    with col_m:
        st.markdown("<div class='section-title'>Margem Líquida (%)</div>", unsafe_allow_html=True)
        fig_marg = go.Figure()
        fig_marg.add_trace(go.Scatter(
            x=df['Mês'], y=df['Margem_%'],
            fill='tozeroy', fillcolor='rgba(155,109,255,0.1)',
            line=dict(color='#9b6dff', width=2),
            mode='lines+markers', marker=dict(size=6, color='#9b6dff'),
        ))
        fig_marg.update_layout(
            height=280, showlegend=False,
            xaxis=dict(tickangle=-40, gridcolor='rgba(255,255,255,0.04)'),
            yaxis=dict(ticksuffix='%', gridcolor='rgba(255,255,255,0.04)'),
            **LAYOUT
        )
        st.plotly_chart(fig_marg, use_container_width=True)

    with col_c:
        st.markdown("<div class='section-title'>Jan–Abr: 2025 vs 2026</div>", unsafe_allow_html=True)
        m4   = ['Jan','Fev','Mar','Abr']
        rec25=[1219176.6,1266955.59,1161315.92,1291845.83]
        rec26=[1195579.62,1182451.99,1233783.23,1200783.23]
        res25=[240455.62,203782.51,229255.44,404451.87]
        res26=[231156.35,196076.73,263888.01,236394.76]
        fig_cmp = make_subplots(specs=[[{"secondary_y": True}]])
        fig_cmp.add_trace(go.Bar(name='Receita 2025',x=m4,y=rec25,marker_color='rgba(79,142,247,0.3)',marker_line_color='rgba(79,142,247,0.5)',marker_line_width=1), secondary_y=False)
        fig_cmp.add_trace(go.Bar(name='Receita 2026',x=m4,y=rec26,marker_color='rgba(79,142,247,0.7)',marker_line_color='#4f8ef7',marker_line_width=1), secondary_y=False)
        fig_cmp.add_trace(go.Scatter(name='Res. 2025',x=m4,y=res25,mode='lines+markers',line=dict(color='#2ecf8e',width=2),marker=dict(size=7)), secondary_y=True)
        fig_cmp.add_trace(go.Scatter(name='Res. 2026',x=m4,y=res26,mode='lines+markers',line=dict(color='#f5a623',width=2),marker=dict(size=7,symbol='triangle-up')), secondary_y=True)
        fig_cmp.update_layout(
            barmode='group', height=280,
            legend=dict(font=dict(size=9), orientation='h', yanchor='bottom', y=1.01),
            xaxis=dict(gridcolor='rgba(255,255,255,0)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
            yaxis2=dict(gridcolor='rgba(0,0,0,0)', tickformat=',.0f', tickprefix='R$'),
            **LAYOUT
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

    # ── COMPOSIÇÃO + DISTRIBUIÇÃO ──────────────────────────────────────────────
    col_p, col_d = st.columns(2)
    with col_p:
        st.markdown("<div class='section-title'>Composição da Receita (média)</div>", unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Locação','Condomínio','TX.Exp.Cond.','Contratos','Financeiro','Outros'],
            values=[490000,386000,48500,47000,155000,15000], hole=0.58,
            marker_colors=['#4f8ef7','#2ecf8e','#9b6dff','#f5a623','#f7604f','#7a829a'],
            textfont=dict(size=11, color='#f0f2f8'),
        ))
        fig_pie.update_layout(
            height=280, showlegend=True,
            legend=dict(font=dict(size=10)),
            **LAYOUT
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_d:
        st.markdown("<div class='section-title'>Distribuição de Lucro — média estimada</div>", unsafe_allow_html=True)
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Bar(name='Pró-labore 30%', y=['João (20%)','Ronaldo (52%)','Marcelo (14%)','Juliana (fixo)'], x=[15000,60000,0,8000], orientation='h', marker_color='rgba(79,142,247,0.6)'))
        fig_dist.add_trace(go.Bar(name='Dist. Lucro 70%', y=['João (20%)','Ronaldo (52%)','Marcelo (14%)','Juliana (fixo)'], x=[40000,72000,20000,0], orientation='h', marker_color='rgba(79,142,247,0.25)'))
        fig_dist.update_layout(
            barmode='stack', height=280,
            legend=dict(font=dict(size=10), orientation='h', yanchor='bottom', y=1.01),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
            yaxis=dict(gridcolor='rgba(0,0,0,0)'),
            **LAYOUT
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    # ── TABELA ─────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>Tabela — Período Selecionado</div>", unsafe_allow_html=True)
    df_tab = df.copy()
    df_tab['Margem'] = df_tab['Margem_%'].apply(lambda x: f"{x:.1f}%")
    display_df = df_tab[['Mês','Receita','Contabil','Prov_IR','Despesa','Resultado','Margem']].copy()
    display_df.columns = ['Mês','Receita','Desp. Contábil','Provisão I.R.','Despesa Total','Resultado','Margem']
    for c in ['Receita','Desp. Contábil','Provisão I.R.','Despesa Total','Resultado']:
        display_df[c] = display_df[c].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))

    totals = {
        'Mês':           'TOTAL',
        'Receita':       f"R$ {df['Receita'].sum():,.0f}".replace(",","."),
        'Desp. Contábil':f"R$ {df['Contabil'].sum():,.0f}".replace(",","."),
        'Provisão I.R.': f"R$ {df['Prov_IR'].sum():,.0f}".replace(",","."),
        'Despesa Total': f"R$ {df['Despesa'].sum():,.0f}".replace(",","."),
        'Resultado':     f"R$ {df['Resultado'].sum():,.0f}".replace(",","."),
        'Margem':        f"{(df['Resultado'].sum()/df['Receita'].sum()*100):.1f}%",
    }
    display_df = pd.concat([display_df, pd.DataFrame([totals])], ignore_index=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=min(560, (n_meses+2)*38+40))

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#3a4258;font-size:11px'>Dashboard Financeiro · Resultados2026.xlsx · Mai/2026</p>", unsafe_allow_html=True)
