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
    yearly_rec, avg_sales_type, total_exp, unemployed_sales = df
    chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year',y='Automobile_Sales', title="Automobile Sales Over Time"))
    chart2 = dcc.Graph(figure=px.bar(avg_sales_type, x='Vehicle_Type', y='Automobile_Sales', title="Automobile Sales by Vehicle Type"))
    chart3 = dcc.Graph(figure=px.pie(total_exp, names='Vehicle_Type', values='Advertising_Expenditure', title="Advertising Expenditure by Vehicle Type"))
    chart4 = dcc.Graph(figure=px.bar(unemployed_sales, x='unemployment_rate', y='Automobile_Sales', title="Unemployment Rate Effect on Automobile Sales by Vehicle Type"))
    
    return [
            html.Div(className='chart-item', children=[html.Div(children=chart1), html.Div(children=chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=chart3), html.Div(children=chart4)]),
            ]
       
def compute_recession_info(recession_data):
    yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    avg_sales_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    total_exp = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    unemployed_sales = recession_data.groupby(['unemployment_rate','Vehicle_Type'])['Automobile_Sales'].sum().reset_index()
    return yearly_rec, avg_sales_type, total_exp, unemployed_sales
    
# Run the app
if __name__ == '__main__':
    app.run_server()