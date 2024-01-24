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
            html.H4("Max Geschwindigkeit", className="card-title"),
            html.P(
                "Maximale Geschwindikeit des Fahrzeugs über die Zeit",
                className="card-text",
            ),
            html.P( " 100 ", id="v_max")
        ]
    ),
    style={"width": "14rem"},
)

card2 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H4("Mittlere Geschwindigkeit", className="card-title"),
            html.P(
                "Mittlere Geschwindikeit des Fahrzeugs",
                className="card-text",
            ),
            html.P( " 100 ", id="v_mid")
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
              Output(component_id='v_max', component_property="children" ),
              Output(component_id='v_mid', component_property="children" ),
              Input(component_id='Auswahl', component_property='value'))
def graph_update(value_of_input_component):
    #print(f"Value of input component : {value_of_input_component}")
    df= pd.read_csv(value_of_input_component,';')
    #global max_geschwindigkeit = df
    mid = df["Speed"].mean()
    max = df["Speed"].max()
    print(f"Mittlere Geschwindigkeit:  { mid}")
    print(f"Max Geschwindigkeit:  { max}")
    fig = px.line(df, x='Time', y=['Speed','Angle'])
    return fig,max,mid

if __name__ == '__main__':
    app.run_server(debug=True)