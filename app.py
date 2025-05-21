
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import flask
import plotly.express as px
import pandas as pd

# Server and app initialization
server = flask.Flask(__name__)
server.secret_key = 'sproutsteam'

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sprouts Loyalty Dashboard"

# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=30),
    "Total Registered Users": range(100, 130),
    "Repeat Users": [i * 0.6 for i in range(100, 130)],
    "New Users": [i * 0.4 for i in range(100, 130)],
    "Revenue": [i * 10 for i in range(100, 130)]
})

# Layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Sprouts Loyalty Dashboard", className="my-4"),
        html.Div(id='login-prompt', children=[
            dcc.Input(id="password", type="password", placeholder="Enter passcode", className="mb-2"),
            html.Button("Login", id="login-button", n_clicks=0),
            html.Div(id="login-message")
        ]),
        html.Div(id='main-dashboard', style={"display": "none"}, children=[
            dcc.Dropdown(
                id='metric-selector',
                options=[
                    {"label": "Total Registered Users", "value": "Total Registered Users"},
                    {"label": "Repeat vs New Users", "value": "Repeat vs New Users"},
                    {"label": "Revenue Over Time", "value": "Revenue"}
                ],
                value="Total Registered Users",
                className="mb-4"
            ),
            dcc.Graph(id="metric-graph"),
            html.Div(id="metric-explanation", className="mt-4")
        ])
    ])
])

# Callbacks
@app.callback(
    Output('main-dashboard', 'style'),
    Output('login-message', 'children'),
    Input('login-button', 'n_clicks'),
    State('password', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, password):
    if password in ["sproutsteam", "loyalty rocks"]:
        flask.session['logged_in'] = True
        return {"display": "block"}, ""
    return {"display": "none"}, "Incorrect passcode."

@app.callback(
    Output('metric-graph', 'figure'),
    Output('metric-explanation', 'children'),
    Input('metric-selector', 'value')
)
def update_graph(metric):
    if metric == "Repeat vs New Users":
        fig = px.line(df, x="Date", y=["Repeat Users", "New Users"], title="Repeat vs New Users")
        explanation = "Shows the balance of returning vs. new members over time — a core loyalty health metric."
    else:
        fig = px.line(df, x="Date", y=metric, title=metric)
        explanation = f"This metric tracks {metric.lower()} and helps us monitor loyalty performance."
    return fig, explanation

if __name__ == '__main__':
    app.run_server(debug=True)
