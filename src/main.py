import plotly.graph_objects as go
import csv
import argparse
import os
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.offline import plot

data_csv = 'data/data.csv'
colours_csv = 'data/colours.csv'
delimiter: str = ','
quotechar: str = '|'
datetime_format: str = '%Y.%m.%d'
order_y = True
order_y_reverse = True
title = "Engines updates"
xaxis_title = "Date"
yaxis_title = "Engine"
display_mode = 'offline_html'
# display_mode = 'online_builtin'
# display_mode = 'online_dash'


def load_data(data_file: str):
    with open(data_file, newline='') as csvfile:
        raw_data = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for raw_line in raw_data:
            if len(raw_line) != 2:
                raise Exception(f'Not 2 data in csv: {raw_line}')
            yield raw_line


def convert_data():
    series_names = []
    series_data = {}
    for raw_name, raw_value in load_data(data_csv):
        if raw_name not in series_names:
            series_names.append(raw_name)
            series_data[raw_name] = []
        series_data[raw_name].append(datetime.strptime(raw_value, datetime_format))
        if order_y:
            series_names.sort(reverse=order_y_reverse)
    return series_names, series_data


def get_colour_gen(colours_file: str):
    with open(colours_file, newline='') as csvfile:
        for colour in csvfile:
            yield colour.strip()


names, series = convert_data()
colour_gen = get_colour_gen(colours_csv)
fig = go.Figure()
for name in names:
    a_series = series[name]
    fig.add_trace(go.Scatter(
        x=a_series,
        y=[name] * len(a_series),
        marker=dict(color=next(colour_gen), size=12, symbol="circle"),
        mode="markers",
        name=name,
    ))

fig.update_layout(
    title=title,
    xaxis_title=xaxis_title,
    yaxis_title=yaxis_title
)

if display_mode == 'offline_html':
    plot(
        fig,
        auto_open=False,
        filename='/output/plot_result.html'
    )

if display_mode == 'online_builtin':
    fig.show()

if display_mode == 'online_dash':
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(
        debug=False,
        use_reloader=False,
        port=8050,
        host='0.0.0.0',
    )
