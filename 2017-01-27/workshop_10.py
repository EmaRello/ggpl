# -*- coding: utf-8 -*-
from pyplasm import *
from math import *
from workshop_03 import *
from workshop_07 import *
from workshop_08 import *
from workshop_09 import *

ambient   =  [0.24725, 0.1995, 0.0745, 1.0]
diffuse   =  [0.75164, 0.60648, 0.22648, 1.0]
specular  =  [0.628281, 0.555802, 0.366065, 1.0]
emission  =  [0.0,0.0,0.0,0.0]
shininess =  [51.2]
goldMaterial = ambient+diffuse+specular+emission+shininess

def getFlatFromFile(flatFileName,doorsWindowsFileName,structureDepth,originalEntrance,flatX,flatY,flatZ,enableWall,disableWindows,colors):
    '''
    ricavo la struttura dell' appartamento utilizzando il workshop_8 modificato adeguatamente
    anche questa funzione è influenzata dal booleano "enableWall"
    '''
    flat = lines2structure(flatFileName,doorsWindowsFileName,structureDepth,
                            structureDepth/2.5,originalEntrance,flatX,flatY,flatZ,enableWall,disableWindows,colors)
    
    '''
    genero dei bordi di controllo per verificare che le strutture combacino (corretta funzionalità di workshop_8 modificato)
    '''
    edges = STRUCT([T([1,2])([-flatX/2+structureDepth,-flatY/2+structureDepth]),COLOR(RED)(SKEL_1(CUBOID([flatX-structureDepth*2,flatY-structureDepth*2,flatZ])))])
    edges2 = STRUCT([T([1,2])([-flatX/2,-flatY/2]),COLOR(RED)(SKEL_1(CUBOID([flatX,flatY,flatZ])))])
    edges3 = STRUCT([T([1,2])([-flatX/2+structureDepth/2,-flatY/2+structureDepth/2]),COLOR(RED)(SKEL_1(CUBOID([flatX-structureDepth,flatY-structureDepth,flatZ])))])
    
    #flat = STRUCT([flat,edges,edges2,edges3])
        
    sD = structureDepth

    '''
    Inserisco i pilastri se viene disabilitata la visibilità delle mura
    '''
    if not enableWall :
        pillar = (CUBOID([sD,sD,flatZ]))
        pillar = COLOR(colors[2])(pillar)
        
        pillarNE = T([1,2])([flatX/2-sD,flatY/2-sD])(pillar)
        pillarNW = S([1,2])([-1,1])(pillarNE)
        pillarSW = S([1,2])([-1,-1])(pillarNE)
        pillarSE = S([1,2])([1,-1])(pillarNE)
        
        flat = STRUCT([flat,pillarNE,pillarNW,pillarSW,pillarSE])
        
        pillar = (CUBOID([sD,sD,flatZ]))
        pillar = COLOR(colors[2])(pillar)
        
        midPillarW = T([1,2])([flatX/2-sD,-sD/2])(pillar)
        midPillarN = T([1,2])([-sD/2,flatY/2-sD])(pillar)
        midPillarE = S([1,2])([-1,1])(midPillarW)
        midPillarS = S([1,2])([1,-1])(midPillarN)
        
        flat = STRUCT([flat,midPillarE,midPillarN,midPillarW,midPillarS])
        
    '''
    ritorno l'appartamento
    '''        
    return flat

#VIEW(getFlatFromFile2('plant.lines','doorsWindowsPoints.pointsDW',.5,3,15.0,11.0,3.5,True,[0,3],[]))


