from jupyter_dash import JupyterDash
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

JupyterDash.infer_jupyter_proxy_config()

app = JupyterDash(__name__)

# Create server variable with Flask server object for use with gunicorn
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P("Skewness to the left:"),
                        dcc.Slider(
                            id="skew-left-slider", min=1, max=10, value=2, step=0.5
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.P("Skewness to the right:"),
                        dcc.Slider(
                            id="skew-right-slider", min=1, max=10, value=2, step=0.5
                        ),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
        dcc.Graph(id="graph-with-slider"),
    ]
)


@app.callback(
    Output("graph-with-slider", "figure"),
    [
        Input("skew-right-slider", "value"),
        Input("skew-left-slider", "value"),
    ],
)
def update_figure(skew_right, skew_left):
    n = 5000
    v = np.random.beta(a=skew_left, b=skew_right, size=n)
    v = pd.Series(v)
    fig = px.histogram(
        v,
        nbins=80,
        title="Histogram and quantiles",
        color_discrete_sequence=["#1F1B42"],
    )
    fig.layout.template = "plotly_white"
    fig.update_layout(showlegend=False)

    def draw_quantile_line(v, quantile):
        quant = v.quantile(quantile)
        fig.add_vline(
            x=quant,
            line_width=3,
            line_dash="dash",
            line_color="red",
            annotation_text="Q" + str(int(100 * quantile)),
            annotation_position="top",
        )

    for quantile in [0, 0.25, 0.5, 0.75, 1]:
        draw_quantile_line(v, quantile)

    fig.add_vline(
        x=v.mean(),
        line_width=3,
        line_color="green",
        annotation_text="Mean",
        annotation_position="top",
        annotation_font_color="green",
    )

    return fig
