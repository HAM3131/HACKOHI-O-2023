import plotly.graph_objects as go
from skimage import io
import numpy as np

x = np.linspace(0,5, 640)
y = np.linspace(5, 10, 578)
X, Y = np.meshgrid(x,y)
z = (X+Y)/(2+np.cos(X)*np.sin(Y))*0

img = io.imread('UnionFloor1.jpg',)
io.imshow(img)

pl_grey =[[0.0, 'rgb(0, 0, 0)'],
    [0.05, 'rgb(13, 13, 13)'],
    [0.1, 'rgb(29, 29, 29)'],
    [0.15, 'rgb(45, 45, 45)'],
    [0.2, 'rgb(64, 64, 64)'],
    [0.25, 'rgb(82, 82, 82)'],
    [0.3, 'rgb(94, 94, 94)'],
    [0.35, 'rgb(108, 108, 108)'],
    [0.4, 'rgb(122, 122, 122)'],
    [0.45, 'rgb(136, 136, 136)'],
    [0.5, 'rgb(150, 150, 150)'],
    [0.55, 'rgb(165, 165, 165)'],
    [0.6, 'rgb(181, 181, 181)'],
    [0.65, 'rgb(194, 194, 194)'],
    [0.7, 'rgb(206, 206, 206)'],
    [0.75, 'rgb(217, 217, 217)'],
    [0.8, 'rgb(226, 226, 226)'],
    [0.85, 'rgb(235, 235, 235)'],
    [0.9, 'rgb(243, 243, 243)'],
    [0.95, 'rgb(249, 249, 249)'],
    [1.0, 'rgb(255, 255, 255)']]

surfcolor = np.fliplr(img[:,:,0])

surf = go.Surface(x=x, y=y, z=z,
                  surfacecolor=surfcolor,
                  colorscale=pl_grey,
                  showscale=True)  

layout = go.Layout(
         title='Mapping an image onto a surface', 
         font_family='Balto',
         width=800,
         height=800,
         scene=dict(xaxis_visible=False,
                     yaxis_visible=False, 
                     zaxis_visible=False, 
                     aspectratio=dict(x=1,
                                      y=1,
                                      z=0.5
                                     )
                    ))
        
fig = go.Figure(data=[surf], layout=layout)

fig.show()