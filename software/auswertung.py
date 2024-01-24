from dash import Dash,dcc,html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import os
import sys

def csv_dateien_einlesen():
    csv_dateien = []
    for path, subdirs, files in os.walk("/home/pi/git/camp2code/software/records"):
        for name in files:
            datei= os.path.join(path, name)
            #print (datei)
            if "csv" in datei:
                #dic = {datei:datei}
                csv_dateien.append(datei)
    return csv_dateien

c = csv_dateien_einlesen()

app = Dash(external_stylesheets=[dbc.themes.DARKLY])
card1 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H4("Geschwindigkeit", className="card-title"),
            html.P(
                "Geschwindikeit des Fahrzeugs über die Zeit",
                className="card-text",
            ),
            dbc.Button("Geschwindigkeit", color="primary"),
        ]
    ),
    style={"width": "14rem"},
)

card2 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H4("Lenkwinkel", className="card-title"),
            html.P(
                "Lenkwinkel des Fahrzeugs über die Zeit",
                className="card-text",
            ),
            dbc.Button("Lenkwinkel", color="primary"),
        ]
    ),
    style={"width": "14rem"},
)

app.layout = html.Div(
    children=[
       
        html.H1(children='Auswertung der Fahrten'),
        dcc.Dropdown( c, c[0], id="Auswahl" ),   
         dbc.Row(
            [
            dbc.Col([card1], width="auto"),
            dbc.Col([card2], width="auto"),
            #dbc.Col([card], width=4)
            #dbc.Col([card], width=4)
            ] 
        ),
        dcc.Graph(id='line_plot') # Graph-Komponente 
        #dcc.Dropdown( ['hallo','test'], 'test', id="Auswahl" )
    ]
)

@app.callback(Output(component_id='line_plot', component_property='figure'),
              Input(component_id='Auswahl', component_property='value'))
def graph_update(value_of_input_component):
    #print(f"Value of input component : {value_of_input_component}")
    df= pd.read_csv(value_of_input_component,';')
    fig = px.line(df, x=df['Time'], y=df['Speed'])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)