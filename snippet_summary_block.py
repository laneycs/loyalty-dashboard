
def summary_kpis(metrics: dict):
    return html.Div(style={"display": "flex", "gap": "30px", "flexWrap": "wrap", "marginBottom": "20px"}, children=[
        html.Div(style={{
            "flex": "1",
            "minWidth": "150px",
            "backgroundColor": "#FFFFFF",
            "padding": "15px",
            "borderRadius": "12px",
            "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
            "textAlign": "center"
        }}, children=[
            html.H4(label, style={{"margin": "0", "color": "#007A33", "fontSize": "14px"}}),
            html.H2(value, style={{"margin": "0", "color": "#333333", "fontSize": "24px"}})
        ]) for label, value in metrics.items()
    ])
