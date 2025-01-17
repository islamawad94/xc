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
//================================================================================
//# COPY LEFT and RIGHT:                                                         #
//# Commercial    use    of    this  program without express permission of the   #
//# University  of  California, is strictly encouraged. Copyright and Copyleft   #
//# are covered by the following clause:                                         #
//#                                                                              #
//# Woody's license:                                                             #
//# ``This    source    code is Copyrighted in U.S., by the The Regents of the   #
//# University  of  California,  for  an indefinite period, and anybody caught   #
//# using  it  without  our  permission,  will be mighty good friends of ourn,   #
//# cause  we  don't give a darn. Hack it. Compile it. Debug it. Run it. Yodel   #
//# it. Enjoy it. We wrote it, that's all we wanted to do.'' bj                  #
//#                                                                              #
//#                                                                              #
//#                                                                              #
//# PROJECT:           Object Oriented Finite XC::Element Program                    #
//# PURPOSE:           Rounded Mohr Coulomb Potential Surface                    #
//# CLASS:             RoundedMohrCoulomb01YieldSurface                                         #
//#                                                                              #
//# VERSION:                                                                     #
//# LANGUAGE:          C++                                                       #
//# TARGET OS:         DOS || UNIX || . . .                                      #
//# DESIGNER(S):       Boris Jeremic jeremic@ucdavis.edu                         #
//#                    Zhao Cheng,                                               #
//# PROGRAMMER(S):     Zhao Cheng, Boris Jeremic                                 #
//#                                                                              #
//#                                                                              #
//# DATE:              12 Feb. 2003                                              #
//# UPDATE HISTORY:   Feb 25th 2003  
//#                                                                              #
//# Short Explanation:                                                           #
//#              Willam & Warnke (1974) deviatoric shape                    #
//#                                                                              #
//#                                                                              #
//================================================================================
//

#include "material/nD/Template3Dep/RoundedMohrCoulomb01YieldSurface.h"
#include "material/nD/Template3Dep/RoundedMohrCoulomb01.h"
#include "material/nD/Template3Dep/RoundedMohrCoulomb01.h"
#include "utility/matrix/nDarray/stresst.h"
#include "utility/matrix/nDarray/BJtensor.h"
#include "material/nD/Template3Dep/EPState.h"

//! @brief Virtual constructor.
XC::YieldSurface * XC::RoundedMohrCoulomb01YieldSurface::getCopy(void) 
  { return new RoundedMohrCoulomb01YieldSurface(*this); }

//! @brief Yield criterion evaluation function F(EPState)
double XC::RoundedMohrCoulomb01YieldSurface::f(const EPState *EPS) const 
  {
    double p = EPS->getStress().p_hydrostatic(); // 
    double q = EPS->getStress().q_deviatoric(); // q
    double theta = EPS->getStress().theta(); // theta
//    double temp_phi = EPS->getScalarVar(1)*3.14159265358979/180.0; // frictional angle
//    double temp_cohesive = EPS->getScalarVar(2); // cohesion
//    double a1 = -6*sin(temp_phi)/(3.0-sin(temp_phi));
//    double a2 = -6*temp_cohesive*cos(temp_phi)/(3.0-sin(temp_phi));
    double alfa = EPS->getScalarVar(1); // Take alfa & k as internal variables
    double k = EPS->getScalarVar(2);    // instead of phi & conhesive
    double a1 = (3.0*1.7320508076*alfa) / (2.0+1.7320508076*alfa);
    double e = (3.0-a1)/(3.0+a1); // ratio of tensile radius to compressive radius
    double Frou = g_0(theta, e);
    //double f = a1*p+q*Frou+a2; // yield function
    double f = alfa*p*(-3.0) + Frou*q/1.7320508076 - k; // new form 
    return f;
  }

