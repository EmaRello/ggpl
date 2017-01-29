# -*- coding: utf-8 -*-
from pyplasm import *

ambient   =  [0.24725, 0.1995, 0.0745, 1.0]
diffuse   =  [0.75164, 0.60648, 0.22648, 1.0]
specular  =  [0.628281, 0.555802, 0.366065, 1.0]
emission  =  [0.0,0.0,0.0,0.0]
shininess =  [51.2]
goldMaterial = ambient+diffuse+specular+emission+shininess

"""
Funzione per la realizzazione di un gradino
riser è l'alzata del gradino
tread è la piedata del gradino
width è l'ampiezza del gradino
"""
def step(width,riser,tread) :
    step = MKPOL([[[0,0],[0,riser*2],[tread,riser*2],[tread,riser]],[[1,2,3,4]],1])
    step = PROD([QUOTE([width]), step])
    return step

#VIEW (step(1,0.2,0.25))

"""
Funzione per la realizzazione di una scalinata
"""
def stairs(width,riser,tread,nSteps) :
    structureElements = [CUBOID([width,tread,riser]),T([2])([tread]),step(width,riser,tread)]
    for i in range(2,int(nSteps)):
        structureElements.append(T([2,3])([tread,riser]))
        structureElements.append(step(width,riser,tread))
    s = STRUCT(structureElements)
    return s

#VIEW (stairs(1,0.2,0.25,10))

    
"""
Funzione per adattare le dimensioni dei gradini a quelle della scalinata
"""
def getStepDimensions (dx,dy,dz) :
    treadRef = 0.25

    nSteps = dy/treadRef
    
    nSteps -= nSteps%1
    
    tread=dy/nSteps
    
    riser = dz/nSteps
    
    return [riser,tread,nSteps]

"""
Funzione per la realizzazione di una scalinata adattata
"""
def adaptedStairs (dx,dy,dz) :
    stepDimensions = getStepDimensions(dx,dy,dz)
    
    riser = stepDimensions[0]
    tread = stepDimensions[1]
    nSteps = stepDimensions[2]
    
    return stairs(dx,riser,tread,nSteps)

#VIEW(adaptedStairs(1.0,5.0,4.0))

wall = COLOR(RED)(CUBOID([1.0,5.0,4.0]))
verStruct = STRUCT([adaptedStairs(1.0,5.0,4.0),T(1)(-1.0),wall])
#VIEW(verStruct)

"""
Funzione per la realizzazione di un corrimano
"""
def handRail (hHandRail,sHandRail,xHandRail,riser,tread,dy,dz):
	shHandRail=hHandRail+sHandRail
	
	handRail2D = MKPOL([[[0,riser+hHandRail],[0,riser+shHandRail],[tread/2,riser+hHandRail],
	[tread/2,riser+shHandRail],[dy,dz+riser+hHandRail],[dy,dz+riser+shHandRail],
	[dy-tread/2,dz+riser+hHandRail],[dy-tread/2,dz+riser+shHandRail],
	[0,riser],[tread/4,riser],[tread/4,riser+hHandRail],
	[dy,dz],[dy-tread/4,dz],[dy-tread/4,dz+riser+hHandRail]],
	[[1,2,4,3],[4,3,7,8],[5,6,7,8],[1,9,10,11],[5,12,13,14]],1])
	
	hHandRail = hHandRail/2
	shHandRail=hHandRail+sHandRail
	
	handRail2D = STRUCT([handRail2D, MKPOL([[[0,riser+hHandRail],[0,riser+shHandRail],[tread/2,riser+hHandRail],
	[tread/2,riser+shHandRail],[dy,dz+riser+hHandRail],[dy,dz+riser+shHandRail],
	[dy-tread/2,dz+riser+hHandRail],[dy-tread/2,dz+riser+shHandRail]],
	[[1,2,4,3],[4,3,7,8],[5,6,7,8]],1]) ])
	
	return PROD([QUOTE([xHandRail]), handRail2D])
	
	

verHR = handRail(0.8,0.05,0.1,0.2,0.25,5,4)
#VIEW(verHR)

"""
Funzione per la realizzazione di una scalinata adattata con due corrimano
"""
def adaptedStairsWithHandRail(dx,dy,dz,colorStairs,colorHandRail):
	stepDimensions = getStepDimensions(dx,dy,dz)
	
	riser = stepDimensions[0]
	tread = stepDimensions[1]
	nSteps = stepDimensions[2]
	
	hr = handRail(0.8,0.05,0.1,riser,tread,dy,dz)
	hr = MATERIAL(goldMaterial)(hr)
	
	s = STRUCT([COLOR(colorStairs)(adaptedStairs(dx,dy,dz)),hr,T(1)(dx-0.1),hr])
	return s

#VIEW(adaptedStairsWithHandRail(4.0,5.0,4.0))
    


"""
Funzione di riferimento per il workshop
"""
def ggpl_concrete_stairs(dx,dy,dz):

    x1 = dx/5
    y1 = dy/5
    z1 = dz/5

    stepDimensions1 = getStepDimensions(x1,y1,z1)
    
    riser1 = stepDimensions1[0]
    tread1 = stepDimensions1[1]
    nSteps1 = stepDimensions1[2]

    yLanding = 1.2

    myStairs = adaptedStairsWithHandRail(x1,y1,z1,WHITE,WHITE)
    myStairs = STRUCT ([myStairs,T([2,3])([y1,z1-riser1]),CUBOID([x1,yLanding,riser1])])

    #VIEW(myStairs)

    x2 = x1
    y2 = y1*4
    z2 = z1*4

    myStairs = STRUCT ([myStairs,T([2,3])([y1+yLanding-tread1,z1]),adaptedStairsWithHandRail(x2,y2,z2),T([2,3])([y2,z2-riser1]),CUBOID([x1,yLanding,riser1])])

    #VIEW(myStairs)

    xWall = 0.2
    zWall = 1.4

    wall2D = MKPOL([[[0,0],[0,z1+zWall],[y1+yLanding,z1+zWall],[y1+yLanding,0],[y1+yLanding+y2-tread1,0]
                ,[y1+yLanding+y2-tread1,z1+z2+zWall],[y1+2*yLanding+y2-tread1,0],[y1+2*yLanding+y2-tread1,z1+z2+zWall]],
                [[1,2,3,4],[3,4,5,6],[5,6,7,8]],1])
    wall = PROD([QUOTE([xWall]),wall2D])
    
    finalStructure = STRUCT([myStairs,T(1)(-xWall),wall,T(1)(x2+xWall),wall])
    #VIEW(finalStructure)
    
    return finalStructure
    
'''
dxDefault = 15.0
dyDefault = 5.0
dzDefault = 4.0

#test scalinata stretta
VIEW(ggpl_concrete_stairs(2.0,3.0,3.0))

#test scalinata lunga
VIEW(ggpl_concrete_stairs(5.0,20.0,20.0))

#test scalinata MODELLO
VIEW(ggpl_concrete_stairs(dxDefault,dyDefault,dzDefault))
'''