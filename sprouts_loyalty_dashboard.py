
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load combined POS data
df_pos = pd.read_csv("loyalty_2_0_pos_data_combined.csv", parse_dates=["Date"])

# Generate dummy data for general dashboard
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df_main = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "uptime": np.random.uniform(95, 100, size=90),
    "region": np.random.choice(["CA", "TX", "NY", "FL", "IL", "AZ", "MI"], size=90)
})

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def create_card(title, figure, description):
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5(title)),
            dbc.CardBody([
                dcc.Graph(figure=figure, config={"displayModeBar": False}),
                html.Small(description, style={"color": "#555", "display": "block", "marginTop": "10px"})
            ])
        ], className="mb-4 shadow-sm"),
        width=6
    )

layout_rows = [

    dbc.Row([
        create_card("Daily Active Users",
                    px.line(df_main, x="date", y="daily_active_users", title=""),
                    "Total number of users who used the platform each day."),
        create_card("New Signups",
                    px.bar(df_main, x="date", y="new_signups", title=""),
                    "Number of new users registered each day.")
    ]),

    dbc.Row([
        create_card("Basket Size Over Time",
                    px.area(df_main, x="date", y="basket_size", title=""),
                    "Average basket size ($) of user orders."),
        create_card("Email Clicks",
                    px.bar(df_main, x="date", y="email_clicks", orientation='v', title=""),
                    "User clicks on loyalty-related marketing emails.")
    ]),

    dbc.Row([
        create_card("System Uptime (%)",
                    px.line(df_main, x="date", y="uptime", title=""),
                    "Uptime performance of the loyalty backend systems."),
        create_card("Users by Region (Map)",
                    px.choropleth(df_main.groupby("region").size().reset_index(name="users"),
                                  locations="region", locationmode="USA-states",
                                  color="users", scope="usa"),
                    "User distribution across key U.S. regions.")
    ]),

    html.Hr(),
    html.H2("Loyalty 2.0 POS Performance", className="my-4"),

    dbc.Row([
        create_card("Total Orders",
                    px.line(df_pos, x="Date", y="Total Orders", title=""),
                    "Total number of transactions at POS."),
        create_card("Loyalty Eligible Orders",
                    px.line(df_pos, x="Date", y="Loyalty Eligible Orders", title=""),
                    "Transactions that qualify for loyalty rewards.")
    ]),

    dbc.Row([
        create_card("Loyalty Member Orders",
                    px.line(df_pos, x="Date", y="Loyalty Member Orders", title=""),
                    "Orders made by registered loyalty members."),
        create_card("Matched POS Orders",
                    px.line(df_pos, x="Date", y="Matched POS Orders", title=""),
                    "Orders matched with a member account during checkout.")
    ]),

    dbc.Row([
        create_card("Orders with Redemptions",
                    px.line(df_pos, x="Date", y="Orders with Redemptions", title=""),
                    "Transactions where a loyalty reward was redeemed."),
        create_card("In Lane Clip Count",
                    px.bar(df_pos, x="Date", y="In Lane Clip Count", title=""),
                    "Offers clipped in-store at time of purchase.")
    ]),

    dbc.Row([
        create_card("Scan Rate (%)",
                    px.line(df_pos, x="Date", y="Scan Rate (%)", title=""),
                    "Percent of eligible orders where loyalty account was scanned."),
        create_card("Basket < Reward Count",
                    px.bar(df_pos, x="Date", y="Basket < Reward Count", title=""),
                    "Orders where reward value exceeded basket total (should be zero).")
    ])
]

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4", style={"fontFamily": "Montserrat", "color": "#1A1A1A"}),
    *layout_rows
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
