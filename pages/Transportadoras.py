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


def kpi_card(title, value, color1,color2, help_text=None):
    text_color = "#FFFFFF"  # Mantemos branco para legibilidade
    
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color1}, {color2});
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-family: 'Inter', 'sans-serif';
            font-weight: bold;
            color: {text_color};            
            border: 4px solid {color1};
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

if df is not None:
    # Renomear colunas para facilitar leitura
    df.rename(columns={
        "Shipping carriers": "Transportadoras",
        "Production volumes": "Volume_Pedidos",
        "Shipping costs": "Custos_Envio",
        "Transportation modes": "Modos_Transporte",
        "Costs": "Custos_Totais",
        "Product type": "Categoria",
        "Location": "Localizacao",
        "Revenue generated": "Receita_Gerada",
        "Number of products sold": "Quantidade_Vendida",
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
    # Sidebar com filtros
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

    # Aplicar os filtros no DataFrame
    df_filtered = df.copy()

    if st.session_state.selected_transport != "Todas":
        df_filtered = df_filtered[df_filtered["Modos_Transporte"] == st.session_state.selected_transport]
    if st.session_state.selected_carrier != "Todas":
        df_filtered = df_filtered[df_filtered["Transportadoras"] == st.session_state.selected_carrier]
    if st.session_state.selected_category:
        df_filtered = df_filtered[df_filtered["Categoria"].isin(st.session_state.selected_category)]

    # Header principal
    st.markdown(f"""
        <div style='
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            background: linear-gradient(135deg, {COLORS["blues"][2]}, {COLORS["golds"][0]});
            box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
        '>
            <h1 style='
                color: #FFFFFF;
                font-size: 36px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
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
            "📦 Total de Pedidos",
            f"{volume_total:,}", 
            COLORS["blues"][2],
            COLORS["golds"][1],
            "Total de pedidos processados"
        )

    with col2:
        # Calculando o custo total de envio (soma de todos os custos)
        custo_total = df_filtered["Custos_Envio"].sum()
        kpi_card("🚛 Custo Logístico Total", f"R$ {df_filtered["Custos_Totais"].sum():,.2f}", 
                COLORS["blues"][2],
                COLORS["golds"][1],
                "Custo Total do Envio de Pedidos")

    with col3:
        # Calculando o custo médio por pedido (custo total / volume total)
        df_filtered["Receita_Gerada"] = df_filtered["Receita_Gerada"].fillna(0)  # Evita erro com NaN
        percentual_custo_logistico = (custo_total / df_filtered["Receita_Gerada"].sum()) * 100 if df_filtered["Receita_Gerada"].sum() > 0 else 0

        kpi_card(
            "📉 % Envio sobre Faturamento",
            f"{percentual_custo_logistico: .2f}%",
            COLORS["blues"][2],
            COLORS["golds"][1],
            "Percentual do custo de envio em relação ao faturamento total"
        )

    with col4:
        custo_medio_transportadora = df_filtered.groupby("Transportadoras")["Custos_Envio"].mean().mean()

        kpi_card(
            "📊 Custo Médio de Envio",
            f"R$ {custo_medio_transportadora:,.2f}", 
            COLORS["blues"][2],
            COLORS["golds"][1],
            "Média dos custos de envio por transportadora"
        )

    custom_divider()

    col1, col2=  st.columns(2)
    # Volume de Pedidos por Transportadora
    with col1:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>📦 Volume de Pedidos por Transportadora</h2>
            </div>
            """, unsafe_allow_html=True)

        # Gráfico de barras com volume de pedidos
        fig_volume = px.bar(
            df_filtered.groupby("Transportadoras")["Volume_Pedidos"].sum().reset_index(),
            x="Transportadoras",
            y="Volume_Pedidos",
            title=" ",
            color="Transportadoras",
            color_discrete_sequence=COLORS['blues'],
        )
        fig_volume.update_traces(
        texttemplate="%{y:}",
        textposition="outside",
        outsidetextfont=dict(color=COLORS["warm_yellows"][0]) 

    )
        fig_volume.update_layout(
            showlegend= False,
            height=550,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['warm_yellows'][0],
            font_color=COLORS['warm_yellows'][0],
            font=dict(size=20,family="Inter, sans-serif"),
            legend_font=dict(size=18,family="Inter, sans-serif"),
            xaxis=dict(
                    title="Transportadora",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
                ),
            yaxis=dict(
                    title="Volume de Pedidos",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
                ),
        )
        st.plotly_chart(fig_volume, use_container_width=True)
        st.markdown("""
        <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
            🔍 Transportadoras com maior volume têm poder de negociação. 
            Avalie o custo-benefício de contratos exclusivos.
        </div>
        """, unsafe_allow_html=True)

    
    # Custos de Envio por Transportadora
    with col2:
        # 📊 Gráfico de Receita vs Custo por Transportadora
        st.markdown(f"""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>⚖️ Faturamento vs. Custo por Transportadora</h2>
            </div>
            """, unsafe_allow_html=True)
        receita_transportadora = df_filtered.groupby("Transportadoras")["Receita_Gerada"].sum().reset_index()
        custo_transportadora = df_filtered.groupby("Transportadoras")["Custos_Totais"].sum().reset_index()
        
        fig_transp = go.Figure()
        
        # Barra Principal - Receita Total
        fig_transp.add_trace(go.Bar(
            x=receita_transportadora["Transportadoras"],
            y=receita_transportadora["Receita_Gerada"],
            name="Receita Total",
            marker=dict(color=COLORS["blues"][1]),
            text=[f"R$ {x:,.2f}" for x in receita_transportadora["Receita_Gerada"]],
            textposition='outside',
            width= 0.5,
            outsidetextfont=dict(color=COLORS['cool_greens'][2])
        ))
        
        # Barra Secundária - Custo Total
        fig_transp.add_trace(go.Bar(
            x=custo_transportadora["Transportadoras"],
            y=custo_transportadora["Custos_Totais"],
            name="Custo Total",
            marker=dict(color=COLORS["warm_reds"][2]),
            width=0.1888,
            offset= -0.4
        ))
        
        fig_transp.update_layout(
            barmode="group",
            title=" ",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=550,
            font=dict(family="Inter, sans-serif", size=18),
            xaxis_title="Transportadora",
            yaxis_title="Valores (R$)",
            legend=dict(font=dict(size=16)),
        )

        st.plotly_chart(fig_transp, use_container_width=True)
        st.markdown("""
            <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
                🔍 Transportadoras com alto custo e baixa receita podem indicar ineficiência ou tarifas desfavoráveis. Avalie renegociações e redistribuições estratégicas.
            </div>
            """, unsafe_allow_html=True)
        
    custom_divider()
    col3, col4 = st.columns(2)

    # Custos por Modalidade de Transporte
    with col3:
        # 📊 Gráfico de Custo de Envio vs. Volume por Modalidade de Transporte
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>⚖️ Custo de Envio vs. Volume por Modalidade</h2>
            </div>
            """, unsafe_allow_html=True)

        # Agrupando os dados
        modalidade_data = df_filtered.groupby("Modos_Transporte").agg({
            "Quantidade_Vendida": "sum",
            "Custos_Totais": "sum"
        }).reset_index()

        # Criando gráfico de barras horizontais
        fig_modalidade = go.Figure()

        # Barra Principal - Custo Total por Modalidade
        fig_modalidade.add_trace(go.Bar(
            y=modalidade_data["Modos_Transporte"],
            x=modalidade_data["Custos_Totais"],
            name="Custo Total de Envio",
            marker=dict(color=COLORS["blues"][2]),
            orientation='h',
            width=0.5,
            text=[f"R$ {x:,.2f}" for x in modalidade_data["Custos_Totais"]],
            textposition='inside',
            insidetextfont=dict(color="#FFFFFF")
        ))

        # Barra Secundária - Volume Total de Pedidos
        fig_modalidade.add_trace(go.Bar(
            y=modalidade_data["Modos_Transporte"],
            x=modalidade_data["Quantidade_Vendida"],
            name="Volume Total de Pedidos",
            marker=dict(color=COLORS["golds"][1]),
            width=0.4,
            orientation='h',
            offset=-0.58,
            text=[f"{x:,.0f}" for x in modalidade_data["Quantidade_Vendida"]],
            textposition='inside',
            insidetextfont=dict(color="#FFFFFF")
        ))

        fig_modalidade.update_layout(
            barmode="group",
            title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=640,
            font=dict(family="Inter, sans-serif", size=18),
            xaxis_title="Valores (R$ e Unidades)",
            yaxis_title="Modalidade de Transporte",
            legend=dict(font=dict(size=16)),
        )

        st.plotly_chart(fig_modalidade, use_container_width=True)
        st.markdown("""
            <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
                🔍 O modal mais barato pode não ser o mais eficiente. Analise o equilíbrio entre custo e volume para otimizar a alocação de transporte.
            </div>
            """, unsafe_allow_html=True)
        

    # Custos por Cidade
    with col4:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>🚚 Custos por Modalidade de Transporte</h2>
            </div>
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
            color_discrete_sequence=COLORS["blues"],
            #text_auto=True
        )
        fig_modalidade.update_traces(
            #text=[f"R$ {x:,.0f}" for x in custos_modalidade["Custos_Totais"]],
            texttemplate="R$ %{y:,.2f}",
            textposition="outside",
            outsidetextfont=dict(color=COLORS["warm_yellows"])  # Garante visibilidade dos números
        )  
        fig_modalidade.update_layout(
            showlegend=False,
            height=640,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['warm_yellows'][0],
            font_color=COLORS['warm_yellows'][0],
            font=dict(family="Inter, sans-serif",size=23),
            legend_font=dict(family="Inter, sans-serif",size=18),
            xaxis=dict(
                    title="Modalidade de Transporte",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo X
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo X
                ),
            yaxis=dict(
                    title="Custo Médio Total de Envio (R$)",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
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
    col5, col6 = st.columns(2)

    with col5:
        # 🌆 Análise de Custos por Cidade
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>🌆 Custo Total vs. Volume de Pedidos por Cidade</h2>
            </div>
            """, unsafe_allow_html=True)
            
        # Calculando os custos totais por cidade ANTES de passar para o gráfico
        
        custos_cidade = df_filtered.groupby("Localizacao")["Custos_Totais"].sum().sort_values(ascending=True).reset_index()
        volume_cidade = df_filtered.groupby("Localizacao")["Quantidade_Vendida"].sum().reset_index()

        # Gráfico de barras horizontal para custos por cidade
        fig_cidade = go.Figure()
    
        # Barra Principal - Custo Total por Cidade
        fig_cidade.add_trace(go.Bar(
            y=custos_cidade["Localizacao"],
            x=custos_cidade["Custos_Totais"],
            name="Custo Total de Envio",
            marker=dict(color=COLORS["blues"][1]),
            orientation='h',
            width= 0.5,
            text=[f"R$ {x:,.2f}" for x in custos_cidade["Custos_Totais"]],
            textposition='inside',
            insidetextfont=dict(color=COLORS["warm_yellows"][3]) 
        ))
        
        # Barra Secundária - Volume Total de Pedidos
        fig_cidade.add_trace(go.Bar(
            y=volume_cidade["Localizacao"],
            x=volume_cidade["Quantidade_Vendida"],
            name="Volume Total de Pedidos",
            marker=dict(color=COLORS["warm_yellows"][2]),
            width=0.4,
            orientation='h',
            offset=-0.58,
            text=volume_cidade["Quantidade_Vendida"],
            textposition='inside',
            insidetextfont=dict(color=COLORS["blues"][1]) 
        ))
        
        fig_cidade.update_layout(
            barmode="group",
            title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=640,
            font=dict(family="Inter, sans-serif", size=18),
            xaxis_title="Valores (R$ e Unidades)",
            yaxis_title="Cidade",
            legend=dict(font=dict(size=16)),
        )

        st.plotly_chart(fig_cidade, use_container_width=True)
        st.markdown("""
            <div style='text-align: center; font-size: 18px; font-weight: 500; color: #FFD700; padding-top: 5px;'>
                🔍 Regiões de alto custo podem indicar gargalos logísticos. 
                Avalie transportadoras locais e a viabilidade de novos hubs.
            </div>
            """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
            <div style='text-align: center; padding-top: 10px;'>
                <h2 style='
                    color: #FFFFFF;
                    font-size: 29px;
                    font-weight: bold;
                    font-family: Inter, sans-serif;
                    background: linear-gradient(135deg, #1b2e7b, #d4a642);
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                '>💰 Custos de Envio por Transportadora</h2>
            </div>
            """, unsafe_allow_html=True)

        # Box plot de custos

        fig_custos = go.Figure()
        for transportadoras in df_filtered["Transportadoras"].unique():
            dados_transp = df_filtered[df_filtered["Transportadoras"] == transportadoras]
            fig_custos.add_trace(go.Box(
                y=dados_transp["Custos_Envio"],
                name=transportadoras,
                marker_color=COLORS["warm_reds"][2],
                #boxmean='sd'
            ))

            fig_custos.update_traces(
                marker=dict(opacity=0.8),  # Reduz impacto de outliers
                line=dict(width=1.5)  # Melhora visual da borda do boxplot
            )
        fig_custos.update_layout(    
            showlegend=False,
            title=" ",
            height=640,
            margin=dict(t=40,b=40,l=20,r=20),
            title_font_color=COLORS['warm_yellows'][0],
            font_color=COLORS['warm_yellows'][0],
            font=dict(family="Inter, sans-serif",size=20),
            legend_font=dict(family="Inter, sans-serif",size=18),

            yaxis=dict(
                    title="Custos de Envio (R$)",
                    title_font=dict(family="Inter, sans-serif",size=20),  # Aumentando fonte do nome do eixo Y
                    tickfont=dict(family="Inter, sans-serif",size=18)  # Aumentando fonte dos valores do eixo Y
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
    # Tabela detalhada
    # 📋 Dados Detalhados
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <h2 style='
                color: #FFFFFF;
                font-size: 29px;
                font-weight: bold;
                font-family: Inter, sans-serif;
                background: linear-gradient(135deg, #1b2e7b, #d4a642);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            '>📋 Dados Detalhados</h2>
        </div>
        """, unsafe_allow_html=True)

    # Selecionar e formatar colunas para exibição
    colunas_exibir = [
        "Transportadoras",
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