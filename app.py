import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
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
            html.H1("KeepNAI", style={'color': 'white', 'margin-bottom': '50px'}),
            html.Button('Mapa', id='tab-inicio', n_clicks=0, className='tab-button'),
            html.Button('Resources', id='tab-resources', n_clicks=0, className='tab-button'),
            html.Button('Information', id='tab-information', n_clicks=0, className='tab-button'),
            html.Button('Configuración', id='tab-configuracion', n_clicks=0, className='tab-button'),
        ], className='sidebar'),
        html.Div(id='page-content', className='content')
    ], className='app-container'),
    
    # Hidden div to store all components
    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': i, 'value': i} for i in df['City'].unique()],
            value='SF',
            className='dropdown'
        ),
        dcc.Graph(id='fruit-graph'),
        dcc.Graph(id='chile-map')
    ], style={'display': 'none'})
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
        return render_inicio()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'tab-inicio':
            return render_inicio()
        elif button_id == 'tab-resources':
            return render_resources()
        elif button_id == 'tab-information':
            return render_information()
        elif button_id == 'tab-configuracion':
            return render_configuracion()

def render_inicio():
    return html.Div([
        html.H3('Inicio'),
        html.Div([
            html.Div([
                html.H4('Chile Landscape'),
                dcc.Graph(id='chile-map')
            ], className='card'),
            html.Div([
                html.H4('Fruit Data'),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[{'label': i, 'value': i} for i in df['City'].unique()],
                    value='SF',
                    className='dropdown'
                ),
                dcc.Graph(id='fruit-graph')
            ], className='card')
        ])
    ])

def render_resources():
    return html.Div([
        html.H3('Resources'),
        html.Div([
            html.P('This is the content of the Resources tab.')
        ], className='card')
    ])

def render_information():
    return html.Div([
        html.H3('Information'),
        html.Div([
            html.P('This is the content of the Information tab.')
        ], className='card')
    ])

def render_configuracion():
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

@app.callback(
    Output('chile-map', 'figure'),
    Input('tab-inicio', 'n_clicks')
)
def update_map(_):
    fig = go.Figure(go.Scattermapbox(
        lat=[-33.4489],
        lon=[-70.6693],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text=['Santiago'],
    ))

    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=-33.4489, lon=-70.6693),
            zoom=4,
        ),
        showlegend=False,
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)