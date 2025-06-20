import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

df = pd.read_csv("D:/ecommerce_estatistica.csv", sep=",", encoding="utf-8")

def converter_vendas(valor):
    if pd.isna(valor):
        return 0
    valor_str = str(valor).lower().replace(".", "").replace("mil", "000")
    try:
        return int(valor_str)
    except ValueError:
        return 0

df["Qtd_Vendidos"] = df["Qtd_Vendidos"].apply(converter_vendas)

def limpar_temporada(temp):
    if pd.isna(temp):
        return "não definido"
    temp = temp.lower().strip()

    if "primavera" in temp and "verão" in temp:
        return "primavera/verão"
    elif "outono" in temp and "inverno" in temp:
        return "outono/inverno"
    elif "primavera" in temp or "verão" in temp:
        return "primavera/verão"
    elif "outono" in temp or "inverno" in temp:
        return "outono/inverno"
    elif "2021" in temp:
        return "2021"
    else:
        return temp

df["Temporada"] = df["Temporada"].apply(limpar_temporada)

top_marcas = df.groupby("Marca")["Qtd_Vendidos"].sum().sort_values(ascending=False).head(5).reset_index()
fig1 = px.bar(top_marcas, x="Marca", y="Qtd_Vendidos",
              title="Top 5 Marcas Mais Vendidas", text_auto=True)

preco_material = df.groupby("Material")["Preço"].mean().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(preco_material, x="Material", y="Preço",
              title="Preço Médio por Material", text_auto=".2f")

nota_genero = df.groupby("Gênero")["Nota"].mean().reset_index()
fig3 = px.bar(nota_genero, x="Gênero", y="Nota",
              title="Nota Média por Gênero", text_auto=".2f")

desconto_temporada = df.groupby("Temporada")["Desconto"].mean().reset_index()
fig4 = px.bar(desconto_temporada, x="Temporada", y="Desconto",
              title="Desconto Médio por Temporada", text_auto=".1f")

app = dash.Dash(__name__)
app.title = "Dashboard E-commerce"

app.layout = html.Div([
    html.H1("Dashboard de E-commerce", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label="Marcas Mais Vendidas", children=[
            dcc.Graph(figure=fig1)
        ]),
        dcc.Tab(label="Preço por Material", children=[
            dcc.Graph(figure=fig2)
        ]),
        dcc.Tab(label="Nota por Gênero", children=[
            dcc.Graph(figure=fig3)
        ]),
        dcc.Tab(label="Desconto por Temporada", children=[
            dcc.Graph(figure=fig4)
        ]),
    ])
])


if __name__ == "__main__":
    app.run(debug=True)
