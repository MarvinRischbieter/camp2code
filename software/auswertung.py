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

dateiliste = csv_dateien_einlesen()
#parameterlist=['Speed','Angle']

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
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div(
    children=[
       
        html.H1(children='Auswertung der Fahrten'),
        dcc.Dropdown( dateiliste, dateiliste[0], id="Dateiauswahl", style ={'backgroundColor': "#ffffff",'color': '#660066'}  ),   
        dcc.RadioItems(options= ['Speed', 'Angle','Direction','Distance','Infra'], value='Speed',
                id='fahrdaten',
                inline=True
            ),
        dbc.Row(
            [
            dbc.Col([card1], width="auto"),
            dbc.Col([card2], width="auto"),
            dbc.Col([card3], width="auto"),
            dbc.Col([card4], width="auto"),
            dbc.Col([card5], width="auto"),
            ] 
        ),        
        dcc.Graph(id='line_plot'), # Graph Basis
        #dcc.Graph(id='line_plot_dist'), # Graph-Komponente 
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
              Input(component_id='Dateiauswahl', component_property='value'),
              Input(component_id='fahrdaten', component_property='value'),)
def graph_update(value_of_input_component,fahrdaten):

    df= pd.read_csv(value_of_input_component,';')  # Dataframe aus der CSV erstellen
    # Datafram um die Spalte Time ergänzen (ohne Datum und Millisekunden)
    Timestamp= df["Time"]
    Time = []
    for t in Timestamp:
        Time.append(t[11:-7])
    Timeseries = pd.Series(Time) 
    df["Time2"] = Timeseries
    
    ################################################################
    # Wenn die Datei IR Values enthält. wird der Dataframe um 
    # min, max, Mittelwert und Index des kleinsten Ir Werts ergänst
    if "IR Value" in df :
        # listen für den Ir Werte initialisieren
        ir_min = []  
        ir_max = []
        ir_mid = []
        ir_index =[]
 
        Infra = df["IR Value"]         # series mit den Ir Werten
        min = 100
        mid = -100
        max = 0
        
        for p in Infra:        # schleife über die Infrarotwerte 
            p1=list(p.replace("[","").replace("]","").split(","))       # String mit den IR werten in eine Liste wandeln
            p2=list(map(float,p1))                                      # Werte der Liste in floats mapen
            
            for f in p2:          # schleife über die Werte der 5 Sensoren
                if f < min: min = f
                if f > max: max = f
                mid = mid+f
            # Ir werte anhängen 
            ir_min.append(min)  
            ir_max.append(max)
            ir_mid.append(mid)
            ir_index.append(p2.index(min))
            # rücksetzen der werte 
            min = 100   
            max = -100
            mid = 0
        
        # Datafram um die IR Werte ergänzen    
        df["IR-Min"] = ir_min
        df["IR-Max"] = ir_max
        df["IR-Mid"] = ir_mid
        df["IR-Index"] = ir_index

    # Extremwerte der Fahrt ermitteln
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
    if "IR Value" not in df and fahrdaten =="Infra":
        fig = px.line(df, x='Time2', y=["Speed"])
    elif "IR Value" in df and fahrdaten =="Infra":
        fig = px.line(df, x='Time2', y=['IR-Min', 'IR-Max','IR-Index'])
    else:
        fig = px.line(df, x='Time2', y=[fahrdaten])
    
    return fig,v_max,v_mid,v_min,v_time,v_dist
'''
@app.callback(Output(component_id='line_plot_dist', component_property='figure'),
              Input(component_id='Dateiauswahl', component_property='value'))
def graph_update(value_of_input_component):
    df= pd.read_csv(value_of_input_component,';')  # Dataframe aus der CSV erstellen
    Timestamp= df["Time"]
    Time = []
    for t in Timestamp:
        Time.append(t[11:-7])
    Timeseries = pd.Series(Time) 
    df["Time2"] = Timeseries
    fig2 = px.line(df, x='Time2', y=['Distance'])
    return fig2
'''

if __name__ == '__main__':
    app.run_server(debug=True)