def assembleStairsAndLanding(landingX,landingY,dz,landingPlus,floorNumber,structureDepth,enableWall,colors):
    '''
    ricavo le dimensioni della scalla da quelle del pianerottolo.
    utilizzo il workshop_3 per realizzare la scala con il corrimano
    '''
    dx = landingX/4
    dy = landingY/2
    stepDimensions = getStepDimensions(dx,dy,dz)
    
    riser = stepDimensions[0]
    tread = stepDimensions[1]
    nSteps = stepDimensions[2]
    
    landing = STRUCT([T([1,2,3])([-dx*2,-dy,dz-structureDepth]),CUBOID([landingX,landingY+landingPlus,structureDepth])])
    
    '''
    realizzo una barriera per il vano scala
    '''
    barrierH = 0.85 + riser
    barrierS = 0.1                  
    stairs = STRUCT([T([1,2])([-dx-barrierS,-dy/2]),adaptedStairsWithHandRail(dx,dy,dz,colors[3],colors[4])])
    
    
    landingHole = STRUCT([T([1,2,3])([-dx-barrierS,-dy/2,dz-structureDepth]),CUBOID([dx,dy,structureDepth+barrierH+0.1])])
    landingHoleBarrier = STRUCT([T([1,2,3])([-dx-barrierS*2,-dy/2-barrierS,dz]),CUBOID([dx+barrierS*3,dy+barrierS,barrierH])])
    landingHoleBarrier = DIFFERENCE([landingHoleBarrier,landingHole])
    if (floorNumber % 2 == 0) : 
                    stairs = STRUCT([S([1,2])([-1,-1]),stairs])
                    landingHole = STRUCT([S([1,2])([-1,-1]),landingHole])
                    landingHoleBarrier = STRUCT([S([1,2])([-1,-1]),landingHoleBarrier])
                      
    landing = DIFFERENCE([landing,landingHole])
    landing = COLOR(colors[3])(landing)
    
    '''
    in funzione dell'abilitazione dei muri realizzo le mura del pianerottolo oppure i pilastri che sostengono il piano superiore
    '''
    pillarDepth = structureDepth
    if enableWall : 
        pillarDepth = landingX
        pillarColor = colors[0]
        
    else : pillarColor = colors[2]
    
    pillar = CUBOID([pillarDepth,structureDepth,dz-structureDepth])
    
    '''
    inserisco una finestra dirimpetto alla scalinata
    '''
    pillarN = T([1,2,3])([-pillarDepth/2,-landingY/2,dz])(pillar)
    windowHoleX = structureDepth+0.5
    windowX = structureDepth
	# MOD : window Y + 1.0
    windowY = 2.0
    windowZ = 1.5
    windowH = 1.0
    window = T([1,2,3])([-windowX/2,-windowY/2,windowH+dz])(firstWindow(windowX,windowY,windowZ))
    windowHole = T([1,2,3])([-windowHoleX/2,-windowY/2,windowH+dz])(CUBOID([windowHoleX,windowY,windowZ]))
    window = R([1,2])(3*math.pi/2)(window)
    windowHole = R([1,2])(math.pi/2)(windowHole)
    window = T(2)(-landingY/2+structureDepth/2)(window)
    windowHole = T(2)(-landingY/2+structureDepth/2)(windowHole)
    pillarN = DIFFERENCE([pillarN,windowHole])
    pillarN = COLOR(pillarColor)(pillarN)
    pillarN = STRUCT([pillarN,window])
    
    pillarS = T([1,2,3])([-pillarDepth/2,+landingY/2-structureDepth+landingPlus,dz])(pillar)
    pillarS = COLOR(pillarColor)(pillarS)
    
    landing = STRUCT([landing,pillarN,pillarS])
    
    landingHoleBarrier = MATERIAL(goldMaterial)(landingHoleBarrier)
    stairsAndLanding = STRUCT([stairs,landing,landingHoleBarrier])
    
    '''
    ritorno il pianerottolo con le scale
    '''                  
    return stairsAndLanding


