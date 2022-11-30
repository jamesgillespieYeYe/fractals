import json
import os

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import fractals as fracts

style_sheet = [os.path.join("assets", "style.css")]



app = Dash(__name__, external_stylesheets=style_sheet)

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='fractal'
            ),
    ], style={'display': 'inline-block', 'width': '49%', 'color':'black'}),
    html.Div([
        dcc.Graph(id='sequence'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        dcc.Graph(id='julia'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
])

@app.callback(
    Output('julia', 'figure'),
    Input('fractal', 'clickData')
)
def gen_julia(hover_data):
    re = 0
    im = 0
    if (hover_data != None):
        points = hover_data['points'][0]
        re = points['x']
        im = points['y']
    
    c = fracts.complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=21)
    members = fracts.get_members_julia(c, parameter=complex(re, im), num_iterations=20)
    fig = px.scatter(x=members.real, y = members.imag, title='Julia')

    fig.update_layout(clickmode='event+select', plot_bgcolor='rgb(50, 50, 50)', paper_bgcolor="rgba(0, 0, 200, 0)")
    fig.update_traces(marker_color='red')
    return fig

@app.callback(
    Output('fractal', 'figure'),
    Input('submit-val', 'n_clicks')
    
)
def gen_fractal(value):
    c = fracts.complex_matrix(-2, 0.5, -1.5, 1.5, pixel_density=21)
    members = fracts.get_members(c, num_iterations=20)
    fig = px.scatter(x=members.real, y = members.imag, title='Fractal')

    fig.update_layout(clickmode='event+select', plot_bgcolor='rgb(50, 50, 50)', paper_bgcolor="rgba(0, 0, 200, 0)")

    #fig.update_traces(marker_size=5)

    

    return fig
@app.callback(
    Output('sequence', 'figure'),
    Input('fractal', 'hoverData')
    
)
def gen_sequence(hover_data):
    re = 0
    im = 0
    if (hover_data != None):
        points = hover_data['points'][0]
        re = points['x']
        im = points['y']

    (xList, yList) = fracts.first_n_elements(complex(re, im), 10)
    
    fig = px.scatter(x=xList, y=yList, title='Sequence')

    fig.update_layout(clickmode='event+select', plot_bgcolor='rgb(50, 50, 50)', paper_bgcolor="rgba(0, 0, 200, 0)")

    fig.update_traces(marker_color='red')

    

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)