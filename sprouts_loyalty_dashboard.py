
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create dummy data
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

df_weekly = df.groupby("week").agg({"daily_active_users": "sum"}).reset_index().rename(columns={"week": "date"})
df_monthly = df.groupby("month").agg({"daily_active_users": "sum"}).reset_index().rename(columns={"month": "date"})

# Initialize app
app = Dash(__name__)
server = app.server

# App layout
app.layout = html.Div(style={
    "backgroundColor": "#FFFFFF",
    "padding": "30px",
    "fontFamily": "Open Sans, sans-serif"
}, children=[
    html.H1("Sprouts Loyalty Dashboard", style={
        "textAlign": "left", "color": "#1A1A1A", "fontFamily": "Montserrat, sans-serif"
    }),

    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginTop": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("📈 Daily Active Users", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="dau-view-toggle",
                options=[
                    {"label": "Daily", "value": "daily"},
                    {"label": "Weekly", "value": "weekly"},
                    {"label": "Monthly", "value": "monthly"}
                ],
                value="daily",
                clearable=False,
                style={
                    "width": "180px",
                    "fontSize": "14px",
                    "border": "1px solid #ccc",
                    "borderRadius": "6px"
                }
            )
        ]),
        html.Div(id="dau-graph-container", style={"marginTop": "20px"}),
        html.P("This chart shows the number of active users over time. Use the toggle to view by day, week, or month.",
               style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ])
])

@app.callback(
    Output("dau-graph-container", "children"),
    Input("dau-view-toggle", "value")
)
def update_dau_graph(view):
    if view == "weekly":
        data = df_weekly
        title = "Weekly Active Users"
    elif view == "monthly":
        data = df_monthly
        title = "Monthly Active Users"
    else:
        data = df
        title = "Daily Active Users"

    fig = px.line(data, x="date", y="daily_active_users", title=title)
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)
