import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

data = spacex_df[['Launch Site', 'class']].groupby(by = ['Launch Site']).agg({'class': ['sum', 'count']})
data.columns = ['Success', 'Total']
data['Total'] = data['Total'] - data['Success']
data.columns = ['Success', 'Failure']

app = dash.Dash(__name__)

app.layout = html.Div(children = [
    html.H1('SpaceX Launch Records Dashboard', 
        style = {
            'textAlign': 'center', 
            'color': '#503D36',
            'font-size': 40}),

    dcc.Dropdown(
        id = 'site-dropdown', 
        options = [
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value = 'ALL',
        placeholder = 'Select a Launch Site here',
        searchable = True
    ),

    html.Br(),

    html.Div(dcc.Graph(id = 'success-pie-chart')),
    html.Br(),

    html.P('Payload range (Kg):'),

    dcc.RangeSlider(
        id = 'payload-slider',
        min = 0,
        max = 10000,
        step = 1000,
        marks = dict(zip(
            list(range(0, 10001, 1000)), 
            list(map(str,list(range(0, 10001, 1000)))))),
        value = [min_payload, max_payload],
    ),

    html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            data.reset_index(),
            values = 'Success',
            names = 'Launch Site',
            title = 'Success Launch by Site'
        )
    else:
        fig = px.pie(
            values = data.loc[entered_site].values,
            names = data.loc[entered_site].keys(),
            title = 'Success/Failure Launch by ' + entered_site
        )
    return fig

@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')
)

def get_scatter_chart(entered_site, payload_range):
    data = spacex_df[
        (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
        (spacex_df['Payload Mass (kg)'] >= payload_range[0])
    ]
    if entered_site != 'ALL':
        data = data[data['Launch Site'] == entered_site]
    
    data['Booster Version'] = list(map(lambda x : x.split()[1], data['Booster Version']))
    
    fig = px.scatter(
        data,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Success Launch by Booster Version by ' + entered_site + ' site'
    )
    fig.update_layout(legend_title_text = 'Booster Version')
    
    return fig

if __name__ == '__main__':
    app.run_server()