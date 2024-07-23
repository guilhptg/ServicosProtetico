import dash
from dash import dash_table
import plotly.express as px
import pandas as pd 
from dash import html, dcc, Input, Output

# Dados dos serviços com chaves atualizadas
import pandas as pd

data = [
    {"Servico": "Metal Cerâmica", "Preco": "250,00"},
    {"Servico": "Munhão Personalizado", "Preco": "80,00"},
    {"Servico": "Coroa Dicilicato", "Preco": "300,00"},
    {"Servico": "Bloco Dicilicato", "Preco": "280,00"},
    {"Servico": "Coroa Ceromero", "Preco": "120,00"},
    {"Servico": "Bloco Ceromero", "Preco": "90,00"},
    {"Servico": "Provisório Unitário", "Preco": "80,00"},
    {"Servico": "Protese Adesiva", "Preco": "150,00"},
    {"Servico": "Núcleo Liga de Prata", "Preco": "140,00"},
    {"Servico": "Núcleo Metal Amarelo", "Preco": "100,00"},
    {"Servico": "Protocolo Cerâmico", "Preco": "3.500,00"},
    {"Servico": "Protocolo Resina", "Preco": "1.300,00"},
    {"Servico": "Protocolo Provisório", "Preco": "700,00"},
    {"Servico": "Protese Total", "Preco": "300,00"},
    {"Servico": "PPA", "Preco": "200,00"},
    {"Servico": "PPR Acrilizada", "Preco": "350,00"},
    {"Servico": "PPFlex", "Preco": "500,00"},
    {"Servico": "Placa Miorrelaxante", "Preco": "150,00"},
    {"Servico": "Placa Clareamento", "Preco": "100,00"},
    {"Servico": "Concertos em Geral Apartir", "Preco": "120,00"}
]

# Convertendo os preços para valores numéricos
def formatar_preco(preco):
    preco_formatado = preco.replace('.', '').replace(',', '.')
    return float(preco_formatado)

# Aplicar a formatação aos preços
for item in data:
    item['Preco'] = formatar_preco(item['Preco'])

# Ordenar os dados pelo preço
ordenado = sorted(data, key=lambda x: x['Preco'])

# Convertendo os dados para um DataFrame
df = pd.DataFrame(ordenado)

# start app

app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# graff

grafico = px.bar(df, x='Servico', y='Preco', title='Preco dos Servicos')

# layout

app.layout = html.Div([
    html.H1(children="Serviços Labor Ice - Dentista"),
     dcc.Input(
        id='search-bar',
        type='text',
        value='',
        placeholder='Pesquisar serviços...'
    ),
    html.Button('Pesquisar', id='search-button', n_clicks=0),

    dash_table.DataTable(
        id='tabela-servicos',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_action='native',
        page_current=0,
        page_size=10
    ),

    dcc.Graph(figure=grafico)

])

@app.callback(
    Output('tabela-servicos', 'data'),
    Input('search-bar', 'value')
)
def update_table(search_value):
    if search_value:
        filtered_df = df[df['Servico'].str.contains(search_value, case=False, na=False)]
    else:
        filtered_df = df
    return filtered_df.to_dict('records')

# ServerExecut

if __name__ == '__main__':
    app.run_server(debug=True)
