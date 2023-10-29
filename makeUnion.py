from interior import *
from pathfinding import *

unionSpace = Space()
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
unionSpace.add_connection('F2NH-F2WH', 'Floor 2 North Elevators')
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