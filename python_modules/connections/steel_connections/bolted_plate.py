# -*- coding: utf-8 -*-
''' Naive bolted plate model.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2020, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

import math
import json
import importlib
import geom
from import_export import block_topology_entities as bte
from misc_utils import log_messages as lmsg
from connections.steel_connections import plates


class BoltArrayBase(object):
    distances= [50e-3, 75e-3, 100e-3, 120e-3, 150e-3, 200e-3, 250e-3,.3,.4,.5,.6,.7,.8,.9]
    ''' Base class for bolt array. This class must be code agnostic
        i.e. no AISC, EC3, EAE clauses here. There is certainly some
        work to do in that sense (LP 09/2020). 

    :ivar bolt: bolt type.
    :ivar nRows: row number.
    :ivar nCols: column number.
    :ivar dist: distance between rows and columns
                 (defaults to three diameters).
    '''
    def __init__(self, bolt, nRows= 1, nCols= 1, dist= None):
        ''' Constructor.

        :param bolt: bolt type.
        :param nRows: row number.
        :param nCols: column number.
        :param dist: distance between rows and columns
                     (defaults to three diameters).
        '''
        self.bolt= bolt
        self.nRows= nRows
        self.nCols= nCols
        if(dist):
            self.dist= dist
        else:
            tmp= 3.0*self.bolt.diameter
            for d in self.distances:
                if(d>= tmp):
                    self.dist= d
                    break

    def getNumberOfBolts(self):
        ''' Return the number of bolts of the array.'''
        return self.nRows*self.nCols

    def checkDistanceBetweenCenters(self):
        ''' Check distance between centers return a
            number < 1 if the distance is ok.'''
        return self.bolt.getRecommendedDistanceBetweenCenters()/self.dist

    def getWidth(self):
        ''' Return the distance between the centers of the first and the 
            last rows.'''
        return self.dist*(self.nRows-1)

    def getLength(self):
        ''' Return the distance between the centers of the first and the 
            last columns.'''
        return self.dist*(self.nCols-1)
        
    def getMinPlateWidth(self):
        ''' Return the minimum plate width.'''
        retval= 0.0
        if(self.bolt):
            minEdgeDist= self.bolt.getMinimumEdgeDistance()
            return 2.0*minEdgeDist+self.getWidth()
        return retval        

    def getMinPlateLength(self):
        ''' Return the minimum plate length.'''
        retval= 0.0
        if(self.bolt):
            minEdgeDist= self.bolt.getMinimumEdgeDistance()
            return 2.0*minEdgeDist+self.getLength()
        return retval

    def getStandardPlateLength(self):
        ''' Return the standard plate length as the
            searching in self.distances for a length
            greater or equal to the minimum length
            imposed by the bolt arrangement.'''
        minLength= self.getMinPlateLength()
        stdLength= max(minLength,self.getLength()+self.dist)
        retval= stdLength
        for d in self.distances:
            if(d>= stdLength):
                retval= d
                break
        return retval

    def getNetWidth(self, plateWidth):
        ''' Return the net width due to the bolt holes.

        :param plateWidth: width of the bolted plate.
        '''
        designDiameter= self.bolt.getDesignHoleDiameter()
        return plateWidth-self.nRows*designDiameter

    def getDesignShearStrength(self, doubleShear= False):
        ''' Return the shear strength of the bolt group.

        :param doubleShear: true if double shear action.
        '''
        retval= self.getNumberOfBolts()*self.bolt.getDesignShearStrength()
        if(doubleShear):
            retval*=2.0
        return retval

    def getDesignShearEfficiency(self, Pd, doubleShear= False):
        ''' Return the shear efficiency of the bolt group.

        :param Pd: design value of the force to resist.
        :param doubleShear: true if double shear action.
        '''
        return Pd/self.getDesignShearStrength(doubleShear)

    def getShearStrengthEfficiency(self, Pd, doubleShear= False):
        ''' Return the value of efficiency with respect to
            the shear strength.

        :param Pd: design value of the force to resist.
        :param doubleShear: true if double shear action.
        '''
        return self.getDesignShearEfficiency(Pd, doubleShear)

    def __str__(self):
        return ' number of rows: '+str(self.nRows)+' number of columns: '+str(self.nCols)+' distance between centers: '+str(self.dist)+ ' bolts: '+str(self.bolt) 
    def getDict(self):
        ''' Put member values in a dictionary.'''
        boltClassName= str(self.bolt.__class__)[8:-2]
        return {'boltClassName':boltClassName,'bolt':self.bolt.getDict(), 'nRows':self.nRows, 'nCols':self.nCols, 'dist':self.dist}    

    def setFromDict(self,dct):
        ''' Read member values from a dictionary.'''
        tmp= dct['boltClassName'].rsplit('.', 1)
        boltClassName= tmp[1]
        moduleName= tmp[0]
        module= importlib.import_module(moduleName)
        cls= getattr(module, boltClassName)
        self.bolt= cls(diameter= 0.004)
        self.bolt.setFromDict(dct['bolt'])
        self.nRows= dct['nRows']
        self.nCols= dct['nCols']
        self.dist= dct['dist']

    def getCenter(self):
        ''' Return the position of the bolt array centroid.'''
        x0= self.dist*(self.nCols-1)/2.0
        y0= self.dist*(self.nRows-1)/2.0
        return geom.Pos2d(x0,y0)
        
    def getLocalPositions(self):
        ''' Return the local coordinates of the bolts.'''
        retval= list()
        center= self.getCenter()
        for j in range(0,self.nCols):
            for i in range(0,self.nRows):
                x= j*self.dist-center.x
                y= i*self.dist-center.y
                retval.append(geom.Pos2d(x, y))
        return retval

    def getColumnPositions(self, j):
        ''' Return the local coordinates of the bolts at
            the j-th column.

        :param j: index of the column.
        '''
        retval= list()
        center= self.getCenter()
        for i in range(0,self.nRows):
            x= j*self.dist-center.x
            y= i*self.dist-center.y
            retval.append(geom.Pos2d(x, y))
        return retval
    
    def getRowPositions(self, i):
        ''' Return the local coordinates of the bolts at
            the i-th row.

        :param i: index of the column.
        '''
        retval= list()
        center= self.getCenter()
        for j in range(0,self.nCols):
            x= j*self.dist-center.x
            y= i*self.dist-center.y
            retval.append(geom.Pos2d(x, y))
        return retval
    
    def getClearDistances(self, contour, loadDirection):
        ''' Return the clear distance between the edge of the hole and
            the edge of the adjacent hole or edge of the material.

        :param contour: 2D polygon defining the bolted plate contour.
        :param loadDirection: direction of the load.
        '''
        retval= list()
        localPos= self.getLocalPositions()
        for pLocal in localPos:
            cover= contour.getCover(pLocal, loadDirection)
            retval.append(min(self.dist,cover))
        return retval
    
    def getMinimumCover(self, contour):
        ''' Return the minimum of the distances between the centers
            of the holes and the plate contour.

        :param contour: 2D polygon defining the bolted plate contour.
        :param loadDirection: direction of the load.
        '''
        retval= 1e6
        localPos= self.getLocalPositions()
        for pLocal in localPos:
            cover= contour.getCover(pLocal)
            retval= min(retval,cover)
        return retval

    def getMinimumCoverInDir(self, contour, direction):
        ''' Return the minimum of the distances between the centers
            of the holes and the intersection of the ray from that
            point in the direction argument with the contour.

        :param contour: 2D polygon defining the bolted plate contour.
        :param direction: direction of the rays.
        '''
        retval= 1e6
        localPos= self.getLocalPositions()
        for pLocal in localPos:
            cover= contour.getCover(pLocal, direction)
            retval= min(retval,cover)
        return retval
        
    def getHoleBlocks(self, refSys= geom.Ref3d3d(), blockProperties= None):
        ''' Return octagons inscribed in the holes.

        :param refSys: coordinate reference system used to compute
                       the geometry of the holes.
        :param blockProperties: labels and attributes of the holes.
        '''
        localPos= self.getLocalPositions()
        holes= list()
        for pLocal in localPos:
            circle= geom.Circle2d(pLocal,self.bolt.getNominalHoleDiameter()/2.0)
            octagon= circle.getInscribedPolygon(8,0.0).getVertexList()
            holes.append((pLocal,octagon))
        retval= bte.BlockData()
        # Base points (A)
        for h in holes:
            # Hole vertices.
            holeVertices= list()
            for v in h[1]:
                p3d= geom.Pos3d(v.x,v.y,0.0)
                holeVertices.append(refSys.getGlobalPosition(p3d))
            blk= retval.blockFromPoints(holeVertices, blockProperties)
            # Hole center.
            centerProperties= bte.BlockProperties.copyFrom(blockProperties)
            centerProperties.appendAttribute('objType','hole_center')
            centerProperties.appendAttribute('ownerId', 'f'+str(blk.id)) # Hole center owner.
            centerProperties.appendAttribute('diameter', self.bolt.diameter)
            centerProperties.appendAttribute('boltMaterial', self.bolt.steelType.name)
            center= h[0]
            center3d= refSys.getGlobalPosition(geom.Pos3d(center.x, center.y, 0.0))
            retval.appendPoint(-1, center3d.x, center3d.y, center3d.z, pointProperties= centerProperties)
        return retval
                    
    def getPositions(self, refSys= geom.Ref3d3d()):
        ''' Return the global coordinates of the bolts.

        :param refSys: 3D reference system.
        '''
        localPos= self.getLocalPositions()
        retval= list()
        for pLocal in localPos:
            p3d= geom.Pos3d(pLocal.x,pLocal.y, 0.0)
            retval.append(refSys.getGlobalPosition(p3d))
        return retval
    
    def report(self, outputFile):
        ''' Reports connection design values.'''
        outputFile.write('      bolts:\n')
        outputFile.write('        number of bolts: '+str(self.getNumberOfBolts())+' x '+self.bolt.getName()+'\n')
        outputFile.write('        spacing: '+str(self.dist*1000)+' mm\n')
        self.bolt.report(outputFile)
        
class BoltedPlateBase(plates.Plate):
    ''' Base class for bolted plates. This class must be code agnostic
        i.e. no AISC, EC3, EAE clauses here. There is certainly some
        work to do in that sense (LP 09/2020).

    :ivar boltArray: bolt array.
    :ivar eccentricity: eccentricity of the plate with respect the center
                        of the bolt array.
    :ivar doublePlate: if true there is one plate on each side
                       of the main member.
    '''
    def __init__(self, boltArray, width= None, length= None, thickness= 10e-3, steelType= None, notched= False, eccentricity= geom.Vector2d(0.0,0.0), doublePlate= False):
        ''' Constructor.

        :param boltArray: bolt array.
        :param width: plate width (if None it will be computed from the bolt arrangement.)
        :param length: plate length (if None it will be computed from the bolt arrangement.)
        :param thickness: plate thickness.
        :param steelType: steel type.
        :param notched: if true use notchs when appropriate.
        :param eccentricity: eccentricity of the plate with respect the center
                             of the bolt array.
        :param doublePlate: if true there is one plate on each side
                            of the main member.
        '''
        super(BoltedPlateBase,self).__init__(width= width, length= length, thickness= thickness, steelType= steelType, notched= notched)
        self.setBoltArray(boltArray)
        self.eccentricity= eccentricity
        self.doublePlate= doublePlate

    def getMinWidth(self):
        ''' Return the minimum plate width.'''
        return self.boltArray.getMinPlateWidth()

    def getMinLength(self):
        ''' Return the minimum plate length.'''
        return self.boltArray.getMinPlateLength()

    def checkWidth(self):
        ''' Return true if the plate width is enough with respect to
            the bolt arrangement.'''
        return (self.width>self.getMinWidth())

    def checkLength(self):
        ''' Return true if the plate length is enough with respect to
            the bolt arrangement.'''
        return (self.length>self.getMinLength())
    
    def checkDimensions(self):
        ''' Check the plate dimensions with respect to the bolt
            arrangement.'''
        minWidth= self.getMinWidth()
        minLength= self.getMinLength()
        return ((self.width>=minWidth) and (self.length>=minLength))
        
    def computeWidth(self):
        ''' Compute the plate width from the bolt
            arrangement.'''
        minWidth= self.getMinWidth()
        for d in self.boltArray.distances:
            if(d>= minWidth):
                self.width= d
                break
            
    def computeLength(self):
        ''' Assigns the bolt arrangement.'''
        minLength= self.getMinLength()
        for d in self.boltArray.distances:
            if(d>= minLength):
                self.length= d
                break
        
    def computeDimensions(self):
        ''' Compute the plate dimensions from the bolt
            arrangement.'''
        if(not self.width):
            self.computeWidth()
        else:
            self.checkWidth()
        if(not self.length):
            self.computeLength()
        else:
            self.checkLength()
                    
    def setBoltArray(self, boltArray):
        ''' Assigns the bolt arrangement.'''
        self.boltArray= boltArray
        ok= True
        if(self.width and self.length):
            ok= self.checkDimensions()
        elif(self.width):
            self.computeLength()
            ok= self.checkWidth()            
        elif(self.length):
            self.computeWidth()
            ok= self.checkLength()
        else:
            self.computeDimensions()
        if(not ok):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            lmsg.error(className+'.'+methodName+'; plate too small for the bolt arrangement. Length= '+str(self.length)+', min. length: '+str(self.getMinLength()))
 
    def getNetWidth(self):
        ''' Return the net width due to the bolt holes.'''
        return self.boltArray.getNetWidth(self.width)

    def getNetArea(self):
        ''' Return the net area due to the bolt holes.'''
        return self.getNetWidth()*self.thickness
    
    def checkThickness(self, Pd):
        ''' Check plate thickness; return a number < 1 if the 
            thickness is ok.

        :param Pd: design value of the force to resist.
        '''
        return self.getMinThickness(Pd)/self.thickness
    
    def getShearStrengthEfficiency(self, Pd):
        ''' Return the value of efficiency with respect
            to the strength of the bolted plate.

        :param Pd: design value of the force to resist.
        '''
        retval= self.boltArray.getShearStrengthEfficiency(Pd, doubleShear= self.doublePlate)
        retval= max(retval, self.checkThickness(Pd))
        return retval

    def getEfficiency(self, internalForces):
        '''Return efficiency according to section 

        :param internalForces: internal forces.
        '''
        if(internalForces.N<0): # compression
            CF= self.getShearStrengthEfficiency(-internalForces.N)
        else:
            CF= self.getShearStrengthEfficiency(internalForces.N)
        if(abs(internalForces.My)>1e-3):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            lmsg.error(className+'.'+methodName+'; bending not implemented yet.')
        if(abs(internalForces.Mz)>1e-3):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            lmsg.error(className+'.'+methodName+'; bending not implemented yet.')
        if(abs(internalForces.Vy)>1e-3):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            lmsg.error(className+'.'+methodName+'; shear not implemented yet.')
        if(abs(internalForces.Vz)>1e-3):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            lmsg.error(className+'.'+methodName+'; shear not implemented yet.')
        return CF

    def __str__(self):
        tmp= super(BoltedPlateBase,self).__str__()
        return tmp + ' double plate: '+ str(self.doublePlate) + ' bolts: ' + str(self.boltArray)
    
    def getDict(self):
        ''' Returns a dictionary populated with the member values.'''
        retval= super(BoltedPlateBase,self).getDict()
        retval.update({'boltArray':self.boltArray.getDict(), 'doublePlate':self.doublePlate})
        return retval

    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: dictionary to read values from.
        '''
        super(BoltedPlateBase,self).setFromDict(dct)
        self.boltArray.setFromDict(dct['boltArray'])
        self.computeDimensions()
        self.doublePlate= dct['doublePlate']

    def report(self, outputFile):
        ''' Reports connection design values.'''
        super(BoltedPlateBase, self).report(outputFile)
        # report bolts
        self.boltArray.report(outputFile)

    def getCoreContour2d(self):
        ''' Return the contour points of the plate core 
            in local coordinates.'''
        l2= self.length/2.0
        w2= self.width/2.0
        return [geom.Pos2d(-l2+self.eccentricity.x,-w2+self.eccentricity.y), geom.Pos2d(l2+self.eccentricity.x,-w2+self.eccentricity.y), geom.Pos2d(l2+self.eccentricity.x,w2+self.eccentricity.y), geom.Pos2d(-l2+self.eccentricity.x,w2+self.eccentricity.y)]
    
    def getObjectTypeAttr(self):
        ''' Return the object type attribute (used in getBlocks).'''
        return 'bolted_plate'

    def getBlocks(self, blockProperties= None, loadTag= None, loadDirI= None, loadDirJ= None, loadDirK= None):
        ''' Return the blocks that define the plate.

        :param blockProperties: labels and attributes to assign to the newly created blocks.
        :param loadTag: tag of the applied loads in the internal forces file.
        :param loadDirI: I vector of the original element. Vector that 
                         points to the loaded side of the plate.
        :param loadDirJ: J vector of the of the original element.
        :param loadDirK: K vector of the of the original element.
        '''
        retval= bte.BlockData()
        plateProperties= bte.BlockProperties.copyFrom(blockProperties)
        plateProperties.appendAttribute('objType', self.getObjectTypeAttr())
        if(loadTag):
            plateProperties.appendAttribute('loadTag', loadTag)
            plateProperties.appendAttribute('loadDirI', [loadDirI.x, loadDirI.y, loadDirI.z])
            plateProperties.appendAttribute('loadDirJ', [loadDirJ.x, loadDirJ.y, loadDirJ.z])
            plateProperties.appendAttribute('loadDirK', [loadDirK.x, loadDirK.y, loadDirK.z])
        # Get the plate contour
        contourVertices= self.getContour()
        blk= retval.blockFromPoints(contourVertices, plateProperties, thickness= self.thickness, matId= self.steelType.name)
        ownerId= 'f'+str(blk.id)
        # Get the hole blocks for the new plate
        holeProperties= bte.BlockProperties.copyFrom(blockProperties)
        holeProperties.appendAttribute('objType', 'hole')
        holeProperties.appendAttribute('ownerId', ownerId)
        blk.holes= self.boltArray.getHoleBlocks(self.refSys,holeProperties)
        retval.extend(blk.holes)
        # Get the weld blocks for the plate
        wBlocks= self.getWeldBlocks(ownerId, blockProperties) # Get the weld blocks for the plate
        if(wBlocks):
            blk.weldBlocks= wBlocks 
            retval.extend(blk.weldBlocks)
        return retval

    def getClearDistances(self, loadDirection):
        ''' Return the clear distance between the edge of the hole and
            the edge of the adjacent hole or edge of the material.

        :param loadDirection: direction of the load.
        '''
        contour= geom.Polygon2d(self.getCoreContour2d())
        retval= self.boltArray.getClearDistances(contour, loadDirection)
        return retval
    
    def getMinimumCover(self):
        ''' Return the minimum of the distances between the centers
            of the holes and the plate contour.

        :param loadDirection: direction of the load.
        '''
        contour= geom.Polygon2d(self.getCoreContour2d())
        return self.boltArray.getMinimumCover(contour)

    def getMinimumCoverInDir(self, direction):
        ''' Return the minimum of the distances between the centers
            of the holes and the intersection of the ray from that
            point in the direction argument with the plate contour.

        :param direction: direction of the rays.
        '''
        contour= geom.Polygon2d(self.getCoreContour2d())
        return self.boltArray.getMinimumCoverInDir(contour, direction)

    def jsonWrite(self, outputFileName):
        ''' Write object to JSON file.

        :param outputFileName: name of the output file.
        '''
        outputDict= self.getDict()
        with open(outputFileName, 'w') as outfile:
            json.dump(outputDict, outfile)
        outfile.close()


