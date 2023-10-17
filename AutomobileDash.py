# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Variables
year_list = [i for i in range(1980, 2024, 1)]
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = 'Automobile Statistics Dashboard'

# Build dash app layout
app.layout = html.Div([
    html.H1('Automobile Sales Statistics Dashboard', style={'text-align': 'center', 'color': '#503D36', 'font-size': 24}),
                       
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a Report Type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a Year',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# Creating Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='disabled')
    )

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return yearly_report(selected_year)
    else:
        return recession_report()

def yearly_report(selected_year):
    df = compute_yearly_info(data[data['Year'] == selected_year])
    return

def compute_yearly_info(yearly_data):
     return
 
def recession_report():
    df = compute_recession_info(data[data['Recession'] == 1])
    return
       
def compute_recession_info(recession_data):
    return
    
# Run the app
if __name__ == '__main__':
    app.run_server()