def assembleSingleFloor(structureDepth,numberOfFloors,floorHeight,
                           numberOfFlatsForFloor,flatFileName,doorsWindowsFileName,flatOriginalEntrance,
                           flatX,flatY,landingX,landingY,enableWall,floorCount,colors) :
    
        '''
        calcolo la lunghezza aggiuntiva del pianerottolo in funzione del numero di appartemanti per piano.
        se la lunghezza lo consente inserisco una nuova rampa di scale speculare alla prima.
        '''
        landingPlus = -landingY + flatY*(int(float(numberOfFlatsForFloor)/2+0.5))
        
        if landingPlus > landingY :
            landingPlus = (landingPlus-landingY)/2
            centralLanding = assembleStairsAndLanding(landingX,landingY,floorHeight,
                                                      landingPlus,floorCount,structureDepth,enableWall,colors)
            centralLandingReverse = S([1,2])([-1,-1])(centralLanding) 
            centralLandingReverse = T(2)(landingY+landingPlus*2)(centralLandingReverse)
            centralLanding = STRUCT([centralLanding,centralLandingReverse])
            
        else :
            centralLanding = assembleStairsAndLanding(landingX,landingY,floorHeight,
                                                      landingPlus,floorCount,structureDepth,enableWall,colors)
        
        singleFloor = centralLanding           
        
        tX = -landingX/2-flatX/2
        tY = -landingY/2-flatY/2
        
        '''
        inserisco progressivamente gli appartamenti nel piano, gestendo dei casi particolari
        '''
        for i in range (0,numberOfFlatsForFloor) :
            
            '''
            a seconda della posizione dell'appartamento decido quali finestre esterne vanno disabilitate.
            le finestre che danno sul pianerottolo (concordi alla porta di ingresso) vengono disabilitate sempre
            '''
            est = 3
            nord = est + 1
            ovest = est + 2
            sud = est + 3
            for c in [est,nord,ovest,est] :
                if c == 4 : c = 0
                if c == 5 : c = 1
                if c == 6 : c = 2
            
            if numberOfFlatsForFloor <= 2 : disableWindows = [est]
                
            elif numberOfFlatsForFloor == 3 and i == 1 : disableWindows = [est]
            
            elif i == 0 or i == 1 : disableWindows = [sud,est]
                
            elif i == numberOfFlatsForFloor-1 or i == numberOfFlatsForFloor-2 : disableWindows = [nord,est]
                
            else : disableWindows = [nord,sud,est]            
            
            '''
            genero un appartamento
            '''
            flat = getFlatFromFile(flatFileName,doorsWindowsFileName,structureDepth,
                                    flatOriginalEntrance,flatX,flatY,floorHeight-structureDepth,enableWall,disableWindows,colors)
            flat = STRUCT([flat,T([1,2,3])([-flatX/2,-flatY/2,-structureDepth]),COLOR(colors[3])(CUBOID([flatX,flatY,structureDepth]))])
            flat = T(3)(floorHeight)(flat)
            flatReverse = S(1)(-1)(flat)
            
            '''
            assemblo progressivamente gli appartamenti al piano
            '''
            tX = -tX
            flatToAdd = flatReverse
            if (i % 2 == 0) : 
                tY += flatY
                flatToAdd = flat
                
            singleFloor = STRUCT([singleFloor,T([1,2])([tX,tY]),flatToAdd])
        
        '''
        gestisco mura, pilastri, porte e finestre del piano (non dell'appartamento) in funzione al numero di appartamenti(paro o disparo)
        '''
        if not (numberOfFlatsForFloor % 2 == 0) :
            oddPillarX = structureDepth
            oddPillarY = structureDepth
            if enableWall : oddPillarY = flatY
            oddPillar = T([1,2,3])([-landingX/2,-oddPillarY-landingY/2+flatY*(int(float(numberOfFlatsForFloor)/2+0.5)),floorHeight])(CUBOID([oddPillarX,oddPillarY,floorHeight-structureDepth]))
            if not enableWall : oddPillarColor = colors[2]
            else : oddPillarColor = colors[0]
            
            windowHoleX = structureDepth+0.5
            windowX = structureDepth
			# MOD : window Y + 1.0
            windowY = 2.0
            windowZ = 1.5
            windowH = 1.0
            window = T([1,2,3])([-windowX/2,-windowY/2,windowH+floorHeight])(firstWindow(windowX,windowY,windowZ))
            
            if floorCount == 0 :
				# MOD : window Y + 1.0
                windowY = 3.5
                windowZ = 2.5
                windowH = 0.0
                window = T([1,2,3])([-windowX/2,-windowY/2,windowH+floorHeight])(secondDoor(windowX,windowY,windowZ))     
                
            windowHole = T([1,2,3])([-windowHoleX/2,-windowY/2,windowH+floorHeight])(CUBOID([windowHoleX,windowY,windowZ]))
            window = R([1,2])(2*math.pi/2)(window)
            windowHole = R([1,2])(2*math.pi/2)(windowHole)
            
            window = T([1,2])([-landingX/2+structureDepth/2,flatY*(int(float(numberOfFlatsForFloor)/2+0.5))-flatY/2-landingY/2])(window)
            windowHole = T([1,2])([-landingX/2+structureDepth/2,flatY*(int(float(numberOfFlatsForFloor)/2+0.5))-flatY/2-landingY/2])(windowHole)
            oddPillar = DIFFERENCE([oddPillar,windowHole])
            oddPillar = COLOR(oddPillarColor)(oddPillar)
            
            if enableWall : oddPillar = STRUCT([oddPillar,window])
            
            singleFloor = STRUCT([singleFloor,oddPillar])
            
            if (numberOfFlatsForFloor==1 and not enableWall) :
                singularPillar = T(2)(structureDepth-flatY*(int(float(numberOfFlatsForFloor)/2+0.5)))(oddPillar)
                singleFloor = STRUCT([singleFloor,singularPillar])
        '''
        ritorno il singolo piano
        '''
        return singleFloor


