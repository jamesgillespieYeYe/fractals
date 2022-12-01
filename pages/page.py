from dash import Dash, dcc, html, callback
import json
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pandas as pd
import os
import numpy as np
from PIL import Image
from image_generation import generate_image, proxy_viewport
from viewport import *

dash.register_page(
	__name__,
)

image_path = os.path.join("assets", "image.jpg")

layout = html.Div(children=[
    html.H1(children='Functions'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Graph(
        id="picture"
    ),
    html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**
            """),
            html.Pre(id='relayout-data'),
        ], className='three columns'),
    dcc.Store(id='viewport_data', storage_type='session'),
    dcc.Store(id='generated', storage_type='session')
])

@callback(
    Output('relayout-data', 'children'),
    Input('picture', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


def pixel_center(relay):
    print("relay asdfasdf:", relay)
    xMin = relay['xaxis.range[0]']
    xMax = relay['xaxis.range[1]']
    yMin = relay['yaxis.range[1]']
    yMax = relay['yaxis.range[0]']
    x = (xMax - xMin) // 2 + xMin
    y = (yMax - yMin) // 2 + yMin
    print(x, y)
    return (x, y)
def offset(center, width):
    return center + complex(-width, width) / 2
def scale(width, image_width=256):
    return width / image_width

def pixel_to_complex(x:int, y:int, scale, offset):
    return complex(x, -y)*scale + offset

@callback(
    Output('picture', 'figure'),
    Output('viewport_data', 'data'),
    Output('generated', 'data'),
    Input('picture', 'relayoutData'),
    Input('viewport_data', 'data'),
    Input('generated', 'data')
)
def display_image(relay, data, generated):
    print("generated:", generated)
    if generated == None:
        print("Generating initial image")
        print(generated)
        generated = json.dumps("{True}")
        generate_image(center = -1, width = 2)
        data = json.dumps({'center_re':-1, 'center_im':0,  'width':2})
    else:

        
        print(relay)
        if relay != None:
            if 'xaxis.autorange' in relay and 'yaxis.autorange' in relay:
                print("Reseting to default")
                generate_image(center = -1, width = 2)
                data = json.dumps({'center_re':-1, 'center_im':0,  'width':2})
            elif 'xaxis.range[0]' in relay:
                print("Change")
                
                data_dict = json.loads(data)
                print(type(data_dict))
                data_dict['width'] = data_dict['width'] / 2

                

                pcenter = pixel_center(relay)
                ccenter = pixel_to_complex(pcenter[0], pcenter[1], 
                    scale(data_dict['width']), 
                    offset(complex(data_dict['center_re'], 
                    data_dict['center_im']), data_dict['width'])
                    )
                data_dict['center_re'] = ccenter.real
                data_dict['center_im'] = ccenter.imag


                generate_image(center=complex(data_dict['center_re'], data_dict['center_im']), width=data_dict['width'])
                data = json.dumps(data_dict)
                

    img = np.array(Image.open(image_path))
    fig = px.imshow(img, color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
    )
    
    print("data: ", data)
    return (fig, data, generated)