# -*- coding: utf-8 -*-

from pyplasm import *
import math

def rotateXYdeg(obj, degrees) :
    obj = STRUCT([R([1,2])(degrees*math.pi*2.0/360.0),obj])
    return obj

def rotateYZdeg(obj, degrees) :
    obj = STRUCT([R([2,3])(degrees*math.pi*2.0/360.0),obj])
    return obj

def rad2deg(radians) :
    return (radians*360.0)/(math.pi*2.0)

def complementar(degrees) :
    return 90-degrees

def translateXY(obj,vector) :
    obj = STRUCT([T([1,2])([vector[0],vector[1]]),obj])
    return obj

def points2center(pointA,pointB) :
    C = []
    C.append((pointA[0]+pointB[0])/2)
    C.append((pointA[1]+pointB[1])/2)
    C.append((pointA[2]+pointB[2])/2)
    return C

def negativeVector(vector) :
    newVector = []
    for val in vector:
        newVector.append(-val)
    return newVector

def points2segment(pointA,pointB) :
    segment = MKPOL([[pointA,pointB],[[1,2]],1])
    return segment
	
def segment2plane(pointA,pointB,degreesInclination) :
    """
    Funzione che genera un piano inclinato passante per un segmento dato
    
    Args:
        pointA[lista di coordinate]: è il primo punto del segmento
        pointB[lista di coordinate]: è il secondo punto del segmento
        degreesInclination[gradi]: è langolo di inclinazione del piano generato espresso in gradi
        
    Returns:
        plane(oggetto hpc): è il piano generato
    """
    
    #pointC è il punto C, centro del segmento AB
    pointC = points2center(pointA,pointB)
    
    #NC è il negativo del vettore posizione del punto C
    NC = negativeVector(pointC)
    
    #segment è il segmento AB
    segment = points2segment(pointA,pointB)

    #utilizzo il vettore NC per centrare il segmento AB rispetto all'origine
    centeredSegment = translateXY(segment,NC)
    
    '''
    utilizzo il punto A (primo parametro) come riferimento per orientare il segmento
    nello specifico traspongo il punto A in un oggetto hpc, lo traslo di NC, 
    ed opero per trovare un angolo che mi permetta di ruotare il segmento AB in modo da avere 
    il punto A giacente sul semiasse positivo delle ascisse
    
    per trovare tale angolo ruoto di 90° il punto A (e conseguentemente l'intero segmento AB)
    fino a che non si trova nel I quadrante (x>0,y>0) e memorizzo le volte con cui ho efettuato la rotazione.
    Successivamente mi calcolo l'angolo che separa il segmento OA (O è l'origine) dall'asse X positivo. 
    Ruoto in senso opposto il segmento AB dell'angolo trovato. Ottengo che l'angolo AB giace interamente sull'asseX
    in maniera orientata (A su asse x positivo e B su asse x negativo)
    '''
    
    pointA = MKPOL([[pointA],[[1]],[[1]]])
    pointA = translateXY(pointA,NC)
    pointAUK = UKPOL(pointA)
    
    counter = 0
    while pointAUK[0][0][0]<0 or pointAUK[0][0][1]<0:
        centeredSegment = rotateXYdeg(centeredSegment,90)
        pointA = rotateXYdeg(pointA,90)
        pointAUK = UKPOL(pointA)
        counter += 1
        
    angleXYrad = complementar(rad2deg(math.atan2(pointAUK[0][0][0],pointAUK[0][0][1])))

    centeredAlignedSegment = rotateXYdeg(centeredSegment,-angleXYrad)
    
    '''
    A partire dal segmento AB costruisco un piano effettuando un JOIN su AB stesso e una sua 
    copia ingrandita e traslata sul semipiano XY con y positivo.
    Faccio l'OFFSET del piano per permettere le intersezioni.
    Effettuo sul piano le stesse operazioni di rotazione e traslazione effettuate sul segmento ma in ordine inverso
    Il piano generato si trova nella posizione originale del segmento. 
    '''
    
    plane = JOIN([centeredAlignedSegment,STRUCT([T(2)(4),S(1)(5),centeredAlignedSegment])])
    plane = OFFSET([0.0,0.0,0.01])(plane)
    plane = rotateYZdeg(plane,degreesInclination)
    plane = rotateXYdeg(plane,angleXYrad)
    while counter > 0 :
        plane = rotateXYdeg(plane,-90)
        counter -= 1
    plane = translateXY(plane,pointC)
    
    return plane
	
