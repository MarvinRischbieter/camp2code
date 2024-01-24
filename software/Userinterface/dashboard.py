import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import csv
import os

csv_file_path = 'software/Userinterface/text.csv'

max_speed_data = [0]
min_speed_data = [0]
avg_speed_data = [0]
total_distance_data = [0]
total_time_data = [0]

print("Dateien im aktuellen Verzeichnis:", os.listdir())

try:
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

        if data:
            max_speed_data = [float(row['max_speed']) for row in data]
            min_speed_data = [float(row['min_speed']) for row in data]
            avg_speed_data = [float(row['avg_speed']) for row in data]
            total_distance_data = [float(row['total_distance']) for row in data]
            total_time_data = [float(row['total_time']) for row in data]
except FileNotFoundError:
    print(f"Die CSV-Datei '{csv_file_path}' wurde nicht gefunden.")
    data = []

dev_stalesheet = ['src/css/stylesheet.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dev_stalesheet])

timestamps = [datetime.now() - timedelta(minutes=i * 10) for i in range(10)]  # Beispiel: Zeitstempel für die letzten 10 Zeiträume

# Layout der App
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1("Raspberry Car Dashboard", className="text-center text-white m-0 p-3 h-100")
                            ],
                            className="col-md-11 p-0 text-center",
                        ),
                        html.Div(
                            [
                                html.P(id='current-datetime', className="text-right text-white align-middle m-0 p-3 h-100"),
                            ],
                            className="col-md-1 p-0 text-center m-0",  
                        ),
                    ],
                    className="row m-0 shadow align-middle", style={"background-color": "#0d4671"},  
                ),
            ],
        ),
        # Interval-Komponente zum Aktualisieren von Datum und Uhrzeit
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Alle 1000 Millisekunden aktualisieren (1 Sekunde)
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Maximum Speed", className="card-title"),
                                html.P(f"{max_speed_data[-1]:.2f} km/h", className="card-text"),
                            ]
                        ),
                        className="shadow"
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Minimum Speed", className="card-title"),
                                html.P(f"{min_speed_data[-1]:.2f} km/h", className="card-text"),
                            ]
                        ),
                        className="shadow"
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Average Speed", className="card-title"),
                                html.P(f"{avg_speed_data[-1]:.2f} km/h", className="card-text"),
                            ]
                        ),
                        className="shadow"
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Total Distance Traveled", className="card-title"),
                                html.P(f"{total_distance_data[-1]:.2f} km", className="card-text"),
                            ]
                        ),
                        className="shadow"
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Total Driving Time", className="card-title"),
                                html.P(f"{total_time_data[-1]:.2f} hours", className="card-text"),
                            ]
                        ),
                        className="shadow"
                    ),
                ),
            ],
            className="mb-4 mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.Div(
                                    [
                                        html.H4("Drivedata Chart", className="card-title text-center flex-grow-1"),
                                        dbc.DropdownMenu(
                                            [
                                                dbc.DropdownMenuItem("Maximale Geschwindigkeit", id="max-speed-option"),
                                                dbc.DropdownMenuItem("Minimale Geschwindigkeit", id="min-speed-option"),
                                                dbc.DropdownMenuItem("Durchschnittsgeschwindigkeit", id="avg-speed-option"),
                                                dbc.DropdownMenuItem("Zurückgelegte Gesamtfahrstrecke", id="total-distance-option"),
                                                dbc.DropdownMenuItem("Gesamtfahrzeit", id="total-time-option"),
                                            ],
                                            label="Daten auswählen",
                                            right=True,
                                            className="ms-auto",
                                        ),
                                    ],
                                    className="d-flex align-items-center",  # Hiermit werden die Elemente vertikal zentriert
                                ),
                            ),
                            dbc.CardBody(
                                [
                                    dcc.Graph(
                                        id='max-speed-graph',
                                        figure={
                                            'data': [
                                                {'x': timestamps, 'y': max_speed_data, 'type': 'line', 'name': 'Maximale Geschwindigkeit'},
                                            ],
                                            'layout': {
                                                'title': 'Entwicklung der Maximalen Geschwindigkeit',
                                                'xaxis': {'title': 'Zeit'},
                                                'yaxis': {'title': 'Maximale Geschwindigkeit (km/h)'},
                                            }
                                        }
                                    ),
                                ]
                            ),
                        ],
                        className="shadow"
                    ),
                ),
            ],
            className="mb-4 mt-4",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('current-datetime', 'children'),
    Input('interval-component', 'n_intervals'),
)

def update_datetime(n):
    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime

@app.callback(
    Output('max-speed-graph', 'figure'),
    Input('max-speed-option', 'n_clicks'),
    Input('min-speed-option', 'n_clicks'),
    Input('avg-speed-option', 'n_clicks'),
    Input('total-distance-option', 'n_clicks'),
    Input('total-time-option', 'n_clicks'),
)

def update_graph(max_speed_clicks, min_speed_clicks, avg_speed_clicks, total_distance_clicks, total_time_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'max-speed-option' in changed_id:
        y_data = max_speed_data
        title = 'Entwicklung der Maximalen Geschwindigkeit'
    elif 'min-speed-option' in changed_id:
        y_data = min_speed_data
        title = 'Entwicklung der Minimalen Geschwindigkeit'
    elif 'avg-speed-option' in changed_id:
        y_data = avg_speed_data
        title = 'Entwicklung der Durchschnittsgeschwindigkeit'
    elif 'total-distance-option' in changed_id:
        y_data = total_distance_data
        title = 'Entwicklung der Zurückgelegten Gesamtfahrstrecke'
    elif 'total-time-option' in changed_id:
        y_data = total_time_data
        title = 'Entwicklung der Gesamtfahrzeit'
    else:
        y_data = max_speed_data
        title = 'Entwicklung der Maximalen Geschwindigkeit'

    # Erstellen Sie das aktualisierte Diagramm
    figure = {
        'data': [
            {'x': timestamps, 'y': y_data, 'type': 'line', 'name': title},
        ],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Zeit'},
            'yaxis': {'title': 'Werte'},
        }
    }
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)

