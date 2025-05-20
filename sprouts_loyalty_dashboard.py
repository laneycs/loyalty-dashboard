
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate dummy data
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)

data = {
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "weekly_active_users": np.random.randint(3000, 5000, size=90),
    "monthly_active_users": np.random.randint(8000, 12000, size=90),
    "avg_basket_size": np.random.uniform(20, 40, size=90),
    "repeat_visits": np.random.randint(100, 300, size=90),
    "conversion_rate": np.random.uniform(0.05, 0.15, size=90),
    "region": np.random.choice(["West", "Midwest", "Southwest", "Southeast"], size=90),
    "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"], size=90)
}

df = pd.DataFrame(data)

# Create placeholder charts
fig_dau = px.line(df, x="date", y="daily_active_users", title="📈 Daily Active Users")
fig_tiers = px.pie(df, names="loyalty_tier", title="🥧 Loyalty Tier Distribution")
fig_region = px.bar(df.groupby("region").size().reset_index(name="count"),
                    x="region", y="count", title="🏪 Users by Region")
fig_repeat = px.histogram(df, x="repeat_visits", nbins=20, title="🔁 Repeat Visits Distribution")
fig_api = px.line(df, x="date", y="conversion_rate", title="🛰️ API Health (Placeholder for Latency/Errors)")
fig_email = px.bar(df.iloc[:10], x="date", y="conversion_rate", title="📧 Email Conversion Rate (Dummy Data)")

# Create the Dash app
app = Dash(__name__)
server = app.server

# Styles
colors = {
    "background": "#F6F6F6",
    "primary": "#007A33",
    "text": "#333333"
}

app.layout = html.Div(style={"fontFamily": "Open Sans, sans-serif", "backgroundColor": colors["background"], "padding": "20px"}, children=[
    html.H1("Sprouts Loyalty Dashboard", style={"color": colors["primary"], "textAlign": "center"}),
    html.H4("Prototype Demo • All Sections Scrollable", style={"color": colors["text"], "textAlign": "center"}),

    html.Div([
        html.H2("Overview", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_dau)
    ]),

    html.Div([
        html.H2("Loyalty Tiers", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_tiers)
    ]),

    html.Div([
        html.H2("User Distribution by Region", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_region)
    ]),

    html.Div([
        html.H2("Repeat Visits", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_repeat)
    ]),

    html.Div([
        html.H2("Email Performance (Placeholder)", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_email)
    ]),

    html.Div([
        html.H2("API Health Monitoring (Placeholder)", style={"color": colors["primary"]}),
        dcc.Graph(figure=fig_api)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
