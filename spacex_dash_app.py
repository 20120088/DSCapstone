import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

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
            {'lable': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'lable': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'lable': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'lable': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value = 'ALL',
        placeholder = 'Select a Launch Site here',
        searchable = True
    ),

    html.Br(),

    html.Div(dcc.Graph(id = 'success-pie-chart')),
    html.Br(),

    html.P('Payload range (Kg):'),

    #Task3

    html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)

def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site', 'class']].groupby(by = ['Launch Site']).mean()
    filtered_df.rename(columns = {'class': 'Success'}, inplace = True)
    filtered_df['Failure'] = 1 - filtered_df['Success']
    if entered_site == 'ALL':
        fig = px.pie(
            data = filtered_df.reset_index(),
            values = 'Success',
            names = 'Launch Site',
            title = 'Success Launch by Site'
        )
    else:
        fig = px.pie(
            values = filtered_df.loc[entered_site].values,
            name = filtered_df.loc[entered_site].keys(),
            title = 'Success/Failure Launch by ' + entered_site
        )
    return fig

#Task4

if __name__ == '__main__':
    app.run_server()