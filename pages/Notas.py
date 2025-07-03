# ⚠️ Mesma importação e autenticação da versão anterior
import streamlit as st
import pandas as pd
import datetime
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Cadastro de Compras", layout="wide")

usuarios_autorizados = st.secrets["users"]["allowed"]
st.sidebar.title("🔐 Acesso")
usuario = st.sidebar.text_input("Nome de usuário")
if usuario not in usuarios_autorizados:
    st.sidebar.error("🚫 Acesso negado.")
    st.stop()
else:
    st.sidebar.success(f"✅ Bem-vindo, {usuario}!")

# Conexão com GSheets
planilha_id = st.secrets["gsheets"]["S"]
conexao = st.connection("gsheets", type=GSheetsConnection)
df_existente = conexao.read(spreadsheet=planilha_id, worksheet="invent", usecols=list(range(8)), ttl=5)
df_existente = df_existente.dropna(how="all")

# Tabs
aba1, aba2 = st.tabs(["📝 Cadastrar Compra", "📈 Visualizar Compras"])

# ------------------------------------------------------------------------------
# ABA 1 — Cadastrar Compra
# ------------------------------------------------------------------------------
with aba1:
    col_img, col_form = st.columns([1, 2])
    imagem = col_img.file_uploader("🖼️ Selecionar imagem do comprovante", type=["jpg", "jpeg", "png"])
    imagem_processada = None
    if imagem:
        imagem_colorida = Image.open(imagem)
        imagem_pb = imagem_colorida.convert("L")
        buffer_preview = io.BytesIO()
        imagem_pb.save(buffer_preview, format="JPEG", quality=70, optimize=True)
        buffer_preview.seek(0)
        imagem_processada = Image.open(buffer_preview)
        col_img.image(imagem_processada, caption="Prévia da imagem (PB, qualidade 70%)", use_container_width=True)

    with col_form.form("formulario_compra"):
        st.subheader("🧾 Novo Cadastro de Compra")
        estabelecimento = st.text_input("🏪 Nome do estabelecimento")
        valor = st.number_input("💰 Valor da compra (R$)", format="%.2f")
        data_compra = st.date_input("📅 Data da compra", value=datetime.date.today())
        enviado = st.form_submit_button("Salvar dados")

        if enviado:
            if estabelecimento and valor and imagem_processada:
                buffer_final = io.BytesIO()
                imagem_processada.save(buffer_final, format="JPEG", quality=70, optimize=True)
                img_bytes = buffer_final.getvalue()
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                nova_linha = {
                    "imagem": img_b64,
                    "dia": data_compra.strftime("%d/%m/%Y"),
                    "valor": valor,
                    "estabelecimento": estabelecimento,
                    "usuario": usuario
                }
                df_atualizado = pd.concat([df_existente, pd.DataFrame([nova_linha])], ignore_index=True)
                conexao.update(spreadsheet=planilha_id, worksheet="invent", data=df_atualizado)
                st.success("✅ Compra cadastrada com sucesso!")
            else:
                st.warning("⚠️ Preencha todos os campos e envie uma imagem.")

