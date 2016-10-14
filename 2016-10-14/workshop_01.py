from pyplasm import *
from numpy import *

def out():
	y = QUOTE([.1,-.3]*5)
	#ya = QUOTE([2.6])
	ya = QUOTE([.8,-.15]*5)
	a = PROD([y,ya])
	
	zb = QUOTE([-.8,.15]*5)
	z = QUOTE([1.7])
	b = PROD([z,zb])

	s = STRUCT([a,b])

	xc = QUOTE([.2])

	return PROD([xc,s])

def out2(xbeam,zbeam,xpillar,ypillar,dpdato,dbdato,beamPriority):
	
	dp = [ypillar]
	for val in dpdato:
		dp.append(-val+ypillar)
		dp.append(ypillar)

	db = []
	for val in dbdato:
		db.append(-val+zbeam)
		db.append(zbeam)

	dpn = []
	dbn = []

	dpsum = 0
	for val in dp:
    		dpsum += abs(val)
		dpn.append(-val)

	dbsum = 0
	for val in db:
    		dbsum += abs(val)
		dbn.append(-val)

	arrayA = []
	arrayB = []

	if beamPriority:
		arrayA = dbn
		arrayB.append(dpsum) 
	else:
		arrayA.append(dbsum)
		arrayB= dpn
		
	print(dbsum)
	print(dpsum)

	y = QUOTE(dp)
	#ya = QUOTE([dbsum])
	#ya = QUOTE(dbn)
	ya = QUOTE(arrayA)
	a = PROD([y,ya])
	
	zb = QUOTE(db)
	#z = QUOTE([dpsum])
	#z = QUOTE(dpn)
	z= QUOTE(arrayB)
	b = PROD([z,zb])

	#s = STRUCT([a,b])

	#xc = QUOTE([.2])

	xa = QUOTE([xpillar])

	xb = QUOTE([xbeam])

	#return PROD([xc,s])

	return STRUCT([T(1)(-xpillar/2),PROD([xa,a]),T(1)(-(xbeam-xpillar)/2),PROD([xb,b])])



dpdato = [(i+2)*2 for i in xrange(10)]
dbdato = [(i+2)*2 for i in xrange(10)]
xbeam = 5
zbeam = 2
xpillar = 1
ypillar = 1

VIEW(out2(xbeam,zbeam,xpillar,ypillar,dpdato,dbdato,TRUE))