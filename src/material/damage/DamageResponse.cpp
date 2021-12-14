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
                                                                        
// $Revision: 1.1 $
// $Date: 2004/09/01 03:54:28 $
// $Source: /usr/local/cvs/OpenSees/SRC/damage/DamageResponse.cpp,v $
                                                                        
// Written: Arash Altoontash, Gregory Deierlein
// Created: Aug 2002
//
// Description: This file contains the XC::DamageResponse class implementation

#include <material/damage/DamageResponse.h>
#include <material/damage/DamageModel.h>

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id)
  : Response(), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, int val)
  : Response(val), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, double val)
  : Response(val), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, const XC::ID &val)
  : Response(val), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, const XC::Vector &val)
  : Response(val), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, const XC::Matrix &val)
  : Response(val), theDamage(dmg), responseID(id) {}

XC::DamageResponse::DamageResponse(DamageModel *dmg, int id, const BJtensor &val)
  : Response(val), theDamage(dmg), responseID(id) {}

int XC::DamageResponse::getResponse(void)
  { return theDamage->getResponse(responseID, myInfo); }