# ------------------------------------------------------------------------------
# ABA 2 — Visualizar Compras
# ------------------------------------------------------------------------------
with aba2:
    # Pré-processamento
    df = df_existente.copy()
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data_dt"] = pd.to_datetime(df["dia"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["data_dt", "valor"])
    df["ano"] = df["data_dt"].dt.year
    df["mes"] = df["data_dt"].dt.month

    # Filtros principais
    col_f1, col_f2 = st.columns(2)
    usuarios_unicos = df["usuario"].dropna().unique()
    anos_disponiveis = sorted(df["ano"].dropna().unique(), reverse=True)
    usuario_selecionado = col_f1.selectbox("👤 Usuário", ["Todos"] + list(usuarios_unicos))
    ano_selecionado = col_f2.selectbox("📅 Ano", anos_disponiveis)

    df_ano = df[df["ano"] == ano_selecionado]
    df_filtrado = df_ano if usuario_selecionado == "Todos" else df_ano[df_ano["usuario"] == usuario_selecionado]

    # Totais mensais com destaque
    totais_mensais = df_filtrado.groupby("mes")["valor"].sum().reindex(range(1, 13), fill_value=0).round(2)
    mes_atual = datetime.date.today().month
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    for i in range(0, 12, 3):
        c1, c2, c3 = st.columns(3)
        for col, m in zip([c1, c2, c3], range(i+1, i+4)):
            valor_mes = totais_mensais[m]
            nome_mes = meses_pt[m - 1]
            if m == mes_atual:
                label = f"**:blue[{nome_mes}]**"
            else:
                label = f"*{nome_mes}*"
            col.metric(label=label, value=f"R$ {valor_mes:,.2f}", border=True)

    st.write('---')

    # Visualizações em 4 colunas
    col1, col2, col3, col4 = st.columns(4)

    # Gráfico de linha: evolução mensal
    with col1:
        st.markdown("#### 📈 Gastos por Dia (por Mês)")
        df_mes_linha = df_filtrado.copy()
        df_mes_linha["Dia"] = df_mes_linha["data_dt"].dt.day
        df_mes_linha["Mês"] = df_mes_linha["data_dt"].dt.strftime("%b")

        fig_multilinha = px.line(
            df_mes_linha,
            x="Dia",
            y="valor",
            color="Mês",
            markers=True,
            labels={"valor": "Valor (R$)", "Dia": "Dia do Mês", "Mês": "Mês"},
            title="Distribuição dos Gastos Diários por Mês"
        )
        fig_multilinha.update_layout(legend_title_text="Mês")
        st.plotly_chart(fig_multilinha, use_container_width=True)

    # Gráfico de pizza por usuário
    with col2:
        df_pizza = df_ano.groupby("usuario")["valor"].sum().reset_index()
        fig_pizza = px.pie(df_pizza, values="valor", names="usuario", title="Distribuição por Usuário")
        st.plotly_chart(fig_pizza, use_container_width=True)

    # Métricas gerais
    with col3:
        st.markdown("#### 📋 Estatísticas Totais")
        total = df_ano["valor"].sum()
        media = df_ano["valor"].mean()
        maximo = df_ano["valor"].max()
        minimo = df_ano["valor"].min()
        registros = df_ano.shape[0]
        st.metric("Total", f"R$ {total:,.2f}")
        st.metric("Média", f"R$ {media:,.2f}")
        st.metric("Máximo", f"R$ {maximo:,.2f}")
        st.metric("Mínimo", f"R$ {minimo:,.2f}")
        st.metric("Registros", registros)

    # Métricas por usuário
    with col4:
        st.markdown("#### 👤 Estatísticas por Usuário")
        usuario_especifico = st.selectbox("Selecionar usuário para análise", usuarios_unicos)
        df_user = df_ano[df_ano["usuario"] == usuario_especifico]
        soma_user = df_user["valor"].sum()
        media_user = df_user["valor"].mean()
        max_user = df_user["valor"].max()
        min_user = df_user["valor"].min()
        qtd_user = df_user.shape[0]

        soma_total = df_ano["valor"].sum()
        media_total = df_ano["valor"].mean()
        max_total = df_ano["valor"].max()
        min_total = df_ano["valor"].min()
        qtd_total = df_ano.shape[0]

        def porcento(parcial, total):
            return f" ({(parcial / total):.2%})" if total else ""

        st.metric("Total", f"R$ {soma_user:,.2f}" + porcento(soma_user, soma_total))
        st.metric("Média", f"R$ {media_user:,.2f}" + porcento(media_user, media_total))
        st.metric("Máximo", f"R$ {max_user:,.2f}" + porcento(max_user, max_total))
        st.metric("Mínimo", f"R$ {min_user:,.2f}" + porcento(min_user, min_total))
        st.metric("Registros", f"{qtd_user}" + porcento(qtd_user, qtd_total))

    st.write('---')

    # Função atualizada para gerar URI de imagem base64 compatível com st.column_config.ImageColumn
    def encode_image(img_data):
        try:
            if isinstance(img_data, str):
                if img_data.startswith("b'") or img_data.startswith('b"'):
                    img_data = eval(img_data)  # Transforma string de bytes em bytes reais
                else:
                    img_data = base64.b64decode(img_data)
            return f"data:image/jpeg;base64,{base64.b64encode(img_data).decode('utf-8')}"
        except Exception:
            return None

    # Prepara o DataFrame visual com imagens renderizadas
    df_visual = df_filtrado[["data_dt", "valor", "estabelecimento", "usuario", "imagem"]].copy()
    df_visual["imagem"] = df_visual["imagem"].apply(encode_image)

    st.data_editor(
        df_visual.rename(columns={
            "imagem": "Imagem",
            "data_dt": "Data",
            "valor": "Valor",
            "estabelecimento": "Estabelecimento",
            "usuario": "Usuário"
        }),
        column_config={
            "Imagem": st.column_config.ImageColumn("Imagem"),
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "Estabelecimento": st.column_config.TextColumn("Estabelecimento"),
            "Usuário": st.column_config.TextColumn("Usuário"),
        },
        column_order=["Imagem", "Data", "Valor", "Estabelecimento", "Usuário"],
        use_container_width=True,
        disabled=True
    )
