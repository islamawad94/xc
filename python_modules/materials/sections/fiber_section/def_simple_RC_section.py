# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2015, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es" "ana.Ortega@ciccp.es"

import sys
import math
import uuid
import geom
import xc
from materials.sections import section_properties
from materials.sections import stress_calc as sc
from misc_utils import log_messages as lmsg
import matplotlib.pyplot as plt

# Classes defining reinforcement.

class ShearReinforcement(object):
    ''' Definition of the variables that make up a family of shear 
    reinforcing bars.

    :ivar familyName: name identifying the family of shear reinforcing bars.
    :ivar nShReinfBranches:  number of effective branches. 
    :ivar areaShReinfBranch: area of the shear reinforcing bar [in the unit of 
                             area of the model]. 
    :ivar shReinfSpacing: longitudinal distance between transverse 
                          reinforcements [in the unit of length of the model] 
    :ivar angAlphaShReinf: angle between the shear reinforcing bars and the 
                           axis of the member expressed in radians.
    :ivar angThetaConcrStruts: angle between the concrete's compression struts 
                             and the axis of the member expressed in radians.
    '''
    def __init__(self,familyName= None,nShReinfBranches= 0.0,areaShReinfBranch= 0.0,shReinfSpacing= 0.2,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0):
        '''
        :param familyName: name identifying the family of shear reinforcing bars.
        :param nShReinfBranches:  number of effective branches. 
        :param areaShReinfBranch: area of the shear reinforcing bar [in 
                                  the unit of area of the model]. 
        :param shReinfSpacing: longitudinal distance between transverse 
                               reinforcements [in the unit of length 
                               of the model] 
        :param angAlphaShReinf: angle between the shear reinforcing bars 
                                and the axis of the member expressed in
                                radians.
        :param angThetaConcrStruts: angle between the concrete's compression 
                                    struts and the axis of the member
                                    expressed in radians.
        '''
 
        # If no name provided, generate it.
        if(not familyName):
            familyName= str(uuid.uuid1())
        self.familyName= familyName # name identifying the family of shear reinforcing bars
        self.nShReinfBranches= nShReinfBranches # Number of effective branches
        self.areaShReinfBranch= areaShReinfBranch # Area of the shear reinforcing bar
        self.shReinfSpacing= shReinfSpacing # longitudinal distance between transverse reinforcements
        self.angAlphaShReinf= angAlphaShReinf # angle between the shear reinforcing bars and the axis of the member.
        self.angThetaConcrStruts= angThetaConcrStruts # angle between the concrete's compression struts and the axis of the member
        
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= (self.familyName == other.familyName)
            if(retval):
                retval= (self.nShReinfBranches == other.nShReinfBranches)
            if(retval):
                retval= (self.areaShReinfBranch == other.areaShReinfBranch)
            if(retval):
                retval= (self.shReinfSpacing == other.shReinfSpacing)
            if(retval):
                retval= (self.angAlphaShReinf == other.angAlphaShReinf)
            if(retval):
                retval= (self.angThetaConcrStruts == other.angThetaConcrStruts)
        else:
            retval= True
        return retval
    
    def getAs(self):
        '''returns the area per unit length of the family of shear 
           reinforcements.
        '''
        return self.nShReinfBranches*self.areaShReinfBranch/self.shReinfSpacing

    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        steelArea= self.getAs()
        if(steelArea>0.0):
            os.write(indentation+'family name: '+str(self.familyName)+'\n')
            os.write(indentation+'number of effective branches: '+str(self.nShReinfBranches)+'\n')
            os.write(indentation+'area of the shear reinforcing bar: '+str(self.areaShReinfBranch)+'\n')
            os.write(indentation+'longitudinal distance between transverse reinforcements: '+str(self.shReinfSpacing)+'\n')
            os.write(indentation+'angle between the shear reinforcing bars and the axis of the member: '+str(math.degrees(self.angAlphaShReinf))+'\n')
            os.write(indentation+'angle between the concrete\'s compression struts and the axis of the member: '+str(math.degrees(self.angThetaConcrStruts))+'\n')
        else:
            os.write(indentation+'family name: -\n')

