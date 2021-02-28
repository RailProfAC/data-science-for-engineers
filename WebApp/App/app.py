# coding: utf8
import os
# Flask imports
from flask import Flask
from flask import render_template
# Data science tools
import pandas as pd
import numpy as np
# Json framework to read data
import json
#Plotly 
import plotly.graph_objs as go
import plotly.offline as po

# Create the Flask app
app = Flask(__name__)

@app.before_first_request
def _run_on_start():
    # Read data here
    global df # Global dataframe, visible in all functions
    x = []
    y = []
    z = []
    for fn in os.listdir('data'):
        with open('data/'+fn) as json_file:   
            json_data = json.load(json_file)
        x.extend(json_data['x'])
        y.extend(json_data['y'])
        z.extend(json_data['v'])
    df = pd.DataFrame({'x': x, 'y': y, 'v': z})
    df = df[df['v'] >= 0]

@app.route("/")
def index():
    try:
        global df
        data = dict(
            y = df['v'],
            type = 'scatter'
        )
        layout = dict(
            title = 'Test Drive Velocity over time',
            xaxis_title="t/s",
            yaxis_title="v/(m/s)",
        )
        fig = dict(data=data, layout=layout)

        plotcode = po.plot(fig, 
        output_type='div',
        validate = True, show_link=False)
        return render_template('chart.html', plotcode=plotcode)
    except Exception as e:
        estr = repr(e)
        return render_template('404.html', ecode=estr), 404
        

@app.route("/geo")
def geo():
    try:
        global df
        data = dict(
            x = df['y'],
            y = df['x'],
            mode = 'markers',
            #hoverinfo = '',
            marker=dict(
                size=5,
                color = 3.6*df['v'], 
                colorscale='Jet',
                showscale=True
            ),
            type = 'scatter'
        )
        
        layout = dict(
            #title = 'Test Drive Velocity v/(km/h)',
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                #autotick=True,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                #autotick=True,
                ticks='',
                showticklabels=False
            ),
        )
        fig = dict(data=data, layout=layout)
        plotcode = po.plot(fig, #include_plotlyjs=False,
        output_type='div',
        validate = True, show_link=False)
        return render_template('chart.html', plotcode=plotcode)
    except Exception as e:
        estr = repr(e)
        return render_template('404.html', ecode=estr), 404
    
@app.route("/hist")
def hist():
    try:
        global df
        data = go.Histogram(
            x = 3.6*df['z']
        )
        layout = dict(
            title = 'Test Drive Velocity Distribution v/(km/h)',
        )

        fig = dict(data=data, layout=layout)
        
        plotcode = po.plot(fig, #include_plotlyjs=False,
        output_type='div',
        validate = True, show_link=False)
        return render_template('chart.html', plotcode=plotcode)
    except Exception as e:
        print(e)
        estr = repr(e)
        return render_template('404.html'), 404

app.run(debug = True, host='0.0.0.0')

