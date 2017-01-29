# -*- coding: utf-8 -*-
ambient   = [0.0, 0.0, 0.0, 1.0]
diffuse   = [0.588235, 0.670588, 0.729412, 0.5]
specular  = [0.9, 0.9, 0.9, 1.0]
emission  = [0.0, 0.0, 0.0, 1.0]
shininess = [96.0]
glassMaterial = ambient + diffuse + specular + emission + shininess

from pyplasm import *

def sumAllElements(myList):
    """
    Funzione per sommare gli elementi di una lista.
    
    Args:
        myList (lista di reali): lista di cui calcolare la somma degli elementi
        
    Returns:
        s (numero reale): è la soma degli elementi della lista 
    """
    s = 0
    for val in myList:
        s += val
    return s

	
def adaptListToDimension(myList,dim):
    """
    Funzione per adattare gli elementi di una lista ad un valore dello stesso tipo: 
    se il valore dato differisce dalla somma degli elementi della lista, questi ultimi vengono modificati. 
    
    Args:
        myList (lista di reali): lista di numeri da adattare
        dim (reale o intero): valore di riferimento su cui riadattare gli elementi della lista
        
    Returns:
        myList (lista di reali): è la lista opportunatamente riadattata (la somma degli elementi è ora uguale a "dim") 
    """
    summatory = sumAllElements(myList)
    diff = summatory - dim
    diff = diff / len(myList)
    correctList = []
    if summatory is not dim:
        for val in myList : correctList.append(val - diff)
        return correctList
    return myList

def door2D (Ylist,Zlist,occupancy):
    """
    Funzione per generare famiglie di porte o finestre in 2D (piano YZ)
    
    Args:
        Ylist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        Zlist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        occupancy (matrice bidimensionale): matrice che rappresenta l'occupazione o meno di una cella da parte del "solido pieno"
        
    Returns:
        door2D0 (funzione): funzione annidata
    """
    def door2D0(dy,dz):
        """
        Args:
            dy (numero reale): dimensione massima su y del solido
            dz (numero reale): dimensione massima su z del solido
        
        Returns:
            structure (oggetto hpc): porta o finestra riprodotta
        """
    
        Y = adaptListToDimension(Ylist,dy)
        Z = adaptListToDimension(Zlist,dz)
        
        occ = occupancy
        
        structure = STRUCT([CUBOID([0,0,0])])

        sumZ = 0
        i  = 0
        
        for row in occ :
            tmpY = []
            j=0
            for val in row:
                
                if val: tmpY.append(Y[j])
                else: tmpY.append(-Y[j])
                j+=1
                
            qy = QUOTE(tmpY)
            qz = QUOTE([Z[i]])
            pxy = PROD([QUOTE([0]),qy])
            pyz = PROD([pxy,qz])
        
            structure = STRUCT([structure,T([3])([sumZ]),pyz])
            sumZ += Z[i]
            i += 1
            
        return structure
    return door2D0

def door (Xlist,Ylist,Zlist,occupancy):
    """
    Funzione per generare famiglie di porte o finestre in 3D
    
    Args:
        Xlist (lista di reali): lista delle dimensioni sull'asse X di tutte le celle che compongono il solido
        Ylist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        Zlist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        occupancy (matrice tridimensionale booleana): matrice che rappresenta l'occupazione o meno di una cella da parte del "solido pieno"
        
    Returns:
        door0 (funzione): funzione annidata
    """
    def door0(dx,dy,dz):
        """
        Args:
            dx (numero reale): dimensione massima su x del solido
            dy (numero reale): dimensione massima su y del solido
            dz (numero reale): dimensione massima su z del solido
        
        Returns:
            structure (oggetto hpc): porta o finestra riprodotta
        """
        
        X = adaptListToDimension(Xlist,dx)
        Y = adaptListToDimension(Ylist,dy)
        Z = adaptListToDimension(Zlist,dz)
        
        occ = occupancy
        
        structure = STRUCT([CUBOID([0,0,0])])
        
        
        
        sumX = 0
        k = 0
        
        for plan in occ:
            
            page = STRUCT([CUBOID([0,0,0])])
            
            sumZ = 0
            i  = 0
            
            for row in plan :
                tmpY = []
                j=0
                
                allNegative = 1
                
                for val in row:
                
                    if val: 
                        tmpY.append(Y[j])
                        allNegative = 0
                        
                    else: tmpY.append(-Y[j])
                    
                    j+=1
                
                if not allNegative:
                    
                    qy = QUOTE(tmpY)
                    qz = QUOTE([Z[i]])
                    pxy = PROD([QUOTE([X[k]]),qy])
                    pyz = PROD([pxy,qz])
        
                    page = STRUCT([page,T([3])([sumZ]),pyz])
            
                sumZ += Z[i]
                i += 1
            
            structure = STRUCT([structure,T([1])([sumX]),page])
            
            sumX += X[k]
            k += 1
            
        
            
        return structure
    return door0
	
