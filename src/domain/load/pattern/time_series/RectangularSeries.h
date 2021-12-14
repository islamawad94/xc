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
                                                                        
// $Revision: 1.2 $
// $Date: 2003/02/14 23:01:00 $
// $Source: /usr/local/cvs/OpenSees/SRC/domain/load/pattern/RectangularSeries.h,v $
                                                                        
                                                                        
#ifndef RectangularSeries_h
#define RectangularSeries_h

// File: ~/domain/load/pattern/RectangularSeries.h
//
// Written: fmk 
// Created: 07/99
// Revision: A
//
// Purpose: This file contains the class definition for RectangularSeries.
// RectangularSeries is a concrete class. A RectangularSeries object provides
// a rectangular pulse time series. the factor is given by the pseudoTime and 
// a constant factor provided in the constructor, the duration by tStart
// and tFinal;
//
// What: "@(#) RectangularSeries.h, revA"

#include "PulseBaseSeries.h"

namespace XC {

//! @ingroup TSeries
//
//! @brief Rectangular pulse.
class RectangularSeries: public PulseBaseSeries
  {
  public:
    // constructors
    RectangularSeries(double tStart, double tFinal, double cFactor = 1.0);
    RectangularSeries(void);
    TimeSeries *getCopy(void) const
      { return new RectangularSeries(*this); }
    
    // method to get load factor
    double getFactor(double pseudoTime) const;    
  };
} // end of XC namespace

#endif
