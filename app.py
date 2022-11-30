import json
import os

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pandas as pd

import fractals as fracts

style_sheet = [os.path.join("assets", "style.css")]



#app = Dash(__name__, external_stylesheets=style_sheet, use_pages=True)
app = Dash(__name__, external_stylesheets=style_sheet)
server = app.server

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='mandlebrot'
            ),
        html.Div([
            html.H5('Pixel Density', style={'textAlign':'center', 'color':'white'}),
            dcc.Slider(10, 120, 20,
                value=40,
                id='mandlebrot-density-selector'
                ),

        ]),
        
    ], style={'display': 'inline-block', 'width': '49%', 'color':'black'}),
    html.Div([
        dcc.Graph(id='sequence'),
        html.Div([
            html.H5('Iterations', style={'textAlign':'center', 'color':'white'}),
            dcc.Slider(10, 40, 1,
                value=21,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id='num-iterations-selector'
                ),

        ]),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        dcc.Graph(id='julia'),
        html.Div([
            html.H5('Pixel Density', style={'textAlign':'center', 'color':'white'}),
            dcc.Slider(10, 120, 20,
                value=40,
                id='julia-density-selector'
                ),

        ]),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    #dash.page_container
])

@app.callback(
    Output('julia', 'figure'),
    Input('mandlebrot', 'hoverData'),
    Input('julia-density-selector', 'value')
)
def gen_julia(hover_data, value):
    re = 0
    im = 0
    if (hover_data != None):
        points = hover_data['points'][0]
        re = points['x']
        im = points['y']
    
    c = fracts.complex_matrix(-2, 2, -2, 2, pixel_density=value)
    members = fracts.get_members_julia(c, parameter=complex(re, im), num_iterations=20)
    fig = px.scatter(x=members.real, y = members.imag, title='Julia')

    fig.update_layout(
        clickmode='event+select', 
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
        xaxis_title="Re",
        yaxis_title="Im"
        )
    fig.update_traces(marker_color='green')
    if (value >= 60):
        fig.update_traces(marker_size=1)
    elif (value <= 20):
        fig.update_traces(marker_size=3)
    else:
        fig.update_traces(marker_size=2)
    return fig

@app.callback(
    Output('mandlebrot', 'figure'),
    Input('mandlebrot-density-selector', 'value'),
    Input('num-iterations-selector', 'value')
)
def gen_mandlebrot(density, iterations):
    c = fracts.complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=density)
    members = fracts.get_members(c, num_iterations=iterations)
    fig = px.scatter(x=members.real, y = members.imag, title='Mandlebrot')

    fig.update_layout(
        clickmode='event+select', 
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
        xaxis_title="Re",
        yaxis_title="Im"
        )
    if (density >= 60):
        fig.update_traces(marker_size=1)
    elif (density <= 20):
        fig.update_traces(marker_size=3)
    else:
        fig.update_traces(marker_size=2)
    return fig

@app.callback(
    Output('sequence', 'figure'),
    Input('mandlebrot', 'hoverData'),
    Input('num-iterations-selector', 'value')
)
def gen_sequence(hover_data, iterations):
    re = 0
    im = 0
    if (hover_data != None):
        points = hover_data['points'][0]
        re = points['x']
        im = points['y']

    (xList, yList) = fracts.first_n_elements(complex(re, im), iterations)
    
    fig = px.scatter(x=xList, y=yList, title='Sequence')

    fig.update_layout(
        clickmode='event+select', 
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
        xaxis_title="Iteration",
        yaxis_title="Magnitude"
        )

    fig.update_traces(marker_color='red')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)