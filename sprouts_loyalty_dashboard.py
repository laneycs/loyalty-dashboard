
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

# Create a chart
fig_dau = px.line(df, x="date", y="daily_active_users", title="Daily Active Users")

# Create the Dash app
app = Dash(__name__)
server = app.server

# Styles
colors = {
    "background": "#F6F6F6",
    "primary": "#007A33",
    "accent": "#8DC63F",
    "text": "#333333"
}

app.layout = html.Div(style={"fontFamily": "Open Sans, sans-serif", "backgroundColor": colors["background"]}, children=[
    html.Div(style={"padding": "20px", "textAlign": "center"}, children=[
        html.H1("Sprouts Loyalty Dashboard", style={"color": colors["primary"], "marginBottom": "5px"}),
        html.H4("Tracking Loyalty Behavior & Engagement", style={"color": colors["text"]})
    ]),

    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("Key Metrics Summary", style={"color": colors["primary"]}),
                dcc.Graph(figure=fig_dau)
            ])
        ]),
        dcc.Tab(label='Acquisition & Enrollment', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("Sign-ups and Acquisition Channels", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ]),
        dcc.Tab(label='Engagement & Behavior', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("User Activity & Shopping Patterns", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ]),
        dcc.Tab(label='Loyalty Tiers & Progression', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("Tier Breakdown & Progression", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ]),
        dcc.Tab(label='Marketing Email Performance', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("Email Conversions & Open Rates", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ]),
        dcc.Tab(label='Retention & Churn', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("User Retention Analysis", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ]),
        dcc.Tab(label='Technical Performance & Bugs', children=[
            html.Div(style={"padding": "20px"}, children=[
                html.H2("API and Issue Tracking", style={"color": colors["primary"]}),
                html.P("More charts coming soon...", style={"color": colors["text"]})
            ])
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
