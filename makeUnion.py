from interior import *
from pathfinding import *
import plotly.graph_objects as go
from skimage import io
import numpy as np

x = np.linspace(-93,732, 825)
y = np.linspace(-83, 661, 745)
X, Y = np.meshgrid(x,y)
z = -(X+Y)/(X+Y)*.05
z2 = (X+Y)/(X+Y)*(.95)

img = io.imread('UnionFloor1V2.jpg',)
img2 = io.imread('UnionFloor2.jpg',)

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
surfcolor2 = np.fliplr(img2[:,:,0])

surf = go.Surface(x=x, y=y, z=z,
                  surfacecolor=surfcolor,
                  colorscale=pl_grey,
                  showscale=False)

surf2 = go.Surface(x=x, y=y, z=z2,
                  surfacecolor=surfcolor2,
                  colorscale=pl_grey,
                  showscale=False)












unionSpace = Space(image=[surf, surf2])
# {'x':,'y':,'z':,'type':NodeType.}
data = {'East Main Atrium': {'x':333,'y':233,'z':0,'type':NodeType.ROOM},
        'West Main Atrium': {'x':333,'y':372,'z':0,'type':NodeType.ROOM},
        'PGH-EMA O': {'x':274,'y':186,'z':0,'type':NodeType.OTHER},
        'PGH-UBS H': {'x':252,'y':186,'z':0,'type':NodeType.HALLWAY,'hName':'Parking Garage Hallway'},
        'PGH-GE H': {'x':96,'y':169,'z':0,'type':NodeType.HALLWAY,'hName':'Parking Garage Hallway'},
        'Parking Garage Exit': {'x':78,'y':170,'z':0,'type':NodeType.EXIT},
        'East Main Exit': {'x':329,'y':154,'z':0,'type':NodeType.EXIT},
        'F1SB D': {'x':369,'y':365,'z':0, 'type':NodeType.DOOR},
        'Floor 1 South Bathrooms': {'x':403,'y':365,'z':0, 'type':NodeType.ROOM},
        'Floor 1 West Stairs': {'x':294,'y':451,'z':0,'type':NodeType.STAIRS},
        'Floor 1 North Elevator': {'x':288,'y':392,'z':0,'type':NodeType.ELEVATOR},
        'Floor 2 North Elevator':  {'x':288,'y':392,'z':1,'type':NodeType.ELEVATOR},
        'Floor 2 West Stairs': {'x':294,'y':451,'z':1,'type':NodeType.STAIRS},
        'Archie M. Griffin Grand Ballroom': {'x':214,'y':250,'z':1,'type':NodeType.ROOM},
        'AGB D': {'x':269,'y':305,'z':1,'type':NodeType.DOOR},
        'F2NH-AGB H':  {'x':291,'y':304,'z':1,'type':NodeType.HALLWAY,'hName':'F2 North Hallway'},
        'F2NH-F2EH': {'x':290,'y':210,'z':1,'type':NodeType.HALLWAY, 'hName':"F2 North and East Intersection"},
        'F2EH-DPSL H':  {'x':329,'y':210,'z':1,'type':NodeType.HALLWAY, 'hName':"F2 East Hallway"},
        'DPSL D':  {'x':325,'y':198,'z':1,'type':NodeType.DOOR},
        'Danny Price Student Lounge': {'x':327,'y':179,'z':1,'type':NodeType.ROOM},
        'F2NH-F2WH':  {'x':298,'y':399,'z':1,'type':NodeType.HALLWAY,'hName':"F2 North and West Intersection"},
        'F2WH-GAL H':  {'x':335,'y':409,'z':1,'type':NodeType.HALLWAY, 'hName':'F2 West Hallway'},
        'GAL D': {'x':334,'y':420,'z':1,'type':NodeType.DOOR},
        'Glass Art Lounge':  {'x':334,'y':436,'z':1,'type':NodeType.ROOM}
        }

rAngle = -1.436
for key,val in data.items():
    oldData = copy.copy(val)
    newData = copy.copy(val)
    # print(newData)
    newData['x'] = np.cos(rAngle)*oldData['x'] + np.sin(rAngle)*-oldData['y']
    newData['y'] = -np.sin(rAngle)*oldData['x'] + np.cos(rAngle)*-oldData['y']
    unionSpace.add_node(key, newData)


# Floor 2

unionSpace.add_connection('Floor 2 West Stairs', 'F2NH-F2WH')
unionSpace.add_connection('F2NH-F2WH', 'Floor 2 North Elevator')
unionSpace.add_connection('F2NH-F2WH', 'F2NH-AGB H')
unionSpace.add_connection('AGB D', 'F2NH-AGB H')
unionSpace.add_connection('AGB D', 'Archie M. Griffin Grand Ballroom')
unionSpace.add_connection('F2NH-AGB H','F2NH-F2EH')
unionSpace.add_connection('F2NH-F2EH','F2EH-DPSL H')
unionSpace.add_connection('DPSL D', 'F2EH-DPSL H')
unionSpace.add_connection('DPSL D', 'Danny Price Student Lounge')
unionSpace.add_connection('F2NH-F2WH','F2WH-GAL H')
unionSpace.add_connection('F2WH-GAL H','GAL D')
unionSpace.add_connection('Glass Art Lounge','GAL D')

#unionSpace.add_node("East Main Atrium", {'x':'type':NodeType.HALLWAY})
# Floor 1 North East Wing
unionSpace.add_connection('East Main Atrium', 'PGH-EMA O')
unionSpace.add_connection('PGH-EMA O', 'PGH-UBS H')
unionSpace.add_connection('PGH-UBS H', 'PGH-GE H')


unionSpace.add_connection('East Main Exit', 'East Main Atrium')
unionSpace.add_connection('East Main Atrium', 'West Main Atrium')

unionSpace.add_connection('West Main Atrium','F1SB D')
unionSpace.add_connection('F1SB D', 'Floor 1 South Bathrooms')

unionSpace.add_connection('West Main Atrium', 'Floor 1 West Stairs')
unionSpace.add_connection('West Main Atrium', 'Floor 1 North Elevator')

unionSpace.add_connection('Floor 1 West Stairs', 'Floor 2 West Stairs')
unionSpace.add_connection('Floor 1 North Elevator', 'Floor 2 North Elevator')

# path = pathFindingAlgorithm(unionSpace, "East Main Exit", "Danny Price Student Lounge")
# unionSpace.plot_space_highlight(path[0])
