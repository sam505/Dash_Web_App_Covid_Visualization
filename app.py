from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json
from dash.dependencies import Input, Output

data_jurisdiction = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv")
data_county = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_County.csv")
data_original = pd.read_csv(r"United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv")
dates = list(data_jurisdiction.Date.unique())
indicators_state = list(data_county.Recip_State.unique())
indicators_county = list(data_county.Recip_County.unique())
dates.reverse()

markers = {}
length = len(dates)
for m in range(20):
    markers[int(length / 20 * m)] = dates[int(length / 20 * m)]

with open('geojson-counties-fips.json') as json_data:
    counties = json.load(json_data)

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children="US COVID 19 DATA TRACKER", style={"text-align": "center"}),
        html.Hr(),
        dcc.RadioItems(id='Vaccination-Radio',
                       options=[{'label': 'Fully Vaccinated', 'value': 'Series_Complete_Pop_Pct'},
                                {'label': 'Single Dose', 'value': 'Administered_Dose1_Pop_Pct'}, ],
                       value='Series_Complete_Pop_Pct'),
        dcc.Graph(id='choropleth'),
        dcc.Slider(id='date-slider',
                   min=0,
                   max=len(dates),
                   value=1,
                   marks=markers),
        html.Hr(),
        html.Br(),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='choosing_state',
                    options=[{'label': i, 'value': i} for i in indicators_state],
                    value=indicators_state[0],
                    style={"width": "50%"}
                )
            ], className="six columns"),
            html.Div([
                dcc.Dropdown(
                    id='choosing_county',
                    options=[{'label': i, 'value': i} for i in indicators_county],
                    value=indicators_county[0],
                    style={"width": "50%"}
                )
            ], className="six columns")]
        )
    ]
)


@app.callback(
    Output(component_id='choropleth', component_property='figure'),
    Input(component_id='date-slider', component_property='value'),
    Input(component_id='Vaccination-Radio', component_property='value')
)
def function_one(date, status):
    fig = px.choropleth(data_jurisdiction[data_jurisdiction.Date == dates[date]], geojson=counties,
                        locations='Location',
                        locationmode='USA-states',
                        color=status,
                        range_color=[0, 100],
                        color_continuous_scale='Viridis',
                        scope='usa',
                        labels={status: "% vaccinated"})
    return fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


if __name__ == "__main__":
    app.run_server(debug=True)
