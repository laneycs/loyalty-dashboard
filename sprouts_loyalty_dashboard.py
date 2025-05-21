
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "uptime": np.random.uniform(95, 100, size=90)
})

def create_card(title, fig_id):
    return dbc.Col(dbc.Card([
        dbc.CardHeader(html.H4(title, style={"marginBottom": "0", "color": "#007A33"})),
        dbc.CardBody(html.Div(id=fig_id))
    ], className="mb-4 shadow-sm"), width=6)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4", style={"fontFamily": "Montserrat, sans-serif", "color": "#1A1A1A"}),

    dbc.Row([
        create_card("Daily Active Users", "graph-dau"),
        create_card("New Signups", "graph-signups"),
        create_card("Basket Size", "graph-basket"),
        create_card("Email Clicks", "graph-email"),
        create_card("System Uptime", "graph-uptime")
    ])
], fluid=True)

@app.callback(Output("graph-dau", "children"), Input("graph-dau", "id"))
def show_dau(_): return dcc.Graph(figure=px.line(df, x="date", y="daily_active_users", title="DAU"))

@app.callback(Output("graph-signups", "children"), Input("graph-signups", "id"))
def show_signups(_): return dcc.Graph(figure=px.bar(df, x="date", y="new_signups", title="Signups"))

@app.callback(Output("graph-basket", "children"), Input("graph-basket", "id"))
def show_basket(_): return dcc.Graph(figure=px.area(df, x="date", y="basket_size", title="Basket Size"))

@app.callback(Output("graph-email", "children"), Input("graph-email", "id"))
def show_email(_): return dcc.Graph(figure=px.bar(df, x="date", y="email_clicks", title="Email Clicks"))

@app.callback(Output("graph-uptime", "children"), Input("graph-uptime", "id"))
def show_uptime(_): return dcc.Graph(figure=px.line(df, x="date", y="uptime", title="System Uptime %"))

if __name__ == "__main__":
    app.run_server(debug=True)