def getAngle(Poriginal,Ooriginal,Qoriginal) :
    """
    Funzione che ritorna l'angolo compreso tra 3 punti dati
    
    Args:
        Poriginal[lista di coordinate]: è il punto che precede quello su cui è calcolato l'angolo
        Ooriginal[lista di coordinate]: è il punto su cui è calcolato l'angolo
        Qoriginal[lista di coordinate]: è il punto che segue quello su cui è calcolato l'angolo
        
    Returns:
        angle(gradi): è l'angolo compreso tra i segmenti PO e OQ espresso in gradi
    """
    '''
    copio i punti in nuove strutture dati per non modificare quelle originali
    il punto centrale su cui voglio calcolare l'angolo è O, P lo precede mentre Q viene subito dopo.
    L'angolo di interesse è dunque compreso tra i segmenti PO e OQ
    '''
    P = [Poriginal[0],Poriginal[1]]
    O = [Ooriginal[0],Ooriginal[1]]
    Q = [Qoriginal[0],Qoriginal[1]]
    
    '''traspongo i punti in oggetti hpc'''
    O1 = MKPOL([[[O[0],O[1]]],[[1]],[[1]]])
    P1 = MKPOL([[[P[0],P[1]]],[[1]],[[1]]])
    Q1 = MKPOL([[[Q[0],Q[1]]],[[1]],[[1]]])

    '''traslo P e Q del negativo del vettore posizione di O (O diventa l'origine)'''
    P1 = STRUCT([T([1,2])([-O[0],-O[1]]),P1])
    Q1 = STRUCT([T([1,2])([-O[0],-O[1]]),Q1])

    '''aggiorno le coordinate di P'''
    P[0] = (UKPOL(P1))[0][0][0]
    P[1] = (UKPOL(P1))[0][0][1]
    
    '''ricavo l'angolo alfa che intercorre tra il semiasse positivo X ed il segmento PO'''
    alfa = math.atan2(P[1],P[0])
    
    '''ruoto l' intera struttura di -alfa (PO giace sul semiasse positivo X) '''
    Q1 = STRUCT([R([1,2])(-alfa),Q1])
    P1 = STRUCT([R([1,2])(-alfa),P1])
    
    '''aggiorno le coordinate di Q'''
    Q[0] = (UKPOL(Q1))[0][0][0]
    Q[1] = (UKPOL(Q1))[0][0][1]
    
    '''calcolo l' angolo di interesse come l' angolo compreso tra il semiasse positivo X ed il segmento OQ'''
    beta = math.atan2(Q[1],Q[0])
    
    if beta>0 :
        angle = beta*180.0/math.pi
        return angle
    else:
        angle = (2*math.pi+beta)*180.0/math.pi
        return angle
    
    
    
    
