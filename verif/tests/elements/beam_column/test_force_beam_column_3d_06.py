# -*- coding: utf-8 -*-
# home made test

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Ménsula horizontal sometida a carga de tracción en su extremo.

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

# Geometry
width= .05
depth= .1
nDivIJ= 5
nDivJK= 10
y0= 0
z0= 0
L= 1.5 # Bar length (m)
Iy= width*depth**3/12 # Cross section moment of inertia (m4)
Iz= depth*width**3/12 # Cross section moment of inertia (m4)
E= 210e9 # Young modulus of the steel.
nu= 0.3 # Poisson's ratio
G= E/(2*(1+nu)) # Shear modulus
J= .2e-1 # Cross section torsion constant (m4)

# Load
M= 1.5e3 # Load magnitude en N

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   
nodes= preprocessor.getNodeLoader
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(0,0.0,0.0)
nod= nodes.newNodeXYZ(L,0.0,0.0)


trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])

# Materials definition
fy= 275e6 # Yield stress of the steel.
acero= typical_materials.defSteel01(preprocessor, "acero",E,fy,0.001)

respT= typical_materials.defElasticMaterial(preprocessor, "respT",G*J) # Respuesta de la sección a torsión.
respVy= typical_materials.defElasticMaterial(preprocessor, "respVy",1e9) # Respuesta de la sección a cortante según y.
respVz= typical_materials.defElasticMaterial(preprocessor, "respVz",1e9) # Respuesta de la sección a cortante según z.
# Secciones
import os
pth= os.path.dirname(__file__)
#print "pth= ", pth
if(not pth):
  pth= "."
execfile(pth+"/../../aux/testQuadRegion.py")

materiales= preprocessor.getMaterialLoader
quadFibers= materiales.newMaterial("fiber_section_3d","quadFibers")
fiberSectionRepr= quadFibers.getFiberSectionRepr()
fiberSectionRepr.setGeomNamed("testQuadRegion")
quadFibers.setupFibers()
A= quadFibers.getFibers().getSumaAreas

agg= materiales.newMaterial("section_aggregator","agg")
agg.setSection("quadFibers")
agg.setAdditions(["T","Vy","Vz"],["respT","respVy","respVz"])
 # Respuestas a torsión y cortantes.



# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "agg"
elementos.numSections= 2 # Número de sections along the element.
elementos.defaultTag= 1
el= elementos.newElement("force_beam_column_3d",xc.ID([1,2]))



# Constraints
modelSpace.fixNode000_000(1)

# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([0,0,0,0,0,M]))
#We add the load case to domain.
casos.addToDomain("0")
# Procedimiento de solución
analisis= predefined_solutions.simple_static_modified_newton(prueba)
result= analisis.analyze(10)


nodes.calculateNodalReactions(True) 
nod2= nodes.getNode(2)
delta= nod2.getDisp[1]  # Node 2 displacement según z
theta= nod2.getDisp[5]  # Giro del nodo según y
nod1= nodes.getNode(1)
RM= nod1.getReaction[5] 

elementos= preprocessor.getElementLoader

elem1= elementos.getElement(1)
elem1.getResistingForce()
scc= elem1.getSections()[0]

V= scc.getStressResultantComponent("Vz")
M1= scc.getStressResultantComponent("My")

deltateor= (M*L**2/(2*E*Iy))
thetateor= (M*L/(E*Iy))
ratio1= (abs((delta-deltateor)/deltateor))
ratio2= (abs((M+RM)/M))
ratio3= (abs((M+M1)/M))
ratio4= (abs((theta-thetateor)/thetateor))

''' 
print "delta: ",delta
print "deltaTeor: ",deltateor
print "theta: ",theta
print "thetaTeor: ",thetateor
print "ratio1= ",ratio1
print "M= ",M
print "RM= ",RM
print "ratio2= ",ratio2
print "M1= ",M1
print "ratio3= ",ratio3
print "ratio4= ",ratio4
   '''
import os
from miscUtils import LogMessages as lmsg
fname= os.path.basename(__file__)
if (abs(ratio1)<0.02) & (abs(ratio2)<1e-10) & (abs(ratio3)<1e-10) & (abs(ratio4)<0.02):
  print "test ",fname,": ok."
else:
  lmsg.error(fname+' ERROR.')
