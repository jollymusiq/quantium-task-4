import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go
import plotly.express as px

# Paths (relative instead of absolute)
df0 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_0.csv")
df1 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_1.csv")
df2 = pd.read_csv("/workspaces/quantium-task-4/new/data/daily_sales_data_2.csv")
df = pd.concat([df0, df1, df2], ignore_index=True)

# Data cleaning
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
df['quantity'] = df['quantity'].astype(int)
df = df[df['product'] == 'pink morsel']
df['Sales'] = df['quantity'] * df['price']
df['region'] = df['region'].str.lower()

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods", style={'font-family': 'Arial'}),
    html.H2("Pink Morsel", style={'font-family': 'Arial'}),
    
    html.Label("Select Region:"),
    dcc.RadioItems(
        id="region-selector",
        options=[{'label': r.capitalize(), 'value': r} for r in ['all','north','south','east','west']],
        value='all',
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Div([
        dcc.Graph(id="sales-graph", style={'width': '50%'}),
        dcc.Graph(id="daily-sales-graph", style={'width': '50%'})
    ], style={'display': 'flex'}),
    
    html.Div(id="drill-output")
])

@app.callback(
    Output("sales-graph", "figure"),
    Output("daily-sales-graph", "figure"),
    Output("drill-output", "children"),
    Input("region-selector", "value"),
    Input("daily-sales-graph", "clickData")
)
def update_graphs(selected_region, clickData):
    filtered_df = df if selected_region == "all" else df[df["region"] == selected_region]

    # Line chart
    daily_sales = filtered_df.groupby(["date", "region"])["Sales"].sum().reset_index()
    line_fig = px.line(daily_sales, x="date", y="Sales", color="region", title="Daily Sales by Region")

    # 3D Scatter
    scatter_fig = go.Figure()
    if selected_region == "all":
        for r in df["region"].unique():
            rd = df[df["region"] == r].sort_values("date")
            scatter_fig.add_trace(go.Scatter3d(
                x=rd["date"].dt.strftime('%Y-%m-%d'),
                y=[r] * len(rd),
                z=rd["price"],
                mode="lines+markers",
                name=r.capitalize()
            ))
    else:
        rd = filtered_df.sort_values("date")
        scatter_fig.add_trace(go.Scatter3d(
            x=rd["date"].dt.strftime('%Y-%m-%d'),
            y=[selected_region] * len(rd),
            z=rd["price"],
            mode="lines+markers",
            name=selected_region.capitalize()
        ))

    scatter_fig.update_layout(title="3D Daily Price Trend", template="plotly_white")

    # Drill info
    drill_info = ""
    if clickData:
        clicked_date = pd.to_datetime(clickData["points"][0]["x"])
        clicked_year = clicked_date.year
        year_data = df[df["date"].dt.year == clicked_year]
        drill_info = html.Div([
            html.H3(f"Drill-through: {clicked_year}"),
            html.P(f"Total Sales: ${year_data['Sales'].sum():,.2f}"),
            html.P(f"Average Price: ${year_data['price'].mean():.2f}")
        ])

    return line_fig, scatter_fig, drill_info

if __name__ == "__main__":
    app.run(debug=True)
