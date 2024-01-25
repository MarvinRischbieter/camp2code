from dash import Dash,dcc,html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import os
import sys
from datetime import datetime, timedelta, time

#################################################################################
# durchläuft das recordverzeichnis und gibt eine liste mit den Dateinamen zurück
#################################################################################
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

#################################################################
# Definition der cards (1: Geschwindigkeit, 2 mittlere Gesch., ...)
#################################################################
card1 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H5("Max Geschwindigkeit", className="card-title"),
            html.H6( " 100 ", id="v_max")
        ]
    ),
    style={"width": "14rem"},
)

card2 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H5("Mittlere Geschwindigkeit", className="card-title"),
            html.H6( " 100 ", id="v_mid")
        ]
    ),
    style={"width": "14rem"},
)

card3 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H5("Min Geschwindigkeit", className="card-title"),
            html.H6( " 100 ", id="v_min")
        ]
    ),
    style={"width": "14rem"},
)

card4 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H5("Fahrzeit", className="card-title"),
            html.H6( " 100 ", id="v_time")
        ]
    ),
    style={"width": "14rem"},
)

card5 = dbc.Card(
    #dbc.CardImg(src="/home/pi/git/camp2code/dash/static/images/squirrel.png", top=True),
    dbc.CardBody(
        [
            html.H5("Distanz", className="card-title"),
            html.H6( " 100 ", id="v_dist")
        ]
    ),
    style={"width": "14rem"},
)

app.layout = html.Div(
    children=[
       
        html.H1(children='Auswertung der Fahrten'),
        dcc.Dropdown( c, c[0], id="Dateiauswahl" ),   
        #dbc.DropdownMenu(label="Datei Auswahl", children=c2),
        dbc.Row(
            [
            dbc.Col([card1], width="auto"),
            dbc.Col([card2], width="auto"),
            dbc.Col([card3], width="auto"),
            dbc.Col([card4], width="auto"),
            dbc.Col([card5], width="auto"),
            ] 
        ),        
        dcc.Graph(id='line_plot') # Graph-Komponente 
    ]
)

#####################################################################
# Callback wird ausgeführt wenn der Inputwert "Auswal" geändert wird.
# Auswahl ist die Dropdown liste mit den Record Dateien.
#####################################################################
@app.callback(Output(component_id='line_plot', component_property='figure'),
              Output(component_id='v_max', component_property="children" ),
              Output(component_id='v_mid', component_property="children" ),
              Output(component_id='v_min', component_property="children" ),
              Output(component_id='v_time', component_property="children" ),
              Output(component_id='v_dist', component_property="children" ),
              Input(component_id='Dateiauswahl', component_property='value'))
def graph_update(value_of_input_component):
    df= pd.read_csv(value_of_input_component,';')  # Dataframe aus der CSV erstellen
    mid = df["Speed"].mean()
    max = df["Speed"].max()
    min = df["Speed"].min()
    v_mid = f"{mid*0.4} cm/s"
    v_max = f"{max*0.4} cm/s"
    v_min = f"{min*0.4} cm/s"

    # Startzeit auslesen und in Datetime umwandeln    
    t1 = df["Time"].iloc[0]
    t2 = t1[:-7]
    starttime = datetime.strptime(t2, '%Y-%m-%d_%H:%M:%S')
    
    # Fahrtende auslesen und in Datetime umwandeln
    t1 = df["Time"].iloc[-1]
    t2 = t1[:-7]
    endtime = datetime.strptime(t2, '%Y-%m-%d_%H:%M:%S') 
    
    #Zeitdifferenz berechnen
    time_dif= endtime - starttime  
    d = mid*time_dif.total_seconds()*0.4  
    d2 = round(d, 2)
    
    # Gesamtdistanz und Fahzeit ermitteln
    v_dist = f"{d2} cm"
    v_time = f"{time_dif.total_seconds()} sec."   
    fig = px.line(df, x='Time', y=['Speed','Angle','Direction',])
    
    return fig,v_max,v_mid,v_min,v_time,v_dist

if __name__ == '__main__':
    app.run_server(debug=True)