//! @brief BJtensor dF/dsigma_ij  
XC::BJtensor XC::RoundedMohrCoulomb01YieldSurface::dFods(const EPState *EPS) const 
  {
  
    BJtensor dFoverds( def_dim_2, 0.0);

//    double p = EPS->getStress().p_hydrostatic();
    double q = EPS->getStress().q_deviatoric();
    double theta = EPS->getStress().theta(); 
//    double temp_phi = EPS->getScalarVar(1)*3.14159265358979/180.0;
//    double temp_cohesive = EPS->getScalarVar(2);
    BJtensor DpoDs = EPS->getStress().dpoverds(); // dp/ds
    BJtensor DqoDs = EPS->getStress().dqoverds(); // dq/ds
    BJtensor DthetaoDs = EPS->getStress().dthetaoverds();  // d(theta)/ds
//    double a1 = -6*sin(temp_phi)/(3.0-sin(temp_phi));
//    double a2 = -6*temp_cohesive*cos(temp_phi)/(3.0-sin(temp_phi));
    double alfa = EPS->getScalarVar(1);
//    double k = EPS->getScalarVar(2);
    double a1 = (3.0*1.7320508076*alfa) / (2.0+1.7320508076*alfa);
    double e = (3.0-a1)/(3.0+a1);
    double Frou = g_0(theta, e);
    double Frou_prime = g_prime(theta, e);
    double dFoverdp = alfa*(-3.0);
//    double dFoverdq = Frou;
//    double dFoverdtheta = q*Frou_prime;    
    double dFoverdq = Frou/1.7320508076;
    double dFoverdtheta = q*Frou_prime/1.7320508076;

    dFoverds = DpoDs  * dFoverdp +
               DqoDs  * dFoverdq +
               DthetaoDs * dFoverdtheta; // dF/ds

    return dFoverds;
  }

//! @brief double xi_s1 = dF/dS1 = dF/dalfa1 = I1  Derivative in terms of first scalar var 
double XC::RoundedMohrCoulomb01YieldSurface::xi_s1( const EPState *EPS ) const  
  {
    double p = EPS->getStress().p_hydrostatic();
//    double q = EPS->getStress().q_deviatoric();
//    double theta = EPS->getStress().theta();
//    double temp_phi = EPS->getScalarVar(1)*3.14159265358979/180.0;
//    double temp_cohesive = EPS->getScalarVar(2);
//    double e = (3.0-a1)/(3.0+a1);
//    double Frou = g_0(theta, e);
//    double temp1 = 3.0 - sin(temp_phi);
//    double temp2 = temp1 * temp1;
//    double temp3 = -18.0 * cos(temp_phi) / temp2;
//    double temp4 = -6.0 * temp_cohesive * (1.0 -3.0 * sin(temp_phi)) / temp2;
//    double temp = (temp3 * p + temp4)*3.14159265358979/180.0;
//    return temp;
    return p*(-3.0);
  }

//! @brief double xi_s2 = dF/dS2 = dF/k = -1.0  Derivative in terms of second scalar var 
double XC::RoundedMohrCoulomb01YieldSurface::xi_s2( const EPState *EPS ) const 
  {
//    double p = EPS->getStress().p_hydrostatic();
//    double q = EPS->getStress().q_deviatoric();
//    double theta = EPS->getStress().theta();
//    double temp_phi = EPS->getScalarVar(1)*3.14159265358979/180.0;
//   double temp_cohesive = EPS->getScalarVar(2);
//   double e = (3.0-a1)/(3.0+a1);
//    double Frou = g_0(theta, e);
//    double temp1 = 3.0 - sin(temp_phi);
//    double temp2 = cos(temp_phi);
//    double temp3 = -6 * temp2 / temp1;
//    double temp = temp3;
//    return temp;
    return -1.0;
  }


// double xi_t1 = dF/dt1  Derivative in terms of first tensorial var 

//BJtensor XC::RoundedMohrCoulomb01YieldSurface::xi_t1( ) const 
//{
//}

std::ostream& XC::operator<<(std::ostream &os, const RoundedMohrCoulomb01YieldSurface & YS)
  {
    os << "Rounded Mohr Coulomb Surface Parameters: " << std::endl;
    return os;
  }


