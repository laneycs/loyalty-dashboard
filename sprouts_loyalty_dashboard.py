
from dash import Dash, html, dcc
import dash_draggable
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "new_signups": np.random.randint(100, 500, size=90),
    "basket_size": np.random.uniform(20, 60, size=90),
    "email_clicks": np.random.randint(100, 1000, size=90),
    "uptime": np.random.uniform(95, 100, size=90)
})

app = Dash(__name__)
server = app.server

# Generate example figures
figs = {
    "Daily Active Users": px.line(df, x="date", y="daily_active_users", title="Active Users"),
    "New Signups": px.bar(df, x="date", y="new_signups", title="New Signups"),
    "Basket Size": px.area(df, x="date", y="basket_size", title="Basket Size"),
    "Email Clicks": px.bar(df, x="date", y="email_clicks", title="Email Clicks"),
    "Uptime": px.line(df, x="date", y="uptime", title="System Uptime %")
}

cards = [
    dash_draggable.GridItem([
        html.Div(style={
            "backgroundColor": "#FAFAFA",
            "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
        }, children=[
            html.H3(title, style={"marginBottom": "10px", "color": "#007A33", "fontFamily": "Montserrat, sans-serif"}),
            dcc.Graph(figure=fig)
        ])
    ], key=title, dataGrid={"x": i % 2, "y": i // 2, "w": 1, "h": 1, "minW": 1, "minH": 1})
    for i, (title, fig) in enumerate(figs.items())
]

app.layout = html.Div([
    html.H1("Sprouts Loyalty Dashboard", style={"color": "#1A1A1A", "fontFamily": "Montserrat, sans-serif", "paddingBottom": "20px"}),
    dash_draggable.GridLayout(
        children=cards,
        className="layout",
        cols=2,
        rowHeight=300,
        width=1200,
        style={"margin": "0 auto"}
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
