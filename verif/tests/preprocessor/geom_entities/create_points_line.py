# -*- coding: utf-8 -*-
from __future__ import print_function

import geom
import xc
import math
import os

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# feProblem.setVerbosityLevel(0)
NumDiv= 4
CooMax= NumDiv
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor

points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPoint(geom.Pos3d(0.0,0.0,0.0))
pt2= points.newPoint(geom.Pos3d(CooMax,CooMax,CooMax))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt1.tag,pt2.tag)
l1.nDiv= NumDiv
points.defaultTag= 100 # The following point will have tag= 100
l1.divide()

cumple= True
pos= points.get(101).getPos 
cumple= (abs(pos.x-1.0)<1e-5) & (cumple) 
cumple= (abs(pos.y-1.0)<1e-5) & (cumple) 
cumple= (abs(pos.z-1.0)<1e-5) & (cumple) 
pos= points.get(102).getPos 
cumple= (abs(pos.x-2.0)<1e-5) & (cumple) 
cumple= (abs(pos.y-2.0)<1e-5) & (cumple) 
cumple= (abs(pos.z-2.0)<1e-5) & (cumple) 
pos= points.get(103).getPos 
cumple= (abs(pos.x-3.0)<1e-5) & (cumple) 
cumple= (abs(pos.y-3.0)<1e-5) & (cumple) 
cumple= (abs(pos.z-3.0)<1e-5) & (cumple) 
pos= points.get(104).getPos 
cumple= (abs(pos.x-4.0)<1e-5) & (cumple) 
cumple= (abs(pos.y-4.0)<1e-5) & (cumple) 
cumple= (abs(pos.z-4.0)<1e-5) & (cumple) 


import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if cumple:
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
