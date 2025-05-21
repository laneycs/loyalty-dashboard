
from dash import Dash, html, dcc, Input, Output, State
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
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server  # <-- Required for Render

app.layout = html.Div([
    html.H1("Sprouts Loyalty Dashboard — Secure"),
    html.P("✅ This version is password protected and ready for review."),
])

if __name__ == "__main__":
    app.run_server(debug=True)
