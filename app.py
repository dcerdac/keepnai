import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Create some sample data
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 1, 2, 2, 4, 5],
    'City': ['SF', 'SF', 'SF', 'NYC', 'MTL', 'NYC']
})

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("My Dash App", style={'color': 'white', 'margin-bottom': '50px'}),
            html.Button('Inicio', id='tab-inicio', n_clicks=0, className='tab-button'),
            html.Button('Resources', id='tab-resources', n_clicks=0, className='tab-button'),
            html.Button('Information', id='tab-information', n_clicks=0, className='tab-button'),
            html.Button('Configuración', id='tab-configuracion', n_clicks=0, className='tab-button'),
        ], className='sidebar'),
        html.Div(id='page-content', className='content')
    ], className='app-container')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('tab-inicio', 'n_clicks'),
     Input('tab-resources', 'n_clicks'),
     Input('tab-information', 'n_clicks'),
     Input('tab-configuracion', 'n_clicks')]
)
def display_page(btn1, btn2, btn3, btn4):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div([
            html.H3('Inicio'),
            html.Div([
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': i, 'value': i} for i in df['City'].unique()],
                    value='SF',
                    className='dropdown'
                ),
                dcc.Graph(id='fruit-graph')
            ], className='card')
        ])
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'tab-inicio':
            return html.Div([
                html.H3('Inicio'),
                html.Div([
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=[{'label': i, 'value': i} for i in df['City'].unique()],
                        value='SF',
                        className='dropdown'
                    ),
                    dcc.Graph(id='fruit-graph')
                ], className='card')
            ])
        elif button_id == 'tab-resources':
            return html.Div([
                html.H3('Resources'),
                html.Div([
                    html.P('This is the content of the Resources tab.')
                ], className='card')
            ])
        elif button_id == 'tab-information':
            return html.Div([
                html.H3('Information'),
                html.Div([
                    html.P('This is the content of the Information tab.')
                ], className='card')
            ])
        elif button_id == 'tab-configuracion':
            return html.Div([
                html.H3('Configuración'),
                html.Div([
                    html.P('This is the content of the Configuración tab.')
                ], className='card')
            ])

@app.callback(
    Output('fruit-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    filtered_df = df[df['City'] == selected_city]
    fig = px.bar(filtered_df, x='Fruit', y='Amount', title=f'Fruit in {selected_city}')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#2c3e50'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)