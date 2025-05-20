
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create dummy data
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "repeat_visits": np.random.randint(100, 300, size=90),
    "conversion_rate": np.random.uniform(0.05, 0.15, size=90),
    "loyalty_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"], size=90),
    "region": np.random.choice(["West", "Midwest", "Southwest", "Southeast"], size=90)
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

def group_data(col):
    return {
        "daily": df[["date", col]],
        "weekly": df.groupby("week").agg({col: "sum"}).reset_index().rename(columns={"week": "date"}),
        "monthly": df.groupby("month").agg({col: "sum"}).reset_index().rename(columns={"month": "date"})
    }

data_groups = {
    "daily_active_users": group_data("daily_active_users"),
    "repeat_visits": group_data("repeat_visits"),
    "conversion_rate": group_data("conversion_rate")
}

tier_counts = df["loyalty_tier"].value_counts().reset_index()
tier_counts.columns = ["tier", "count"]
region_counts = df["region"].value_counts().reset_index()
region_counts.columns = ["region", "count"]

app = Dash(__name__)
server = app.server

def card(title, description, graph_id, toggle_id):
    return html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2(title, style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id=toggle_id,
                options=[
                    {"label": "Daily", "value": "daily"},
                    {"label": "Weekly", "value": "weekly"},
                    {"label": "Monthly", "value": "monthly"}
                ],
                value="daily",
                clearable=False,
                style={
                    "width": "180px",
                    "fontSize": "14px",
                    "border": "1px solid #ccc",
                    "borderRadius": "6px"
                }
            )
        ]),
        html.Div(id=graph_id, style={"marginTop": "20px"}),
        html.P(description, style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ])

app.layout = html.Div(style={
    "backgroundColor": "#FFFFFF",
    "padding": "30px",
    "fontFamily": "Open Sans, sans-serif"
}, children=[
    html.H1("Sprouts Loyalty Dashboard", style={
        "textAlign": "left", "color": "#1A1A1A", "fontFamily": "Montserrat, sans-serif"
    }),

    card("📈 Daily Active Users", 
         "This chart shows the number of active users over time.", 
         "dau-graph-container", "dau-view-toggle"),

    card("🔁 Repeat Visits", 
         "This chart shows how often users return and engage with Sprouts.", 
         "repeat-graph-container", "repeat-view-toggle"),

    card("📧 Email Conversion Rate (Dummy)", 
         "Simulated conversion rates by campaign date, not real data yet.", 
         "email-graph-container", "email-view-toggle"),

    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.H2("🥧 Loyalty Tier Distribution", style={"color": "#007A33"}),
        dcc.Graph(figure=px.pie(tier_counts, names="tier", values="count", title="Loyalty Tier Distribution")),
        html.P("This pie chart displays how users are distributed across loyalty tiers.", style={"fontSize": "14px", "color": "#555"})
    ]),

    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.H2("🏪 Regional Distribution", style={"color": "#007A33"}),
        dcc.Graph(figure=px.bar(region_counts, x="region", y="count", title="User Count by Region")),
        html.P("Shows the number of users per region where Sprouts loyalty features are used.", style={"fontSize": "14px", "color": "#555"})
    ])
])

@app.callback(Output("dau-graph-container", "children"), Input("dau-view-toggle", "value"))
def update_dau_chart(view):
    data = data_groups["daily_active_users"][view]
    fig = px.line(data, x="date", y="daily_active_users", title=f"{view.capitalize()} Active Users")
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("repeat-graph-container", "children"), Input("repeat-view-toggle", "value"))
def update_repeat_chart(view):
    data = data_groups["repeat_visits"][view]
    fig = px.line(data, x="date", y="repeat_visits", title=f"{view.capitalize()} Repeat Visits")
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("email-graph-container", "children"), Input("email-view-toggle", "value"))
def update_email_chart(view):
    data = data_groups["conversion_rate"][view]
    fig = px.bar(data, x="date", y="conversion_rate", title=f"{view.capitalize()} Email Conversion Rate")
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)
