import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dummy-Daten für Geschwindigkeit, Lenkwinkel und Fahrrichtung
speed_data = random.uniform(0, 100)
steering_angle_data = random.uniform(-90, 90)
direction_data = random.choice(['Vorwärts', 'Rückwärts'])

# Layout der App
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("RaspberryPi Car Dashboard", className="mx-auto text-center", style={"background-color": "#1e3a5c", "color": "white", "padding-top": "20px", "padding-bottom": "20px"}),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Geschwindigkeit", className="card-title"),
                                html.P(f"{speed_data:.2f} km/h", className="card-text"),
                            ]
                        )
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Lenkwinkel", className="card-title"),
                                html.P(f"{steering_angle_data:.2f} °", className="card-text"),
                            ]
                        )
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Fahrrichtung", className="card-title"),
                                html.P(direction_data, className="card-text"),
                            ]
                        )
                    )
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button("Fahrparcours 1", id="btn-parcours-1", n_clicks=0, color="primary", className="mb-2")),
                dbc.Col(dbc.Button("Fahrparcours 2", id="btn-parcours-2", n_clicks=0, color="primary", className="mb-2")),
                dbc.Col(dbc.Button("Fahrparcours 3", id="btn-parcours-3", n_clicks=0, color="primary", className="mb-2")),
                dbc.Col(dbc.Button("Fahrparcours 4", id="btn-parcours-4", n_clicks=0, color="primary", className="mb-2")),
                dbc.Col(dbc.Button("Fahrparcours 5", id="btn-parcours-5", n_clicks=0, color="primary", className="mb-2")),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button("Stopp", id="btn-stop", n_clicks=0, color="danger", className="mb-2")),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# Callbacks für die Aktualisierung der Daten
@app.callback(
    [Output("btn-parcours-1", "n_clicks"),
     Output("btn-parcours-2", "n_clicks"),
     Output("btn-parcours-3", "n_clicks"),
     Output("btn-parcours-4", "n_clicks"),
     Output("btn-parcours-5", "n_clicks"),
     Output("btn-stop", "n_clicks")],
    [Input("btn-parcours-1", "n_clicks"),
     Input("btn-parcours-2", "n_clicks"),
     Input("btn-parcours-3", "n_clicks"),
     Input("btn-parcours-4", "n_clicks"),
     Input("btn-parcours-5", "n_clicks"),
     Input("btn-stop", "n_clicks")]
)
def update_buttons(*clicks):
    return clicks

if __name__ == "__main__":
    app.run_server(debug=True)
