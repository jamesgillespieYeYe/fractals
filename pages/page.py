from dash import Dash, dcc, html, callback, no_update, callback_context
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

default_width = 2

dash.register_page(
	__name__,
)

image_path = os.path.join("assets", "image.jpg")

layout = html.Div(children=[
    html.H1(children='Select an area on the image to zoom in'),
    #html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div([
        dcc.Graph(
            id="picture",
            style={'width': '90vh', 'height': '90vh'}
        ),
        dcc.Dropdown(['twilight', 'twilight_shifted', 'hsv', 'viridis'], 'twilight', id='colormap',persistence=True),
        
    ],style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
            html.Div([
                html.H5('Pixels', style={'textAlign':'center', 'color':'white'}),
                dcc.Slider(256, 1024, 128,
                    value=256,
                    id='pixels',
                    vertical=True,
                    persistence=True
                    ),
            ], className='four columns'),
            # html.Div([
            #     html.H5('Other', style={'textAlign':'center', 'color':'white'}),
            #     dcc.Slider(10, 120, 20,
            #         value=40,
            #         id='other',
            #         vertical=True
            #         ),
            # ], className='four columns'),
            # html.Div([
            #     html.H5('Other', style={'textAlign':'center', 'color':'white'}),
            #     dcc.Slider(10, 120, 20,
            #         value=40,
            #         id='other2',
            #         vertical=True
            #         ),
            # ], className='four columns'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="picture3",
                        style={'width': '50vh', 'height': '45vh'}
                    ),
                    dcc.Graph(
                        id="picture4",
                        style={'width': '50vh', 'height': '45vh'}
                    ),
                ], className = 'column'), 
                
            
        
            ],className='four columns', style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),

        ], className='row', style={'float': 'center', 'display': 'inline-block'}),
        
    
    
    # html.Div([
    #         dcc.Markdown("""
    #             **Zoom and Relayout Data**
    #         """),
    #         html.Pre(id='relayout-data'),
    #     ], className='three columns'),
    dcc.Store(id='viewport_data', storage_type='session'),
    dcc.Store(id='generated', storage_type='session')
])

#--------------------------------------------------------
def pixel_center(relay):
    #print("relay asdfasdf:", relay)
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

def get_width_ratio(relay, default=256):
    xMin = relay['xaxis.range[0]']
    xMax = relay['xaxis.range[1]']
    return (xMax - xMin) / default
#--------------------------------------------------------

@callback(
    Output('picture3', 'figure'),
    Input('picture', 'hoverData'),
    Input('viewport_data', 'data'),
    Input('pixels', 'value')
)
def gen_picture3(hover_data, viewport_data, num_pixels):
    print("hoverdata: ", hover_data)
    print('viewport data: ', viewport_data)
    if (hover_data == None):
        print("No update")
        return no_update
    
    
    
    points = hover_data['points'][0]
    print("points: ", points)
    x = points['x']
    y = points['y']

    #Convert points into complex coordinates
    if viewport_data != None and 'width' in viewport_data:
        print("Can generate points")
        data_dict = json.loads(viewport_data)
        #Scale
        scale_ratio = scale(width=data_dict['width'], image_width=num_pixels)
        print("scale: ", scale_ratio)
        #Offset
        center_re = data_dict['center_re']
        center_im = data_dict['center_im']
        center = complex(center_re, center_im)
        offset_value = offset(center=center, width=data_dict['width'])
        print("offset_value: ", offset_value)
        complex_point = pixel_to_complex(x=x, y=y, scale=scale_ratio, offset=offset_value)
        print("Complex point: ", complex_point)

    else:
        print("Necessary information to generate points not available")


    

    return None

# @callback(
#     Output('relayout-data', 'children'),
#     Input('picture', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)



@callback(
    Output('picture', 'figure'),
    Output('viewport_data', 'data'),
    Output('generated', 'data'),
    Input('picture', 'relayoutData'),
    Input('viewport_data', 'data'),
    Input('generated', 'data'),
    Input('pixels', 'value'),
    Input('colormap', 'value')
)
def display_image(relay, data, generated, num_pixels, map_name):
    
    # print("--------------")
    # print(relay)
    # print(data)
    # print(generated)
    # print(callback_context.triggered)
    # print("--------------")
    # if relay == None and generated != None:
    #     print("returning no update")
    #     return (no_update, no_update, no_update)
    # elif (callback_context.triggered[0]['prop_id'] == '.'):
    #     print("bruh")
    # print("generated:", generated)
    # if (callback_context.triggered[0]['prop_id'] == 'picture.relayoutData'):
    #     if 'autosize' in relay:
    #         return (no_update, no_update, no_update)
    print("-----------------------------------------------------")
    print("Triggered by: ", callback_context.triggered)
    if generated == None:
        print("Generating initial image")
        print(generated)
        generated = json.dumps("{True}")
        generate_image(center = -1, width = default_width, dimension=num_pixels, map=map_name)
        data = json.dumps({'center_re':-1, 'center_im':0,  'width':default_width})
    else:

        
        #print(relay)
        if relay != None:
            #print("num_pixels: ", num_pixels)
            if 'xaxis.autorange' in relay and 'yaxis.autorange' in relay:
                print("Reseting to default")
                generate_image(center = -1, width = default_width, colormap=True, map=map_name)
                data = json.dumps({'center_re':-1, 'center_im':0,  'width':default_width})
            elif 'xaxis.range[0]' in relay:
                print("Change in zoom")
                
                data_dict = json.loads(data)
                print(type(data_dict))
                

                

                pcenter = pixel_center(relay)
                #print("pcenter: ", pcenter)
                ccenter = pixel_to_complex(pcenter[0], pcenter[1], 
                    scale(data_dict['width'], image_width=num_pixels), 
                    offset(complex(data_dict['center_re'], 
                    data_dict['center_im']), data_dict['width'])
                    )
                data_dict['center_re'] = ccenter.real
                data_dict['center_im'] = ccenter.imag

                data_dict['width'] = data_dict['width'] * get_width_ratio(relay, num_pixels)


                generate_image(center=complex(data_dict['center_re'], data_dict['center_im']), width=data_dict['width'], dimension=num_pixels, colormap=True, map=map_name)
                data = json.dumps(data_dict)
            elif callback_context.triggered[0]['prop_id'] == 'pixels.value':
                print("Change in pixels")
                data_dict = json.loads(data)
                generate_image(center=complex(data_dict['center_re'], data_dict['center_im']), width=data_dict['width'], dimension=num_pixels, colormap=True, map=map_name)
                data = json.dumps(data_dict)
            elif callback_context.triggered[0]['prop_id'] == 'colormap.value':
                print("Change in colormap")
                data_dict = json.loads(data)
                generate_image(center=complex(data_dict['center_re'], data_dict['center_im']), width=data_dict['width'], dimension=num_pixels, colormap=True, map=map_name)
                data = json.dumps(data_dict)
            else:
                print("No change")
        else:
            print("Relay is None; no change")

    img = np.array(Image.open(image_path))
    fig = px.imshow(img, color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        plot_bgcolor='rgb(50, 50, 50)', 
        paper_bgcolor="rgba(0, 0, 200, 0)",
    )
    
    #print("data: ", data)
    return (fig, data, generated)