# -*- coding: utf-8 -*-
''' Test from Ansys manual
 Reference:  Strength of Material, Part I, Elementary Theory and Problems, pg. 26, problem 10.'''

from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import math
import geom
import xc
from model import predefined_spaces
from actions.basic_loads import nodal_loads
from materials import typical_materials

NumDiv= 100
E= 30e6 # Young modulus (psi)
lng= 10 # Cable length in inches
sigmaPret= 1500 # Prestressing force (pounds)
area= 2.0
fPret= sigmaPret*area # Prestressing force (pounds)
F= 100/NumDiv # Carga vertical

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)

# Model definition


    
# Define materials
cable= typical_materials.defCableMaterial(preprocessor, "cable",E,sigmaPret,0.0)
    
''' We define nodes at the points where loads will be applied.
    We will not compute stresses so we can use an arbitrary
    cross section of unit area.'''
    
# Seed element definition
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= cable.name
seedElemHandler.dimElem= 3 # Dimension of element space
truss= seedElemHandler.newElement("CorotTruss",xc.ID([0,0]))
truss.sectionArea= area
# seed element definition ends

points= preprocessor.getMultiBlockTopology.getPoints
pt= points.newPoint(1,geom.Pos3d(0.0,0.0,0.0))
pt= points.newPoint(2,geom.Pos3d(lng,0.0,0.0))
lines= preprocessor.getMultiBlockTopology.getLines
l= lines.newLine(1,2)
l.nDiv= NumDiv

l.genMesh(xc.meshDir.I)
    
# Constraints
constraints= preprocessor.getBoundaryCondHandler
predefined_spaces.ConstraintsForLineExtremeNodes(l,modelSpace.fixNode000_000)
predefined_spaces.ConstraintsForLineInteriorNodes(l,modelSpace.fixNodeFFF_000)


# Load case definition.
lPattern= '0'
lp0= modelSpace.newLoadPattern(name= lPattern)
modelSpace.setCurrentLoadPattern(lPattern)
nodal_loads.load_on_nodes_in_line(l,lp0,xc.Vector([0,-F,0,0,0,0]))
modelSpace.addLoadCaseToDomain(lPattern)


Nstep= 10  #  apply load in 10 steps
DInc= 1./Nstep 	#  first load increment


solu= feProblem.getSoluProc
solCtrl= solu.getSoluControl
solModels= solCtrl.getModelWrapperContainer
sm= solModels.newModelWrapper("sm")
numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("simple")
cHandler= sm.newConstraintHandler("plain_handler")
solutionStrategies= solCtrl.getSolutionStrategyContainer
solutionStrategy= solutionStrategies.newSolutionStrategy("solutionStrategy","sm")
solAlgo= solutionStrategy.newSolutionAlgorithm("newton_raphson_soln_algo")
ctest= solutionStrategy.newConvergenceTest("norm_unbalance_conv_test")
ctest.tol= 1e-6
ctest.maxNumIter= 100
integ= solutionStrategy.newIntegrator("load_control_integrator",xc.Vector([]))
integ.dLambda1= DInc
soe= solutionStrategy.newSystemOfEqn("band_gen_lin_soe")
solver= soe.newSolver("band_gen_lin_lapack_solver")
analysis= solu.newAnalysis("static_analysis","solutionStrategy","")
result= analysis.analyze(Nstep)

index= int(NumDiv/2)+1
midNode= l.getNodeI(index)

nodes.calculateNodalReactions(True,1e-7)
R1X= l.lastNode.getReaction[0]
R1Y= l.lastNode.getReaction[1] 
R2X= l.firstNode.getReaction[0]
R2Y= l.firstNode.getReaction[1] 
deltaX= midNode.getDisp[0]
deltaY= midNode.getDisp[1]  

alpha= -math.atan2(deltaY,lng/2)
Ftot= (NumDiv-1)*F
ratio1= (abs(R1X+R2X)/fPret)
ratio2= (abs(R1Y-Ftot/2.0)/(Ftot/2))
ratio3= (abs(R2Y-Ftot/2.0)/(Ftot/2))
    
''' 
print("F= ",(F))
print("alpha= ",rad2deg((alpha)))
print("R1X= ",R1X)
print("R1Y= ",R1Y)
print("R2X= ",R2X)
print("R2Y= ",R2Y)
print("deltaX= ",deltaX)
print("deltaY= ",deltaY)
print("ratio1= ",(ratio1))
print("ratio2= ",(ratio2))
print("ratio3= ",(ratio3))
'''
    
import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-11) & (abs(ratio2)<1e-11) & (abs(ratio3)<1e-11) :
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')

