
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setup
np.random.seed(42)
dates = pd.date_range(end=datetime.today(), periods=90)
df = pd.DataFrame({
    "date": dates,
    "daily_active_users": np.random.randint(800, 1200, size=90),
    "repeat_visits": np.random.randint(100, 300, size=90),
    "conversion_rate": np.random.uniform(0.05, 0.15, size=90),
})
df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)

def dummy_chart(title):
    return px.line(df, x="date", y="daily_active_users", title=title)

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

    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Overview", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-0",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-0", style={"marginTop": "20px"}),
        html.P("📊 Overall program health snapshot.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Acquisition & Enrollment", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-1",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-1", style={"marginTop": "20px"}),
        html.P("📈 How users join and start their loyalty journey.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Engagement & Behavior", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-2",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-2", style={"marginTop": "20px"}),
        html.P("🔁 How users shop, redeem, and return.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Tier Progression", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-3",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-3", style={"marginTop": "20px"}),
        html.P("🥇 How users move between loyalty levels.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Retention & Churn", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-4",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-4", style={"marginTop": "20px"}),
        html.P("📉 Who’s staying, who’s going, and who we win back.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Email & Campaigns", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-5",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-5", style={"marginTop": "20px"}),
        html.P("📧 How email and offers are performing.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
    html.Div(style={
        "backgroundColor": "#FAFAFA",
        "padding": "25px",
        "borderRadius": "16px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        "marginBottom": "30px"
    }, children=[
        html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
            html.H2("Technical + Operational", style={"marginBottom": "0", "color": "#007A33"}),
            dcc.Dropdown(
                id="toggle-6",
                options=[{"label": "Daily", "value": "daily"}, {"label": "Weekly", "value": "weekly"}, {"label": "Monthly", "value": "monthly"}],
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
        html.Div(id="graph-6", style={"marginTop": "20px"}),
        html.P("🛠️ API uptime, bugs, incidents, and system health.", style={"fontSize": "14px", "color": "#555", "marginTop": "10px"})
    ]),
    
])

# Dummy callbacks for now

@app.callback(Output("graph-0", "children"), Input("toggle-0", "value"))
def update_graph_0(view):
    fig = dummy_chart("Overview - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-1", "children"), Input("toggle-1", "value"))
def update_graph_1(view):
    fig = dummy_chart("Acquisition & Enrollment - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-2", "children"), Input("toggle-2", "value"))
def update_graph_2(view):
    fig = dummy_chart("Engagement & Behavior - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-3", "children"), Input("toggle-3", "value"))
def update_graph_3(view):
    fig = dummy_chart("Tier Progression - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-4", "children"), Input("toggle-4", "value"))
def update_graph_4(view):
    fig = dummy_chart("Retention & Churn - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-5", "children"), Input("toggle-5", "value"))
def update_graph_5(view):
    fig = dummy_chart("Email & Campaigns - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

@app.callback(Output("graph-6", "children"), Input("toggle-6", "value"))
def update_graph_6(view):
    fig = dummy_chart("Technical + Operational - View: " + view.capitalize())
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=40, b=10))
    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)