def fillPolygon (polygonPointsOriginal) :
    """
    Funzione che dato un perimetro, lo "riempie", restituendo l'oggetto hpc relativo
    
    Args:
        polygonPointsOriginal[lista di punti]: sono i punti che costituiscono il perimetro del poligono
        
    Returns:
        .(oggetto hpc): è il risultato della differenza tra il minimo poligono convesso e 
        gli spazi vuoti generati dalle concavità oppure è il minimo poligono convesso se non ci sono 
        spazi vuoti da eliminare.
    """
    '''imposto una variabile di controllo'''
    control = 0
    
    '''copio la lista di punti per non modificare l' originale '''
    polygonPoints = list(polygonPointsOriginal)
    
    '''ricavo il piano minimo convesso comprendente i punti della lista'''
    cell = []
    for i in range(1,len(polygonPoints)+1) : cell.append(i)
    convexPolygon = MKPOL([polygonPoints,[cell],1])
    
    
    finish = False
    spacesToEliminate = []
    concaveList = []
    indicesPointsToPreserve = []
    #print "sto entrando nel while"
    
    '''
    Itero l' algoritmo fino a che ho tutti vertici convessi oppure ho superato il limite imposto dal controllo
    L' algoritmo consiste nell'individuare gli spazi vuoti presenti nelle concavità del poligono.
    Ciascuno spazio vuoto è ottenuto come JOIN di una serie di vertici concavi consecutivi ed i due vertici convessi 
    che rispettivamente precedono e seguono la serie di concavi.
    Per ogni spazio vuoto individuato viene memorizzato il relativo piano e vengono eliminati dalla lista di punti 
    i vertici concavi che lo generano.
    Dopo un certo numero di iterazioni rimarranno solo i vertici di bordo del piano minimo convesso che li racchiude tutti
    '''
    while not finish and control <10:
        #print "sono nel while"
        finish = True
        prevIsConcave = False
        
        if indicesPointsToPreserve:
            oldPolygonPoints = list(polygonPoints)
            polygonPoints = []
            for i in indicesPointsToPreserve : polygonPoints.append(oldPolygonPoints[i])
        indicesPointsToPreserve = []
        
        #print polygonPoints
            
        for i in range(0,len(polygonPoints)) :
            #print i
            
            currentPoint = polygonPoints[i]
            if i == 0 :     
                prevPoint = polygonPoints[len(polygonPoints)-1]
                nextPoint = polygonPoints[i+1]
            elif i == len(polygonPoints)-1 :
                prevPoint = polygonPoints[i-1]
                nextPoint = polygonPoints[0]
            else : 
                prevPoint = polygonPoints[i-1]
                nextPoint = polygonPoints[i+1]

            angle = getAngle(prevPoint,currentPoint,nextPoint)
            
            currentHPC = MKPOL([[[currentPoint[0],currentPoint[1]]],[[1]],[[1]]])
            prevHPC = MKPOL([[[prevPoint[0],prevPoint[1]]],[[1]],[[1]]])
            nextHPC = MKPOL([[[nextPoint[0],nextPoint[1]]],[[1]],[[1]]])
            
            if angle > 180.0 :
                #print "concave"
                if not prevIsConcave : concaveList.append(prevHPC)
                concaveList.append(currentHPC)
                
                
                finish = False
                prevIsConcave = True
                
            else :
                indicesPointsToPreserve.append(i)
                #print "convex"
                #print prevIsConcave
                if prevIsConcave : 
                    #print "colcluso serie di concavi"
                    concaveList.append(currentHPC)
                    #if concaveList : print "lista di concavi non vuota"
                    spacesToEliminate.append(JOIN(concaveList))
                    concaveList = []
                    prevIsConcave = False
            
        control += 1
    
    '''Per ottenere il piano di interesse sottraggo gli spazi vuoti individuati al piano minimo convesso'''
    convexPolygon = OFFSET([0.0,0.0,0.01])(convexPolygon)
    if spacesToEliminate : 
        spacesToEliminate = OFFSET([0.0,0.0,0.01])(STRUCT(spacesToEliminate))
        return DIFFERENCE([convexPolygon,spacesToEliminate])
    else : return convexPolygon
	