def getBoltedPointBlocks(gussetPlateBlocks, boltedPlateBlocks, distBetweenPlates, blockProperties):
    ''' Return the lines corresponding to the bolts between the two pieces.

    :param gussetPlateBlocks: blocks of the gusset plate.
    :param boltedPlateBlocks: plate bolted to the gusset plate.
    :param distBetweenPlates: distance between plates.
    :param blockProperties: labels and attributes to assign to the newly created blocks.
    '''
    retval= bte.BlockData()
    # Hole centers in the gusset plate.
    gussetPlateBoltCenters= list()
    for key in gussetPlateBlocks.points:
        p= gussetPlateBlocks.points[key]
        if(p.getAttribute('objType')=='hole_center'):
            gussetPlateBoltCenters.append(p)
    # Hole center in the bolted plate.
    boltedPlateBoltCenters= list()
    for key in boltedPlateBlocks.points:
        p= boltedPlateBlocks.points[key]
        if(p.getAttribute('objType')=='hole_center'):
            boltedPlateBoltCenters.append(p)
    tol= distBetweenPlates/100.0
    # Bolt properties.
    boltProperties= bte.BlockProperties.copyFrom(blockProperties)
    boltProperties.appendAttribute('objType', 'bolt_axis')
    boltProperties.appendAttribute('ownerId', None) # Has no owner.
    for pA in gussetPlateBoltCenters:
        for pB in boltedPlateBoltCenters:
            dist= math.sqrt((pA.coords[0]-pB.coords[0])**2+(pA.coords[1]-pB.coords[1])**2+(pA.coords[2]-pB.coords[2])**2)
            if(abs(dist-distBetweenPlates)<tol):
                boltBlk= bte.BlockRecord(id= -1, typ= 'line', kPoints= [pA.id, pB.id], blockProperties= boltProperties)
                id= retval.appendBlock(boltBlk)
    return retval
