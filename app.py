from dash import Dash, html, dcc
import dash
import os
style_sheet = [os.path.join("assets", "style.css")]
app = Dash(__name__, use_pages=True, external_stylesheets=style_sheet)
server = app.server

app.layout = html.Div([
	html.H1('Fractals', style={'textAlign':'center'}),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)