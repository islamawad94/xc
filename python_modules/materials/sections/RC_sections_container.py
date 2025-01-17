# -*- coding: utf-8 -*-
__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2016, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

import sys
import xc
# Macros
from misc_utils import log_messages as lmsg

# TO ENHANCE: Interactions diagrams ("d" and "k") are calculated each time we 
# call the checking routines. Maybe it's a good idea to calculate them once and
# write them in a file to use them as needed.

class SectionContainer(object):
    ''' Section container.

    :ivar sections: List with the section definitions.
    :ivar mapSections: Dictionary with pairs (sectionName, reference to
                       section definition.
    :ivar mapInteractionDiagrams:  file containing a dictionary such that
                                   associates each element with the two 
                                   interactions diagrams of materials 
                                   to be used in the verification.
    '''
    def __init__(self):
        ''' Container for the reinforced concrete definitions (name, concrete
        type, rebar positions,...).

        '''
        self.sections= [] # List with the section definitions.
        self.mapSections= {} # Dictionary with pairs (sectionName, reference to
                             # section definition.
        self.mapInteractionDiagrams= None

    def append(self, rcSections):
        ''' Append the argument to the container.

        :param rcSections: 
        '''
        rcSections.createSections()
        self.sections.append(rcSections)
        # Update references to individual sections.
        for ss in rcSections.lstRCSects:
            self.mapSections[ss.name]= ss

    def extend(self, other):
        ''' Add all the elements of the container argument to the calling one.

        :param other: SectionContainer object.
        '''
        self.sections.extend(other.sections)
        self.mapSections.update(other.mapSections)

    def search(self,nmb):
        ''' Return section named nmb (if founded) '''
        retval= None
        for s in self.sections:
          if(s.name==nmb):
            retval= s
        return retval

    def createRCsections(self,preprocessor,matDiagType):
        '''Creates for each element in the container the fiber sections 
        (RCsimpleSections) associated with it.
        Depending on the value of attribute 'initTensStiff' of the concrete 
        class, the method generates the concrete fibers using a constitutive 
        model without tension branch (diagram ot type concrete01) or 
        uses a concrete02 model, that initializes the material in order to
        check the cracking limit state (tension stiffening models).

        :param preprocessor: XC preprocessor for the finite element model.
        :param matDiagType: type of stress-strain diagram (="k" for characteristic diagram, ="d" for design diagram)
        '''
        for s in self.sections:
            for i in range(len(s.lstRCSects)):
                s.lstRCSects[i].defRCSection(preprocessor,matDiagType)


    def calcInteractionDiagrams(self,preprocessor,matDiagType, diagramType= 'NMyMz'):
        '''Calculates 3D interaction diagrams for each section.

        :param preprocessor:   XC preprocessor for the finite element model.
        :param matDiagType:    'k' for characteristic, 'd' for design
        :param diagramType:    three dimensional diagram: NMyMz
                               bi-dimensional diagram: NMy
                               bi-dimensional diagram: NMz
        '''
        self.mapInteractionDiagrams= {}
        for s in self.sections:
            for rcs in s.lstRCSects:
                diag= None
                if(diagramType=='NMyMz'):
                    diag= rcs.defInteractionDiagram(preprocessor)
                elif(diagramType=='NMy'):
                    diag= rcs.defInteractionDiagramNMy(preprocessor,matDiagType)
                elif(diagramType=='NMz'):
                    diag= rcs.defInteractionDiagramNMz(preprocessor,matDiagType)
                else:
                    lmsg.error("calcInteractionDiagrams; interaction diagram type: " + diagramType + "' unknown.")
                self.mapInteractionDiagrams[rcs.name]= diag

    def report(self, os= sys.stdout, indentation= ''):
        ''' Get a report of the object contents.'''
        for s in self.sections:
            s.report(os= os, indentation= indentation)
