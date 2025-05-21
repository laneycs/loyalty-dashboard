
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

def create_card(title, figure, description):
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5(title, className="text-primary fw-semibold", style={"fontFamily": "Montserrat"})),
            dbc.CardBody([
                dcc.Graph(figure=figure, config={"displayModeBar": False}),
                html.Small(description, style={"color": "#555", "fontFamily": "Open Sans"})
            ])
        ], className="shadow-sm", style={"borderRadius": "16px", "marginBottom": "20px"}),
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
    grouped = {
        "daily_active_users": group_data("daily_active_users")[view_type],
        "new_signups": group_data("new_signups")[view_type],
        "basket_size": group_data("basket_size")[view_type],
        "email_clicks": group_data("email_clicks")[view_type],
        "uptime": group_data("uptime")[view_type],
        "region": df.groupby("region").size().reset_index(name="users")
    }

    return [
        html.H2("Loyalty Engagement", style={"fontFamily": "Montserrat"}),
        dbc.Row([
            create_card("Daily Active Users", px.line(grouped["daily_active_users"], x="date", y="daily_active_users"), "How many users engage with us each day."),
            create_card("New Signups", px.bar(grouped["new_signups"], x="date", y="new_signups"), "New loyalty members acquired.")
        ]),

        html.H2("Program Interaction", style={"fontFamily": "Montserrat"}),
        dbc.Row([
            create_card("Basket Size Over Time", px.area(grouped["basket_size"], x="date", y="basket_size"), "Average basket size per transaction."),
            create_card("Email Clicks", px.bar(grouped["email_clicks"], x="date", y="email_clicks"), "Marketing engagement through email clicks.")
        ]),

        html.H2("POS Program Performance", style={"fontFamily": "Montserrat"}),
        dbc.Row([
            create_card("Scan Rate (%)", px.line(df_pos, x="Date", y="Scan Rate (%)"), "Percent of eligible orders where loyalty account was scanned."),
            create_card("Orders with Redemptions", px.line(df_pos, x="Date", y="Orders with Redemptions"), "Rewards used by loyalty members.")
        ]),
        dbc.Row([
            create_card("In Lane Clip Count", px.bar(df_pos, x="Date", y="In Lane Clip Count"), "Offers clipped in-store at checkout."),
            create_card("Loyalty Member Orders", px.line(df_pos, x="Date", y="Loyalty Member Orders"), "Orders placed by registered members.")
        ]),

        html.H2("Operational Health & Regions", style={"fontFamily": "Montserrat"}),
        dbc.Row([
            create_card("System Uptime %", px.line(grouped["uptime"], x="date", y="uptime"), "System reliability for loyalty operations."),
            create_card("User Activity by Region", px.choropleth(grouped["region"], locations="region", locationmode="USA-states", color="users", scope="usa"), "Geographic distribution of users.")
        ])
    ]

if __name__ == "__main__":
    app.run_server(debug=True)
