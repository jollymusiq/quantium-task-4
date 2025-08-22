import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.express as px

def load_data():
    df0 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_2.csv")
    df1 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_1.csv")
    df2 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_2.csv")
    df = pd.concat([df0, df1, df2], ignore_index=True)

    df['date'] = pd.to_datetime(df['date'])
    df['price'] = df['price'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
    df['quantity'] = df['quantity'].astype(int)
    df = df[df['product'] == 'pink morsel']
    df['sales'] = df['quantity'] * df['price']
    df['region'] = df['region'].str.lower()
    return df

def update_graphs(selected_region, start_date, end_date):
    df = load_data()

    df['date'] = pd.to_datetime(df['date'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # filter by region
    if selected_region.lower() != "all":
        df = df[df["region"].str.lower() == selected_region.lower()]

    # filter by date range
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if df.empty:
        return px.line(title="No data"), px.scatter(title="No data"), "No data available for selection."

    daily_sales = df.groupby(["date", "region"])["sales"].sum().reset_index()

    line_fig = px.line(
        daily_sales, x="date", y="sales", color="region", 
        title="Daily Sales by Region"
    )

    scatter_fig = px.scatter(
        daily_sales, x="date", y="sales", color="region", 
        size="sales", title="Sales Scatter Plot"
    )

    return line_fig, scatter_fig, ""

def create_dash_app():
    df = load_data()

    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Soul Foods", id="header-h1"),
        html.H2("Pink Morsel", id="header-h2"),

        html.Label("Select Region:"),
        dcc.RadioItems(
            id="region-selector",
            options=[{'label': r.capitalize(), 'value': r} for r in ['all','north','south','east','west']],
            value='all'
        ),

        dcc.DatePickerRange(
            id="date-picker",
            start_date=df["date"].min(),
            end_date=df["date"].max()
        ),

        html.Button("Submit", id="submit-button"),

        dcc.Graph(id="line-graph"),
        dcc.Graph(id="scatter-graph"),

        html.Div(id="error-message", style={"color": "red"})
    ])

    @app.callback(
        Output("line-graph", "figure"),
        Output("scatter-graph", "figure"),
        Output("error-message", "children"),
        Input("region-selector", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    )
    def update_graph_callback(selected_region, start_date, end_date):
        return update_graphs(selected_region, start_date, end_date)

    return app

if __name__ == "__main__":
    create_dash_app().run(debug=True)
