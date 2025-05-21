import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Dummy data for demo
df = pd.DataFrame({
    "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "Total Registrations": [1200, 1350, 1600, 1750],
    "Repeat Shoppers": [300, 400, 450, 600],
    "Referral Signups": [80, 100, 150, 200],
})

USERNAME_PASSWORD_PAIRS = [["sproutsteam", "dashboard"]]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

app.title = "Sprouts Loyalty Dashboard"

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4 text-center"),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.line(df, x="Week", y="Total Registrations", title="Total Registrations")
        ), md=6),
        dbc.Col(dcc.Graph(
            figure=px.bar(df, x="Week", y="Repeat Shoppers", title="Repeat Shoppers")
        ), md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(
            figure=px.area(df, x="Week", y="Referral Signups", title="Referral Signups")
        ), md=12),
    ])
], fluid=True)