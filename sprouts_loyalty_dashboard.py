
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def create_card(title, metric, view_type, chart_type="line", description=""):
    grouped = group_data(metric)[view_type]
    if chart_type == "bar":
        fig = px.bar(grouped, x="date", y=metric)
    elif chart_type == "area":
        fig = px.area(grouped, x="date", y=metric)
    else:
        fig = px.line(grouped, x="date", y=metric)
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=280)
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5(title, className="text-primary fw-semibold", style={"fontFamily": "Montserrat"})),
            dbc.CardBody([
                dcc.Graph(figure=fig, config={"displayModeBar": False}),
                html.Small(description, style={"color": "#555", "display": "block", "marginTop": "10px", "fontFamily": "Open Sans"})
            ])
        ], className="shadow-sm", style={"borderRadius": "16px"}),
        width=6
    )

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4", style={"fontFamily": "Montserrat", "color": "#1A1A1A"}),

    html.Div([
        html.Label("View By:", className="fw-bold me-2", style={"fontFamily": "Open Sans"}),
        dcc.RadioItems(
            id="global-toggle",
            options=[
                {"label": "Daily", "value": "day"},
                {"label": "Weekly", "value": "week"},
                {"label": "Monthly", "value": "month"}
            ],
            value="day",
            inline=True,
            labelStyle={"marginRight": "15px", "fontFamily": "Open Sans"}
        )
    ], className="mb-4"),

    html.Div(id="dashboard-content")
], fluid=True)

@app.callback(
    Output("dashboard-content", "children"),
    Input("global-toggle", "value")
)
def update_dashboard(view_type):
    return [
        html.Div([
            html.H2("Loyalty Engagement", className="mb-3", style={"fontFamily": "Montserrat"}),
            html.P("A pulse on how well the loyalty program is engaging users day-to-day.", style={"fontFamily": "Open Sans"}),
            dbc.Row([
                create_card("Daily Active Users", "daily_active_users", view_type, "line",
                            "How many users engage with us each day."),
                create_card("New Signups", "new_signups", view_type, "bar",
                            "New loyalty members acquired.")
            ]),
        ], className="mb-5"),

        html.Div([
            html.H2("Program Interaction", className="mb-3", style={"fontFamily": "Montserrat"}),
            html.P("Exploring user behavior post-signup and marketing effectiveness.", style={"fontFamily": "Open Sans"}),
            dbc.Row([
                create_card("Basket Size Over Time", "basket_size", view_type, "area",
                            "Average basket size per transaction."),
                create_card("Email Clicks", "email_clicks", view_type, "bar",
                            "Marketing engagement through email clicks.")
            ])
        ], className="mb-5"),

        html.Div([
            html.H2("Platform Operations", className="mb-3", style={"fontFamily": "Montserrat"}),
            html.P("Reliability and health of the backend loyalty infrastructure.", style={"fontFamily": "Open Sans"}),
            dbc.Row([
                create_card("System Uptime %", "uptime", view_type, "line",
                            "System availability for loyalty operations."),
            ])
        ], className="mb-5"),
    ]

if __name__ == "__main__":
    app.run_server(debug=True)
