
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
    "repeat_visits": np.random.randint(100, 300, size=90),
    "conversion_rate": np.random.uniform(0.05, 0.15, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_opens": np.random.randint(500, 1500, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "open_bugs": np.random.randint(5, 20, size=90),
    "incidents": np.random.randint(0, 5, size=90),
    "uptime": np.random.uniform(95, 100, size=90),
    "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"], size=90),
    "region": np.random.choice(["West", "Midwest", "Southwest", "Southeast"], size=90)
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

# Pre-summarized data
tier_counts = df["loyalty_tier"].value_counts().reset_index()
tier_counts.columns = ["tier", "count"]
region_counts = df["region"].value_counts().reset_index()
region_counts.columns = ["region", "count"]

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

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("📈 Daily Active Users"),
        dcc.Graph(figure=px.line(df, x="date", y="daily_active_users", title="Daily Active Users"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("📊 New Signups Over Time"),
        dcc.Graph(figure=px.bar(df, x="date", y="new_signups", title="New Signups"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("📦 Basket Size by Day"),
        dcc.Graph(figure=px.area(df, x="date", y="basket_size", title="Basket Size Over Time"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("🥧 Loyalty Tier Distribution"),
        dcc.Graph(figure=px.pie(tier_counts, names="tier", values="count", title="Tier Breakdown"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("🏪 Users by Region"),
        dcc.Graph(figure=px.bar(region_counts, x="region", y="count", title="Users by Region"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("📧 Email Performance"),
        dcc.Graph(figure=px.bar(df, x="date", y="email_clicks", title="Email Clicks Over Time"))
    ]),

    html.Div(style={"marginBottom": "40px"}, children=[
        html.H2("🛠️ API Health Monitoring"),
        dcc.Graph(figure=px.line(df, x="date", y="uptime", title="System Uptime %"))
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
