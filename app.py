import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime
import json
import os

today = datetime.datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
maptoken = os.getenv('MAPBOXTOKEN')

data = pd.read_csv(f'output_data-{today}.csv')
try:
    old_data = pd.read_csv(f'output_data-{yesterday}.csv')
except:
    old_data = data
lga_name19 = data.lga_name19.fillna('nan').unique()
lga_name19.sort()
postcodes = data.postcode.unique()
postcodes.sort()

df = pd.read_csv('mapdata.csv')
with open('lgamap_rs.json', 'r') as f:
    lgas = json.load(f)

def maplotting():
    fig = go.Figure(go.Choroplethmapbox(geojson=lgas, locations=df.id, z=df.infections, colorscale='Reds', zmin=0, zmax=174, hovertext=df['LGAName']))
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=maptoken, mapbox_zoom=9, mapbox_center={"lat":-33.864694,"lon":151.208308})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def orderedList(bycol):
    b = data.groupby(bycol)['_id'].count()
    a = b.sort_values(ascending=False).head()
    return html.Ul(
        [html.Li("Top 5 LGAs:", className='collection-header')]+[html.Li(f"{i}: {a.loc[i]}", className='collectionItem') for i in a.index],
        className='collection with-header'
    )

def total_infections():
    fig = go.Figure()

    total = data['_id'].nunique()
    oldtotal = old_data['_id'].nunique()
    fig.add_trace(go.Indicator(
        value=total,
        mode='number+delta',
        delta={'reference': oldtotal},
        title={'text': "Total Infections"}
    ))
    return fig


external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']
app = dash.Dash(__name__, external_scripts=external_js, external_stylesheets=external_stylesheets)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>My Dashboard</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
app.layout = html.Div(children=[
    html.H4(children='NSW Infections'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dcc.Dropdown(
                                id='radio1',
                                options=[
                                    {'label': 'Postcodes', 'value': 'postcode'},
                                    {'label': 'Local Government Area', 'value': 'LGA'}
                                ],
                                value='Poscodes',
                                multi=False
                            )
                        ],
                        className='col s6')
                        ,
                        html.Div(children=[
                            dcc.Dropdown(
                                id='generaldropdown',
                                multi=False
                            )
                        ],
                        className='col s6')
                    ],
                    className='row'),
                    html.Div(children=[
                        html.Div(children=[
                        dcc.Graph(
                            'bar_plot',
                            config={'displayModeBar': False}
                        )
                        ],
                        className='col s12'
                    )
                    ],
                    className='row')
                
            ],
            className='card white'
            )
        ],
        className='col s12 l6'
        ),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Span(children=[
                            'Infection Map'
                        ],
                        className='card-title'
                        ),
                        dcc.Graph(
                            figure=maplotting(),
                            config={'displayModeBar': False}
                        )
                    ],
                    className='col s12'
                    )
                ],
                className='row'
                )
            ],
            className='card white'
            )
        ],
        className='col s12 l6'
        )
    ],
    className='row'
    ),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(
                    figure=total_infections(),
                    config={'displayModeBar': False}
                )
            ])
        ],
        className='col s12 l6'
        ),
        html.Div(children=[
            orderedList('lga_name19')
        ])
    ],
    className='row')
    ])
])

@app.callback(
    Output(component_id='bar_plot', component_property='figure'),
    [Input(component_id='generaldropdown', component_property='value'),
    Input(component_id='radio1', component_property='value')]
)
def bar_plot(dropdown, radio):
    if dropdown is None:
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        return fig
    if not dropdown:
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        return fig
    if radio == 'LGA':
        cols = 'lga_name19'
        df = data.loc[data[cols] == dropdown, ['notification_date','_id']]
    elif radio == 'postcode':
        cols = 'postcode'
        df = data.loc[data[cols] == float(dropdown), ['notification_date','_id']]
    
    g = df.groupby('notification_date').count()
    g['cumsum'] = g.cumsum()
    y = g['_id'].values
    y2 = g['cumsum'].values
    x = g.index.values
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(
        go.Bar(name='Notifications', x=x, y=y),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(name='Total Infections', x=x, y=y2),
        secondary_y=True
    )
    fig.update_layout(
        legend_orientation='h',
        xaxis_title='Notification Date',
        legend=dict(
            x=0,
            y=1
        ),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )
    fig.update_yaxes(title_text="Daily Notifications", secondary_y=False)
    fig.update_yaxes(title_text="Total Notifications", secondary_y=True)

    return fig

@app.callback(
    Output(component_id='generaldropdown', component_property='options'),
    [Input(component_id='radio1', component_property='value')]
)
def switchdropdown(input_values):
    ans=[]
    if input_values == 'LGA':
        ans = [{'label': str(i), 'value': i} for i in lga_name19]
    elif input_values == 'postcode':
        ans = [{'label': str(i), 'value': str(i)} for i in postcodes]
    return ans


@app.callback(
    Output(component_id='generaldropdown', component_property='value'),
    [Input(component_id='radio1', component_property='value')]
)
def setdefauldropdown(input_values):
    ans = ''
    return ans


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