def assembleGroundFloor(structureDepth,numberOfFloors,floorHeight,numberOfFlatsForFloor,flatX,flatY,landingX,landingY,enableWall,colors):
    groundFloor = CUBOID([0,0,0])
    
    '''
    predispongo per il calcolo delle dimensioni dell'edificio ed il posizionamento dei pilastri
    '''
    sdD = structureDepth*2
    pillarDepth = structureDepth
    wallDepth = structureDepth
    landingPlus = -landingY + flatY*(int(float(numberOfFlatsForFloor)/2+0.5))
    buildingX = flatX*2 + landingX
    buildingY = landingY + landingPlus
    
    pillar = T([1,2])([-sdD/2,-sdD/2])(CUBOID([sdD,sdD,floorHeight-structureDepth]))
    
    '''
    definisco le posizioni dei piloni angolari
    '''
    pointNE = [-landingX/2-flatX+sdD/2,-landingY/2+sdD/2]
    pointNW = [+landingX/2+flatX-sdD/2,-landingY/2+sdD/2]
    pointSW = [+landingX/2+flatX-sdD/2,landingY/2+landingPlus-sdD/2]
    pointSE = [-landingX/2-flatX+sdD/2,landingY/2+landingPlus-sdD/2]
    quadraturePoints = [pointNE,pointNW,pointSW,pointSE]
    
    '''
    gestisco il caso in cui ho solo un appartamento per piano (perdo la simmetria rispetto al pianerottolo)
    '''
	
	#MOD : commented if structure
    '''
    if numberOfFlatsForFloor == 1 :
        pointNE[0] += flatX
        pointSE[0] += flatX
    '''
        
    doorHoleX = sdD+0.5
    doorX = sdD
    doorY = 3.0
    doorZ = 3.0
    door = secondDoor(doorX,doorY,doorZ)
    door = T([1,2])([-doorX/2,-doorY/2])(door)
    doorHole = T([1,2])([-doorHoleX/2,-doorY/2])(CUBOID([doorHoleX,doorY,doorZ]))
    door = R([1,2])(math.pi/2)(door)
    door2 = R([1,2])(math.pi)(door)
    doorHole = R([1,2])(math.pi/2)(doorHole)
    
    '''
    genero le mura perimetrali o i pilastri perimetrali a seconda dell'abilitazione o meno delle mura
    '''
    if enableWall[0] :
        wall = T([1,2])([-buildingX/2,-landingY/2])(CUBOID([buildingX,buildingY,floorHeight-structureDepth]))
        wallHole = T([1,2])([+sdD-buildingX/2,+sdD-landingY/2])(CUBOID([buildingX-sdD*2,buildingY-sdD*2,floorHeight*2-structureDepth]))
        wall = DIFFERENCE([wall,wallHole])
        
		#MOD : commented if structure
        '''
        if numberOfFlatsForFloor == 1 :
            wall = S(1)(1-flatX/buildingX)(wall)
            wall = T(1)(flatX/2)(wall)
        '''
            
        doorHole = T(2)(buildingY-landingY/2-sdD/2)(doorHole)
        wall = DIFFERENCE([wall,doorHole])
        doorHole = T(2)(-buildingY+sdD)(doorHole)
        wall = DIFFERENCE([wall,doorHole])
        
        wall = COLOR(colors[0])(wall)
        
        groundFloor = STRUCT([groundFloor,wall])
        
    else :
        pillar = COLOR(colors[2])(pillar)
        pillarPoints=[pointNE,pointNW,pointSW,pointSE]
        pX = pointNE[0]
        pY = pointNE[1] - sdD/2
        for pX in [pointNE[0],pointNE[0]+flatX-sdD/2,pointNW[0],pointNW[0]-flatX+sdD/2]:
            while pY<=pointSE[1]:
                if pY > pointNE[1] : pillarPoints.append([pX,pY])
                pY = pY + flatY #- sdD/2
            pY = pointNE[1] - sdD/2
        
        '''
        genero i pilastri interni
        '''
        for point in pillarPoints :
            groundFloor = STRUCT([groundFloor,T([1,2])([point[0],point[1]]),pillar])
    
    groundFloor = STRUCT([groundFloor,T(2)(buildingY-landingY/2-sdD/2),door,T(2)(-buildingY+sdD),door2])
    
    '''
    realizzo una terrazza nel caso in cui è presente un numero dispari di appartamenti per piano
    '''
	
	# MOD : reintroduced terrace in one flat building
    if (not (numberOfFlatsForFloor % 2 == 0)) :
        gardenPlan = T([2,3])([buildingY-flatY,floorHeight-structureDepth])(CUBOID([flatX,flatY,structureDepth]))
        gardenPlan = T([1,2])([pointNE[0]-sdD/2,pointNE[1]-sdD/2])(gardenPlan)
        #gardenPlan = COLOR(colors[3])(gardenPlan)
        gardenPlan = TEXTURE("textures/texture_terrace_amplied.jpg")(gardenPlan)
        
        railingH = 0.8
        railingPoints = [[-landingX/2-flatX,-landingY/2+flatY*(int(float(numberOfFlatsForFloor)/2+0.5))-flatY],
                         [-landingX/2-flatX,-landingY/2+flatY*(int(float(numberOfFlatsForFloor)/2+0.5))],
                         [-landingX/2,-landingY/2+flatY*(int(float(numberOfFlatsForFloor)/2+0.5))]]
						 
        if numberOfFlatsForFloor == 1: railingPoints = [[-landingX/2,-landingY/2]] + railingPoints
		
        railingLines = STRUCT([MKPOL([[railingPoints[0],railingPoints[1]],[[1,2]],1]),MKPOL([[railingPoints[1],railingPoints[2]],[[1,2]],1])])
		
        if numberOfFlatsForFloor == 1: railingLines = STRUCT([MKPOL([[railingPoints[0],railingPoints[1]],[[1,2]],1]),MKPOL([[railingPoints[1],railingPoints[2]],[[1,2]],1]),MKPOL([[railingPoints[2],railingPoints[3]],[[1,2]],1])])
        
        railingElements = []
        for point in railingPoints :
            railingElements.append(STRUCT([T([1,2,3])([point[0],point[1],floorHeight]),CYLINDER([.01,railingH])(10)]))
        railingElements.append(OFFSET([.02,.02,.02])(STRUCT([T(3)(floorHeight+railingH*3.0/5.0),railingLines,T(3)(railingH*1.0/5.0),railingLines,T(3)(railingH*1.0/5.0),railingLines])))

        railing = COLOR(BLACK)(STRUCT(railingElements))
        
        groundFloor = STRUCT([groundFloor,gardenPlan,railing])
    
    '''
    ritorno il piano terra
    '''
    return groundFloor
	


