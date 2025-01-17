# -*- coding: utf-8 -*-
'''Home cooked test.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import math
import geom

points= [geom.Pos2d(0,0), geom.Pos2d(1,0), geom.Pos2d(1, 1), geom.Pos2d(0,1)]
    
plg= geom.Polygon2d(points)
sg= geom.Segment2d(geom.Pos2d(.5,.5), geom.Pos2d(1.5,0.5))
clippedSegment= plg.clip(sg)

p0= clippedSegment.getFromPoint()
p1= clippedSegment.getToPoint()
ratio= math.sqrt(p0.dist2(sg.getFromPoint()) + p1.dist2(geom.Pos2d(1.0,0.5)))

'''
print('polygon: ', plg)
print('original segment: ', sg, 'length: ', sg.getLength())
print('clipped segment: ', clippedSegment, 'length: ', clippedSegment.getLength())
print('ratio= ', ratio)
'''

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if (ratio<1e-12):
    print("test "+fname+": ok.")
else:
    print("test "+fname+": ERROR.")
