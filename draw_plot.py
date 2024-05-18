import plotly
import plotly.graph_objects as go
import numpy as np


def set_default_grid(fig: plotly.graph_objects.Figure):
    if fig.data[0]['type'] == 'scatter':
        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_xaxes(showgrid=True, gridcolor='rgb(200,200,200)', griddash='dot', zeroline=False, mirror=True,
                         showline=True, linecolor='black')
        fig.update_yaxes(showgrid=True, gridcolor='rgb(200,200,200)', griddash='dot', zeroline=False, mirror=True,
                         showline=True, linecolor='black')
        return fig

    if fig.data[0]['type'] == 'scatter3d':
        fig.update_layout(
            scene=dict(
                xaxis=dict(backgroundcolor='white', showgrid=True, gridcolor='rgb(150,150,150)', gridwidth=0.5),
                yaxis=dict(backgroundcolor='white', showgrid=True, gridcolor='rgb(150,150,150)', gridwidth=0.5),
                zaxis=dict(backgroundcolor='white', showgrid=True, gridcolor='rgb(150,150,150)', gridwidth=0.5)
            )
        )
        return fig


def set_axis_equal(fig: plotly.graph_objects.Figure):
    if fig.data[0]['type'] == 'scatter':
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        return fig

    if fig.data[0]['type'] == 'scatter3d':
        fig.update_layout(
            scene=dict(
                aspectmode='data'
            )
        )
        return fig

    raise Exception('axis_equal is implemented only for scatter and scatter3d figures.')


def draw_2d(x: np.ndarray, y: np.ndarray, filename, xlabel: str = 'x', ylabel: str = 'y', name: str = '',
            fig: plotly.graph_objects.Figure = None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=name))
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    fig.update_traces(mode='lines')

    fig = set_default_grid(fig)
    fig.write_html(filename)

    return fig


def draw_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray,
            filename, xlabel: str = 'x', ylabel: str = 'y', zlabel: str = 'z', name: str = '',
            fig: plotly.graph_objects.Figure = None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, name=name))
    fig.update_layout(
        scene=dict(xaxis_title=xlabel,
                   yaxis_title=ylabel,
                   zaxis_title=zlabel)
    )
    fig.update_traces(mode='lines')
    fig = set_default_grid(fig)
    fig = set_axis_equal(fig)
    fig.write_html(filename)

    return fig