def assembleBuildingFloors(structureDepth,numberOfFloors,floorHeight,
                           numberOfFlatsForFloor,flatFileName,doorsWindowsFileName,flatOriginalEntrance,
                           flatX,flatY,landingX,landingY,enableWall,enableRoof,colors) :
    '''
    predispongo il calcolo delle dimensioni totali dell'edificio (altezza: escluso il tetto)
    '''
    
    buildingZ = floorHeight
    landingPlus = -landingY + flatY*(int(float(numberOfFlatsForFloor)/2+0.5))
    buildingX = flatX*2 + landingX
    buildingY = landingY + landingPlus
    
    '''
    genero il piano terra con la relativa abilitazione ("enableWall[0]") per la visibilità delle mura
    '''
    building = assembleGroundFloor(structureDepth,numberOfFloors,floorHeight,
                                   numberOfFlatsForFloor,flatX,flatY,landingX,landingY,enableWall,colors)
    
    '''
    genero i piani uno alla volta con le relative abilitazioni ("enableWall[1]-enableWall[numberOfFloors+1]") per la visibilità delle mura
    '''
    for i in range(0,numberOfFloors) : 
        singleFloor = assembleSingleFloor(structureDepth,numberOfFloors,floorHeight,
                           numberOfFlatsForFloor,flatFileName,doorsWindowsFileName,flatOriginalEntrance,
                           flatX,flatY,landingX,landingY,enableWall[i+1],i,colors)
        
        building = STRUCT([building,T(3)(i*floorHeight),singleFloor])
        buildingZ += floorHeight
        
    pointNE = [-landingX/2-flatX,-landingY/2,0]
    pointNW = [+landingX/2+flatX,-landingY/2,0]
    pointSW = [+landingX/2+flatX,landingY/2+landingPlus,0]
    pointSE = [-landingX/2-flatX,landingY/2+landingPlus,0]
    
    '''
    genero il tetto utilizzando workshop_09
    '''
    if enableRoof :
        points = [[0,0,0],[0,buildingY,0],[buildingX,buildingY,0],[buildingX,0,0]]

        roofPlan = CUBOID([buildingX,buildingY,structureDepth])
        roofPlan = COLOR(colors[2])(roofPlan)

        if not (numberOfFlatsForFloor % 2 == 0) :
            points = [[0,0,0],[0,buildingY-flatY,0],[+flatX,buildingY-flatY,0],[+flatX,buildingY,0],[buildingX,buildingY,0],[buildingX,0,0]]
            roofPlanHole = T(2)(buildingY-flatY)(CUBOID([flatX,flatY,structureDepth]))
            roofPlan = DIFFERENCE([roofPlan,roofPlanHole])

            if numberOfFlatsForFloor == 1 : points = [[+flatX,0,0],[+flatX,buildingY,0],[buildingX,buildingY,0],[buildingX,0,0]]

        roofH = 2.5
        roof = STRUCT([generateRoof(points,roofH,40),T(3)(-structureDepth),roofPlan])

        roof = T([1,2])([pointNE[0],pointNE[1]])(roof)

        building = STRUCT([building,T(3)(buildingZ),roof])
    
    '''
    traslo l'edificio interamente nel primo quadrante
    '''
    #MOD: commented if structure
	#if numberOfFlatsForFloor < 2 : flatX = 0
    building = T([1,2])([landingX/2+flatX,landingY/2])(building)
    building = STRUCT([CUBOID([buildingX,buildingY,0.01]),T(3)(0.01),building])
	
    
    '''
    ritorno l'edificio
    '''
    return building
        
    
    
