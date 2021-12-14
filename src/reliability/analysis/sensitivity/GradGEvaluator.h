// -*-c++-*-
//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis C. Pérez Tato
//
//  This program derives from OpenSees <http://opensees.berkeley.edu>
//  developed by the  «Pacific earthquake engineering research center».
//
//  Except for the restrictions that may arise from the copyright
//  of the original program (see copyright_opensees.txt)
//  XC is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or 
//  (at your option) any later version.
//
//  This software is distributed in the hope that it will be useful, but 
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. 
//
//
// You should have received a copy of the GNU General Public License 
// along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 2001, The Regents of the University of California    **
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
** Reliability module developed by:                                   **
**   Terje Haukaas (haukaas@ce.berkeley.edu)                          **
**   Armen Der Kiureghian (adk@ce.berkeley.edu)                       **
**                                                                    **
** ****************************************************************** */
                                                                        
// $Revision: 1.2 $
// $Date: 2003/10/27 23:45:44 $
// $Source: /usr/local/cvs/OpenSees/SRC/reliability/analysis/sensitivity/GradGEvaluator.h,v $


//
// Written by Terje Haukaas (haukaas@ce.berkeley.edu)
//

#ifndef GradGEvaluator_h
#define GradGEvaluator_h

#include <utility/matrix/Vector.h>
#include <utility/matrix/Matrix.h>
#include <reliability/domain/components/ReliabilityDomain.h>
#include <tcl.h>

namespace XC {

//! @ingroup ReliabilityAnalysis
//!
//! @brief Base class for the evaluators of
//! the gradient of the limit surface.
class GradGEvaluator
  {
  private:
    Matrix DgDpar;
  protected:
    Vector grad_g;
    Matrix grad_g_matrix;
    mutable Matrix DgDdispl;
    bool doGradientCheck;
    
    int computeParameterDerivatives(double g);
    ReliabilityDomain *theReliabilityDomain;
    Tcl_Interp *theTclInterp;
  public:
    GradGEvaluator(ReliabilityDomain *theReliabilityDomain, Tcl_Interp *theTclInterp, bool doGradientCheck);
    virtual ~GradGEvaluator();

    // Methods provided by the sub-classes
    virtual int computeGradG(double gFunValue, const Vector &passed_x) =0;
    virtual int computeAllGradG(Vector gFunValues, const Vector &passed_x) =0;

    virtual const Vector &getGradG(void) const;
    virtual const Matrix &getAllGradG(void) const;

    // Methods that are provided by sub-classes, but rather specific to FE reliability
    virtual const Matrix &getDgDdispl(void) const;
    virtual const Matrix &getDgDpar(void) const;
  };
} // end of XC namespace

#endif
