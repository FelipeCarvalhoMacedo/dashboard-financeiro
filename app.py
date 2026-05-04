import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilo custom ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background-color: #0d0f14; }
[data-testid="stAppViewContainer"] { background-color: #0d0f14; }
[data-testid="stHeader"] { background-color: #0d0f14; }

.kpi-card {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 20px;
    text-align: left;
}
.kpi-label { font-size: 11px; color: #7a829a; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 8px; }
.kpi-val   { font-size: 26px; font-weight: 500; color: #f0f2f8; line-height: 1; margin-bottom: 4px; }
.kpi-sub   { font-size: 11px; color: #7a829a; }

.section-title {
    font-size: 10px; font-weight: 600; letter-spacing: .12em;
    text-transform: uppercase; color: #7a829a; margin: 24px 0 12px;
    border-bottom: 1px solid rgba(255,255,255,0.07); padding-bottom: 8px;
}
h1 { font-family: 'DM Serif Display', serif !important; color: #f0f2f8 !important; }
h1 em { color: #4f8ef7 !important; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ── Dados hardcoded (resumo da Planilha1) ──────────────────────────────────────
@st.cache_data
def load_data():
    meses   = ['Jan/25','Fev/25','Mar/25','Abr/25','Mai/25','Jun/25',
                'Jul/25','Ago/25','Set/25','Dez/25','Jan/26','Fev/26','Mar/26','Abr/26']
    receita = [1219176.6,1266955.59,1161315.92,1291845.83,1219985.68,1213612.69,
               1311490.14,1220322.12,1280506.9,1617184.76,1195579.62,1182451.99,1233783.23,1200783.23]
    despesa = [978720.98,1063173.08,932060.48,887393.96,973646.15,948208.93,
               1077979.11,999233.1,1027861.47,1205541.18,964423.27,986375.26,969895.22,964388.47]
    resultado=[240455.62,203782.51,229255.44,404451.87,246339.53,265403.76,
               233511.03,221089.02,252645.43,411643.58,231156.35,196076.73,263888.01,236394.76]
    df = pd.DataFrame({'Mês': meses,'Receita': receita,'Despesa': despesa,'Resultado': resultado})
    df['Margem_%'] = (df['Resultado'] / df['Receita'] * 100).round(1)
    return df

df = load_data()

# ── HEADER ─────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("<h1>Dashboard <em>Financeiro</em></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7a829a;font-size:13px;margin-top:-10px'>Resultados mensais Jan/2025 – Abr/2026 · Lucro Presumido</p>", unsafe_allow_html=True)
with col_h2:
    total_res = df['Resultado'].sum()
    st.markdown(f"""
    <div class='kpi-card' style='border-top:2px solid #2ecf8e;text-align:right;margin-top:8px'>
        <div class='kpi-label'>Resultado Acumulado</div>
        <div class='kpi-val' style='color:#2ecf8e'>R$ {total_res/1e6:.2f}M</div>
        <div class='kpi-sub'>14 meses</div>
    </div>""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Indicadores Gerais</div>", unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, label, val, sub, color):
    col.markdown(f"""
    <div class='kpi-card' style='border-top:2px solid {color}'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-val'>{val}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)

kpi(k1,"Receita média/mês", f"R$ {df['Receita'].mean()/1e6:.2f}M", "base jan/25–abr/26","#4f8ef7")
kpi(k2,"Despesa média/mês",  f"R$ {df['Despesa'].mean()/1e3:.0f}K", "incl. provisão I.R.","#f7604f")
kpi(k3,"Resultado médio/mês",f"R$ {df['Resultado'].mean()/1e3:.0f}K","após I.R. e Juliana","#2ecf8e")
kpi(k4,"Margem líquida média",f"{df['Margem_%'].mean():.1f}%","resultado / receita","#9b6dff")
idx_max = df['Resultado'].idxmax()
kpi(k5,"Melhor mês", df.loc[idx_max,'Mês'], f"resultado R$ {df.loc[idx_max,'Resultado']/1e3:.0f}K","#f5a623")

st.markdown("<br>", unsafe_allow_html=True)

# ── GRÁFICO PRINCIPAL ──────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Receita, Despesa e Resultado mensal</div>", unsafe_allow_html=True)

fig_main = make_subplots(specs=[[{"secondary_y": True}]])
fig_main.add_trace(go.Bar(
    name='Receita', x=df['Mês'], y=df['Receita'],
    marker_color='rgba(79,142,247,0.25)',
    marker_line_color='#4f8ef7', marker_line_width=1.5), secondary_y=False)
fig_main.add_trace(go.Bar(
    name='Despesa', x=df['Mês'], y=df['Despesa'],
    marker_color='rgba(247,96,79,0.2)',
    marker_line_color='#f7604f', marker_line_width=1.5), secondary_y=False)
fig_main.add_trace(go.Scatter(
    name='Resultado', x=df['Mês'], y=df['Resultado'],
    line=dict(color='#2ecf8e', width=2.5),
    fill='tozeroy', fillcolor='rgba(46,207,142,0.06)',
    mode='lines+markers', marker=dict(size=6, color='#2ecf8e')), secondary_y=True)

fig_main.update_layout(
    barmode='group', height=320,
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#7a829a', family='DM Sans', size=11),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(size=11)),
    margin=dict(l=0,r=0,t=10,b=0),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickangle=-40),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
    yaxis2=dict(gridcolor='rgba(255,255,255,0)', tickformat=',.0f', tickprefix='R$'),
)
st.plotly_chart(fig_main, use_container_width=True)

# ── MARGEM + COMPARATIVO ───────────────────────────────────────────────────────
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
        height=240, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7a829a', size=10), margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(tickangle=-40, gridcolor='rgba(255,255,255,0.04)'),
        yaxis=dict(ticksuffix='%', range=[10,40], gridcolor='rgba(255,255,255,0.04)'),
        showlegend=False,
    )
    st.plotly_chart(fig_marg, use_container_width=True)

with col_c:
    st.markdown("<div class='section-title'>Jan–Abr: 2025 vs 2026</div>", unsafe_allow_html=True)
    m4 = ['Jan','Fev','Mar','Abr']
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
        barmode='group', height=240,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7a829a', size=10), margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(font=dict(size=9)),
        xaxis=dict(gridcolor='rgba(255,255,255,0)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
        yaxis2=dict(gridcolor='rgba(255,255,255,0)', tickformat=',.0f', tickprefix='R$'),
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

# ── COMPOSIÇÃO + DISTRIBUIÇÃO ──────────────────────────────────────────────────
col_p, col_d = st.columns(2)

with col_p:
    st.markdown("<div class='section-title'>Composição da Receita (média)</div>", unsafe_allow_html=True)
    labels_pie = ['Locação','Condomínio','TX.Exp.Cond.','Contratos','Financeiro','Outros']
    values_pie = [490000,386000,48500,47000,155000,15000]
    fig_pie = go.Figure(go.Pie(
        labels=labels_pie, values=values_pie, hole=0.58,
        marker_colors=['#4f8ef7','#2ecf8e','#9b6dff','#f5a623','#f7604f','#7a829a'],
        textfont=dict(size=11, color='#f0f2f8'),
    ))
    fig_pie.update_layout(
        height=240, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7a829a', size=11), margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(font=dict(size=10)),
        showlegend=True,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_d:
    st.markdown("<div class='section-title'>Distribuição de Lucro — média estimada</div>", unsafe_allow_html=True)
    socios  = ['João (20%)','Ronaldo (52%)','Marcelo (14%)','Juliana (fixo)']
    pro_lab = [15000, 60000, 0, 8000]
    dist_lc = [40000, 72000, 20000, 0]
    fig_dist = go.Figure()
    fig_dist.add_trace(go.Bar(name='Pró-labore 30%', y=socios, x=pro_lab, orientation='h', marker_color='rgba(79,142,247,0.6)'))
    fig_dist.add_trace(go.Bar(name='Dist. Lucro 70%', y=socios, x=dist_lc, orientation='h', marker_color='rgba(79,142,247,0.25)'))
    fig_dist.update_layout(
        barmode='stack', height=240,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#7a829a', size=11), margin=dict(l=0,r=0,t=0,b=0),
        legend=dict(font=dict(size=10)),
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', tickformat=',.0f', tickprefix='R$'),
        yaxis=dict(gridcolor='rgba(255,255,255,0)'),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# ── TABELA ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Tabela Completa — Mês a Mês</div>", unsafe_allow_html=True)

prov_ir = [137382.23,137382.23,145855.73,148012.97,154662.20,162626.40,
           165686.13,161280.53,168822.96,208629.70,166865.69,159689.26,178013.22,166793.22]
contabil= [841338.75,925790.85,917193.02,784047.51,732731.76,785382.53,
           782836.81,838418.57,858662.33,996881.48,797557.58,826686.00,791882.00,797595.25]

df_tab = df.copy()
df_tab['Despesa Contábil'] = contabil
df_tab['Provisão I.R.']    = prov_ir
df_tab['Margem'] = df_tab['Margem_%'].apply(lambda x: f"{x:.1f}%")

display_df = df_tab[['Mês','Receita','Despesa Contábil','Provisão I.R.','Despesa','Resultado','Margem']].copy()

for col in ['Receita','Despesa Contábil','Provisão I.R.','Despesa','Resultado']:
    display_df[col] = display_df[col].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))

totals = {
    'Mês': 'TOTAL',
    'Receita':           f"R$ {df['Receita'].sum():,.0f}".replace(",","."),
    'Despesa Contábil':  f"R$ {sum(contabil):,.0f}".replace(",","."),
    'Provisão I.R.':     f"R$ {sum(prov_ir):,.0f}".replace(",","."),
    'Despesa':           f"R$ {df['Despesa'].sum():,.0f}".replace(",","."),
    'Resultado':         f"R$ {df['Resultado'].sum():,.0f}".replace(",","."),
    'Margem':            f"{(df['Resultado'].sum()/df['Receita'].sum()*100):.1f}%",
}
display_df = pd.concat([display_df, pd.DataFrame([totals])], ignore_index=True)

st.dataframe(display_df, use_container_width=True, hide_index=True, height=560)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7a829a;font-size:11px'>Dashboard gerado a partir da planilha Resultados2026.xlsx · Mai/2026</p>", unsafe_allow_html=True)
