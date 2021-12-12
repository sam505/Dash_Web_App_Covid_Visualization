from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import json
from dash.dependencies import Input, Output

data_jurisdiction = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv")
data_county = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_County.csv")
data_original = pd.read_csv(r"United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv")
dates = list(data_county.Date.unique())
indicators_state = list(data_county.Recip_State.unique())
indicators_county = list(data_county.Recip_County.unique())
dates.reverse()

markers = {}
length = len(dates)
points = 10
for m in range(10):
    markers[int(length / points * m)] = dates[int(length / points * m)]

with open('geojson-counties-fips.json') as json_data:
    counties = json.load(json_data)

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children="US COVID 19 DATA TRACKER", style={"text-align": "center"}),
        html.Hr(),
        dcc.RadioItems(id='input-1',
                       options=[{'label': 'Fully Vaccinated', 'value': 'Series_Complete_Pop_Pct'},
                                {'label': 'Single Dose', 'value': 'Administered_Dose1_Pop_Pct'}, ],
                       value='Series_Complete_Pop_Pct',
                       labelStyle={'display': 'inline-block'}
                       ),
        dcc.Graph(id='graph-1'),
        dcc.Slider(id='input-2',
                   min=0,
                   max=len(dates),
                   value=1,
                   marks=markers),
        html.Hr(),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='input-3',
                    options=[{'label': i, 'value': i} for i in indicators_state],
                    value=indicators_state[0],
                    style={"width": "50%"}),
                dcc.RadioItems(id='input-5',
                               options=[{'label': 'Fully Vaccinated', 'value': 'Series_Complete_Pop_Pct'},
                                        {'label': 'Single Dose', 'value': 'Administered_Dose1_Pop_Pct'}, ],
                               value='Series_Complete_Pop_Pct',
                               labelStyle={'display': 'inline-block'}),
                dcc.Graph(id='graph-2'),
                dcc.Slider(id='input-6',
                           min=0,
                           max=len(dates),
                           value=1,
                           marks=markers)
            ],
                className="six columns"),
            html.Div([
                dcc.Dropdown(
                    id='input-4',
                    options=[{'label': i, 'value': i} for i in indicators_county],
                    value=indicators_county[0],
                    style={"width": "50%"}
                ),
                html.Br(),
                dcc.RangeSlider(
                        id='input-7',
                        min=0,
                        max=20,
                        step=0.5,
                        value=[5, 15]
                    ),
                dcc.Graph(id='graph-3'),
                dcc.Graph(id='graph-4')
            ], className="six columns")],
            className="row"
        )
    ]
)


@app.callback(
    Output(component_id='graph-1', component_property='figure'),
    Output(component_id='graph-2', component_property='figure'),
    Input(component_id='input-1', component_property='value'),
    Input(component_id='input-2', component_property='value'),
    Input(component_id='input-3', component_property='value'),
    Input(component_id='input-4', component_property='value'),
    Input(component_id='input-5', component_property='value'),
    Input(component_id='input-6', component_property='value'),
    Input(component_id='input-7', component_property='value')
)
def function_one(input_1, input_2, input_3, input_4, input_5, input_6, input_7):
    fig1 = px.choropleth(data_county[data_county.Date == dates[input_2]], geojson=counties,
                         locations='Recip_State',
                         locationmode='USA-states',
                         color=input_1,
                         range_color=[0, 100],
                         color_continuous_scale='Viridis',
                         scope='usa',
                         labels={input_1: "% vaccinated"})
    fig2 = px.choropleth(data_county[data_county.Recip_State == input_3], geojson=counties,
                         locations='Recip_County',
                         locationmode='USA-states',
                         color=input_5,
                         range_color=[0, 100],
                         color_continuous_scale='Viridis',
                         scope='usa',
                         labels={input_1: "% vaccinated"})
    return fig1.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0}),\
           fig2.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


if __name__ == "__main__":
    app.run_server(debug=True)
