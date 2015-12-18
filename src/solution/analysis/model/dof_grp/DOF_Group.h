//----------------------------------------------------------------------------
//  programa XC; cálculo mediante el método de los elementos finitos orientado
//  a la solución de problemas estructurales.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  El programa deriva del denominado OpenSees <http://opensees.berkeley.edu>
//  desarrollado por el «Pacific earthquake engineering research center».
//
//  Salvo las restricciones que puedan derivarse del copyright del
//  programa original (ver archivo copyright_opensees.txt) este
//  software es libre: usted puede redistribuirlo y/o modificarlo 
//  bajo los términos de la Licencia Pública General GNU publicada 
//  por la Fundación para el Software Libre, ya sea la versión 3 
//  de la Licencia, o (a su elección) cualquier versión posterior.
//
//  Este software se distribuye con la esperanza de que sea útil, pero 
//  SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
//  MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO. 
//  Consulte los detalles de la Licencia Pública General GNU para obtener 
//  una información más detallada. 
//
// Debería haber recibido una copia de la Licencia Pública General GNU 
// junto a este programa. 
// En caso contrario, consulte <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
                                                                        
// $Revision: 1.11 $
// $Date: 2005/11/28 21:40:46 $
// $Source: /usr/local/cvs/OpenSees/SRC/analysis/model/dof_grp/DOF_Group.h,v $
                                                                        
                                                                        
#ifndef DOF_Group_h
#define DOF_Group_h

// File: ~/analysis/model/dof_grp/DOF_Group.h
// 
// Written: fmk 
// Created: 11/96
// Revision: A
//
// Description: This file contains the class definition for DOF_Group.
// A DOF_Group object is instantiated by the ConstraintHandler for 
// every unconstrained node in the domain. The constrained nodes require 
// specialised types of DOF_Group; which deal with the constraints. DOF_Group
// objects can handle 0 boundary constraints; if the eqn number of a DOF is 
// less than START_EQN_NUM a value of 0.0 is set for disp, vel and accel when
// a setNode*(Vector &) is invoked.
//
// What: "@(#) DOF_Group.h, revA"

#include <utility/matrix/ID.h>
#include <utility/tagged/TaggedObject.h>
#include <vector>
#include "solution/analysis/UnbalAndTangent.h"

namespace XC {
class Node;
class Vector;
class Matrix;
class TransientIntegrator;
class Integrator;

//! @ingroup Analisis
//
//! @defgroup AnalisisDOF Grupos de grados de libertad para el análisis.
//
//! @ingroup AnalisisDOF
//! @brief A DOF_Group object is instantiated by the ConstraintHandler for 
//! every unconstrained node in the domain. The constrained nodes require 
//! specialised types of DOF_Group; which deal with the constraints. DOF_Group
//! objects can handle 0 boundary constraints; if the eqn number of a DOF is 
//! less than START_EQN_NUM a value of 0.0 is set for disp, vel and accel when
//! a setNode*(Vector &) is invoked.
class DOF_Group: public TaggedObject
  {
  private:
    // private variables - a copy for each object of the class        
    ID 	myID;

    // static variables - single copy for all objects of the class	    
    static Matrix errMatrix;
    static Vector errVect;
    static UnbalAndTangentStorage unbalAndTangentArray; //!< array of class wide vectors and matrices
    static int numDOF_Groups; //!< number of objects of this class

    void inicID(void);
  protected:
    void  addLocalM_Force(const Vector &Udotdot, double fact = 1.0);     

    // protected variables - a copy for each object of the class            
    UnbalAndTangent unbalAndTangent;
    Node *myNode;

    friend class AnalysisModel;
    DOF_Group(int tag, Node *myNode);
    DOF_Group(int tag, int ndof);
  public:
    virtual ~DOF_Group();    

    virtual void setID(int dof, int value);
    virtual void setID(const ID &values);
    virtual const ID &getID(void) const;
    int inicID(const int &value);

    virtual int getNodeTag(void) const;
    inline virtual int getNumDOF(void) const
      { return myID.Size(); }
    virtual int getNumFreeDOF(void) const;
    virtual int getNumConstrainedDOF(void) const;

    // methods to form the tangent
    virtual const Matrix &getTangent(Integrator *theIntegrator);
    virtual void  zeroTangent(void);
    virtual void  addMtoTang(double fact = 1.0);    
    virtual void  addCtoTang(double fact = 1.0);    

    // methods to form the unbalance
    virtual const Vector &getUnbalance(Integrator *theIntegrator);
    virtual void  zeroUnbalance(void);
    virtual void  addPtoUnbalance(double fact = 1.0);
    virtual void  addPIncInertiaToUnbalance(double fact = 1.0);    
    virtual void  addM_Force(const Vector &Udotdot, double fact = 1.0);        

    virtual const Vector &getTangForce(const Vector &x, double fact = 1.0);
    virtual const Vector &getC_Force(const Vector &x, double fact = 1.0);
    virtual const Vector &getM_Force(const Vector &x, double fact = 1.0);

    // methods to obtain committed responses from the nodes
    virtual const Vector & getCommittedDisp(void);
    virtual const Vector & getCommittedVel(void);
    virtual const Vector & getCommittedAccel(void);
    
    // methods to update the trial response at the nodes
    virtual void setNodeDisp(const Vector &u);
    virtual void setNodeVel(const Vector &udot);
    virtual void setNodeAccel(const Vector &udotdot);

    virtual void incrNodeDisp(const Vector &u);
    virtual void incrNodeVel(const Vector &udot);
    virtual void incrNodeAccel(const Vector &udotdot);

    // methods to set the eigen vectors
    virtual void setEigenvector(int mode, const Vector &eigenvalue);
	
    // method added for TransformationDOF_Groups
    virtual Matrix *getT(void);

// AddingSensitivity:BEGIN ////////////////////////////////////
    virtual void addM_ForceSensitivity(const Vector &Udotdot, double fact = 1.0);        
    virtual void addD_ForceSensitivity(const Vector &vel, double fact = 1.0);
    virtual void addD_Force(const Vector &vel, double fact = 1.0);

    virtual const Vector & getDispSensitivity(int gradNumber);
    virtual const Vector & getVelSensitivity(int gradNumber);
    virtual const Vector & getAccSensitivity(int gradNumber);
    virtual int saveSensitivity(Vector *v,Vector *vdot,Vector *vdotdot,int gradNum,int numGrads);
// AddingSensitivity:END //////////////////////////////////////
    virtual void  Print(std::ostream &, int = 0) {return;};
    virtual void resetNodePtr(void);
  };
} // end of XC namespace

#endif

