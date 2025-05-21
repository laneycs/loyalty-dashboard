
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
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

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
    dbc.themes.BOOTSTRAP
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Open Sans', sans-serif;
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

def create_card(title, figure, description):
    return dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5(title, className="text-success", style={"fontWeight": "600"})),
            dbc.CardBody([
                dcc.Graph(figure=figure, config={"displayModeBar": False}),
                html.Small(description, style={"color": "#555"})
            ])
        ], className="shadow-sm", style={"borderRadius": "12px", "marginBottom": "20px"}),
        width=6
    )

app.layout = dbc.Container([
    html.H1("Sprouts Loyalty Dashboard", className="my-4", style={"fontWeight": "700"}),

    html.Div([
        html.Label("Toggle View:", className="fw-bold me-2"),
        dbc.ButtonGroup([
            dbc.Button("Daily", id="btn-daily", n_clicks=1, color="success", outline=False),
            dbc.Button("Weekly", id="btn-weekly", n_clicks=0, color="success", outline=True),
            dbc.Button("Monthly", id="btn-monthly", n_clicks=0, color="success", outline=True),
        ], className="mb-4")
    ]),

    dcc.Store(id="view-store", data="day"),

    html.Div(id="dashboard-content")
], fluid=True)

@app.callback(
    Output("view-store", "data"),
    Input("btn-daily", "n_clicks"),
    Input("btn-weekly", "n_clicks"),
    Input("btn-monthly", "n_clicks"),
)
def set_view(d, w, m):
    ctx = dash.callback_context.triggered_id
    if ctx == "btn-daily":
        return "day"
    elif ctx == "btn-weekly":
        return "week"
    elif ctx == "btn-monthly":
        return "month"
    return "day"

@app.callback(
    Output("dashboard-content", "children"),
    Input("view-store", "data")
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
        html.H2("Loyalty Engagement"),
        html.P("This section gives a pulse on daily platform activity and acquisition of new loyalty members."),
        dbc.Row([
            create_card("Daily Active Users", px.line(grouped["daily_active_users"], x="date", y="daily_active_users", color_discrete_sequence=["#198754"]).update_traces(line_shape='spline'), "How many users engaged with the platform."),
            create_card("New Signups", px.bar(grouped["new_signups"], x="date", y="new_signups", color_discrete_sequence=["#20c997"]), "New loyalty member registrations.")
        ]),

        html.H2("User Behavior & Offers"),
        html.P("What happens after sign-up? This section dives into user spend and interaction with promotional emails."),
        dbc.Row([
            create_card("Basket Size", px.area(grouped["basket_size"], x="date", y="basket_size", color_discrete_sequence=["#0dcaf0"]).update_traces(line_shape='spline'), "Average spend per order."),
            create_card("Email Clicks", px.bar(grouped["email_clicks"], x="date", y="email_clicks", color_discrete_sequence=["#6f42c1"]), "Clicks from loyalty email campaigns.")
        ]),

        html.H2("POS Program Insights"),
        html.P("This section illustrates how loyalty translates into real transactions and redemptions at checkout."),
        dbc.Row([
            create_card("Scan Rate", px.line(df_pos, x="Date", y="Scan Rate (%)", color_discrete_sequence=["#ffc107"]).update_traces(line_shape='spline'), "Percent of orders scanned with loyalty."),
            create_card("Orders with Redemptions", px.line(df_pos, x="Date", y="Orders with Redemptions", color_discrete_sequence=["#fd7e14"]).update_traces(line_shape='spline'), "Total rewards redeemed.")
        ]),

        dbc.Row([
            create_card("In-Lane Clip Count", px.bar(df_pos, x="Date", y="In Lane Clip Count", color_discrete_sequence=["#dc3545"]), "Clip actions triggered during checkout."),
            create_card("Loyalty Member Orders", px.line(df_pos, x="Date", y="Loyalty Member Orders", color_discrete_sequence=["#0d6efd"]).update_traces(line_shape='spline'), "Transactions made by members.")
        ]),

        html.H2("System Health & Geography"),
        html.P("Operational reliability and geographic distribution of loyalty activity."),
        dbc.Row([
            create_card("System Uptime", px.line(grouped["uptime"], x="date", y="uptime", color_discrete_sequence=["#198754"]).update_traces(line_shape='spline'), "Backend performance availability."),
            create_card("User Activity by Region", px.choropleth(grouped["region"], locations="region", locationmode="USA-states", color="users", scope="usa"), "Where loyalty traffic is concentrated.")
        ])
    ]

if __name__ == "__main__":
    app.run_server(debug=True)