class ReinfRow(object):
    ''' Definition of the variables that make up a family (row) of main 
    (longitudinal) reinforcing bars.

    :ivar rebarsDiam: diameter of the bars (if omitted, the diameter is calculated from the rebar area) 
    :ivar areaRebar: cross-sectional area of the bar (if omitted, the area is calculated from the rebar diameter)
    :ivar rebarsSpacing: spacing between bars (not considered if nRebars is defined)
    :ivar nRebars: number of rebars to be placed in the row (>1)
    :ivar width: width of the cross-section (defautls to 1m)
    :ivar cover: concrete cover.
    '''
    def __init__(self, rebarsDiam=None, areaRebar= None, rebarsSpacing= None, nRebars= None, width= 1.0, nominalCover= 0.03, nominalLatCover= 0.03):
        ''' Constructor.

        :param rebarsDiam: diameter of the bars (if omitted, the diameter is calculated from the rebar area) 
        :param areaRebar: cross-sectional area of the bar (if omitted, the area is calculated from the rebar diameter)
        :param rebarsSpacing: spacing between bars (not considered if nRebars is defined)
        :param nRebars: number of rebars to be placed in the row (>1)
        :param width: width of the cross-section (defautls to 1 m)
        :param nominalCover: nominal cover (defaults to 0.03m)
        :param nominalLatCover: nominal lateral cover (only considered if nRebars is defined, defaults to 0.03)
        '''
        if rebarsDiam:
            self.rebarsDiam= rebarsDiam
        elif areaRebar:
            self.areaRebar= areaRebar
            self.rebarsDiam=2*math.sqrt(areaRebar/math.pi)
        else:
            lmsg.warning('You must define either the diameter or the area of rebars')
        if areaRebar:
            self.areaRebar= areaRebar
        elif rebarsDiam:
            self.areaRebar=math.pi*rebarsDiam**2/4.
        else:
            lmsg.warning('You must define either the diameter or the area of rebars')
        self.width= width
        if nRebars:
            self.nRebars= nRebars
            # if width==1.0:
            #     lmsg.warning('Spacing is calculated using a section width = 1 m')
            self.rebarsSpacing= (width-2*nominalLatCover-self.rebarsDiam)/(nRebars-1)
        elif rebarsSpacing:
            self.rebarsSpacing= rebarsSpacing
            nRebarsTeor= width/rebarsSpacing
            self.nRebars= int(math.floor(nRebarsTeor))
        else:
            lmsg.warning('You must define either the number of rebars or the rebar spacing')
        self.cover= nominalCover+self.rebarsDiam/2.0
        self.centerRebars(width)
        
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= (self.rebarsDiam == other.rebarsDiam)
            if(retval):
                retval= (self.areaRebar == other.areaRebar)
            if(retval):
                retval= (self.rebarsSpacing == other.rebarsSpacing)
            if(retval):
                retval= (self.nRebars == other.nRebars)
            if(retval):
                retval= (self.width == other.width)
            if(retval):
                retval= (self.cover == other.cover)
        else:
            retval= True
        return retval
    
    def getAs(self):
        ''' Returns the total cross-sectional area of reinforcing steel 
           in the family.
        '''
        return self.nRebars*self.areaRebar

    def getI(self):
        ''' Return the moment of inertia around the axis containing the bar
            centers.'''
        return self.nRebars*math.pi*(self.rebarsDiam/2.0)**4/4.0
      
    def centerRebars(self,width):
        '''center the row of rebars in the width of the section'''
        self.coverLat= (width-(self.nRebars-1)*self.rebarsSpacing)/2.0

    def defStraightLayer(self, reinforcement, layerCode, diagramName, p1, p2):
        '''Definition of a straight reinforcement layer in the XC section 
           geometry object between the 2d positions p1 and p2.

        :param reinforcement: XC section geometry reinforcement.
        :param layerCode: identifier for the layer.
        :param diagramName: name of the strain-stress diagram of the steel.
        :param p1: first point of the layer.
        :param p2: last point of the layer.
        '''
        if(self.nRebars>0):
            self.reinfLayer= reinforcement.newStraightReinfLayer(diagramName)
            self.reinfLayer.code= layerCode
            self.reinfLayer.numReinfBars= self.nRebars
            self.reinfLayer.barDiameter= self.rebarsDiam
            self.reinfLayer.barArea= self.areaRebar
            self.reinfLayer.p1= p1
            self.reinfLayer.p2= p2
            return self.reinfLayer
        
    def defCircularLayer(self,reinforcement, code, diagramName, extRad, initAngle= 0.0, finalAngle= 2*math.pi):
        '''Definition of a circular reinforcement layer in the XC section 
           geometry object between the angle arguments.

        :param reinforcement: XC section geometry reinforcement.
        :param code: identifier for the layer.
        :param diagramName: name of the strain-stress diagram of the steel.
        :param extRad: concrete external radius. 
        :param initAngle: initial angle.
        :param finalAngle: final angle.
        '''
        if(self.nRebars>0):
            self.reinfLayer= reinforcement.newCircReinfLayer(diagramName)
            self.reinfLayer.code= code
            self.reinfLayer.numReinfBars= self.nRebars
            self.reinfLayer.barDiameter= self.rebarsDiam
            self.reinfLayer.barArea= self.areaRebar
            self.reinfLayer.initAngle= initAngle
            self.reinfLayer.finalAngle= finalAngle
            self.reinfLayer.radius= extRad-self.cover
            return self.reinfLayer
        
    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        os.write(indentation+'bar diameter: '+str(self.rebarsDiam*1e3)+' mm\n')
        os.write(indentation+'bar area: '+str(self.areaRebar*1e4)+' cm2\n')
        os.write(indentation+'spacing: '+str(self.rebarsSpacing*1e3)+' mm\n')
        os.write(indentation+'number of bars: '+str(self.nRebars)+'\n')
        os.write(indentation+'width: '+str(self.width*1e3)+' mm\n')
        os.write(indentation+'cover: '+str(self.cover*1e3)+' mm\n')

def RebarRow2ReinfRow(rebarRow, width= 1.0, nominalLatCover= 0.03):
    ''' Returns a RebarRow object from a ReinfRow object
        as defined in the rebar_family module.

    :param rebarRow: RebarRow object.
    :param width: width of the cross-section (defautls to 1 m)
    :param nominalLatCover: nominal lateral cover (only considered if nRebars is defined, defaults to 0.03)
    '''
    return RebarRow(rebarsDiam= rebarRow.diam,rebarsSpacing= rebarRows.spacing,width= widht, nominalCover= rebarRow.cover, nominalLatCover= nominalLatCover)

