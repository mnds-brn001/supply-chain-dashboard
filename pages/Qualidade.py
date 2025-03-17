import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os


# Configuração da página
st.set_page_config(
    page_title="🔍 Análise de Qualidade",
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
    'warm_reds': ['#5A0E17', '#7D1128', '#8B1E3F', '#A93226', '#C0392B', '#D92E1C', '#E84118'],

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

def kpi_card(title, value, color1,color2, help_text=None):

    text_color = "#FFFFFF"  # Mantemos branco para legibilidade
    border_color = color1  # A borda será da mesma cor do KPI
    bg_opacity = "0.60"  # Define a opacidade do fundo (85%)
    
    def hex_to_rgba(hex_color, alpha=1):
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r},{g},{b},{alpha})"

    #bg_rgba = hex_to_rgba(color1, bg_opacity)

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color1}, {color2});
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-family: 'Inter';
            font-weight: bold;
            color: {text_color};            
            border: 4px solid {border_color}; /* Borda sólida */
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);">
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

if df is not None:
    # Renomear colunas para facilitar leitura
    df.rename(columns={
        "Shipping carriers": "Transportadoras",
        "Defect rates": "Taxa_Defeitos",
        "Production volumes": "Volume_Pedidos",
        "Shipping costs": "Custos_Envio",
        "Transportation modes": "Modos_Transporte",
        "Costs": "Custos_Totais",
        "Product type": "Categoria",
        "SKU": "Produto_SKU",
        "Location": "Localizacao",
        "Revenue generated": "Receita_Gerada"
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
        df["Modos_Transporte"] = df["Modos_Transporte"].map(transporte_traducao).fillna(df["Modos_Transporte"])
        df["Transportadoras"] = df["Transportadoras"].map(transportadora_traducao).fillna(df["Transportadoras"])
    
    # Inicializa os valores dos filtros no session_state se ainda não existirem
    for key in ["selected_category", "selected_transportadora", "selected_mode"]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "selected_category" else []

    # Sidebar para filtros
    st.sidebar.header("🔍 Filtros")

    # Inicializar session state para armazenar filtros
    if "selected_transport" not in st.session_state:
        st.session_state.selected_transport = "Todas"
    if "selected_carrier" not in st.session_state:
        st.session_state.selected_carrier = "Todas"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = list(df["Categoria"].unique())
    
    # Filtros
    st.session_state.selected_transport = st.sidebar.selectbox(
        "🚛 Modo de Transporte",
        ["Todas"] + list(df["Modos_Transporte"].unique()),
        index=(["Todas"] + list(df["Modos_Transporte"].unique())).index(st.session_state.selected_transport)
    )

    st.session_state.selected_carrier = st.sidebar.selectbox(
        "🏢 Transportadora",
        ["Todas"] + list(df["Transportadoras"].unique()),
        index=(["Todas"] + list(df["Transportadoras"].unique())).index(st.session_state.selected_carrier)
    )

    st.session_state.selected_category = st.sidebar.multiselect(
        "📦 Categorias de Produto",
        options=list(df["Categoria"].unique()),
        default=st.session_state.selected_category
    )
    
    # Aplicando os filtros
    df_filtered = df.copy()

    if st.session_state.selected_transport != "Todas":
        df_filtered = df_filtered[df_filtered["Modos_Transporte"] == st.session_state.selected_transport]
    if st.session_state.selected_carrier != "Todas":
        df_filtered = df_filtered[df_filtered["Transportadoras"] == st.session_state.selected_carrier]
    if st.session_state.selected_category:
        df_filtered = df_filtered[df_filtered["Categoria"].isin(st.session_state.selected_category)]

    # Calculando campos adicionais
    df_filtered["Receita_Gerada"] = pd.to_numeric(df_filtered["Receita_Gerada"], errors="coerce").fillna(0)
    df_filtered['Lucro'] = df_filtered['Receita_Gerada'] - df_filtered['Custos_Totais']
    df_filtered['Margem'] = (df_filtered['Lucro'] / df_filtered['Receita_Gerada']) * 100

    # Calcular o prejuízo causado por defeitos
    df_filtered["Prejuizo_Defeitos"] = df_filtered["Receita_Gerada"] * (df_filtered["Taxa_Defeitos"] / 100)

    # Header principal com título e descrição
    st.markdown(f"""
        <div style='
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            background: linear-gradient(135deg, {COLORS["warm_reds"][0]}, {COLORS["warm_oranges"][3]});
            box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
        '>
            <h1 style='
                color: #FFFFFF;
                font-size: 36px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>🔍 Análise de Qualidade e Defeitos</h1>
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
            '>Dashboard ativo para análise de qualidade na cadeia de suprimentos</h3>
        </div>
        """, unsafe_allow_html=True)

    # KPIs principais
    col1, col2 = st.columns(2)

    with col1:
        taxa_defeitos = df_filtered["Taxa_Defeitos"].mean()
        kpi_card(
            "❌ Taxa Média de Defeitos",
            f"{taxa_defeitos:.2f}%", 
            COLORS["warm_reds"][0],
            COLORS["warm_oranges"][3],
            "Média geral de defeitos em produtos"
        )

    with col2:
        prejuizo_total = df_filtered["Prejuizo_Defeitos"].sum()
        kpi_card(
            "💰 Prejuízo Total",
            f"R$ {prejuizo_total:,.2f}", 
            COLORS["warm_reds"][0],
            COLORS["warm_reds"][5],
            "Receita perdida devido a produtos defeituosos"
        )

    custom_divider()
    # 📊 Análise de Defeitos por Categoria
    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 10px;
        '>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(135deg, #5A0E17, #d35400);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>📊 Análise de Defeitos por Categoria</h2>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg, #5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>📉 Taxa Média de Defeitos por Categoria</h3>
            </div>
            """, unsafe_allow_html=True)
        defeitos_categoria = df_filtered.groupby("Categoria")["Taxa_Defeitos"].mean().reset_index()
        df_filtered.groupby("Categoria")["Taxa_Defeitos"].mean().reset_index()
        # Taxa média de defeitos por categoria
        df_filtered.groupby("Categoria")["Taxa_Defeitos"].mean().reset_index()
        fig_defeitos = px.bar(
        defeitos_categoria,
        x="Categoria",
        y="Taxa_Defeitos",
        title=" ",
        color="Categoria",
        color_discrete_sequence=COLORS['warm_oranges']
        )

        fig_defeitos.update_traces(
            #text=defeitos_categoria["Taxa_Defeitos"].apply(lambda x: (f"{x:.2f}%")),
            texttemplate="%{y:.2f}%",
            textposition="outside",
            outsidetextfont=dict(color=COLORS["golds"])  # Mantém o texto visível dentro das barras
        )

        fig_defeitos.update_layout(
            showlegend=False,
            height=670,
            margin=dict(t=40, b=40,l=20, r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['primary'],
            font=dict(size=20,family="Inter, sans-serif"),
            xaxis_title="Categoria de Produto",
                xaxis=dict(
                title="Categoria de Produto",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis_title="Taxa de Defeitos (%)",
            yaxis=dict(
                title="Taxa de Defeitos (%)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )
        st.plotly_chart(fig_defeitos, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg, #5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>💸 Distribuição do Prejuízo por Categoria</h3>
            </div>
            """, unsafe_allow_html=True)
        # Prejuízo por categoria
        prejuizo_categoria = df_filtered.groupby("Categoria")["Prejuizo_Defeitos"].sum().reset_index()
        fig_prejuizo = go.Figure(data=[go.Pie(
                labels=prejuizo_categoria["Categoria"],
                values=prejuizo_categoria["Prejuizo_Defeitos"],
                hole=.4,
                marker_colors=COLORS['warm_reds'],
                textinfo='percent+label'
        )])
        fig_prejuizo.update_layout(
            title=" ",
            showlegend=False,
            height=670,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['secondary'],
            font=dict(size=23,family="Inter, sans-serif"),
            legend_font=dict(size=18,family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_prejuizo, use_container_width=True)

    custom_divider()
    # Top 10 Produtos com Maior Taxa de Defeitos
    # ❌ Produtos Críticos
    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 10px;
        '>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(135deg, #5A0E17, #d35400);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>❌ Produtos Críticos</h2>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg,#5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>⚠️ Top 10 Produtos com Maior Taxa de Defeitos</h3>
            </div>
            """, unsafe_allow_html=True)
        # Top 10 produtos com maior taxa de defeitos
        top_defeitos = df_filtered.sort_values(by="Taxa_Defeitos", ascending=False).head(10)

        fig_top_defeitos = px.bar(
            top_defeitos,
            x="Taxa_Defeitos",
            y="Produto_SKU",
            color="Categoria",
            title=" ",
            color_discrete_sequence=COLORS['warm_oranges'],
            text="Taxa_Defeitos"
        )

        fig_top_defeitos.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="inside",
            insidetextfont=dict(color=COLORS['golds'][3])
        )

        fig_top_defeitos.update_layout(
            showlegend= False,
            height=670,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=18),
            legend_font=dict(family="Inter, sans-serif",size=16),
            xaxis_title="Taxa de Defeitos (%)",
            xaxis=dict(
                title="Taxa de Defeitos (%)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis_title="Produto (SKU)",
            yaxis=dict(
                title="Produto (SKU)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )

        st.plotly_chart(fig_top_defeitos, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg, #5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>💰 Top 10 Produtos com Maior Prejuízo</h3>
            </div>
            """, unsafe_allow_html=True)
        # Top 10 produtos com maior prejuízo
        top_prejuizo = df_filtered.sort_values(by="Prejuizo_Defeitos", ascending=False).head(10)

        fig_top_prejuizo = px.bar(
            top_prejuizo,
            x="Prejuizo_Defeitos",
            y="Produto_SKU",
            color="Categoria",
            title=" ",
            color_discrete_sequence=COLORS['warm_reds'],
            text="Prejuizo_Defeitos"
        )

        fig_top_prejuizo.update_traces(
            texttemplate="R$ %{text:,.2f}",
            textposition="inside",
            insidetextfont=dict(color=COLORS['golds'][3])
        )

        fig_top_prejuizo.update_layout(
            showlegend= False,
            height=670,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=18),
            legend_font=dict(family="Inter, sans-serif",size=16),
            xaxis=dict(
                title="Prejuízo (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis=dict(
                title="Produto (SKU)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )

        st.plotly_chart(fig_top_prejuizo, use_container_width=True)

    custom_divider()
    # 📍 Análise por Localização
    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 10px;
        '>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(135deg, #5A0E17, #d35400);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>📍 Análise por Localização</h2>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg, #5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>🌍 Taxa Média de Defeitos por Localização</h3>
            </div>
            """, unsafe_allow_html=True)
        # Taxa de defeitos por localização
        defeitos_local = df_filtered.groupby("Localizacao")["Taxa_Defeitos"].mean().reset_index()
        fig_local_defeitos = px.bar(
            defeitos_local,
            x="Localizacao",
            y="Taxa_Defeitos",
            title=" ",
            color_discrete_sequence=[COLORS['warm_oranges']]
        )

        fig_local_defeitos.update_traces(
            text=[f"{x:.2f}%" for x in defeitos_local["Taxa_Defeitos"]],
            textposition="outside",
            insidetextfont=dict(color="white")
        )
        fig_local_defeitos.update_layout(
            height=670,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=20),
            xaxis=dict(
                title="Localização",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis=dict(
                title="Taxa de Defeitos (%)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )
        st.plotly_chart(fig_local_defeitos, use_container_width=True)

    with col2:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h3 style='
                    color: white;
                    background: linear-gradient(135deg, #5A0E17, #d35400);
                    font-size: 20px;
                    font-weight: 600;
                    font-family: Inter, sans-serif;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                '>🏙️ Prejuízo Total por Localização</h3>
            </div>
            """, unsafe_allow_html=True)
        # Prejuízo por localização
        prejuizo_local = df_filtered.groupby("Localizacao")["Prejuizo_Defeitos"].sum().reset_index()
        fig_prejuizo_local = px.bar(
            prejuizo_local,
            x="Localizacao",
            y="Prejuizo_Defeitos",
            title=" ",
            color_discrete_sequence=[COLORS['warm_reds']]
        )

        fig_prejuizo_local.update_traces(
            text=[f"R$ {x:,.2f}" for x in prejuizo_local["Prejuizo_Defeitos"]],
            textposition="outside",
            insidetextfont=dict(color="white")
        )

        fig_prejuizo_local.update_layout(
            height=670,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['secondary'],
            font_color=COLORS['secondary'],
            font=dict(family="Inter, sans-serif",size=20),
            xaxis=dict(
                title="Localização",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
            ),
            yaxis=dict(
                title="Prejuízo (R$)",
                title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
            ),
        )
        st.plotly_chart(fig_prejuizo_local, use_container_width=True)

    custom_divider()
    # Tabela detalhada
    # 📋 Dados Detalhados
    st.markdown("""
        <div style='
            text-align: center;
            padding-top: 10px;
        '>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(135deg, #5A0E17, #d35400);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>📋 Dados Detalhados</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Selecionar e formatar colunas para exibição
    colunas_exibir = [
        "Produto_SKU",
        "Categoria",
        "Taxa_Defeitos",
        "Prejuizo_Defeitos",
        "Localizacao"
    ]

    st.dataframe(
        df_filtered[colunas_exibir].style.format({
            "Taxa_Defeitos": "{:.2f}%",
            "Prejuizo_Defeitos": "R$ {:,.2f}"
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
            file_name="dados_qualidade.csv",
            mime="text/csv"
        )

    with col_xlsx:
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_buffer.getvalue(),
            file_name="dados_qualidade.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.markdown("<h2 style='color:#7D1128;'>📝 Minhas Anotações", unsafe_allow_html=True)

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
            Dashboard atualizado em: {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("Não foi possível carregar os dados. Por favor, verifique o arquivo de dados.")