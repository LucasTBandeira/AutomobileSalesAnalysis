# Import required libraries
import calendar
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Variables
year_list = [i for i in range(1980, 2024, 1)]
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Dark theme CSS
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# Initialize the Dash app with the dark theme
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Build dash app layout
app.layout = html.Div(
    style={"backgroundColor": "#1E1E1E", "color": "white"},
    children=[
        html.H1("Automobile Sales Statistics Dashboard", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label(
                    "Select Statistics:",
                    style={"padding": "3px", "font-size": "20px", "color": "white"},
                ),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=[
                        {"label": "Yearly Statistics", "value": "Yearly Statistics"},
                        {
                            "label": "Recession Period Statistics",
                            "value": "Recession Period Statistics",
                        },
                    ],
                    value="Yearly Statistics",
                    placeholder="Select a Report Type",
                    style={
                        "padding": "3px",
                        "font-size": "20px",
                        "text-align-last": "center",
                        "color": "black",
                    },
                ),
            ],
            style={"width": "50%"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": i, "value": i} for i in year_list],
                    placeholder="Select a Year",
                    style={
                        "padding": "3px",
                        "font-size": "20px",
                        "text-align-last": "center",
                        "color": "black",
                    },
                )
            ],
            style={"width": "50%"},
        ),
        html.Div(
            [
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={"display": "flex"},
                ),
            ]
        ),
    ],
)


# Creating Callbacks
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False
    else:
        return True


@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="select-year", component_property="value"),
        Input(component_id="dropdown-statistics", component_property="value"),
    ],
)
def update_output_container(selected_year, selected_statistics):
    if (selected_year and selected_statistics == "Yearly Statistics"):
        return yearly_report(selected_year)
    elif selected_statistics == "Recession Period Statistics":
        return recession_report()
    else:
        return None
    

def yearly_report(selected_year):
    df = compute_yearly_info(data[data["Year"] == selected_year])
    yearly_sales, monthly_sales, avg_sales_type, adv_exp = df
    monthly_sales = monthly_sales.sort_values(by="Month", key=lambda x: x.map({month: i for i, month in enumerate(month_order)}))
    chart1 = dcc.Graph(
        figure=px.line(
            yearly_sales,
            x="Year",
            y="Automobile_Sales",
            title="Automobile Sales Over Time",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart2 = dcc.Graph(
        figure=px.line(
            monthly_sales,
            x="Month",
            y="Automobile_Sales",
            title="Automobile Sales by Month",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart3 = dcc.Graph(
        figure=px.bar(
            avg_sales_type,
            x="Vehicle_Type",
            y="Automobile_Sales",
            title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(selected_year),
            color="Vehicle_Type",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart4 = dcc.Graph(
        figure=px.pie(
            adv_exp,
            names="Vehicle_Type",
            values="Advertising_Expenditure",
            title="Advertising Expenditure by Vehicle Type in the Year {}".format(selected_year),
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    return [
        html.Div(className="chart-item", children=[chart1, chart2], style={"flex": "50%"}),
        html.Div(className="chart-item", children=[chart3, chart4], style={"flex": "50%"}),
    ]


def compute_yearly_info(yearly_data):
    yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
    avg_sales_type = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    adv_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    return yearly_sales, monthly_sales, avg_sales_type, adv_exp


def recession_report():
    df = compute_recession_info(data[data["Recession"] == 1])
    yearly_rec, avg_sales_type, total_adv_exp, unemployed_sales = df

    # Apply dark theme to charts and customize chart colors
    chart1 = dcc.Graph(
        figure=px.line(
            yearly_rec,
            x="Year",
            y="Automobile_Sales",
            title="Automobile Sales Over Time",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart2 = dcc.Graph(
        figure=px.bar(
            avg_sales_type,
            x="Vehicle_Type",
            y="Automobile_Sales",
            title="Automobile Sales by Vehicle Type",
            color="Vehicle_Type",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart3 = dcc.Graph(
        figure=px.pie(
            total_adv_exp,
            names="Vehicle_Type",
            values="Advertising_Expenditure",
            title="Advertising Expenditure by Vehicle Type",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )
    chart4 = dcc.Graph(
        figure=px.bar(
            unemployed_sales,
            x="unemployment_rate",
            y="Automobile_Sales",
            title="Unemployment Rate Effect on Automobile Sales by Vehicle Type",
            color="Vehicle_Type",
        ).update_layout(template="plotly_dark"),
        style={"width": "100%"},
    )

    return [
        html.Div(className="chart-item", children=[chart1, chart2], style={"flex": "50%"}),
        html.Div(className="chart-item", children=[chart3, chart4], style={"flex": "50%"}),
    ]


def compute_recession_info(recession_data):
    yearly_rec = recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
    avg_sales_type = (recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index())
    total_adv_exp = (recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index())
    unemployed_sales = (recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"].sum().reset_index())
    return yearly_rec, avg_sales_type, total_adv_exp, unemployed_sales


# Run the app
if __name__ == "__main__":
    app.run_server()
