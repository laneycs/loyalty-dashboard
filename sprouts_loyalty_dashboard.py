
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dummy data
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "uptime": np.random.uniform(95, 100, size=90),
    "state": np.random.choice(["CA", "TX", "NY", "FL", "IL", "AZ", "MI"], size=90)
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

def group_data(metric):
    return {
        "daily": df[["date", metric]],
        "weekly": df.groupby("week").agg({metric: "sum"}).reset_index().rename(columns={"week": "date"}),
        "monthly": df.groupby("month").agg({metric: "sum"}).reset_index().rename(columns={"month": "date"})
    }

grouped_data = {
    "daily_active_users": group_data("daily_active_users"),
    "new_signups": group_data("new_signups"),
    "basket_size": group_data("basket_size"),
    "email_clicks": group_data("email_clicks"),
    "uptime": group_data("uptime")
}

# Regional map data
map_data = df.groupby("state").size().reset_index(name="users")

# App setup
app = Dash(__name__)
server = app.server

app.layout = html.Div(style={
    "backgroundColor": "#FFFFFF",
    "padding": "30px",
    "fontFamily": "Open Sans, sans-serif"
}, children=[
    html.H1("Sprouts Loyalty Dashboard", style={
        "textAlign": "left", "color": "#1A1A1A", "fontFamily": "Montserrat, sans-serif"
    }),

    html.Div([
        html.H2("📈 Daily Active Users"),
        dcc.Dropdown(id="toggle-dau", options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"},
        ], value="daily", style={"width": "200px"}),
        html.Div(id="graph-dau")
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("📊 New Signups"),
        dcc.Dropdown(id="toggle-signups", options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"},
        ], value="daily", style={"width": "200px"}),
        html.Div(id="graph-signups")
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("📦 Basket Size"),
        dcc.Dropdown(id="toggle-basket", options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"},
        ], value="daily", style={"width": "200px"}),
        html.Div(id="graph-basket")
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("📧 Email Clicks"),
        dcc.Dropdown(id="toggle-email", options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"},
        ], value="daily", style={"width": "200px"}),
        html.Div(id="graph-email")
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("🛠️ Uptime %"),
        dcc.Dropdown(id="toggle-uptime", options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"},
        ], value="daily", style={"width": "200px"}),
        html.Div(id="graph-uptime")
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("🗺️ Users by Region (Map)"),
        dcc.Graph(figure=px.choropleth(map_data, locations="state", locationmode="USA-states",
            color="users", scope="usa", title="User Distribution by State"))
    ], style={"marginBottom": "40px"})
])

@app.callback(Output("graph-dau", "children"), Input("toggle-dau", "value"))
def update_dau(view):
    fig = px.line(grouped_data["daily_active_users"][view], x="date", y="daily_active_users", title="Active Users")
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-signups", "children"), Input("toggle-signups", "value"))
def update_signups(view):
    fig = px.bar(grouped_data["new_signups"][view], x="date", y="new_signups", title="New Signups")
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-basket", "children"), Input("toggle-basket", "value"))
def update_basket(view):
    fig = px.area(grouped_data["basket_size"][view], x="date", y="basket_size", title="Basket Size Over Time")
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-email", "children"), Input("toggle-email", "value"))
def update_email(view):
    fig = px.bar(grouped_data["email_clicks"][view], x="date", y="email_clicks", title="Email Clicks")
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-uptime", "children"), Input("toggle-uptime", "value"))
def update_uptime(view):
    fig = px.line(grouped_data["uptime"][view], x="date", y="uptime", title="System Uptime %")
    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)
