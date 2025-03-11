import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import os

# Configuração da página
st.set_page_config(
    page_title="🚛 Análise de Transportadoras",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body, .plotly-chart {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Definindo a paleta de cores personalizada
COLORS = {
    'primary': '#1a365d',  # Azul profundo
    'secondary': '#FFD700',  # Dourado queimado
    # **Azuis (tons frios)**
    'blues': ['#1a365d', '#1b2e7b', '#2a4a7f', '#2f3aa6', '#3a5ea1', '#3759ab', '#4b72c4', '#4379c9', '#5c86e7', '#4d9cd1', '#6d9aff'],

    # **Verdes Frios e Petrolatos (contraste com dourado)**
    'cool_greens': ['#0e4025', '#1a5632', '#16a085', '#1abc9c', '#1d7979', '#1ee0cc', '#28cdc4', '#3cebea'],
    
    # **Dourados e Amarelos sofisticados**
    'golds': ['#FFD700','#c69214', '#d4a642', '#e2ba70', '#f0ce9e', '#ffe2cc'],
    'warm_yellows': ['#d9a500', '#e4b008', '#f39c12', '#f1c40f'],  

    # **Laranjas sofisticados**
    'warm_oranges': ['#b45309', '#d95e30', '#e67e22', '#d35400', '#f47c26'],  

    # **Vermelhos intensos e profundos**
    'warm_reds': ['#7D1128', '#8B1E3F', '#a93226', '#c0392b', '#d92e1c'],  

    # **Paleta mista final (ordenada por profundidade)**
    'mixed': ['#1a365d', '#1b2e7b', '#c69214', '#2a4a7f', '#d4a642', '#3a5ea1', '#d9a500', '#4b72c4', 
              '#e2ba70', '#0e4025', '#1a5632', '#d95e30', '#7D1128', '#e67e22', '#8B1E3F']

}

# Função para carregar os dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("supply_chain_data.csv")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Carregar os dados
df = load_data()

def custom_divider():
    st.markdown(
        """
        <div style="height: 4px; background-color: #c69214; margin: 25px 0; border-radius: 2px;"></div>
        """,
        unsafe_allow_html=True
    )


def kpi_card(title, value, color, help_text=None):
    text_color = "#FFFFFF"  # Mantemos branco para legibilidade
    border_color = color  # A borda será da mesma cor do KPI
    bg_opacity = "0.60"  # Define a opacidade do fundo (85%)
    
    def hex_to_rgba(hex_color, alpha=1):
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r},{g},{b},{alpha})"

    bg_rgba = hex_to_rgba(color, bg_opacity)

    st.markdown(
        f"""
        <div style="
            background: {bg_rgba};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-family: 'Inter', 'sans-serif';
            font-weight: bold;
            color: {text_color};            
            border: 5px solid {border_color}; /* Borda sólida */
            box-shadow: 20px 20px 200px rgba(0,0,0,0.3);">
            {title}  
            <br>  
            <span style="font-size: 28px; font-weight: bold;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if help_text:
        st.caption(f"ℹ️ {help_text}")

if df is not None:
    # Renomear colunas para facilitar leitura
    df.rename(columns={
        "Shipping carriers": "Transportadora",
        "Production volumes": "Volume_Pedidos",
        "Shipping costs": "Custos_Envio",
        "Transportation modes": "Modos_Transporte",
        "Costs": "Custos_Totais",
        "Location": "Localizacao",
        "Revenue generated": "Receita_Gerada"
    }, inplace=True)

    # Sidebar com filtros
    st.sidebar.title("🔍 Filtros")

    # Filtros
    selected_transport = st.sidebar.selectbox(
        "🚛 Modo de Transporte",
        ["Todas"] + list(df["Modos_Transporte"].unique()),
        help="Selecione o modo de transporte para filtrar os dados"
    )

    selected_carrier = st.sidebar.selectbox(
        "🏢 Transportadora",
        ["Todas"] + list(df["Transportadora"].unique()),
        help="Selecione a transportadora para filtrar os dados"
    )

    # Aplicar os filtros no DataFrame
    df_filtered = df.copy()

    if selected_transport != "Todas":
        df_filtered = df_filtered[df_filtered["Modos_Transporte"] == selected_transport]
    if selected_carrier != "Todas":
        df_filtered = df_filtered[df_filtered["Transportadora"] == selected_carrier]

    # Header principal
    st.markdown("""
        <div style='
            background-color: #1a365d;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        '>
            <h1 style='
                color: #FFFFFF;
                font-size: 36px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>🚛 Análise de Transportadoras</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 5px;
        '>
            <h3 style='
                #color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
                font-family: Inter, sans-serif;
            '>Dashboard interativo para análise de performance logística</h3>
        </div>
        """, unsafe_allow_html=True)

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        volume_total = df_filtered["Volume_Pedidos"].sum()
        kpi_card(
            "📦 Volume Total de Pedidos",
            f"{volume_total:,}", COLORS["golds"][1],
            "Total de pedidos processados"
        )

    with col2:
        # Calculando o custo total de envio (soma de todos os custos)
        custo_total = df_filtered["Custos_Envio"].sum()
        kpi_card("🚛 Custo Logístico Total", f"R$ {df_filtered["Custos_Totais"].sum():,.2f}", COLORS["warm_yellows"][0],"Custo Total do Envio de Pedidos")

    with col3:
        # Calculando o custo médio por pedido (custo total / volume total)
        df_filtered["Receita_Gerada"] = df_filtered["Receita_Gerada"].fillna(0)  # Evita erro com NaN
        percentual_custo_logistico = (custo_total / df_filtered["Receita_Gerada"].sum()) * 100 if df_filtered["Receita_Gerada"].sum() > 0 else 0

        kpi_card(
            "📉 % Logístico sobre Receita",
            f"{percentual_custo_logistico:.2f}%",COLORS["cool_greens"][4],
            "Percentual do custo de envio em relação à receita total"
        )

    with col4:
        custo_medio_transportadora = df_filtered.groupby("Transportadora")["Custos_Envio"].mean().mean()

        kpi_card(
            "📊 Custo Médio de Envio",
            f"R$ {custo_medio_transportadora:,.2f}", COLORS["blues"][1],
            "Média dos custos de envio por transportadora"
        )

    custom_divider()
    # Volume de Pedidos por Transportadora
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(to right, #c69214, #d4a642);
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>📦 Volume de Pedidos por Transportadora</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='
            color: white;
            background: linear-gradient(to right, #c69214, #d4a642);
            font-size: 20px;
            font-weight: 600;
            font-family: Inter, sans-serif;
            text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
            text-align: center;
        '>Volume de Pedidos por Transportadora</h3>
        """, unsafe_allow_html=True)

    # Gráfico de barras com volume de pedidos
    fig_volume = px.bar(
        df_filtered.groupby("Transportadora")["Volume_Pedidos"].sum().reset_index(),
        x="Transportadora",
        y="Volume_Pedidos",
        title=" ",
        color="Transportadora",
        color_discrete_sequence=COLORS['golds']
    )
    fig_volume.update_traces(
    texttemplate="%{y:}",
    textposition="outside",
    outsidetextfont=dict(color=COLORS["warm_yellows"][0]) 

)
    fig_volume.update_layout(
        height=670,
        margin=dict(t=40,b=40,l=20,r=20),
        title_font_color=COLORS['warm_yellows'][0],
        font_color=COLORS['warm_yellows'][0],
        font=dict(size=20,family="Inter, sans-serif"),
        legend_font=dict(size=18,family="Inter, sans-serif"),
        xaxis=dict(
                title="Transportadora",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo X
            ),
        yaxis=dict(
                title="Volume de Pedidos",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo Y
            ),
    )
    st.plotly_chart(fig_volume, use_container_width=True)
    st.markdown("""
    <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
        🔍 Transportadoras com maior volume têm poder de negociação. 
        Avalie o custo-benefício de contratos exclusivos.
    </div>
    """, unsafe_allow_html=True)

    custom_divider()
    # Custos de Envio por Transportadora
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(to right, #c0392b, #d92e1c);
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>💰 Custos de Envio por Transportadora</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='
            color: white;
            background: linear-gradient(to right, #c0392b, #d92e1c);    
            font-size: 20px;
            font-weight: 600;
            font-family: Inter, sans-serif;
            text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
            text-align: center;
        '>Variação dos Custos de Envio por Transportadora</h3>
        """, unsafe_allow_html=True)
        # Box plot de custos

    fig_custos = go.Figure()
    for transportadora in df_filtered["Transportadora"].unique():
        dados_transp = df_filtered[df_filtered["Transportadora"] == transportadora]
        fig_custos.add_trace(go.Box(
            y=dados_transp["Custos_Envio"],
            name=transportadora,
            marker_color=COLORS["warm_yellows"][1],
            #boxmean='sd'
        ))

        fig_custos.update_traces(
            marker=dict(opacity=0.8),  # Reduz impacto de outliers
            line=dict(width=1.5)  # Melhora visual da borda do boxplot
        )
    fig_custos.update_layout(    
        
        title=" ",
        height=670,
        margin=dict(t=40,b=40,l=20,r=20),
        title_font_color=COLORS['warm_yellows'][0],
        font_color=COLORS['warm_yellows'][0],
        font=dict(family="Inter, sans-serif",size=20),
        legend_font=dict(family="Inter, sans-serif",size=18),

        yaxis=dict(
                title="Custos de Envio (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo Y
            ),
    )
    st.plotly_chart(fig_custos, use_container_width=True)
    st.markdown("""
    <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
        🔍 Custos elevados podem indicar falhas operacionais ou tarifas desfavoráveis. 
        Monitore picos anormais e avalie ajustes.
    </div>
    """, unsafe_allow_html=True)

    custom_divider()
    # Custos por Modalidade de Transporte
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(to right, #1a5632, #16a085);
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>🚚 Custos por Modalidade de Transporte</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='
            color: white;
            background: linear-gradient(to right, #1a5632, #16a085);
            font-size: 20px;
            font-weight: 600;
            font-family: Inter, sans-serif;
            text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
            text-align: center;
        '>Custos Médios Totais de Envio por Modalidade de Transporte</h3>
        """, unsafe_allow_html=True)

    
    
    df_filtered["Custos_Totais"] = df_filtered["Custos_Totais"].fillna(0)
    custos_modalidade = df_filtered.groupby("Modos_Transporte")["Custos_Totais"].mean().reset_index()

    # Gráfico de barras para custos por modalidade
    fig_modalidade = px.bar(
        df_filtered.groupby("Modos_Transporte")["Custos_Totais"].mean().reset_index(),
        x="Modos_Transporte",
        y="Custos_Totais",
        title=" ",
        color="Modos_Transporte",
        color_discrete_sequence=COLORS["cool_greens"],
        #text_auto=True
    )
    fig_modalidade.update_traces(
        #text=[f"R$ {x:,.0f}" for x in custos_modalidade["Custos_Totais"]],
        texttemplate="R$ %{y:,.2f}",
        textposition="outside",
        outsidetextfont=dict(color=COLORS["warm_yellows"])  # Garante visibilidade dos números

    )
    
    fig_modalidade.update_layout(
        height=670,
        margin=dict(t=40,b=40,l=20,r=20),
        title_font_color=COLORS['warm_yellows'][0],
        font_color=COLORS['warm_yellows'][0],
        font=dict(family="Inter, sans-serif",size=23),
        legend_font=dict(family="Inter, sans-serif",size=18),
        xaxis=dict(
                title="Modalidade de Transporte",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo X
            ),
        yaxis=dict(
                title="Custo Médio Total de Envio (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo Y
            ),
    )
    st.plotly_chart(fig_modalidade, use_container_width=True)
    st.markdown("""
    <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
        🔍 Cada modalidade tem um equilíbrio entre custo e velocidade. 
        Analise o impacto da escolha na experiência do cliente.
    </div>
    """, unsafe_allow_html=True)

    custom_divider()
    # Custos por Cidade
    # 🌆 Análise de Custos por Cidade
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(to right, #2a4a7f, #4b72c4);
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>🌆 Análise de Custos por Cidade</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='
            color: white;
            background: linear-gradient(to right, #2a4a7f, #4b72c4);
            font-size: 20px;
            font-weight: 600;
            font-family: Inter, sans-serif;
            text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
            text-align: center;
        '>Custo Total de Envio por Cidade</h3>
        """, unsafe_allow_html=True)
        
    # Calculando os custos totais por cidade ANTES de passar para o gráfico
    #df_filtered.groupby("Localizacao")["Custos_Envio"].sum().sort_values(ascending=True).reset_index(),
    custos_cidade = df_filtered.groupby("Localizacao")["Custos_Envio"].sum().reset_index()

    # Gráfico de barras horizontal para custos por cidade
    fig_cidade = px.bar(
        df_filtered.groupby("Localizacao")["Custos_Envio"].sum().sort_values(ascending=True).reset_index(),
        x="Custos_Envio",
        y="Localizacao",
        title=" ",
        color_discrete_sequence=[COLORS['blues'][5]],
        orientation="h"
    )
    fig_cidade.update_traces(
        #text=[f"R$ {x:,.2f}" for x in custos_cidade["Custos_Envio"]],
        texttemplate="R$ %{x:,.2f}",
        textposition="inside",
        insidetextfont=dict(color=COLORS['secondary'])  # Melhor visibilidade
    )
    fig_cidade.update_layout(
        height=670,
        margin=dict(t=40,b=40,l=20,r=20),
        title_font_color=COLORS['warm_yellows'][0],
        font_color=COLORS['secondary'],
        font=dict(family="Inter, sans-serif",size=20),
        xaxis=dict(
                title="Custo Total de Envio (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo X
            ),
        yaxis=dict(
                title="Cidade",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=16)  # Aumentando fonte dos valores do eixo Y
            ),
    )
    st.plotly_chart(fig_cidade, use_container_width=True)
    st.markdown("""
        <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
            🔍 Regiões de alto custo podem indicar gargalos logísticos. 
            Avalie transportadoras locais e a viabilidade de novos hubs.
        </div>
        """, unsafe_allow_html=True)
    
    custom_divider()
    # Tabela detalhada
    # 📋 Dados Detalhados
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(to right, #7D1128, #c0392b);
                text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            '>📋 Dados Detalhados</h2>
        </div>
        """, unsafe_allow_html=True)

    # Selecionar e formatar colunas para exibição
    colunas_exibir = [
        "Transportadora",
        "Modos_Transporte",
        "Localizacao",
        "Volume_Pedidos",
        "Custos_Envio",
        "Custos_Totais"
    ]

    st.dataframe(
        df_filtered[colunas_exibir].style.format({
            "Custos_Envio": "R$ {:,.2f}",
            "Custos_Totais": "R$ {:,.2f}",
            "Volume_Pedidos": "{:,}"
        }),
        use_container_width=True
    )
    # Criar buffer CSV
    csv_buffer = io.StringIO()
    df_filtered[colunas_exibir].to_csv(csv_buffer, index=False, sep=';', decimal=',')

    # Criar buffer Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_filtered[colunas_exibir].to_excel(writer, index=False, sheet_name="Dados_Transportadoras")
        writer.close()

    # Criar botões de download
    col_csv, col_xlsx = st.columns(2)

    with col_csv:
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_buffer.getvalue(),
            file_name="dados_transportadoras.csv",
            mime="text/csv"
        )

    with col_xlsx:
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_buffer.getvalue(),
            file_name="dados_transportadoras.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.markdown("<h3 style='color:#7D1128;'>📝 Minhas Anotações", unsafe_allow_html=True)

    # Criar área de texto para anotações
    nota = st.text_area("Registre suas observações aqui:")

    # Criar buffer de texto para download
    buffer = io.StringIO()
    buffer.write(nota)

    # Botão de download
    st.download_button(
    label="📥 Baixar Anotações",
    data=buffer.getvalue(),
    file_name="minhas_anotacoes.txt",
    mime="text/plain"
    )

    # Footer
    custom_divider()
    st.markdown(
        f"""
        <div style='text-align: center; color: {COLORS['secondary']};'>
            Dashboard atualizado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.error("Não foi possível carregar os dados. Por favor, verifique o arquivo de dados.")