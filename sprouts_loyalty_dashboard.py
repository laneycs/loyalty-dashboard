
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load POS data
df_pos = pd.read_csv("loyalty_2_0_pos_data_combined.csv", parse_dates=["Date"])

# Dummy general data
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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4"),

    html.H2("1. Loyalty Health at a Glance"),
    html.P("This section gives us a pulse on how well the loyalty program is engaging users day-to-day — highlighting overall traffic to the platform and the rate at which shoppers identify themselves at checkout."),
    dbc.Row([
        create_card("Daily Active Users",
                    px.line(df, x="date", y="daily_active_users", title=""),
                    "Total number of users who engaged with the platform each day."),
        create_card("Scan Rate (%)",
                    px.line(df_pos, x="Date", y="Scan Rate (%)", title=""),
                    "Percent of eligible orders where the loyalty ID was scanned.")
    ]),

    html.H2("2. User Growth & Acquisition"),
    html.P("Here we showcase how effectively the program is growing — highlighting both acquisition of new loyalty members and the volume of transactions that are eligible for loyalty."),
    dbc.Row([
        create_card("New Loyalty Signups",
                    px.bar(df, x="date", y="new_signups", title=""),
                    "Daily count of newly registered loyalty members."),
        create_card("Loyalty Eligible Orders",
                    px.line(df_pos, x="Date", y="Loyalty Eligible Orders", title=""),
                    "POS orders that qualified for loyalty benefits.")
    ]),

    html.H2("3. Loyalty Program Engagement"),
    html.P("After sign-up, how do members engage with the program? This section looks at email performance and the rate of actual member-based transactions."),
    dbc.Row([
        create_card("Email Clicks",
                    px.bar(df, x="date", y="email_clicks", title=""),
                    "Volume of loyalty-related email link clicks."),
        create_card("Loyalty Member Orders",
                    px.line(df_pos, x="Date", y="Loyalty Member Orders", title=""),
                    "Orders placed by registered loyalty members.")
    ]),

    html.H2("4. Reward Activation & Redemptions"),
    html.P("This section reveals how well members are using loyalty benefits — whether they are redeeming rewards and actively engaging with in-lane offers."),
    dbc.Row([
        create_card("Orders with Redemptions",
                    px.line(df_pos, x="Date", y="Orders with Redemptions", title=""),
                    "Transactions where a loyalty reward was applied."),
        create_card("In Lane Clip Count",
                    px.bar(df_pos, x="Date", y="In Lane Clip Count", title=""),
                    "Offers clipped in-store during checkout.")
    ]),

    html.H2("5. Operational Health & System Integrity"),
    html.P("A successful loyalty program relies on seamless operations. This section covers backend uptime and checks for edge cases — such as rewards exceeding order value."),
    dbc.Row([
        create_card("System Uptime %",
                    px.line(df, x="date", y="uptime", title=""),
                    "Availability of the backend system handling loyalty."),
        create_card("Basket < Reward Count",
                    px.bar(df_pos, x="Date", y="Basket < Reward Count", title=""),
                    "Orders where reward value exceeded basket total (should always be zero).")
    ]),

    html.H2("6. Regional & Checkout Insights"),
    html.P("Where are users most active? How well are transactions being matched to loyalty accounts at the register? These questions are addressed here."),
    dbc.Row([
        create_card("Users by Region",
                    px.choropleth(df.groupby("region").size().reset_index(name="users"),
                                  locations="region", locationmode="USA-states",
                                  color="users", scope="usa"),
                    "Heatmap of user activity across U.S. regions."),
        create_card("Matched POS Orders",
                    px.line(df_pos, x="Date", y="Matched POS Orders", title=""),
                    "Orders matched to a loyalty member account at checkout.")
    ])
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