def doorExtended (Xlist,Ylist,Zlist,occupancy,colorList):
    """
    Funzione per generare famiglie di porte o finestre in 3D
    
    Args:
        Xlist (lista di reali): lista delle dimensioni sull'asse X di tutte le celle che compongono il solido
        Ylist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        Zlist (lista di reali): lista delle dimensioni sull'asse Y di tutte le celle che compongono il solido
        occupancy (matrice tridimensionale di interi): matrice che rappresenta l'occupazione o meno di una cella da parte del "solido pieno"
        colorList (lista di colori(liste di 3 numeri reali compresi tra 0 e 1)): sono i colori utilizzati nella modellazione
        
    Returns:
        door0 (funzione): funzione annidata
    """
    
    def door0(dx,dy,dz):
        """
        Args:
            dx (numero reale): dimensione massima su x del solido
            dy (numero reale): dimensione massima su y del solido
            dz (numero reale): dimensione massima su z del solido
        
        Returns:
            totalStructure (oggetto hpc): porta o finestra riprodotta
        """
        
        def door1(cod):
            """
            Args:
                cod (numero intero): è un codice che rappresenta un tipo di materiale
        
            Returns:
                structure (oggetto hpc): parte della struttura riprodotta composto da un singolo materiale, rappresentato da "cod"
            """
            
            X = adaptListToDimension(Xlist,dx)
            Y = adaptListToDimension(Ylist,dy)
            Z = adaptListToDimension(Zlist,dz)
        
            occ = occupancy

            structure = CUBOID([0,0,0])



            sumX = 0
            k = 0

            for plan in occ:

                page = CUBOID([0,0,0])

                sumZ = 0
                i  = 0

                for row in plan :
                    tmpY = []
                    j=0

                    allNegative = 1

                    for val in row:

                        if val == cod: 
                            tmpY.append(Y[j])
                            allNegative = 0

                        else: tmpY.append(-Y[j])

                        j+=1

                    if not allNegative:

                        qy = QUOTE(tmpY)
                        qz = QUOTE([Z[i]])
                        pxy = PROD([QUOTE([X[k]]),qy])
                        pyz = PROD([pxy,qz])

                        page = STRUCT([page,T([3])([sumZ]),pyz])

                    sumZ += Z[i]
                    i += 1

                structure = STRUCT([structure,T([1])([sumX]),page])

                sumX += X[k]
                k += 1

            return structure
        
        totalStructure = CUBOID([0,0,0])
        
        c = 0
        for val in colorList :
			if c == len(colorList)-1 :
				partialStructure = MATERIAL(glassMaterial)(door1(c+1))
			else :
				partialStructure = COLOR(colorList[c])(door1(c+1))
				
			totalStructure = STRUCT([totalStructure,partialStructure])
			c += 1
        
        return totalStructure

    return door0
	
woodColor = [94.0/255,41.0/255,0.0/255]
glassColor = [195.0/255,248.0/255,255.0/255]
steelColor = [192.0/255,192.0/255,192.0/255]
darkSteelColor = [96.0/255,96.0/255,96.0/255]
blackWoodColor = [53.0/255,53.0/255,53.0/255]
ornamentalRedColor = [128.0/255,18.0/255,18.0/255]
ornamentalBrownColor = [119.0/255,84.0/255,52.0/255]

