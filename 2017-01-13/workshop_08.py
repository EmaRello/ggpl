# -*- coding: utf-8 -*-
from pyplasm import *
from math import *
from workshop_07 import *

stimatedError = 0.5

def semiEqualsNumber(numberA,numberB,error) :
	return numberA < numberB+error and numberA > numberB-error

def semiEquals(pointA,pointB,error) :
	return pointA[0] < pointB[0]+error and pointA[0] > pointB[0]-error and pointA[1] < pointB[1]+error and pointA[1] > pointB[1]-error

def pointIsInList(point,listOfPoints) :
	for p in listOfPoints :
		if semiEquals(point,p,stimatedError) : return True
	return False

def windowIsDisable(winOrientation,disableWindows):
		for dw in disableWindows:
			if winOrientation == dw : return True
		return False
		
def lines2structure(fileName,doorsWindowsFileName,structureDepth,internalDepth,originalEntrance,plantX,plantY,plantZ,enableWall,disableWindows,colors):
	
	import csv
	with open (fileName, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			
			minx = +1000.
			maxx = -1000.
			miny = +1000.
			maxy = -1000.

			for row in spamreader:
				if float(row[0]) < minx : minx = float(row[0])
				if float(row[0]) > maxx : maxx = float(row[0])
				if float(row[2]) < minx : minx = float(row[2])
				if float(row[2]) > maxx : maxx = float(row[2])
				if float(row[1]) < miny : miny = float(row[1])
				if float(row[1]) > maxy : maxy = float(row[1])	
				if float(row[3]) < miny : miny = float(row[3])
				if float(row[3]) > maxy : maxy = float(row[3])
	
	originalX = maxx-minx
	originalY = maxy-miny
	
	'''
	if not originalEntrance%2 == 0 :
		tmp = plantX
		plantX = plantY
		plantY = tmp
	'''
	
	scaleX = plantX/originalX
	scaleY = plantY/originalY
	
	
	'''
	if not originalEntrance%2 == 0 :
		tmp = scaleX
		scaleX = scaleY
		scaleY = tmp
	'''
	
	minx = float(minx)*scaleX
	maxx = float(maxx)*scaleX
	miny = float(miny)*scaleY
	maxy = float(maxy)*scaleY
	
				
	initialized = False
	with open (fileName, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				
            for row in spamreader:
				points = []
				for val in row:
					points.append(float(val))
					#print points
				
				points[0] = points[0]*scaleX
				points[1] = points[1]*scaleY
				points[2] = points[2]*scaleX
				points[3] = points[3]*scaleY
				
				if semiEqualsNumber(points[0],minx,stimatedError): points[0]=minx
				if semiEqualsNumber(points[0],maxx,stimatedError): points[0]=maxx
				if semiEqualsNumber(points[2],minx,stimatedError): points[2]=minx
				if semiEqualsNumber(points[2],maxx,stimatedError): points[2]=maxx
				if semiEqualsNumber(points[1],miny,stimatedError): points[1]=miny
				if semiEqualsNumber(points[1],maxy,stimatedError): points[1]=maxy
				if semiEqualsNumber(points[3],miny,stimatedError): points[3]=miny
				if semiEqualsNumber(points[3],maxy,stimatedError): points[3]=maxy
				
				listOfPoints = [[minx,miny],[minx,maxy],[maxx,miny],[maxx,maxy]]
				if not (pointIsInList([points[0],points[1]],listOfPoints) and pointIsInList([points[2],points[3]],listOfPoints)) :
					newWall = STRUCT([MKPOL([[[points[0]-(maxx+minx)/2, points[1]-(maxy+miny)/2,0], [points[2]-(maxx+minx)/2, points[3]-(maxy+miny)/2,0]],[[1,2]],[[1]]])])
					if not initialized:
						wall = newWall
						initialized = True
					else : wall = STRUCT([wall,newWall])
	
	
	pointsDW = []
	holesDW = []
	holesDWhpc = CUBOID([0,0,0])
	doorsAndWindows = []
	doorsAndWindowsHPC = CUBOID([0,0,0])
	with open (doorsWindowsFileName, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:
				row[0] = float(row[0])*scaleX
				row[1] = float(row[1])*scaleY
				
				borderPoint = False
				if semiEqualsNumber(row[0],maxx,stimatedError) : 
					row[0] = maxx
					borderPoint = True
				if semiEqualsNumber(row[0],minx,stimatedError) : 
					row[0] = minx
					borderPoint = True
				if semiEqualsNumber(row[1],maxy,stimatedError) : 
					row[1] = maxy
					borderPoint = True
				if semiEqualsNumber(row[1],miny,stimatedError) : 
					row[1] = miny
					borderPoint = True
				
				point = [row[0]-(maxx+minx)/2,row[1]-(maxy+miny)/2]
				
				pointHPC = MKPOL([[point],[[1]],1])
				pointHPC = R([1,2])(math.pi/2*originalEntrance)(pointHPC)
				
				if borderPoint : pointHPC = S([1,2])([1-(structureDepth)/plantX,1-(structureDepth)/plantY])(pointHPC)
				else : pointHPC = S([1,2])([1-(structureDepth*2+internalDepth)/plantX,1-(structureDepth*2+internalDepth)/plantY])(pointHPC)
				
				if not originalEntrance%2 == 0 :
					pointHPC = S([1,2])([plantX/plantY,plantY/plantX])(pointHPC)
				
				point = UKPOL(pointHPC)[0][0]
				
				pointsDW.append(point)
				'''
				if not ( semiEqualsNumber(row[0],maxx,stimatedError) or semiEqualsNumber(row[0],minx,stimatedError) or semiEqualsNumber(row[1],maxy,stimatedError) or semiEqualsNumber(row[1],miny,stimatedError) ) :
					point = [row[0]-(maxx+minx)/2+internalDepth/2,row[1]-(maxy+miny)/2+internalDepth/2]
					pointsDW.append(point)
				else :
					point = [row[0]-(maxx+minx)/2+internalDepth/2,row[1]-(maxy+miny)/2+internalDepth/2]
					point[0] = point[0] * (1+(internalDepth*2+structureDepth*2)/plantX)
					point[1] = point[1] * (1+(internalDepth*2+structureDepth*2)/plantY)
					pointsDW.append(point)	
                '''
				if row[2] == 'd' :
					doorHoleX = structureDepth+0.5
					doorX = internalDepth
					if borderPoint : doorX = structureDepth
					doorY = 1.0
					doorZ = 2.5
					
					door = firstDoor(doorX,doorY,doorZ)
					if borderPoint :
						doorY = 2.0
						door = secondDoor(doorX,doorY,doorZ)
					door = T([1,2])([-doorX/2,-doorY/2])(door)
					doorHole = T([1,2])([-doorHoleX/2,-doorY/2])(CUBOID([doorHoleX,doorY,doorZ]))
					
					door = R([1,2])(math.pi/2*(float(row[3])-originalEntrance))(door)
					doorHole = R([1,2])(math.pi/2*(float(row[3])-originalEntrance))(doorHole)
					
					door = T([1,2])(point)(door)
					doorHole = T([1,2])(point)(doorHole)
					
					holesDW.append(doorHole)
					holesDWhpc = STRUCT([holesDWhpc,doorHole])
					doorsAndWindows.append(door)
					doorsAndWindowsHPC =STRUCT([doorsAndWindowsHPC,door])
					
				if row[2] == 'w' and borderPoint and not windowIsDisable(float(row[3]),disableWindows) :
					windowHoleX = structureDepth+0.5
					windowX = internalDepth
					if borderPoint : windowX = structureDepth
					windowY = 1.0
					windowZ = 1.5
					windowH = 1.0
					
					window = T([1,2,3])([-windowX/2,-windowY/2,windowH])(firstWindow(windowX,windowY,windowZ))
					windowHole = T([1,2,3])([-windowHoleX/2,-windowY/2,windowH])(CUBOID([windowHoleX,windowY,windowZ]))
					
					window = R([1,2])(math.pi/2*(float(row[3])-originalEntrance))(window)
					windowHole = R([1,2])(math.pi/2*(float(row[3])-originalEntrance))(windowHole)
					
					window = T([1,2])(point)(window)
					windowHole = T([1,2])(point)(windowHole)
					
					holesDW.append(windowHole)
					holesDWhpc = STRUCT([holesDWhpc,windowHole])
					doorsAndWindows.append(window)
					doorsAndWindowsHPC = STRUCT([doorsAndWindowsHPC,window])
					
			
	wall = R([1,2])(math.pi/2*originalEntrance)(wall)
	
	if not originalEntrance%2 == 0 :
		wall = S([1,2])([plantX/plantY,plantY/plantX])(wall)
	
	wall = S([1,2])([1-(structureDepth*2+internalDepth)/plantX,1-(structureDepth*2+internalDepth)/plantY])(wall)
	wall = OFFSET([internalDepth,internalDepth,0])(wall)
	wall = T([1,2])([-internalDepth/2,-internalDepth/2])(wall)
    
	wall = OFFSET([0.0,0.0,plantZ])(wall)
	
	wall = DIFFERENCE([wall,holesDWhpc])

	wall = COLOR(colors[1])(wall)
	
	if enableWall :
		sD = structureDepth
		externalWall = DIFFERENCE([T([1,2])([-plantX/2,-plantY/2])(CUBOID([plantX,plantY,plantZ])),T([1,2])([-plantX/2+sD,-plantY/2+sD])(CUBOID([plantX-sD*2,plantY-sD*2,plantZ*1.5]))])
		externalWall = DIFFERENCE([externalWall,holesDWhpc])
		
		externalWall = COLOR(colors[0])(externalWall)
		wall = STRUCT([wall,externalWall])
	
	'''
	print pointsDW
	for p in pointsDW : 
		wall = STRUCT([wall,T([1,2])([p[0],p[1]]),CUBOID([0.1,0.1,8])])
	'''
	wall = STRUCT([wall,doorsAndWindowsHPC])
		
	return wall  
	
