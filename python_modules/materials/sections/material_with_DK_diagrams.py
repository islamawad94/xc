# -*- coding: utf-8 -*-

'''MaterialWithDKDiagrams.py: materials with characteristic (K) and design (D) diagrams.'''

__author__= "Luis C. Pérez Tato (LCPT) Ana Ortega (AO_O)"
__copyright__= "Copyright 2015, LCPT AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com ana.Ortega.Ort@gmail.com"

class MaterialWithDKDiagrams(object):
    """Base class for materials with characteristic (K) and design (D) diagrams 

      :ivar materialName: name of the material.
      :ivar nmbDiagK: name of the characteristic diagram.
      :ivar matTagK:  tag of the uni-axial material in the characteristic diagram.
      :ivar nmbDiagD: name of the design diagram.
    """
    def __init__(self,matName):
        ''' Constructor.

        :param matName: material name.
        '''
        self.setupName(matName)

    def setupName(self,matName):
        ''' Material setup.

        :param matName: material name.
        '''
        self.materialName= matName # Name identifying the material.
        self.nmbDiagK= "dgK"+self.materialName # Name identifying the characteristic stress-strain diagram.
        self.matTagK= -1 # Tag of the uniaxial material with the characteristic stress-strain diagram.
        self.materialDiagramK= None # Characteristic stress-strain diagram.
        self.nmbDiagD= "dgD"+self.materialName # Name identifying the design stress-strain diagram.
        self.matTagD= -1 # Tag of the uniaxial material with the design stress-strain diagram .
        self.materialDiagramD= None # Design stress-strain diagram.

    def __repr__(self):
        return self.materialName

    def getDiagK(self,preprocessor):
        return preprocessor.getMaterialHandler.getMaterial(self.nmbDiagK)
    
    def getDiagD(self,preprocessor):
        return preprocessor.getMaterialHandler.getMaterial(self.nmbDiagD)

