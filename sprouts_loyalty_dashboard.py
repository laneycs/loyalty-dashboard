
from dash import Dash, html, dcc, Input, Output
import dash_auth
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

VALID_USERNAME_PASSWORD_PAIRS = {
    'sproutsteam': 'loyaltyrocks'
}

df_pos = pd.read_csv("loyalty_2_0_pos_data_combined.csv", parse_dates=["Date"])
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)

df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "uptime": np.random.uniform(95, 100, size=90),
    "region": np.random.choice(["CA", "TX", "NY", "FL", "IL", "AZ", "MI"], size=90)
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

def group_data(metric):
    return {
        "day": df[["date", metric]],
        "week": df.groupby("week")[metric].mean().reset_index().rename(columns={"week": "date"}),
        "month": df.groupby("month")[metric].mean().reset_index().rename(columns={"month": "date"})
    }

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
    dbc.themes.BOOTSTRAP
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.server.secret_key = "sprouts-secret-123"  # to prevent session warnings
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sprouts Loyalty Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Open Sans', sans-serif;
                background-color: #f8f9fa;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def create_card(title, figure, desc):
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5(title, className="text-success")),
            dbc.CardBody([
                dcc.Graph(figure=figure, config={"displayModeBar": False}),
                html.P(desc, style={"fontSize": "0.85rem", "color": "#666"})
            ])
        ], className="mb-4 shadow-sm", style={"borderRadius": "12px"}),
        width=6
    )

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4", style={"fontWeight": "700"}),
    html.P("Secure prototype for internal review. Toggle daily/weekly/monthly data at top."),
    dbc.Row([
        create_card("Daily Active Users", px.line(group_data("daily_active_users")["day"], x="date", y="daily_active_users", title="Users", color_discrete_sequence=["#198754"]).update_traces(line_shape="spline"), "How many users engaged with the platform."),
        create_card("New Signups", px.bar(group_data("new_signups")["day"], x="date", y="new_signups", title="Signups", color_discrete_sequence=["#20c997"]), "New loyalty members per day.")
    ]),
    dbc.Row([
        create_card("Email Clicks", px.area(group_data("email_clicks")["day"], x="date", y="email_clicks", title="Email Engagement", color_discrete_sequence=["#6f42c1"]).update_traces(line_shape="spline"), "Engagement from marketing emails."),
        create_card("Basket Size", px.line(group_data("basket_size")["day"], x="date", y="basket_size", title="Avg Basket", color_discrete_sequence=["#0dcaf0"]).update_traces(line_shape="spline"), "Average cart size per purchase.")
    ]),
    html.Hr(),
    dbc.Row([
        create_card("Orders with Redemptions", px.line(df_pos, x="Date", y="Orders with Redemptions", title="Redemptions", color_discrete_sequence=["#fd7e14"]).update_traces(line_shape="spline"), "Reward redemptions from POS data."),
        create_card("System Uptime", px.line(group_data("uptime")["day"], x="date", y="uptime", title="Uptime", color_discrete_sequence=["#0d6efd"]).update_traces(line_shape="spline"), "Loyalty system availability.")
    ])
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