def firstDoor(X,Y,Z) :
	firstDoorX = [0.04,0.03,0.03,0.03,0.08,0.03,0.03,0.03,0.04]
	firstDoorY = [0.1,0.02,0.005,0.15,0.25,0.5,0.25,0.15,0.005,0.02,0.1]
	firstDoorZ = [0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.005,0.02,0.1]

	page1 = [[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]

	page2 = [[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page3 = [[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,1,1,1,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page4 = [[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],
			 [1,1,0,1,0,0,1,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,0,0,1,0,1,1],
			 [1,1,0,1,1,1,1,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page5 = [[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,2,2,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],
			 [1,1,0,1,2,2,1,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,2,2,1,0,1,1],
			 [1,1,0,1,1,1,1,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page6 = [[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],
			 [1,1,0,1,0,0,1,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,1,0,0,1,0,1,1],
			 [1,1,0,1,1,1,1,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page7 = [[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,1,1,1,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,1,1,1,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page8 = [[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],[1,1,0,1,0,0,0,1,0,1,1],
			 [1,1,0,1,0,0,0,1,0,1,1],[1,1,0,0,0,0,0,0,0,1,1],[1,1,1,1,1,1,1,1,1,1,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	page9 = [[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,0,0,0,0,0,0,0,0,0,1],[1,1,0,0,0,0,0,0,0,1,1],[1,0,0,0,0,0,0,0,0,0,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]


	pages = [page1,page2,page3,page4,page5,page6,page7,page8,page9]

	dx = sumAllElements(firstDoorX)
	dy = sumAllElements(firstDoorY)
	dz = sumAllElements(firstDoorZ)

	colorList = [woodColor,glassColor]

	handle = COLOR(steelColor)(STRUCT([CUBOID([0.02,0.08,0.08]),
					 T([1,2,3])([0.02,0.02,0.02]),CUBOID([0.04,0.04,0.04]),
					 T([1,2])([0.04,0.02]),CUBOID([0.01,0.22,0.036])]))

	cylinder = COLOR(steelColor)(CYLINDER([0.01,0.2])(50))

	firstDoor = doorExtended(firstDoorX,firstDoorY,firstDoorZ,pages,colorList)(dx,dy,dz)

	firstDoor = STRUCT([firstDoor,T([1,2,3])([0.3,0.14,1.4]),handle])
	firstDoor = STRUCT([firstDoor,T([1,2,3])([0.3,1.43,0.3]),cylinder,T([3])([2.08]),cylinder])
	
	firstDoor = S([1,2,3])([X/dx,Y/dy,Z/dz])(firstDoor)
	
	return firstDoor

def firstWindow(X,Y,Z) :
	firstWindowX = [0.08,0.06,0.04,0.06,0.04,0.06,0.08,0.1]
	firstWindowY = [0.02,0.1,0.08,0.15,0.03,0.8,0.03,0.15,0.08,0.1,0.02]
	firstWindowZ = [0.12,0.15,0.15,0.03,2.2,0.03,0.15,0.12,0.15]

	page1 = [[0,3,3,3,3,3,3,3,3,3,0],[0,3,0,0,0,0,0,0,0,3,0],[0,3,0,0,0,0,0,0,0,3,0],
			 [0,3,0,0,0,0,0,0,0,3,0],[0,3,0,0,0,0,0,0,0,3,0],[0,3,0,0,0,0,0,0,0,3,0],
			 [0,3,0,0,0,0,0,0,0,3,0],[0,3,0,0,0,0,0,0,0,3,0],[0,3,3,3,3,3,3,3,3,3,0]]

	page2 = [[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,0,0,0,0,0,3,3,0],
			 [0,3,3,0,0,0,0,0,3,3,0],[0,3,3,0,0,0,0,0,3,3,0],[0,3,3,0,0,0,0,0,3,3,0],
			 [0,3,3,0,0,0,0,0,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0]]

	page3 = [[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,0,3,0,3,0,3,3,0],
			 [0,3,3,3,3,3,3,3,3,3,0],[0,3,3,0,3,0,3,0,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],
			 [0,3,3,0,3,0,3,0,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0]]

	page4 = [[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,4,3,4,3,4,3,3,0],
			 [0,3,3,3,3,3,3,3,3,3,0],[0,3,3,4,3,4,3,4,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],
			 [0,3,3,4,3,4,3,4,3,3,0],[0,3,3,3,3,3,3,3,3,3,0],[0,3,3,3,3,3,3,3,3,3,0]]

	page5 = [[1,1,1,1,1,1,1,1,1,1,1],[0,1,2,2,2,2,2,2,2,1,0],[0,1,2,0,2,0,2,0,2,1,0],
			 [0,1,2,2,2,2,2,2,2,1,0],[0,1,2,0,2,0,2,0,2,1,0],[0,1,2,2,2,2,2,2,2,1,0],
			 [0,1,2,0,2,0,2,0,2,1,0],[0,1,2,2,2,2,2,2,2,1,0],[1,1,1,1,1,1,1,1,1,1,1]]

	page6 = [[1,1,1,1,1,1,1,1,1,1,1],[0,1,2,2,2,2,2,2,2,1,0],[0,1,2,0,0,0,0,0,2,1,0],
			 [0,1,2,0,0,0,0,0,2,1,0],[0,1,2,0,0,0,0,0,2,1,0],[0,1,2,0,0,0,0,0,2,1,0],
			 [0,1,2,0,0,0,0,0,2,1,0],[0,1,2,2,2,2,2,2,2,1,0],[1,1,1,1,1,1,1,1,1,1,1]]

	page7 = [[1,1,1,1,1,1,1,1,1,1,1],[0,1,0,0,0,0,0,0,0,1,0],[0,1,0,0,0,0,0,0,0,1,0],
			 [0,1,0,0,0,0,0,0,0,1,0],[0,1,0,0,0,0,0,0,0,1,0],[0,1,0,0,0,0,0,0,0,1,0],
			 [0,1,0,0,0,0,0,0,0,1,0],[0,1,0,0,0,0,0,0,0,1,0],[1,1,1,1,1,1,1,1,1,1,1]]

	page8 = [[1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]

	pages = [page1,page2,page3,page4,page5,page6,page7,page8]

	dx = sumAllElements(firstWindowX)
	dy = sumAllElements(firstWindowY)
	dz = sumAllElements(firstWindowZ)

	colorList = [ornamentalBrownColor,ornamentalRedColor,woodColor,glassColor]

	firstWindow = doorExtended(firstWindowX,firstWindowY,firstWindowZ,pages,colorList)(dx,dy,dz)

	firstWindow = S([1,2,3])([X/dx,Y/dy,Z/dz])(firstWindow)
	
	return firstWindow
	
def secondDoor(X,Y,Z) : 
	secondDoorX = [0.2,0.03,0.3,0.1,0.03]
	secondDoorY = [0.1,0.5,0.2,0.5,0.1,0.3,0.1,0.5,0.2,0.5,0.1]
	secondDoorZ = [0.1,0.3,0.4,0.05,0.4,0.05,0.4,0.05,0.4,0.05,0.4,0.4,0.1]

	page1 = [[1,0,1,1,2,2,2,1,1,0,1],[1,0,1,1,2,2,2,1,1,0,1],[1,0,1,1,2,4,2,1,1,0,1],
			 [1,0,1,1,2,3,2,1,1,0,1],[1,0,1,1,2,4,2,1,1,0,1],[1,0,1,1,2,3,2,1,1,0,1],
			 [1,0,1,1,2,4,2,1,1,0,1],[1,0,1,1,2,3,2,1,1,0,1],[1,0,1,1,2,4,2,1,1,0,1],
			 [1,0,1,1,2,3,2,1,1,0,1],[1,0,1,1,2,4,2,1,1,0,1],[1,0,1,1,2,2,2,1,1,0,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]

	page2 = [[1,0,1,1,2,2,2,1,1,0,1],[1,0,1,1,2,2,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],
			 [1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],
			 [1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],
			 [1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,0,2,1,1,0,1],[1,0,1,1,2,2,2,1,1,0,1],
			 [1,1,1,1,1,1,1,1,1,1,1]]

	page3 = [[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,1,1,0,0,0,0,0,1,1,1]]

	page4 = [[1,1,1,0,0,0,0,0,1,1,1],[1,4,1,0,0,0,0,0,1,4,1],[1,4,1,0,0,0,0,0,1,4,1],
			 [1,3,1,0,0,0,0,0,1,3,1],[1,4,1,0,0,0,0,0,1,4,1],[1,3,1,0,0,0,0,0,1,3,1],
			 [1,4,1,0,0,0,0,0,1,4,1],[1,3,1,0,0,0,0,0,1,3,1],[1,4,1,0,0,0,0,0,1,4,1],
			 [1,3,1,0,0,0,0,0,1,3,1],[1,4,1,0,0,0,0,0,1,4,1],[1,4,1,0,0,0,0,0,1,4,1],
			 [1,1,1,0,0,0,0,0,1,1,1]]

	page5 = [[1,1,1,0,0,0,0,0,1,1,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,1,0,1],
			 [1,1,1,0,0,0,0,0,1,1,1]]

	pages = [page1,page2,page3,page4,page5]

	dx = sumAllElements(secondDoorX)
	dy = sumAllElements(secondDoorY)
	dz = sumAllElements(secondDoorZ)

	colorList = [blackWoodColor,steelColor,darkSteelColor,glassColor]

	weld = COLOR(steelColor)(STRUCT([CUBOID([0.1,0.04,0.04]),T(1)(0.1),CUBOID([0.04,0.1,0.04])]))
	handle = COLOR(steelColor)(STRUCT([CYLINDER([0.04,2.2])(50),T([1,2,3])([-0.12,-0.12,0.3]),weld,T([3])([1.6]),weld]))

	secondDoor = doorExtended(secondDoorX,secondDoorY,secondDoorZ,pages,colorList)(dx,dy,dz)

	secondDoor = STRUCT([secondDoor,T([1,2,3])([0.35,1.05,0.4]),handle])

	secondDoor = S([1,2,3])([X/dx,Y/dy,Z/dz])(secondDoor)
	
	return secondDoor