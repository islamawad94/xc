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
//DampingFactorsIntegrator.h

#ifndef DampingFactorsIntegrator_h
#define DampingFactorsIntegrator_h

#include <solution/analysis/integrator/TransientIntegrator.h>
#include "domain/mesh/element/utils/RayleighDampingFactors.h"

namespace XC {

//! @ingroup TransientIntegrator
//
//! @brief Base class for the integrators that make use of
//! Rayleigh damping factors.
class DampingFactorsIntegrator: public TransientIntegrator
  {
  protected:
    RayleighDampingFactors rayFactors; //!< Rayleigh damping factors

    void setRayleighDampingFactors(void);
    int sendData(Communicator &);
    int recvData(const Communicator &);

    DampingFactorsIntegrator(SolutionStrategy *,int classTag);
    DampingFactorsIntegrator(SolutionStrategy *,int classTag,const RayleighDampingFactors &rF);
  public:
    void Print(std::ostream &s, int flag = 0) const;        
    
  };
} // end of XC namespace

#endif