class LongReinfLayers(object):
    ''' Layers of longitudinal reinforcement.'''
    def __init__(self, lst= None):
        ''' Constructor.'''
        if(lst):
            self.rebarRows= lst  # list of ReinfRow data
        else:
            self.rebarRows= list()
        self.reinfLayers= list()  # list of StraightReinfLayer created.
                    
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= (len(self.rebarRows) == len(other.rebarRows))
            if(retval):
                for rowA, rowB in zip(self.rebarRows, other.rebarRows):
                    retval= (rowA==rowB)
                    if(not retval):
                        break
        else:
            retval= True
        return retval
    
    def __getitem__(self, index):
        '''Return the i-th reinforcement row.'''
        return self.rebarRows[index]

    def __len__(self):
        '''Return the number of reinforcement rows.'''
        return len(self.rebarRows)

    def append(self, rebarRow):
        ''' Append a reinforcement row to the list.'''
        self.rebarRows.append(rebarRow)
        
    def getAsRows(self):
        '''Returns a list with the cross-sectional area of the rebars in 
           each row.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.getAs())
        return retval
       
    def getAs(self):
        '''returns the cross-sectional area of the rebars.'''
        return sum(self.getAsRows())

    def getMinCover(self):
        '''Return the minimum value of the cover.'''
        retval= 1e6
        if(len(self.rebarRows)>0):
            retval= self.rebarRows[0].cover
            for rbRow in self.rebarRows[1:]:
                retval= min(retval,rbRow.cover)
        return retval
        
    def getRowsCGcover(self):
        '''returns the distance from the center of gravity of the rebars
        to the face of the section 
        '''
        retval=0
        if(len(self.rebarRows)>0):
            for rbRow in self.rebarRows:
                retval+= rbRow.getAs()*rbRow.cover
            retval/= self.getAs()
        return retval

    def getSpacings(self):
        '''returns a list with the distance between bars for each row of bars.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.rebarsSpacing)
        return retval
    
    def getDiameters(self):
        '''returns a list with the bar diameter for each row of bars in local 
        positive face.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.rebarsDiam)
        return retval
    
    def getNBar(self):
        '''returns a list with the number of bars for each row.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.nRebars)
        return retval

    def getCover(self):
        '''returns a list with the cover of bars for each row of bars.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.cover)
        return retval
    
    def getLatCover(self):
        '''returns a list with the lateral cover of bars for each row of bars.'''
        retval=[]
        for rbRow in self.rebarRows:
            retval.append(rbRow.coverLat)
        return retval

    def centerRebars(self, b):
        '''centers in the width of the section the rebars.''' 
        for rbRow in self.rebarRows:
            rbRow.centerRebars(b)
            
    def defStraightLayers(self, reinforcement, layerCode, diagramName, pointPairs):
        '''
        Definition of the reinforcement layers

        :param reinforcement: XC section reinforcement.
        :param layerCode: identifier for the layer.
        :param diagramName: name of the strain-stress diagram of the steel.
        :param pointPairs: end points for each row.
        '''
        for rbRow, pts in zip(self.rebarRows, pointPairs):
            p1= pts[0]; p2= pts[1]
            self.reinfLayers.append(rbRow.defStraightLayer(reinforcement,layerCode,diagramName,p1,p2))
            
    def defCircularLayers(self, reinforcement, code, diagramName, extRad, anglePairs= None):
        '''
        Definition of the reinforcement layers

        :param reinforcement: XC section reinforcement.
        :param code: identifier for the layer.
        :param diagramName: name of the strain-stress diagram of the steel.
        :param points: end points for each row.
        '''
        if(len(self.rebarRows)>0):
            if(not anglePairs):
                for rbRow in self.rebarRows:
                    layer= rbRow.defCircularLayer(reinforcement,code,diagramName,extRad)
                    self.reinfLayers.append(layer)
            else:
                for rbRow, angles in zip(self.rebarRows, anglePairs):
                    initAngle= anglePairs[0]; finalAngle= anglePairs[1]
                    layer= rbRow.defCircularLayer(reinforcement,code,diagramName, extRad, initAngle, finalAngle)
                    self.reinfLayers.append(layer)
        else:
            lmsg.warning('No longitudinal reinforcement.')
            
    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        os.write(indentation+'rebar rows: \n')
        for rrow in self.rebarRows:
            rrow.report(os, indentation+'  ')

def rebLayer_mm(fi,s,c):
    '''Defines a layer of main reinforcement bars, given the spacement.

    :param fi: bar diameter [mm]
    :param s: spacing [mm]
    :param c: cover [mm] (nominal cover)
    '''
    return ReinfRow(rebarsDiam=fi*1e-3,areaRebar= math.pi*(fi*1e-3)**2/4.0,rebarsSpacing=s*1e-3,width=1.0,nominalCover=c*1e-3)

def rebLayerByNumFi_mm(n,fi,c,latC,L):
    '''Defines a layer of  main reinforcement bars with a fixed number of rebars. Spacing is calculated
    so that the rebars (and two lateral covers) are inserted in the length L passed as parameter.

    :param n: number of rebars
    :param fi: bar diameter [mm]
    :param c: nominal cover [mm]
    :param latC: nominal lateral cover [mm]
    :param L: length where the n rebars and two lateral covers are inserted [mm]
    '''
    rl=ReinfRow(rebarsDiam=fi*1e-3,areaRebar= math.pi*(fi*1e-3)**2/4.0,nRebars=n,width=L*1e-3,nominalCover=c*1e-3,nominalLatCover=latC*1e-3)
    return rl

# Reinforced concrete.

class RCFiberSectionParameters(object):
    '''
    Parameters needed to create a reinforced concrete fiber section.

    :ivar concrType:       type of concrete (e.g. EHE_materials.HA25)     
    :ivar concrDiagName:   name identifying the characteristic stress-strain 
                           diagram of the concrete material
    :ivar reinfSteelType:  type of reinforcement steel
    :ivar reinfDiagName:   name identifying the characteristic stress-strain 
                           diagram of the reinforcing steel material
    :ivar nDivIJ:          number of cells in IJ (width or radial) direction
    :ivar nDivJK:          number of cells in JK (height or tangential)
                           direction
    '''
    def __init__(self, concrType=None, reinfSteelType=None, nDivIJ= 10, nDivJK= 10):
        self.concrType= concrType
        self.concrDiagName= None
        self.reinfSteelType= reinfSteelType
        self.reinfDiagName= None # Name of the uniaxial material
        self.nDivIJ= nDivIJ
        self.nDivJK= nDivJK
        
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= (self.concrType == other.concrType)
            if(retval):
                retval= (self.concrDiagName == other.concrDiagName)
            if(retval):
                retval= (self.reinfSteelType == other.reinfSteelType)
            if(retval):
                retval= (self.reinfDiagName == other.reinfDiagName)
            if(retval):
                retval= (self.nDivIJ == other.nDivIJ)
            if(retval):
                retval= (self.nDivJK == other.nDivJK)
        else:
            retval= True
        return retval

    def nDivCirc(self):
        '''Alias for nDivIJ when defining circular sections.'''
        return self.nDivIJ
    
    def nDivRad(self):
        '''Alias for nDivJK when defining circular sections.'''
        return self.nDivJK

    def getConcreteDiagram(self,preprocessor):
        ''' Return the concrete strain-stress diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''

        return preprocessor.getMaterialHandler.getMaterial(self.concrDiagName)
      
    def getSteelDiagram(self,preprocessor):
        ''' Return the steel strain-stress diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return preprocessor.getMaterialHandler.getMaterial(self.reinfDiagName)
      
    def getSteelEquivalenceCoefficient(self,preprocessor):
        ''' Return the equivalence coefficiente for the steel (Es/Ec).

        :param preprocessor: preprocessor of the finite element problem.
        '''
        tangHorm= self.getConcreteDiagram(preprocessor).getTangent()
        tangSteel= self.getSteelDiagram(preprocessor).getTangent()
        return tangSteel/tangHorm

    def defDiagrams(self,preprocessor,matDiagType):
        '''Stress-strain diagrams definition.

        :param preprocessor: preprocessor of the finite element problem.
        :param matDiagType: type of stress-strain diagram 
                    ("k" for characteristic diagram, "d" for design diagram)
        '''
        self.diagType= matDiagType
        if(self.diagType=="d"):
            if(self.concrType.matTagD<0):
                unusedConcreteMatTag= self.concrType.defDiagD(preprocessor)
            if(self.reinfSteelType.matTagD<0):
                unusedReinfSteelMaterialTag= self.reinfSteelType.defDiagD(preprocessor)
            self.concrDiagName= self.concrType.nmbDiagD
            self.reinfDiagName= self.reinfSteelType.nmbDiagD
        elif(self.diagType=="k"):
            if(self.concrType.matTagK<0):
                unusedConcreteMatTag= self.concrType.defDiagK(preprocessor)
            if(self.reinfSteelType.matTagK<0):
                unusedReinfSteelMaterialTag= self.reinfSteelType.defDiagK(preprocessor)
            self.concrDiagName= self.concrType.nmbDiagK
            self.reinfDiagName= self.reinfSteelType.nmbDiagK
            
    def defInteractionDiagramParameters(self, preprocessor):
        ''' Defines the parameters for interaction diagrams.

         :param preprocessor: preprocessor of the finite element problem.
        '''
        self.idParams= xc.InteractionDiagramParameters()
        if(self.diagType=="d"):
            self.idParams.concreteTag= self.concrType.matTagD
            self.idParams.reinforcementTag= self.reinfSteelType.matTagD
        elif(self.diagType=="k"):
            self.idParams.concreteTag= self.concrType.matTagK
            self.idParams.reinforcementTag= self.reinfSteelType.matTagK
        return self.idParams
    
    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        os.write(indentation+'concrete type: '+str(self.concrType.materialName)+'\n')
        os.write(indentation+'concrete stress-strain diagram: '+str(self.concrDiagName)+'\n')
        os.write(indentation+'steel type: '+str(self.reinfSteelType.materialName)+'\n')
        os.write(indentation+'steel stress-strain diagram: '+str(self.reinfDiagName)+'\n')
        os.write(indentation+'number of IJ divisions nDivIJ= '+str(self.nDivIJ)+'\n')
        os.write(indentation+'number of JK divisions nDivJK= '+str(self.nDivJK)+'\n')
        

class RCSectionBase(object):
    '''
    Base class for reinforced concrete sections.

    :ivar sectionDescr: section description.
    :ivar fiberSectionParameters: Parameters needed to create a reinforced 
                                  concrete fiber section.
    :ivar fiberSectionRepr: fiber model of the section.
    '''
    def __init__(self, sectionDescr= None, concrType=None,reinfSteelType=None, nDivIJ= 10, nDivJK= 10):
        ''' Constructor.

        :param sectionDescr: section description.
        :param concrType: type of concrete (e.g. EHE_materials.HA25).     
        :param reinfSteelType: type of reinforcement steel.
        :param nDivIJ: number of cells in IJ (width or radial) direction.
        :param nDivJK: number of cells in JK (height or tangential) direction.
        '''
        self.sectionDescr= 'Text describing the role/position of the section in the structure.'
        if(sectionDescr):
            self.sectionDescr= sectionDescr
        self.fiberSectionParameters= RCFiberSectionParameters(concrType= concrType, reinfSteelType= reinfSteelType, nDivIJ= nDivIJ, nDivJK= nDivJK)
        self.fiberSectionRepr= None
        
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= (self.sectionDescr == other.sectionDescr)
            if(retval):
                retval= (self.fiberSectionParameters == other.fiberSectionParameters)
            if(retval):
                retval= (self.fiberSectionRepr == other.fiberSectionRepr)
        else:
            retval= True
        return retval
    
    def getCopy(self):
        ''' Returns a copy of the object.'''
        retval= RCSectionBase(sectionDescr= self.sectionDescr, concrType= self.getConcreteType(), reinfSteelType= self.getReinfSteelType(), nDivIJ= self.getNDivIJ(), nDivJK= self.getNDivJK())
        return retval

    def gmSectionName(self):
        ''' returns the name of the geometric section'''
        return "geom"+self.name

    def getConcreteType(self):
        ''' returns the concrete type of this sections.'''
        return self.fiberSectionParameters.concrType
    
    def getReinfSteelType(self):
        ''' returns the type of the reinforcing steel in this sections.'''
        return self.fiberSectionParameters.reinfSteelType

    def getNDivIJ(self):
        ''' Return the number of cells in IJ (width or radial) direction.'''
        return self.fiberSectionParameters.nDivIJ

    def getNDivJK(self):
        ''' Return the number of cells in JK (height or tangential) direction.'''
        return self.fiberSectionParameters.nDivJK
    
    def getConcreteDiagram(self,preprocessor):
        ''' Return the concrete stress-strain diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return self.fiberSectionParameters.getConcreteDiagram(preprocessor)
      
    def getSteelDiagram(self,preprocessor):
        ''' Return the reinforcing steel stress-strain diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return self.fiberSectionParameters.getSteelDiagram(preprocessor)
      
    def getSteelEquivalenceCoefficient(self,preprocessor):
        ''' Return the steel equivalence coefficient: Es/Ec.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return self.fiberSectionParameters.getSteelEquivalenceCoefficien(preprocessor)

    def defDiagrams(self,preprocessor,matDiagType):
        '''Stress-strain diagrams definition.

        :param preprocessor: preprocessor of the finite element problem.
        :param matDiagType: type of stress-strain diagram 
                    ("k" for characteristic diagram, "d" for design diagram)
        '''
        return self.fiberSectionParameters.defDiagrams(preprocessor, matDiagType)

    def defShearResponse2d(self, preprocessor):
        ''' Define the shear response of the 2D section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        self.respVy= self.getRespVy(preprocessor)
        
    def defShearResponse(self, preprocessor):
        ''' Define the shear/torsional response of the section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        self.respT= self.getRespT(preprocessor) # Torsional response of the section.
        self.respVy= self.getRespVy(preprocessor)
        self.respVz= self.getRespVz(preprocessor)

    def defFiberSection2d(self,preprocessor):
        '''Define 2D fiber section from geometry data.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        self.fs= preprocessor.getMaterialHandler.newMaterial("fiberSectionShear2d", self.name)
        self.fiberSectionRepr= self.fs.getFiberSectionRepr()
        self.fiberSectionRepr.setGeomNamed(self.gmSectionName())
        self.fs.setupFibers()
        self.fs.setRespVyByName(self.respVyName())
        self.fs.setProp('sectionData',self)
        
    def defRCSection2d(self, preprocessor, matDiagType):
        ''' Definition of a 2D reinforced concrete section.

        :param preprocessor: preprocessor of the finite element problem.
        :param matDiagType: type of stress-strain diagram 
                    ("k" for characteristic diagram, "d" for design diagram)
         '''
        self.defShearResponse2d(preprocessor)
        self.defSectionGeometry(preprocessor,matDiagType)
        self.defFiberSection2d(preprocessor)
        
    def defFiberSection(self,preprocessor):
        '''Define fiber section from geometry data.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        self.fs= preprocessor.getMaterialHandler.newMaterial("fiberSectionShear3d",self.name)
        self.fiberSectionRepr= self.fs.getFiberSectionRepr()
        self.fiberSectionRepr.setGeomNamed(self.gmSectionName())
        self.fs.setupFibers()
        self.fs.setRespVyByName(self.respVyName())
        self.fs.setRespVzByName(self.respVzName())
        self.fs.setRespTByName(self.respTName())
        self.fs.setProp('sectionData',self)
        
    def defRCSection(self, preprocessor,matDiagType):
        ''' Definition of an XC reinforced concrete section.

        :param preprocessor: preprocessor of the finite element problem.
        :param matDiagType: type of stress-strain diagram 
                    ("k" for characteristic diagram, "d" for design diagram)
         '''
        self.defShearResponse(preprocessor)
        self.defSectionGeometry(preprocessor,matDiagType)
        self.defFiberSection(preprocessor)

    def isCircular(self):
        ''' Return true if it's a circular section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return False
        
    def defInteractionDiagramParameters(self, preprocessor):
        ''' parameters for interaction diagrams.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return self.fiberSectionParameters.defInteractionDiagramParameters(preprocessor)

    def defInteractionDiagram(self,preprocessor):
        '''Defines 3D interaction diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        if(not self.fiberSectionRepr):
            lmsg.error("defInteractionDiagram: fiber section representation for section: "+ self.name + ";  not defined yet; use defRCSection method.\n")
        self.defInteractionDiagramParameters(preprocessor)
        return preprocessor.getMaterialHandler.calcInteractionDiagram(self.name,self.fiberSectionParameters.idParams)

    def defInteractionDiagramNMy(self,preprocessor):
        '''Defines N-My interaction diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        if(not self.fiberSectionRepr):
            lmsg.error("defInteractionDiagramNMy: fiber section representation for section: "+ self.name + ";  not defined yet; use defRCSection method.\n")
        self.defInteractionDiagramParameters(preprocessor)
        return preprocessor.getMaterialHandler.calcInteractionDiagramNMy(self.name,self.fiberSectionParameters.idParams)

    def defInteractionDiagramNMz(self,preprocessor):
        '''Defines N-Mz interaction diagram.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        if(not self.fiberSectionRepr):
            lmsg.error("defInteractionDiagramNMz: fiber section representation for section: "+ self.name + ";  not defined yet; use defRCSection method.\n")
        self.defInteractionDiagramParameters(preprocessor)
        return preprocessor.getMaterialHandler.calcInteractionDiagramNMz(self.name,self.fiberSectionParameters.idParams)

    def subplot(self, ax, preprocessor, matDiagType= 'k'):
        ''' Put the section drawing in the subplot argument.

        :param ax: matplotlib subplot.
        :param preprocessor: pre-processor of the finite element problem.
        :param matDiagType: type of stress-strain diagram
                     ("k" for characteristic diagram, "d" for design diagram)
        '''
        ax.axis('equal')
        ax.set_title('Section: '+self.name)
        ax.grid(visible= True, linestyle='dotted')
        # Plot contour.
        contour= self.getContour()
        x= list(); y= list()
        for p in contour:
            x.append(p.x)
            y.append(p.y)
        ax.fill(x,y,'tab:gray')
        #ax.plot(x,y,'tab:blue')
        # Plot reinforcement.
        if(not hasattr(self, 'geomSection')):
            self.defSectionGeometry(preprocessor, matDiagType)
        reinforcement= self.geomSection.getReinfLayers
        reinfLayersColors= ['black', 'blue', 'darkblue', 'red', 'darkred', 'darkgreen', 'purple']
        numColors= len(reinfLayersColors)
        for idx, reinfLayer in enumerate(reinforcement):
            rebars= reinfLayer.getReinfBars
            rebarColor= reinfLayersColors[idx % numColors]
            for b in rebars:
                ptPlot= b.getPos2d # bar position.
                rPlot= b.diameter/2.0 # bar radius.
                labelPlot= str(int(round(b.diameter*1e3))) # bar label.
                circle= plt.Circle((ptPlot.x, ptPlot.y), rPlot, color= rebarColor)
                ax.add_patch(circle)
                ax.annotate(labelPlot, (ptPlot.x+rPlot, ptPlot.y+rPlot))

    def plot(self, preprocessor, matDiagType= 'k'):
        ''' Get a drawing of the section using matplotlib.'''
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.subplot(ax, preprocessor= preprocessor, matDiagType= matDiagType)
        plt.show()
   
    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        os.write(indentation+'Section description: '+str(self.sectionDescr)+'\n')
        indentation+= '  '
        os.write(indentation+'Fiber section parameters:\n')
        self.fiberSectionParameters.report(os, indentation+'  ')
        if(self.fiberSectionRepr):
            self.fiberSectionRepr.report(os, indentation+'  ')

class BasicRectangularRCSection(RCSectionBase, section_properties.RectangularSection):
    '''
    Base class for rectangular reinforced concrete sections.

    :ivar shReinfZ:        record of type ShearReinforcement
                           defining the shear reinforcement in Z direction
    :ivar shReinfY:        record of type ShearReinforcement
                           defining the shear reinforcement in Y direction
    '''
    def __init__(self,name= None, sectionDescr= None, width=0.25,depth=0.25,concrType=None, reinfSteelType=None, nDivIJ= 10, nDivJK= 10):
        ''' Constructor.

        :param name: name of the section     
        :param sectionDescr: section description.
        :param width: section width.
        :param depth: section depth.
        :param concrType: type of concrete (e.g. EHE_materials.HA25)     
        :param reinfSteelType: type of reinforcement steel.
        '''
        RCSectionBase.__init__(self, sectionDescr= sectionDescr, concrType= concrType,reinfSteelType= reinfSteelType, nDivIJ= nDivIJ, nDivJK= nDivJK)
        section_properties.RectangularSection.__init__(self,name,width,depth)

        # Transverse reinforcement (z direction)
        self.shReinfZ= ShearReinforcement()
        self.shReinfZ.familyName= "Vz"

        # Transverse reinforcement (y direction)
        self.shReinfY= ShearReinforcement()
        self.shReinfY.familyName= "Vy"
                
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= super(BasicRectangularRCSection, self).__eq__(other)
            if(retval):
                retval= section_properties.RectangularSection.__eq__(self, other)
            if(retval):
                retval= (self.shReinfZ== other.shReinfZ)
            if(retval):
                retval= (self.shReinfY== other.shReinfY)
        else:
            retval= True
        return retval

    def getCopy(self):
        ''' Returns a deep enough copy of the object.'''
        retval= BasicRectangularRCSection(name= self.name, sectionDescr= self.sectionDescr, concrType= self.getConcreteType(), reinfSteelType= self.getReinfSteelType(), width= self.b, depth= self.h, nDivIJ= self.getNDivIJ(), nDivJK= self.getNDivJK())
        return retval

    def getShearReinfY(self):
        '''Return the shear reinforcement for Vy.'''
        return self.shReinfY

    def getShearReinfZ(self):
        '''Return the shear reinforcement for Vz.'''
        return self.shReinfZ
    
    def getRespT(self,preprocessor):
        '''Material for modeling torsional response of section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return section_properties.RectangularSection.getRespT(self,preprocessor,self.fiberSectionParameters.concrType.Gcm()) # Torsional response of the section.

    def getRespVy(self,preprocessor):
        '''Material for modeling Y shear response of section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return section_properties.RectangularSection.getRespVy(self,preprocessor,self.fiberSectionParameters.concrType.Gcm())

    def getRespVz(self,preprocessor):
        '''Material for modeling Z shear response of section.

        :param preprocessor: preprocessor of the finite element problem.
        '''
        return section_properties.RectangularSection.getRespVz(self,preprocessor,self.fiberSectionParameters.concrType.Gcm())

    def getContour(self):
        ''' Return the vertices of the section contour.'''
        pMin= geom.Pos2d(-self.b/2,-self.h/2)
        pMax= geom.Pos2d(self.b/2,self.h/2)
        vertices= [pMin, geom.Pos2d(pMax.x, pMin.y), pMax, geom.Pos2d(pMin.x, pMax.y), pMin]
        return vertices

    def defConcreteRegion(self, geomSection):
        ''' Define a rectangular region filled with concrete.
        '''
        regions= geomSection.getRegions
        rg= regions.newQuadRegion(self.fiberSectionParameters.concrDiagName)
        rg.nDivIJ= self.fiberSectionParameters.nDivIJ
        rg.nDivJK= self.fiberSectionParameters.nDivJK
        rg.pMin= geom.Pos2d(-self.b/2,-self.h/2)
        rg.pMax= geom.Pos2d(self.b/2,self.h/2)

    def getElasticMaterialData(self, overrideRho= None):
        ''' Return an elastic material constitutive model.

        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        return self.fiberSectionParameters.concrType.getElasticMaterialData(overrideRho= overrideRho)
    
    def defElasticSection1d(self, preprocessor, overrideRho= None):
        ''' Return an elastic section appropriate for truss analysis.

        :param preprocessor: preprocessor of the finite element problem.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticSection1d(preprocessor, material= mat, overrideRho= overrideRho)
    
    def defElasticSection3d(self, preprocessor, overrideRho= None):
        ''' Return an elastic section appropriate for 3D beam analysis

        :param preprocessor: preprocessor of the finite element problem.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticSection3d(preprocessor, material= mat, overrideRho= overrideRho)
    
    def defElasticShearSection3d(self, preprocessor, overrideRho= None):
        '''elastic section appropriate for 3D beam analysis, including shear 
           deformations

        :param preprocessor: XC preprocessor for the finite element problem.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
         '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticShearSection3d(preprocessor, material= mat, overrideRho= overrideRho)
    
    def defElasticSection2d(self, preprocessor, majorAxis= True, overrideRho= None):
        ''' Return an elastic section appropriate for 2D beam analysis

        :param preprocessor: XC preprocessor for the finite element problem.
        :param majorAxis: true if bending occurs in the section major axis.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticSection2d(preprocessor, material= mat, majorAxis= majorAxis, overrideRho= overrideRho)
        
    def defElasticShearSection2d(self, preprocessor, majorAxis= True, overrideRho= None):
        '''elastic section appropriate for 2D beam analysis, including 
           shear deformations.

        :param preprocessor: XC preprocessor for the finite element problem.
        :param majorAxis: true if bending occurs in the section major axis.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticShearSection2d(preprocessor, material= mat, majorAxis= majorAxis, overrideRho= overrideRho)

    def defElasticMembranePlateSection(self, preprocessor, overrideRho= None):
        '''Constructs an elastic isotropic section material appropriate 
           for plate and shell analysis.

        :param preprocessor: XC preprocessor of the finite element problem.
        :param overrideRho: if defined (not None), override the value of 
                            the material density.
        '''
        mat= self.getElasticMaterialData(overrideRho= overrideRho)
        return super(BasicRectangularRCSection, self).defElasticMembranePlateSection(preprocessor= preprocessor, material= mat, overrideRho= overrideRho)
    
    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        section_properties.RectangularSection.report(self, os)
        super(BasicRectangularRCSection, self).report(os, indentation)
        indentation+= '  '
        os.write(indentation+'Transverse reinforcement (z direction):\n')
        self.shReinfZ.report(os, indentation+'  ')
        os.write(indentation+'Transverse reinforcement (y direction):\n')
        self.shReinfY.report(os, indentation+'  ')

class RCRectangularSection(BasicRectangularRCSection):
    ''' This class is used to define the variables that make up a reinforced 
        concrete section with top and bottom reinforcement layers.

    :ivar minCover:        minimum value of end or clear concrete cover of main 
                           bars from both the positive and negative faces
    :ivar negatvRebarRows: layers of main rebars in the local negative face of 
                           the section
    :ivar positvRebarRows: layers of main rebars in the local positive face of 
                           the section
    '''
    
    def __init__(self, name= None, sectionDescr= None, width=0.25, depth=0.25, concrType= None, reinfSteelType= None, nDivIJ= 10, nDivJK= 10):
        ''' Constructor.

        :param name: name of the section 
        :param sectionDescr: section description.
        :param width: section width.
        :param depth: section depth.
        :param concrType: type of concrete (e.g. EHE_materials.HA25)     
        :param reinfSteelType: type of reinforcement steel.
        '''
        super(RCRectangularSection,self).__init__(name= name, sectionDescr= sectionDescr, width= width, depth= depth, concrType= concrType, reinfSteelType= reinfSteelType, nDivIJ= nDivIJ, nDivJK= nDivJK)

        # Longitudinal reinforcement
        self.minCover= 0.0 
        self.positvRebarRows= LongReinfLayers() # list of ReinfRow data (positive face)
        self.negatvRebarRows= LongReinfLayers() # list of ReinfRow data (negative face)
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if(self is not other):
            retval= super(RCRectangularSection, self).__eq__(other)
            if(retval):
                retval= (self.minCover == other.minCover)
            if(retval):
                retval= (self.shReinfZ == other.shReinfZ)
            if(retval):
                retval= (self.shReinfY == other.shReinfY)
            if(retval):
                retval= (self.positvRebarRows == other.positvRebarRows)
            if(retval):
                retval= (self.negatvRebarRows == other.negatvRebarRows)
        else:
            retval= True
        return retval

    def flipReinforcement(self):
        ''' Flip the reinforcement top<-->bottom.'''
        self.positvRebarRows, self.negatvRebarRows= self.negatvRebarRows, self.positvRebarRows
        
    def getCopy(self):
        ''' Returns a deep enough copy of the object.'''
        retval= RCRectangularSection(name= self.name, sectionDescr= self.sectionDescr, concrType= self.getConcreteType(), reinfSteelType= self.getReinfSteelType(), width= self.b, depth= self.h, nDivIJ= self.getNDivIJ(), nDivJK= self.getNDivJK())
        return retval

    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        super(RCRectangularSection, self).report(os, indentation)
        indentation+= '  '
        os.write(indentation+'Bottom reinforcement: \n')
        self.positvRebarRows.report(os, indentation+'  ')
        os.write(indentation+'Top reinforcement: \n')
        self.negatvRebarRows.report(os, indentation+'  ')

    def getAsPos(self):
        '''returns the cross-sectional area of the rebars in the positive face.'''
        return self.positvRebarRows.getAs()

    def getPosRowsCGcover(self):
        '''returns the distance from the center of gravity of the positive rebars
        to the positive face of the section.
        '''
        return self.positvRebarRows.getRowsCGcover()

    def hAsPos(self):
        '''Return the distance from the bottom fiber to the 
        centre of gravity of the rebars in the positive face.
        '''
        return self.getPosRowsCGcover()
    
    def getYAsPos(self):
        '''returns the local Y coordinate of the center of gravity of the rebars
           in the positive face.
        '''
        return self.h/2.0-self.getPosRowsCGcover()

    def getAsNeg(self):
        '''returns the cross-sectional area of the rebars in the negative face'''
        return self.negatvRebarRows.getAs()

    def getNegRowsCGcover(self):
        '''returns the distance from the center of gravity of the negative rebars
        to the negative face of the section 
        '''
        return self.negatvRebarRows.getRowsCGcover()

    def hAsNeg(self):
        '''Return the distance from the bottom fiber to the 
        centre of gravity of the rebars in the positive face.
        '''
        return self.h-self.getNegRowsCGcover()
    
    def getYAsNeg(self):
        '''returns the local Y coordinate of the center of gravity of the rebars
           in the negative face
        '''
        return -self.h/2.0+self.getNegRowsCGcover()

    def getAc(self):
        '''Returns the cross-sectional area of the section'''
        return self.b*self.h

    def getAreaHomogenizedSection(self):
        '''Return the area of the homogenized section.'''
        retval= self.getAc()
        n= self.getHomogenizationCoefficient()
        retval+= n*(self.getAsNeg()+self.getAsPos())
        return retval
    
    def hCOGHomogenizedSection(self):
        '''Return the distance from the bottom fiber to the 
        centre of gravity of the homogenized section.
        '''
        retval= self.h/2.0*self.getAc()
        n= self.getHomogenizationCoefficient()
        retval+= self.hAsPos()*n*self.getAsPos()
        retval+= self.hAsNeg()*n*self.getAsNeg()
        retval/=self.getAreaHomogenizedSection()
        return retval
    
    def getRoughVcuEstimation(self):
        '''returns a minimal value (normally shear strength will be greater)
           of the shear strength of the concrete section Vcu expressed
           in newtons.'''
        return 0.5e6*self.getAc() # 0.5 MPa
      
    def getI(self):
        ''' Returns the second moment of area about the middle axis parallel to 
        the width '''
        return 1/12.0*self.b*self.h**3

    def getPosReinforcementIz(self, hCOG, n= 1.0):
        ''' Return the second moment of inertia of the reinforcement in the
            positive side.

        :param hCOG: distance from the section bottom to its center of gravity.
        :param n: homogenizatrion coefficient.
        '''
        retval= 0.0
        for row in self.positvRebarRows:
            retval+= row.getI()
        retval*= n
        d= self.hAsPos()-hCOG
        retval+= (n-1)*self.getAsPos()*d**2 # Steiner.
        return retval
        
    def getNegReinforcementIz(self, hCOG, n= 1.0):
        ''' Return the second moment of inertia of the reinforcement in the
            negative side.

        :param hCOG: distance from the section bottom to its center of gravity.
        :param n: homogenizatrion coefficient.
        '''
        retval= 0.0
        for row in self.negatvRebarRows:
            retval+= row.getI()
        retval*= n
        d= self.hAsNeg()-hCOG
        retval+= (n-1)*self.getAsNeg()*d**2 # Steiner.
        return retval

    def getIzHomogenizedSection(self):
        '''returns the second moment of area about the axis parallel to 
        the section width through the center of gravity'''
        retval= self.getI() # Moment of inertia of the concrete section.
        # Position of the centroid.
        hCOGH= self.hCOGHomogenizedSection()
        # Eccentricity of the concrete section.
        d= self.hCOG()-hCOGH # distance from center of gravity.
        retval+= self.getAc()*d**2 # Steiner.
        # Moment of inertia of the reinforcement.
        n= self.getHomogenizationCoefficient()
        # Reinforcement on the possitive side.
        retval+= self.getPosReinforcementIz(hCOG= hCOGH, n= n)
        # Reinforcement on the possitive side.
        retval+= self.getNegReinforcementIz(hCOG= hCOGH, n= n)
        return retval
    
    def izHomogenizedSection(self):
        '''Return the radius of gyration of the section around
           the axis parallel to the section width that passes 
           through section centroid.
        '''
        return math.sqrt(self.getIzHomogenizedSection()/self.getAreaHomogenizedSection())
   
    def getIyHomogenizedSection(self):
        '''returns the second moment of area about the axis parallel to 
        the section depth through the center of gravity'''
        lmsg.error('getIyHomogenizedSection not implemented yet.')
        # Need to compute the steel distribution along the z axis.
        return self.getIy()
    
    def iyHomogenizedSection(self):
        '''Return the radius of gyration of the section around
           the axis parallel to the section depth that passes 
           through section centroid.
        '''
        lmsg.error('iyHomogenizedSection not implemented yet.')
        # Need to compute the steel distribution along the z axis.
        return self.iy()
    
    def getIz_RClocalZax(self):
        '''returns the second moment of area about the middle axis parallel to 
        the width (RClocalZaxis)'''
        return 1/12.0*self.b*self.h**3

    def getIy_RClocalYax(self):
        '''returns the second moment of area about the middle axis parallel to 
        the depth (RClocalYaxis)'''
        return 1/12.0*self.h*self.b**3

    def getSPos(self):
        '''returns a list with the distance between bars for each row of bars in 
        local positive face.'''
        return self.positvRebarRows.getSpacings()

    def getSNeg(self):
        '''returns a list with the distance between bars for each row of bars in local negative face.'''
        return self.negatvRebarRows.getSpacings()

    def getDiamPos(self):
        '''returns a list with the bar diameter for each row of bars in local 
        positive face.'''
        return self.positvRebarRows.getDiameters()

    def getDiamNeg(self):
        '''returns a list with the bar diameter for each row of bars in local 
        negative face.'''
        return self.negatvRebarRows.getDiameters()

    def getNBarPos(self):
        '''returns a list with the number of bars for each row of bars in local 
        positive face.'''
        return self.positvRebarRows.getNBar()

    def getNBarNeg(self):
        '''returns a list with the number of bars for each row of bars in local 
        negative face.'''
        return self.negatvRebarRows.getNBar()

    def getCoverPos(self):
        '''returns a list with the cover of bars for each row of bars in local 
        positive face.'''
        return self.positvRebarRows.getCover()

    def getCoverNeg(self):
        '''returns a list with the cover of bars for each row of bars in local 
        negative face.'''
        return self.negatvRebarRows.getCover()

    def getLatCoverPos(self):
        '''returns a list with the lateral cover of bars for each row of bars in local positive face.'''
        return self.positvRebarRows.getLatCover()

    def getLatCoverNeg(self):
        '''returns a list with the lateral cover of bars for each row of bars in 
        local negative face.'''
        return self.negatvRebarRows.getLatCover()

    def centerRebarsPos(self):
        '''centers in the width of the section the rebars placed in the positive face''' 
        return self.positvRebarRows.centerRebars(self.b)

    def centerRebarsNeg(self):
        '''centers in the width of the section the rebars placed in the negative 
        face''' 
        return self.negatRebarRows.centerRebars(self.b)

    def getMinCover(self):
        ''' return the minimal cover of the reinforcement.'''
        retval= 1e6
        posCover= self.getCoverPos()
        if(len(posCover)>0):
            retval= min(retval, min(posCover))
        negCover= self.getCoverNeg()
        if(len(negCover)>0):
            retval= min(retval, min(negCover))
        latPosCover= self.getLatCoverPos()
        if(len(latPosCover)>0):
            retval= min(retval, min(latPosCover))
        latNegCover= self.getLatCoverNeg()
        if(len(latNegCover)>0):
            retval= min(retval, min(latNegCover))
        return retval

    def defSectionGeometry(self, preprocessor, matDiagType):
        '''
        Define the XC section geometry object for a reinforced concrete section 

        :param preprocessor: preprocessor of the finite element problem.
        :param matDiagType: type of stress-strain diagram 
                            ("k" for characteristic diagram, "d" for design diagram)
        '''
        self.defDiagrams(preprocessor, matDiagType)
        self.geomSection= preprocessor.getMaterialHandler.newSectionGeometry(self.gmSectionName())
        self.defConcreteRegion(self.geomSection)
        reinforcement= self.geomSection.getReinfLayers
        # Placement of the negative reinforcement.
        negPoints= list()
        ## Compute positions.
        for rbRow in self.negatvRebarRows.rebarRows:
            y= -self.h/2.0+rbRow.cover
            p1= geom.Pos2d(-self.b/2+rbRow.coverLat,y)
            p2= geom.Pos2d(self.b/2-rbRow.coverLat,y)
            negPoints.append((p1,p2))
        self.negatvRebarRows.defStraightLayers(reinforcement,"neg",self.fiberSectionParameters.reinfDiagName,negPoints)
        # Placement of the positive reinforcement.
        posPoints= list()
        ## Compute positions.
        for rbRow in self.positvRebarRows.rebarRows:
            y= self.h/2.0-rbRow.cover
            p1= geom.Pos2d(-self.b/2+rbRow.coverLat,y)
            p2= geom.Pos2d(self.b/2-rbRow.coverLat,y)
            posPoints.append((p1,p2))
        self.positvRebarRows.defStraightLayers(reinforcement,"pos",self.fiberSectionParameters.reinfDiagName,posPoints)
        self.minCover= self.getMinCover()

    def getTorsionalThickness(self):
        '''Return the section thickness for torsion.'''
        return min(self.b,self.h)/2.0

    def getHomogenizationCoefficient(self):
        '''Return the homogenization coefficient of the section.'''
        return self.fiberSectionParameters.reinfSteelType.Es/self.fiberSectionParameters.concrType.Ecm()
    
    def getStressCalculator(self):
        Ec= self.fiberSectionParameters.concrType.Ecm()
        Es= self.fiberSectionParameters.reinfSteelType.Es
        return sc.StressCalc(self.b,self.h,self.getPosRowsCGcover(),self.getNegRowsCGcover(),self.getAsPos(),self.getAsNeg(),Ec,Es)


def get_element_rc_sections(elements, propName= None):
    ''' Return a list containing the reinforced concrete sections from the
        properties defined in the elements arguments. Those properties are:

        - baseSection: RCSectionBase derived object containing the geometry
                       and the material properties of the reinforcec concrete
                       section.
        - reinforcementUpVector: reinforcement "up" direction which defines
                                    the position of the positive reinforcement
                                    (bottom) and the negative reinforcement
                                    (up).
        - bottomReinforcement: LongReinfLayers objects defining the 
                               reinforcement at the bottom of the section.
        - topReinforcement: LongReinfLayers objects defining the 
                            reinforcement at the top of the section.
     
     :param elements: elements for which the reinforce concrete sections 
                      will be computed.
     :param propName: name of the property that stores the section names.
    '''
    retval= list()
    for el in elements:
        reinforcementUpVector= el.getProp("reinforcementUpVector") # reinforcement "up" direction.
        baseSection= el.getProp('baseSection').getCopy()
        dim= el.getDimension
        if(dim==1):
            elementUpOrientation= el.getJVector3d(False)
            upOrientation= reinforcementUpVector.dot(elementUpOrientation)
            pR= el.getProp("bottomReinforcement")
            nR= el.getProp("topReinforcement")
            if(upOrientation<0): # reverse position.
                pR, nR= nR, pR
            baseSection.positvRebarRows= pR
            baseSection.negatvRebarRows= nR
            elementSections= [baseSection]
        elif(dim==2):
            elementUpOrientation= el.getKVector3d(False)
            upOrientation= reinforcementUpVector.dot(elementUpOrientation)
            reinforcementIVector= el.getProp('reinforcementIVector') # direction of the reinforcement in the slab.
            elementIOrientation= el.getIVector3d(False)
            iOrientation= reinforcementIVector.dot(elementIOrientation)
            theta= reinforcementIVector.getAngle(elementIOrientation)
            pRI= el.getProp("bottomReinforcementI")
            nRI= el.getProp("topReinforcementI")
            shRI= None
            if(el.hasProp('shearReinforcementI')):
               shRI= el.getProp('shearReinforcementI')
            pRII= el.getProp("bottomReinforcementII")
            nRII= el.getProp("topReinforcementII")
            shRII= None
            if(el.hasProp('shearReinforcementII')):
                shRII= el.getProp('shearReinforcementII')
            if(abs(iOrientation)<0.7): # reverse reinforcement directions.
                pRI, pRII= pRII, pRI # positive reinforcement.
                nRI, nRII= nRII, nRI # negative reinforcement.
                shRI, shRII= shRII, shRI # shear reinforcement.
                theta-= math.pi/2.0
            if(upOrientation>0): # for 2D elements reverse top and bottom
                                 # positions if dot product > 0.
                pRI, nRI= nRI, pRI # positive reinforcement.
                pRII, nRII= nRII, pRII # positive reinforcement.
                # shear reinforcement not affected.
            if((abs(iOrientation)>1e-3) and (abs(abs(iOrientation)-1.0)>1e-3)): # reinforcement not parallel nor perpendicular
                #el.setProp('theta', theta)
                pass
            baseSectionII= baseSection.getCopy()
            baseSection.name+= 'I'
            baseSection.positvRebarRows= pRI
            baseSection.negatvRebarRows= nRI
            if(shRI):
                baseSection.shReinfY= shRI
            baseSectionII.name+= 'II'
            baseSectionII.positvRebarRows= pRII
            baseSectionII.negatvRebarRows= nRII
            if(shRII):
                baseSection.shReinfY= shRII
            elementSections= [baseSection, baseSectionII]
            
        # Assign elements to each section.
        for i, eSection in enumerate(elementSections):
            if(eSection not in retval):
                eSection.elements= [(el.tag, i)]
                retval.append(eSection)
            else:
                idx= retval.index(eSection)
                retval[idx].elements.append((el.tag, i))
    # Rename the new sections.        
    for i, s in enumerate(retval):
        s.name+= str(i)

    if(not propName is None and (len(elements)>0)):
        # Assign the sections names to the elements
        preprocessor= elements[0].getDomain.getPreprocessor
        elemHandler= preprocessor.getElementHandler
        for elm in elements:
            elm.setProp(propName, ['','']) # Initialize property
        for sct in retval:
            for tple in sct.elements:
                # Each tuple has (element tag, section number).
                eTag= tple[0] 
                sectionIdx= tple[1]
                element= elemHandler.getElement(eTag)
                sectionNames= element.getProp(propName)
                if(sectionNames[sectionIdx]!=''):
                    className= type(self).__name__
                    methodName= sys._getframe(0).f_code.co_name
                    lmsg.error(className+'.'+methodName+'; element '+str(eTag) + ' has alreade section: '+sectionNames[sectionIdx])
                sectionNames[sectionIdx]= sct.name
                element.setProp(propName, sectionNames)
    return retval

                                  
