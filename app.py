from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import json
from dash.dependencies import Input, Output

data_jurisdiction = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv")
data_county = pd.read_csv(r"COVID-19_Vaccinations_in_the_United_States_County.csv")
data_county = data_county[data_county.Recip_State != "UNK"]
data_original = pd.read_csv(r"United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv")
dates = data_county.Date.unique().tolist()
orig_dates = list(data_original.report_date.unique())
indicators_state = list(data_county.Recip_State.unique())
indicators_county = list(data_county.Recip_County.unique())
dates.reverse()

markers = {}
length = len(dates)
points = 10
for m in range(points):
    markers[int(length / points * m)] = dates[int(length / points * m)]

counties = json.load(open('geojson-counties-fips.json'))

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
                   value=30,
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
                dcc.Graph(
                    id='graph-2'
                ),
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
                    options=[],
                    style={"width": "50%"},
                    value="Madera County"
                ),
                html.Br(),
                dcc.RangeSlider(
                    id='input-7',
                    min=0,
                    max=100,
                    step=0.5,
                    value=[30, 50],
                    marks={},
                    allowCross=False
                ),
                dcc.Graph(id='graph-3'),
                dcc.Graph(id='graph-4')
            ], className="six columns")],
            className="row"
        )
    ]
)


@app.callback(
    Output(component_id='input-4', component_property='options'),
    Input(component_id='input-3', component_property='value'),
    Input(component_id='input-4', component_property='value')
)
def get_counties(input_3, input_4):
    county_s = data_county[data_county.Recip_State == input_3]
    county_s = county_s.Recip_County.unique().tolist()
    county_list = [{'label': i, 'value': i} for i in county_s]

    return county_list


@app.callback(
    Output(component_id='graph-1', component_property='figure'),
    Input(component_id='input-1', component_property='value'),
    Input(component_id='input-2', component_property='value')
)
def choropleth_1(input_1, input_2):
    data_choropleth1 = data_county[data_county.Date == dates[input_2]]
    fig1 = px.choropleth(data_choropleth1,
                         locations='Recip_State',
                         locationmode='USA-states',
                         color=input_1,
                         range_color=[0, 100],
                         color_continuous_scale='Viridis',
                         scope='usa',
                         labels={input_1: "% vaccinated"})
    return fig1.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


@app.callback(
    Output(component_id='graph-2', component_property='figure'),
    Input(component_id='input-3', component_property='value'),
    Input(component_id='input-5', component_property='value'),
    Input(component_id='input-6', component_property='value'),
)
def choropleth_2(input_3, input_5, input_6):
    data_choropleth2 = data_county[data_county.Date == dates[input_6]]
    data_choropleth2 = data_choropleth2[data_choropleth2.Recip_State == input_3]
    fig = px.choropleth(
        data_choropleth2,
        range_color=[0, 100],
        locations="FIPS",
        geojson=counties,
        color=input_5,
        scope="usa",
        hover_name="Recip_County"
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


@app.callback(
    Output(component_id='graph-3', component_property='figure'),
    Output(component_id='input-7', component_property='marks'),
    Input(component_id='input-4', component_property='value'),
    Input(component_id='input-7', component_property='value')
)
def positivity_1(input_4, input_7):
    data_positivity = data_original[data_original.county_name == input_4]
    pos_length = len(data_positivity)
    data_positivity.reset_index(inplace=True)
    data_positivity = data_positivity.loc[pos_length / 100 * int(input_7[0]):pos_length / 100 * int(input_7[1])]
    data_positivity["percent_test_results_reported_positive_last_7_days"] = pd.to_numeric(
        data_positivity["percent_test_results_reported_positive_last_7_days"], errors='coerce')
    data_positivity = data_positivity[data_positivity.percent_test_results_reported_positive_last_7_days.notna()]
    fig = px.line(
        data_positivity,
        "report_date",
        "percent_test_results_reported_positive_last_7_days"
    )
    markers_orig = {}
    positivity_dates = data_positivity.report_date.tolist()
    length_positivity = len(positivity_dates)
    for n in range(points):
        markers_orig[int(100 / points * n)] = positivity_dates[int(length_positivity / points * n)]
    return fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0}), markers_orig


@app.callback(
    Output(component_id='graph-4', component_property='figure'),
    Input(component_id='input-4', component_property='value'),
    Input(component_id='input-7', component_property='value')
)
def positivity_2(input_4, input_7):
    data_positivity = data_original[data_original.county_name == input_4]
    pos_length = len(data_positivity)
    data_positivity.reset_index(inplace=True)
    data_positivity = data_positivity.loc[pos_length/100*int(input_7[0]):pos_length/100*int(input_7[1])]
    data_positivity["cases_per_100K_7_day_count_change"] = pd.to_numeric(
        data_positivity["cases_per_100K_7_day_count_change"], errors='coerce')
    data_positivity = data_positivity[data_positivity.cases_per_100K_7_day_count_change.notna()]
    fig = px.line(
        data_positivity,
        "report_date",
        "cases_per_100K_7_day_count_change"
    )
    return fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


if __name__ == "__main__":
    app.run_server(debug=True)
