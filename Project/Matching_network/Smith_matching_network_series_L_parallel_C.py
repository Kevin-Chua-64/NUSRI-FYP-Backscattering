import plotly.graph_objects as go
import plotly.io as pio

# point
value_L = input('Series inductance: ')
value_C = input('Parallel capacitance: ')
name = 'ADG701, Matching network, Series L: %s, Parallel C: %s' % (value_L, value_C)
with open('./Matching_network_series_L_parallel_C.txt', 'r') as f:
    lines = f.readlines()
    data = lines[1].split('\n')[0].split('\t')[1:]

x1 = float(data[0].split(',')[0])
y1 = float(data[0].split(',')[1])
x2 = float(data[1].split(',')[0])
y2 = float(data[1].split(',')[1])

# impedance
gamma1 = x1 + 1j*y1
gamma2 = x2 + 1j*y2
z1 = (1+gamma1) / (1-gamma1)
z2 = (1+gamma2) / (1-gamma2)

fig = go.Figure()

fig.add_trace(go.Scattersmith(
    imag=[z1.imag],
    real=[z1.real],
    marker_symbol='x',
    marker_size=10,
    marker_color="red",
    subplot="smith",
    name='0 V, OFF state'
))

fig.add_trace(go.Scattersmith(
    imag=[z2.imag],
    real=[z2.real],
    marker_symbol='x',
    marker_size=10,
    marker_color="blue",
    subplot="smith",
    name='5 V, ON  state'
))

fig.update_layout(
    smith=dict(
        realaxis_gridcolor='green',
        imaginaryaxis_gridcolor='black',
        domain=dict(x=[0,1])
    ),
    title='Smith Chart: %s'%name
)

fig.update_smiths(bgcolor="lightgrey")

fig.show()
pio.write_image(fig, './Series_L_%s_Parallel_C_%s.jpg' % (value_L, value_C))
