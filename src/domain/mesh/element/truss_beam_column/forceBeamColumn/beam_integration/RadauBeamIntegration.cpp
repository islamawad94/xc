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
// $Date: 2006/01/18 17:16:26 $
// $Source: /usr/local/cvs/OpenSees/SRC/element/forceBeamColumn/RadauBeamIntegration.cpp,v $

#include <domain/mesh/element/truss_beam_column/forceBeamColumn/beam_integration/RadauBeamIntegration.h>
#include <cmath>
#include <iostream>

XC::RadauBeamIntegration::RadauBeamIntegration():
  BeamIntegration(BEAM_INTEGRATION_TAG_Radau)
{
  // Nothing to do
}

XC::BeamIntegration *XC::RadauBeamIntegration::getCopy(void) const
  { return new RadauBeamIntegration(*this); }

#ifdef _WIN32

extern "C" int GAUSSQ(int *kind, int *n, double *alpha, double *beta,
                               int *kpts, double *endpts, double *b,
			       double *t, double *w);

#define gaussq_ GAUSSQ

#else

extern "C" int gaussq_(int *kind, int *n, double *alpha, double *beta,
		       int *kpts, double *endpts, double *b,
		       double *t, double *w);

#endif

void XC::RadauBeamIntegration::getSectionLocations(int numSections, double L,double *xi) const
{
  switch(numSections) {

  case 1:
    xi[0] = -1.0;
    break;
    
  case 2:
    xi[0] = -1.0;
    xi[1] =  0.3333333333;
    break;
    
  case 3:
    xi[0] = -1.0;
    xi[1] = -0.2898979485;
    xi[2] =  0.6898979485;
    break;
    
  case 4:
    xi[0] = -1.0;
    xi[1] = -0.5753189235;
    xi[2] =  0.1810662711;
    xi[3] =  0.8228240809;
    break;
    
  case 5:
    xi[0] = -1.0;
    xi[1] = -0.7204802713;
    xi[2] = -0.1671808647;
    xi[3] =  0.4463139727;
    xi[4] =  0.8857916077;
    break;  
  
  case 6:
    xi[0] = -1.0;
    xi[1] = -0.8029298284;
    xi[2] = -0.3909285467;
    xi[3] =  0.1240503795;
    xi[4] =  0.6039731642;
    xi[5] =  0.9203802858;
    break;

  case 7:
    xi[0] = -1.0;
    xi[1] = -0.8538913426;
    xi[2] = -0.5384677240;
    xi[3] = -0.1173430375;
    xi[4] =  0.3260306194;
    xi[5] =  0.7038428006;
    xi[6] =  0.9413671456;
    break;

  case 8:
    xi[0] = -1.0;
    xi[1] = -0.8874748789;
    xi[2] = -0.6395186165;
    xi[3] = -0.2947505657;
    xi[4] =  0.09430725266;
    xi[5] =  0.4684203544;
    xi[6] =  0.7706418936;
    xi[7] =  0.9550412271;
    break;

  case 9:
    xi[0] = -1.0;
    xi[1] = -0.9107320894;
    xi[2] = -0.7112674859;
    xi[3] = -0.4263504857;
    xi[4] = -0.09037336960;
    xi[5] =  0.2561356708;
    xi[6] =  0.5713830412;
    xi[7] =  0.8173527842;
    xi[8] =  0.9644401697;
    break;

  case 10:
    xi[0] = -1.0;
    xi[1] = -0.9274843742;
    xi[2] = -0.7638420424;
    xi[3] = -0.5256460303;
    xi[4] = -0.2362344693;
    xi[5] =  0.07605919783;
    xi[6] =  0.3806648401;
    xi[7] =  0.6477666876;
    xi[8] =  0.8512252205;
    xi[9] =  0.9711751807;
    break;

  default:
    break;
  }

  for (int i = 0; i < numSections; i++)
    xi[i]  = 0.5*(xi[i] + 1.0);
}

void XC::RadauBeamIntegration::getSectionWeights(int numSections, double L,double *wt) const
{
  switch (numSections) {
    
  case 1:
    wt[0] = 2.0;
    break;

  case 2:
    wt[0] = 0.5;
    wt[1] = 1.5;
    break;
    
  case 3:
    wt[1] =  0.2222222222;
    wt[2] =  1.024971652;
    wt[3] =  0.7528061254;
    break;
    
  case 4:
    wt[1] =  0.125;
    wt[2] =  0.6576886399;
    wt[3] =  0.7763869376;
    wt[4] =  0.4409244223;
    break;
    
  case 5:
    wt[1] =  0.08;
    wt[2] =  0.4462078021;
    wt[3] =  0.6236530459;
    wt[4] =  0.5627120302;
    wt[5] =  0.2874271215;
    break;

  case 6:
    wt[1] =  0.05555555555;
    wt[2] =  0.3196407532;
    wt[3] =  0.4853871884;
    wt[4] =  0.5209267831;
    wt[5] =  0.4169013343;
    wt[6] =  0.2015883852;
    break;

  case 7:
    wt[1] =  0.04081632653;
    wt[2] =  0.2392274892;
    wt[3] =  0.3809498736;
    wt[4] =  0.4471098290;
    wt[5] =  0.4247037790;
    wt[6] =  0.3182042314;
    wt[7] =  0.1489884711;
    break;

  case 8:
    wt[1] =  0.03125;
    wt[2] =  0.1853581548;
    wt[3] =  0.3041306206;
    wt[4] =  0.3765175453;
    wt[5] =  0.3915721674;
    wt[6] =  0.3470147956;
    wt[7] =  0.2496479013;
    wt[8] =  0.1145088147;
    break;

  case 9:
    wt[1] =  0.02469135802;
    wt[2] =  0.1476540190;
    wt[3] =  0.2471893782;
    wt[4] =  0.3168437756;
    wt[5] =  0.3482730027;
    wt[6] =  0.3376939669;
    wt[7] =  0.2863866963;
    wt[8] =  0.2005532980;
    wt[9] =  0.09071450492;
    break;

  case 10:
    wt[1] =  0.02;
    wt[2] =  0.1202966705;
    wt[3] =  0.2042701318;
    wt[4] =  0.2681948378;
    wt[5] =  0.3058592877;
    wt[6] =  0.3135824572;
    wt[7] =  0.2906101648;
    wt[8] =  0.2391934317;
    wt[9] =  0.1643760127;
    wt[10] = 0.07361700548;
    break;

  default:
    break;
  }
  
  for (int i = 0; i < numSections; i++)
    wt[i] *= 0.5;
}

void XC::RadauBeamIntegration::Print(std::ostream &s, int flag) const
{
  s << "Radau" << std::endl;
}
