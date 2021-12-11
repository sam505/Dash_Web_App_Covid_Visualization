import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

jur = pd.read_csv(r'COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv', na_values='0')
print(jur.columns)
jur.dropna(inplace=True)
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('US COVID-19 Data Tracker'),
    html.Hr(),
    dcc.RadioItems(
        id='Vaccination-Radio',
        options=[
            {'label': 'Fully Vaccinated', 'value': 'Series_Complete_Pop_Pct'},
            {'label': 'Single Dose', 'value': 'Administered_Dose1_Pop_Pct'}, ],
        value='Series_Complete_Pop_Pct'),
    dcc.Graph(id='graph-one'),
    dcc.Slider(
        id='date-slider',
        min=0,
        max=len(jur['Date'].unique()),
        value=0),
    dcc.Graph(id='graph-two'),
    html.Div([
        dcc.Dropdown(
            id='choosing_state',
            option=[{'label': i, 'value': i} for i in indicators_state],
            value='try'),
        dcc.Dropdown(
            id='choosing_county',
            option=[{'label': i, 'value': i} for i in indicators_county],
            value='try')
        @ app.callback(
            Output(component_id='graph_one', component_property='figure'),
            Input(component_id='date-slider', component_property='value'),
            Input(component_id='Vaccination-Radio', component_property='value')
        )])])


def function_one(date, status):
    if status == 'Series_Complete_Pop_Pct':
        fig = px.choropleth(jur, geojson=counties, locations='Location', locationmode='USA-states',
                            color='Series_Complete_Pop_Pct', color_continuous_scale='Viridis', scope='usa')
    else:
        fig = px.choropleth(jur, geojson=counties, locations='Location', locationmode='USA-states',
                            color='Administered_Dose1_Pop_Pct', color_continuous_scale='Viridis', scope='usa')
    return fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})


if __name__ == '__main__':
    app.run_server(debug=True)
