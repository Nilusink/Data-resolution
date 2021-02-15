import plotly
import plotly.graph_objects as go



ys = [1, 0, 0, 1, 1]
xs = [0, 0, 1, 1, 0]


smoothTrace1 = {'name' : 'Temperature', 'type' : 'scatter', 'mode' : 'lines', 'x' : ys, 'y' : xs, 'line': {'shape': 'spline', 'smoothing': .5}}

plotly.offline.plot([smoothTrace1])