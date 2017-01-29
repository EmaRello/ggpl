# -*- coding: utf-8 -*-
from pyplasm import *
from math import *

def chair(dx,dy,dz):
    dx = float(dx)
    dy = float(dy)
    dz = float(dz)
    norm = 255.0
    
    mx = dx/20
    my = dy/20

    strutDepth = .04
    
    ch = MKPOL([[
                [0,my,0],[0,dy-my,0],
                [dx-mx,my,0],[dx-mx,dy-my,0],
                [dx-mx,my,dz/4],[dx-mx,dy-my,dz/4],
                [dx-mx,my,dz/2],[dx-mx,dy-my,dz/2],
                [0,my,dz/2],[0,dy-my,dz/2],
                [0,my,dz/6*5],[0,dy-my,dz/6*5],],
                
                [[1,11],[2,12],[3,7],[4,8],[5,6],[7,9],[8,10],[11,12]],1])
    
    ch = COLOR([32/norm,32/norm,32/norm])(STRUCT([T([1,2])([0,-strutDepth/2]),OFFSET([strutDepth,strutDepth,strutDepth])(ch)]))
    
    sittingDepth = .05
    sitting = COLOR([230/norm,131/norm,31/norm])(CUBOID([dx-strutDepth,dy,sittingDepth]))
    ch = STRUCT([ch,T([1,3])([strutDepth,dz/2+strutDepth]),sitting])
    
    backDepth = .05
    back = COLOR([230/norm,131/norm,31/norm])(CUBOID([backDepth,dy,dz/3]))
    ch = STRUCT([ch,T([1,3])([strutDepth,dz-dz/3]),back])
    
    ch =  STRUCT([T([1,2])([-dx/2,-dy/2]),ch])
    return ch