def generateRoof (pointsList,height,inclinationAngle) :
    """
    Funzione che genera il tetto a partire da un poligono qualsiasi dato
    
    Args:
        pointsList[lista di punti]: sono i punti che costituiscono il perimetro del poligono
        height[numero reale]: è l'altezza del tetto
        inclinationAngle[gradi]: è l'angolo di inclinazione delle falde del tetto
        
    Returns:
        finalRoof(oggetto hpc): è il tetto generato
    """
    '''trovo le dimensioni massime del poligono'''
    xMax = pointsList[0][0]
    yMax = pointsList[0][1]
    
    for point in pointsList :
        if point[0] > xMax : xMax = point[0]
        if point[1] > yMax : yMax = point[1]
    
    '''costruisco due liste di segmenti del poligono, la prima contenente oggetti hpc, la seconda contenente coppie di punti'''
    segments = []
    segmentsList = []
    for i in range(0,len(pointsList)) :
        if i == len(pointsList)-1 : 
            segments.append(points2segment(pointsList[i],pointsList[0]))
            segmentsList.append([pointsList[i],pointsList[0]])
        else : 
            segments.append(points2segment(pointsList[i],pointsList[i+1]))
            segmentsList.append([pointsList[i],pointsList[i+1]])
            
    #VIEW(COLOR(RED)(STRUCT(segments)))
    
    '''grazie alla funzione generatrice di piani costruisco una lista di piani corrispondenti ai segmenti del poligono'''
    planeList = []
    for segment in segmentsList :
        planeList.append(segment2plane(segment[0],segment[1],inclinationAngle))
        
    baseCube = COLOR(BLUE)(CUBOID([xMax,yMax,0]))
    planeList.append(baseCube)
    #VIEW(STRUCT(planeList))
    
    '''costruisco una lista di falde intersecando due a due i piani della lista costruita precedentemente'''
    faldesList = []
    for i in range(0,len(planeList)-1):
        if i == len(planeList)-2 : faldesList.append(INTERSECTION([planeList[i],planeList[0]]))
        else : faldesList.append(INTERSECTION([planeList[i],planeList[i+1]]))
                 
    #VIEW(STRUCT(faldesList))

    '''costruisco una nuova lista di falde troncando quelle precedenti in funzione dell' altezza indicata per il tetto'''
    newfaldesList = []
    for falde in faldesList :
        newfaldesList.append(DIFFERENCE([falde,STRUCT([T(3)(height),CUBOID([xMax*2,yMax*2,height*10])])]))

    #VIEW(STRUCT([COLOR(RED)(STRUCT(segments)),COLOR(BLUE)(STRUCT(newfaldesList))]))
    
    '''
    costruisco la lista degli effettivi piani inclinati del tetto facendo il JOIN a due a due 
    delle falde precedentemente individuate
    '''
    newPlanes = []
    for i in range (0,len(newfaldesList)) :
        if i == len(newfaldesList)-1 : newPlanes.append(TEXTURE("textures/texture_roof_amplied.jpg")(JOIN([newfaldesList[i],newfaldesList[0]])))
        else : newPlanes.append(TEXTURE("textures/texture_roof_amplied.jpg")(JOIN([newfaldesList[i],newfaldesList[i+1]])))
    
    '''ottengo la superficie laterale del tetto unendo i piani trovati precedentemente'''
    finalRoof = STRUCT(newPlanes)
    #VIEW(finalRoof)
    
    finalRoofUK = UKPOL(finalRoof)

    '''individuo i punti posti ad altezza massima del tetto(eliminando i doppioni generati dagli OFFSET)'''
    elevatedPoints = []
    for point in finalRoofUK[0] :
        if point[2] < height+0.1 and point[2] > height-0.1 :
            alreadyInsert = False
            for elevatedPoint in elevatedPoints :
                xDiff = point[0] > elevatedPoint[0] + 0.1 or point[0] < elevatedPoint[0] - 0.1
                yDiff = point[1] > elevatedPoint[1] + 0.1 or point[1] < elevatedPoint[1] - 0.1
                if not xDiff and not yDiff : 
                    alreadyInsert = True
            if not alreadyInsert : 
                point[2] = 0.0
                elevatedPoints.append(point)
                
    '''metto in ordine i punti trovati precedentemente ottenendo il poligono di bordo della terrazza'''
    orderedElevatedPoints = []
    for point in pointsList :
        proximityPoint = elevatedPoints[0]
        proximityX = math.fabs(elevatedPoints[0][0]-point[0])
        proximityY = math.fabs(elevatedPoints[0][1]-point[1])
        distance = math.sqrt(proximityX*proximityX+proximityY*proximityY)
        for i in range (1,len(elevatedPoints)):
            newProximityX = math.fabs(elevatedPoints[i][0]-point[0])
            newProximityY = math.fabs(elevatedPoints[i][1]-point[1])
            newDistance = math.sqrt(newProximityX*newProximityX+newProximityY*newProximityY)
            if newDistance < distance :
                proximityPoint = elevatedPoints[i]
                proximityX = newProximityX
                distance = newDistance
                
        orderedElevatedPoints.append(proximityPoint)
        
    elevatedPoints = orderedElevatedPoints
    
    '''genero poligono di bordo della terrazza'''
    elevatedSegments = []
    for i in range(0,len(elevatedPoints)) :
        if i == len(elevatedPoints)-1 : elevatedSegments.append(points2segment(elevatedPoints[i],elevatedPoints[0]))
        else : elevatedSegments.append(points2segment(elevatedPoints[i],elevatedPoints[i+1]))

    #VIEW(STRUCT(elevatedSegments))
    '''genero la terrazza riempiendo il poligono trovato con la funzione "fillPolygon" e vi applico una texture'''
    terrace = STRUCT([T(3)(height),fillPolygon(elevatedPoints)])
    
    terrace = TEXTURE("textures/texture_terrace_amplied.jpg")(terrace)
    #VIEW(terrace)
    
    '''costruisco una ringhiera che segue il perimetro della terrazza'''
    railingH = 0.8
    elevatedPolygon = STRUCT(elevatedSegments)
    railingElements = []
    for point in elevatedPoints :
        railingElements.append(STRUCT([T([1,2,3])([point[0],point[1],height]),CYLINDER([.01,railingH])(10)]))
    railingElements.append(OFFSET([.02,.02,.02])(STRUCT([T(3)(height+railingH*3.0/5.0),elevatedPolygon,T(3)(railingH*1.0/5.0),elevatedPolygon,T(3)(railingH*1.0/5.0),elevatedPolygon])))

    railing = COLOR(BLACK)(STRUCT(railingElements))
    
    '''ritorno la struttura finale comprensiva di superfice laterale, terrazza e ringhiera'''
    finalRoof = STRUCT([finalRoof,terrace,railing])
    return finalRoof