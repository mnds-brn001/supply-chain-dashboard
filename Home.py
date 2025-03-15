import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import io
import os

# Configuração da página
st.set_page_config(
    page_title="🔍 Supply Chain Analysis",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* Organização dos KPIs em telas menores */
        @media (max-width: 768px) {
            div[data-testid="column"] {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            div[data-testid="column"] > div {
                width: 48% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)    
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body, .plotly-chart {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
    <style>
        div[data-testid="stMarkdownContainer"]:hover {
            transform: scale(1.02);
            transition: all 0.3s ease-in-out;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .stMarkdownContainer {
            word-wrap: break-word;
        }
    </style>
    """, unsafe_allow_html=True)

# Definindo a paleta de cores personalizada
COLORS = {
    'primary': '#1a365d',  # Azul profundo
    'secondary': '#FFD700',  # Dourado queimado
    'tertiary': '#4A4A4A', #7D1128  # Cinza Chumbo

    
    # Azuis (tons frios)
    'blues': ['#1a365d', '#2a4a7f', '#3a5ea1', '#4b72c4', '#5c86e7', '#6d9aff'],
    'cool_blues': ['#2f3aa6', '#1b2e7b', '#3759ab', '#4379c9', '#4d9cd1'],
    
    # Dourados e Amarelos sofisticados
    'golds': ['#c69214', '#d4a642', '#e2ba70', '#f0ce9e', '#ffe2cc'],
    'warm_yellows': ['#f39c12', '#f1c40f', '#e4b008', '#d9a500'],  

    # Verdes Frios e Petrolatos (contraste com dourado)
    'cool_greens': ['#1a5632', '#0e4025', '#1abc9c', '#16a085', '#28cdc4', '#3cebea', '#1ee0cc', '#1d7979'],

    # Tons quentes para equilibrar os azuis
    'warm_oranges': ['#d95e30', '#e67e22', '#b45309', '#d35400'],  
    'warm_reds': ['#7D1128', '#c0392b', '#a93226', '#8B1E3F'],  

    # Paleta mista final
    'mixed': ['#1a365d', '#1b2e7b', '#c69214', '#2a4a7f', '#d4a642', '#3a5ea1', '#d9a500', '#4b72c4', 
              '#e2ba70', '#0e4025', '#1a5632', '#d95e30', '#7D1128', '#e67e22', '#8B1E3F']
}

def kpi_card(title, value, color1,color2, help_text=None):
    
    text_color = "#FFFFFF"  # Mantemos branco para legibilidade
    border_color = color1  # A borda será da mesma cor do KPI
    bg_opacity = "0.60"  # Define a opacidade do fundo (85%)
    
    def hex_to_rgba(hex_color, alpha=1):
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r},{g},{b},{alpha})"

    bg_rgba = hex_to_rgba(color1, bg_opacity)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color1}, {color2});
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-family: 'Inter', sans-serif;
            font-weight: bold;
            color: {text_color};            
            border: 4px solid {border_color}; 
            box-shadow: 4px 4px 10px rgba(0,0,0,0.3);">
            {title}  
            <br>  
            <span style="font-size: 28px; font-weight: bold;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if help_text:
        st.markdown(
        f"""
        <p style="font-size: 16px; color: gray; text-align: center; font-style: italic;">
            ℹ️ {help_text}
        </p>
        """,
        unsafe_allow_html=True
    )

# Função para carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("supply_chain_data.csv")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Carregando dados
df = load_data()

# Função custom_divider com espessura maior
def custom_divider():
    st.markdown(
        """
        <div style="height: 4px; background-color: #c69214; margin: 25px 0; border-radius: 2px;"></div>
        """,
        unsafe_allow_html=True
    )


# <hr style="border: 1x solid #c69214; border-radius: 3px; margin: 20px 0;">
# <hr style="border: 1px solid red; border-radius: 3px; margin: 20px 0;">

if df is not None:
    # Renomeando colunas
    df.rename(columns={
        "Shipping costs": "Custos_Envio",
        "Manufacturing costs": "Custos_Manufatura",
        "Costs": "Custos_Totais",
        "Transportation modes": "Modos_Transporte",
        "Production volumes": "Volume_Pedidos",
        "Shipping carriers": "Transportadoras",
        "Revenue generated": "Receita_Gerada",
        "Product type": "Categoria",
        "SKU": "Produto_SKU",
        "Location": "Localizacao",
        "Number of products sold": "Quantidade_Vendida",
        "Customer demographics": "Demografia_Cliente"
    }, inplace=True)
    # Dicionários de tradução
    produto_traducao = {
        "skincare": "Linha para Peles",
        "haircare": "Linha para Cabelos",
        "cosmetics": "Linha para Cosméticos"
    }

    tipo_cliente_traducao = {
        "Female": "Feminino",
        "Male": "Masculino",
        "Non-Binary": "Não-Binário",
        "Unknown": "Desconhecido"
    }

    transporte_traducao = {
        "Road": "Rodoviário",
        "Air": "Aéreo",
        "Sea": "Marítimo",
        "Rail": "Ferroviário"
    }

    transportadora_traducao = {
        "Carrier A": "Transportadora A",
        "Carrier B": "Transportadora B",
        "Carrier C": "Transportadora C"
}


    # Aplicando traduções
    if df is not None:
        df["Categoria"] = df["Categoria"].map(produto_traducao).fillna(df["Categoria"])
        df["Demografia_Cliente"] = df["Demografia_Cliente"].map(tipo_cliente_traducao).fillna(df["Demografia_Cliente"])
        df["Modos_Transporte"] = df["Modos_Transporte"].map(transporte_traducao).fillna(df["Modos_Transporte"])
        df["Transportadoras"] = df["Transportadoras"].map(transportadora_traducao).fillna(df["Transportadoras"])

    # Sidebar - Filtros
    st.sidebar.title("🔍 Filtros")
    selected_transport = st.sidebar.selectbox("🚛 Modo de Transporte", ["Todos"] + list(df["Modos_Transporte"].unique()))
    selected_carrier = st.sidebar.selectbox("🏢 Transportadora", ["Todas"] + list(df["Transportadoras"].unique()))
    selected_category = st.sidebar.multiselect("📦 Categorias de Produto", options=list(df["Categoria"].unique()), default=list(df["Categoria"].unique()))

    # Aplicando filtros
    df_filtered = df.copy()
    if selected_transport != "Todos":
        df_filtered = df_filtered[df_filtered["Modos_Transporte"] == selected_transport]
    if selected_carrier != "Todas":
        df_filtered = df_filtered[df_filtered["Transportadoras"] == selected_carrier]
    if selected_category:
        df_filtered = df_filtered[df_filtered["Categoria"].isin(selected_category)]

    # Calculando campos adicionais
    df_filtered["Receita_Gerada"] = pd.to_numeric(df_filtered["Receita_Gerada"], errors="coerce").fillna(0)
    df_filtered['Lucro'] = df_filtered['Receita_Gerada'] - df_filtered['Custos_Totais']
    df_filtered['Margem'] = (df_filtered['Lucro'] / df_filtered['Receita_Gerada']) * 100
    

    st.markdown(f"""
    <div style='
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background: linear-gradient(135deg, {COLORS["cool_blues"][1]}, {COLORS["golds"][0]});
        box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
    '>
        <h1 style='
            color: #FFFFFF;
            font-size: 36px;
            font-weight: bold;
            font-family: Inter, sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        '>📊 Supply Chain Insights</h1>
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
        '>Análise interativa para decisões estratégicas na cadeia de suprimentos</h3>
    </div>
    """, unsafe_allow_html=True)

    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)

    # Cálculos dos KPIs
    receita_total = df_filtered["Receita_Gerada"].sum()
    vendas_total = df_filtered["Quantidade_Vendida"].sum()
    custo_total = df_filtered["Custos_Totais"].sum()
    margem_media = df_filtered["Margem"].mean()
    margem_media = df_filtered["Lucro"].sum() / df_filtered["Receita_Gerada"].sum() * 100 if df_filtered["Receita_Gerada"].sum() > 0 else 0

    with col1:
        kpi_card("💰 Faturamento Total",
                f"R$ {df_filtered['Receita_Gerada'].sum():,.2f}",
                COLORS['blues'][0],
                COLORS["cool_blues"][2],
                "Soma total da receita gerada")

    with col2:
        kpi_card("📦 Total de Vendas", 
                f"{df_filtered['Quantidade_Vendida'].sum():,}",
                COLORS['cool_blues'][1], 
                COLORS['cool_greens'][3],
                "Quantidade total de produtos vendidos")

    with col3:
        kpi_card("🚛 Total Logística", 
                f"R$ {df_filtered['Custos_Totais'].sum():,.2f}", 
                COLORS['warm_oranges'][1], 
                COLORS["golds"][1],
                "Custo Total do Envio de Pedidos")

    with col4:
        kpi_card("📈 Margem Média", 
                f"{margem_media:.2f}%", 
                COLORS['golds'][0], 
                COLORS["golds"][4],
                "Margem de lucro da operação")

    custom_divider()
    

    # Gráficos principais
    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 10px;
        '>
            <h2 style='
                color: white;
                background: linear-gradient(to right, #c69214, #d4a642);
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>📊 Análise de Vendas e Receita</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Criando as colunas para os subtítulos
    col1, col2 = st.columns([1,1], gap='small')

    with col1:
            st.markdown("""
            <div style='
            text-align: center;
            padding-top: 10px;
            '>
                <h3 style='
                    color: white;
                    background: linear-gradient(to right, #c69214, #d4a642);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    margin: 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>Receita por Categoria</h3>
            </div>
            """, unsafe_allow_html=True)   
    
            # Gráfico de Receita por Categoria (Barras)
            # Corrigir valores da Receita
            df_filtered["Receita_Gerada"] = pd.to_numeric(df_filtered["Receita_Gerada"], errors="coerce").fillna(0)

            # Agregação correta
            receita_categoria = df_filtered.groupby("Categoria", as_index=False).agg({"Receita_Gerada": "sum"})

            
            fig_receita = px.bar(
                receita_categoria,
                x="Categoria",
                y="Receita_Gerada",
                title=" ",
                color="Categoria",
                color_discrete_sequence=COLORS['mixed'],
                hover_data={"Receita_Gerada": ":,.2f"},
                #text_auto=True
            )
            fig_receita.update_traces(
                #text=receita_categoria["Receita_Gerada"].apply(lambda x: (f"R$ {x:,.2f}")),
                texttemplate="R$ %{y:,.2f}",
                textposition="outside",
                outsidetextfont=dict(color=COLORS["cool_greens"][3])
            )

            fig_receita.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=640,
                margin=dict(t=40,b=40,l=20,r=20),
                title_font_color=COLORS['secondary'],
                font=dict(family="Inter, sans-serif",size=20),
                legend_font=dict(family="Inter, sans-serif",size=18),
                xaxis_title="Categoria",
                yaxis_title="Total de Receita (R$)",
                xaxis=dict(
                    title="Categoria",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
                ),
            yaxis=dict(
                title="Total de Receita (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
            )
            st.plotly_chart(fig_receita, use_container_width=True)

    with col2:
            st.markdown("""
                <div style='
                text-align: center;
                padding-top: 10px;
                '>
                    <h3 style='
                        color: white;
                        background: linear-gradient(to right, #c69214, #d4a642);
                        font-size: 20px;
                        font-weight: 600;
                        font-family: Inter, sans-serif;
                        margin: 0;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    '>Distribuição de Vendas por Categoria</h3>
                </div>
                """, unsafe_allow_html=True)
            
            vendas_categoria = df_filtered.groupby("Categoria")["Quantidade_Vendida"].sum().reset_index()
            fig_vendas = go.Figure(data=[go.Pie(
                labels=vendas_categoria["Categoria"],
                values=vendas_categoria["Quantidade_Vendida"],
                hole=.4,
                marker_colors=COLORS['mixed'],
                textinfo='percent+label'
            )])
            fig_vendas.update_layout(
                title=" ",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                legend_font=dict(size=18,family="Inter, sans-serif"),
                height=640,
                font=dict(family="Inter, sans-serif",size=19),
                title_font_color=COLORS['secondary'],
            )
            st.plotly_chart(fig_vendas, use_container_width=True)
    custom_divider()
    
    # Análise de Clientes
    st.markdown("""
    <div style='
        text-align: center;
        padding-top: 10px;
    '>
        <h2 style='
            color: white;
            font-size: 29px;
            font-weight: bold;
            font-family: Inter, sans-serif;
            background: linear-gradient(to right, #c69214, #d4a642);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>👥 Análise de Clientes</h2>
            </div>
           """, unsafe_allow_html=True)

    # Criando as colunas para os subtítulos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='
                text-align: center;
                padding-top: 10px;
            '>
                <h3 style='
                    color: #FFFFFF;
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    background: linear-gradient(to right, #c69214, #d4a642);
                '>Volume de Vendas por Tipo de Cliente</h3>
            </div>
            """, unsafe_allow_html=True)
        # Volume de Vendas por Tipo de Cliente
        vendas_cliente = df_filtered.groupby("Demografia_Cliente")["Quantidade_Vendida"].sum().reset_index()
        
        vendas_cliente.rename(columns={"Quantidade_Vendida": "Vendas"}, inplace=True)

        fig_vendas_cliente = px.bar(
            vendas_cliente,
            x="Demografia_Cliente",
            y="Vendas",
            title=" ",
            color="Demografia_Cliente",
            color_discrete_sequence=COLORS['blues'],
            hover_data={"Vendas": ":,.2f"},
            text_auto=True
        )
        # Garante que os valores corretos sejam atribuídos a cada barra
        fig_vendas_cliente.update_traces(
            text=vendas_cliente["Vendas"].astype(int).apply(lambda x: f"{x:,.2f}"), 
            textposition="outside"
        )
        fig_vendas_cliente.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=600,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=20),
            legend=dict(font=dict(family="Inter, sans-serif",size=16)),  # Legenda maior
            xaxis_title="Tipo de Cliente",
            xaxis=dict(
            title="Tipo de Cliente",
            title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
            tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
        ),
            yaxis_title="Total de Vendas",
            yaxis=dict(
            title="Volume de Vendas (R$)",
            title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
            tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
        ),
        )
        st.plotly_chart(fig_vendas_cliente, use_container_width=True)   
   
    with col2:
        st.markdown("""
            <div style='
                text-align: center;
                padding-top: 10px;
            '>
                <h3 style='
                    color: #FFFFFF;
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    background: linear-gradient(to right, #c69214, #d4a642);
                '>Receita por Tipo de Cliente</h3>
            </div>
            """, unsafe_allow_html=True)
        # Receita por Tipo de Cliente
        receita_cliente = df_filtered.groupby("Demografia_Cliente")["Receita_Gerada"].sum().reset_index()
        fig_receita_cliente = px.pie(
            receita_cliente,
            values="Receita_Gerada",
            names="Demografia_Cliente",
            title=" ",
            color_discrete_sequence=COLORS['mixed']
        )
        fig_receita_cliente.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=600,
            font=dict(family="Inter, sans-serif",size=23),
            title_font_color=COLORS['secondary'],
            legend_font=dict(family="Inter, sans-serif",size=18),  # Legenda maior
        )
        st.plotly_chart(fig_receita_cliente, use_container_width=True)
        

    custom_divider()

    st.markdown("""
    <div style='
        text-align: center;
        padding-top: 10px;
    '>
        <h2 style='
            color: #FFFFFF;
            font-size: 30px;
            font-weight: bold;
            font-family: Inter, sans-serif;
            background: linear-gradient(to right, #c69214, #d4a642);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>💎 Top 15 Produtos com Maior Faturamento</h2>
            """, unsafe_allow_html=True)

    # Calcular os 10 produtos mais lucrativos
    top_produtos = df_filtered.nlargest(15, 'Lucro')[['Produto_SKU', 'Lucro', 'Categoria']]

    fig_produtos = px.bar(
        top_produtos,
        x='Produto_SKU',
        y='Lucro',
        color='Categoria',
        title=' ',
        color_discrete_sequence=COLORS['mixed'],
    )
    fig_produtos.for_each_trace(lambda t: t.update(
        texttemplate="R$ %{y:,.2f}",
        textposition="outside",
        outsidetextfont=dict(family="Inter, sans-serif",color=COLORS["cool_greens"][3])
    ))
    fig_produtos.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
        margin=dict(t=40, b=40,l=20,r=20),
        title_font_color=COLORS['secondary'],
        font=dict(family="Inter, sans-serif",size=20),
        xaxis_title="Produto",
        xaxis=dict(
            title="Categoria",
            title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
            tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
        ),

        yaxis_title="Faturamento (R$)",
        yaxis=dict(
            title="Faturamento (R$)",
            title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
            tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
        ),
        legend=dict(font=dict(size=18)),  # Legenda maior
    )
    st.plotly_chart(fig_produtos, use_container_width=True)

    custom_divider()
    # Análise Geográfica
    st.markdown("""
    <div style='
        text-align: center;
        padding-top: 10px;
    '>
        <h2 style='
            color: #FFFFFF;
            font-size: 30px;
            font-weight: bold;
            font-family: Inter, sans-serif;
            background: linear-gradient(to right, #c69214, #d4a642);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
            '>📍 Análise Geográfica</h2>
            """, unsafe_allow_html=True)

    # Criando as colunas para os subtítulos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='
                text-align: center;
                padding-top: 5px;
            '>
                <h3 style='
                    color: #FFFFFF;
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(to right, #c69214, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>Custo Total por Localização</h3>
            </div>
            """, unsafe_allow_html=True)
        # Custos por localização
        custos_local = df_filtered.groupby("Localizacao")["Custos_Totais"].sum().reset_index() # Changed to sum

        # Renomeando coluna para maior clareza
        custos_local.rename(columns={"Custos_Totais": "Custo Total"}, inplace=True)

        fig_custos = px.bar(
            custos_local,
            x="Localizacao",
            y="Custo Total",
            title=" ",
            color_discrete_sequence=COLORS['blues'],
        )
        fig_custos.update_traces(
            text=[f"R$ {x:,.2f}" for x in custos_local["Custo Total"]],
            textposition="outside",
            outsidetextfont=dict(color=COLORS["warm_reds"][1])
        )
        fig_custos.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=600,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=18),
            xaxis_title="Localizacao",
            yaxis_title="Total de Custos (R$)",
            xaxis=dict(
                title="Cidades",
                title_font=dict(family="Inter, sans-serif",size=18),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis=dict(
                title="Custo Total Envio (R$)",
                title_font=dict(family="Inter, sans-serif",size=18),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )
        st.plotly_chart(fig_custos, use_container_width=True)
        

    with col2:
        st.markdown("""
            <div style='
                text-align: center;
                padding-top: 5px;
            '>
                <h3 style='
                    color: #FFFFFF;
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(to right, #c69214, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>Volume de Vendas por Localização</h3>
            </div>
            """, unsafe_allow_html=True)
        # Mapa de calor por localização
        vendas_local = df_filtered.groupby("Localizacao")["Quantidade_Vendida"].sum().reset_index()

        # Renomear a coluna para garantir que o nome correto apareça no gráfico
        vendas_local.rename(columns={"Quantidade_Vendida": "Vendas"}, inplace=True)

        fig_mapa = px.treemap(
            vendas_local,
            path=["Localizacao"],
            values="Vendas",
            title=" ",
            color_discrete_sequence=COLORS['mixed'],
        )
        fig_mapa.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",height=620,title_font_color=COLORS['secondary'],font=dict(family="Inter, sans-serif",size=20),)
        st.plotly_chart(fig_mapa, use_container_width=True)
        
  
    custom_divider()
    # Tabela detalhada
    st.markdown("""
    <div style='
        text-align: center;
        padding-top: 10px;
    '>
        <h2 style='
            color: #7D1128;
            font-size: 30px;
            font-weight: bold;
            font-family: Inter, sans-serif;
            background: linear-gradient(to right, #c69214, #d4a642);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            '>📋 Dados Detalhados</h2>
            """, unsafe_allow_html=True)

    # Selecionar e formatar colunas para exibição
    colunas_exibir = [
        "Produto_SKU", "Categoria", "Quantidade_Vendida",
        "Receita_Gerada", "Custos_Totais", "Margem", "Lucro"
    ]

    st.dataframe(
        df_filtered[colunas_exibir].style.format({
            "Receita_Gerada": "R$ {:,.2f}",
            "Custos_Totais": "R$ {:,.2f}",
            "Margem": "{:.1f}%",
            "Lucro": "R$ {:,.2f}"
        }),
        use_container_width=True
    )


    # Criar buffer CSV
    csv_buffer = io.StringIO()
    df_filtered[colunas_exibir].to_csv(csv_buffer, index=False, sep=';', decimal=',')

    # Criar buffer Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_filtered[colunas_exibir].to_excel(writer, index=False, sheet_name="Dados_Detalhados")
        writer.close()

    # Criar botões de download
    col_csv, col_xlsx = st.columns(2)

    with col_csv:
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_buffer.getvalue(),
            file_name="dados_vendas.csv",
            mime="text/csv"
        )

    with col_xlsx:
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_buffer.getvalue(),
            file_name="dados_vendas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.subheader("📝 Minhas Anotações")

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
        mime="text/plain",
    )

    # Footer
    custom_divider()
    st.markdown(
        f"""
        <div style='text-align: center; color: {COLORS['secondary']};'>
            Dashboard atualizado em: {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
        """,
        unsafe_allow_html=True
    )
    
else:
    st.error("Não foi possível carregar os dados. Por favor, verifique o arquivo de dados.")