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
    dcc.Store(id='viewport_data'),
])

@callback(
    Output('relayout-data', 'children'),
    Input('picture', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

@callback(
    Output('picture', 'figure'),
    Output('viewport_data', 'data'),
    Input('picture', 'relayoutData'),
    Input('viewport_data', 'data')
)
def display_image(relay, data):
    viewport = proxy_viewport()
    if (relay != None):
        if 'autosize' not in relay:
            #Pixel Coordinates
            xMin = relay['xaxis.range[0]']
            xMax = relay['xaxis.range[1]']
            yMin = relay['yaxis.range[0]']
            yMax = relay['yaxis.range[1]']

            xCenter = (xMin + xMax) // 2
            yCenter = (yMin + yMax) // 2
            #Retrieve viewport from data
            stored = json.loads(data)
            print("stored: ", stored)
            proxyImage = Image.new(mode="L", size=(stored['image_width'], stored['image_height']))
            oldViewport = Viewport(proxyImage, center = complex(stored['center_re'], stored['center_im']), width = stored['width'])
            newWidth = ((xMax - xMin) / (proxyImage.width)) * oldViewport.width
            print("newWidth: ", newWidth)
            pixel = Pixel(viewport=oldViewport, x=xCenter, y=yCenter)
            viewport = generate_image(center=complex(pixel), width=newWidth)
    img = np.array(Image.open(image_path))
    fig = px.imshow(img, color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
    )
    viewport_data = ViewportData(viewport).toJson()
    #print("viewport data: ", viewport_data)
    
    
    
    return (fig, viewport_data)