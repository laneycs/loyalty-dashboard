import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Sample data
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "New Users": [100, 150, 200, 250, 300],
    "Returning Users": [80, 120, 160, 200, 240],
    "Redemptions": [50, 70, 90, 110, 130],
    "Revenue": [1000, 1500, 2000, 2500, 3000]
}
df = pd.DataFrame(data)

# Auth
USERNAME_PASSWORD_PAIRS = [['sproutsteam', 'sprouts2025']]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

# Layout
app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="text-center my-4"),

    html.Div([
        html.P("Toggle metric:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if col != "Month"],
            value='New Users',
            clearable=False
        )
    ], className="mb-4"),

    dcc.Graph(id='metric-graph'),

    html.Div(id='narrative', className='mt-4')
])

@app.callback(
    Output('metric-graph', 'figure'),
    Output('narrative', 'children'),
    Input('metric-dropdown', 'value')
)
def update_graph(metric):
    fig = px.line(df, x="Month", y=metric, markers=True, title=f"{metric} Over Time")
    fig.update_traces(line_shape="spline", marker=dict(size=8))
    fig.update_layout(transition_duration=500)

    insights = {
        "New Users": "We're steadily growing our user base each month — great work on acquisition!",
        "Returning Users": "Customer retention is increasing, suggesting strong program engagement.",
        "Redemptions": "More users are redeeming rewards — a key sign of value delivered.",
        "Revenue": "Revenue growth is on track with user engagement — loyalty is driving value."
    }

    return fig, html.P(insights.get(metric, ""), className="lead")

if __name__ == '__main__':
    app.run_server(debug=True)
