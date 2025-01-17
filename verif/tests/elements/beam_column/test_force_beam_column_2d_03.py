# -*- coding: utf-8 -*-
''' Home made test. Horizontal cantilever under tension load at its end.'''

from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

# Geometry
width= .05
depth= .1
A= width*depth
E= 210e9
I= width*depth**3/12
nu= 0.3
G= E/(2*(1+nu))
L= 1.5 # Bar length (m)

# Load
M= 1.5e3 # Load magnitude en N m

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor   
nodes= preprocessor.getNodeHandler
# Problem type
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
n1= nodes.newNodeXY(0,0.0)
n2= nodes.newNodeXY(L,0.0)


# Geometric transformations
lin= modelSpace.newLinearCrdTransf("lin")

# Materials definition
section= typical_materials.defElasticShearSection2d(preprocessor, "section",A,E,G,I,1.0)

# Elements definition
elements= preprocessor.getElementHandler
elements.defaultTransformation= lin.name # Coordinate transformation for the new elements
elements.defaultMaterial= section.name
beam2d= elements.newElement("ForceBeamColumn2d",xc.ID([n1.tag,n2.tag]))

# Constraints
constraints= preprocessor.getBoundaryCondHandler
modelSpace.fixNode000(n1.tag)

# Load definition.
lp0= modelSpace.newLoadPattern(name= '0')
lp0.newNodalLoad(n2.tag,xc.Vector([0,0,M]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)
# Solution procedure
analysis= predefined_solutions.plain_static_modified_newton(feProblem)
result= analysis.analyze(10)


nodes.calculateNodalReactions(True,1e-7) 
delta= n2.getDisp[1]  # z displacement of node 2
theta= n2.getDisp[2]  # z rotation of the node
RM= n1.getReaction[2] 

elements= preprocessor.getElementHandler

beam2d.getResistingForce()
scc= beam2d.getSections()[0]

V= scc.getStressResultantComponent("Vy")
M1= scc.getStressResultantComponent("Mz")

deltateor= (M*L**2/(2*E*I))
thetateor= (M*L/(E*I))
ratio1= (abs((delta-deltateor)/deltateor))
ratio2= (abs((M+RM)/M))
ratio3= (abs((M-M1)/M))
ratio4= (abs((theta-thetateor)/thetateor))

''' 
print("delta: ",delta)
print("deltaTeor: ",deltateor)
print("theta: ",theta)
print("thetaTeor: ",thetateor)
print("ratio1= ",ratio1)
print("M= ",M)
print("RM= ",RM)
print("ratio2= ",ratio2)
print("M1= ",M1)
print("ratio3= ",ratio3)
print("ratio4= ",ratio4)
   '''
import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if (abs(ratio1)<0.005) & (abs(ratio2)<1e-10) & (abs(ratio3)<1e-10) & (abs(ratio4)<0.02):
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
  
