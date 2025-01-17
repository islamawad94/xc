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
///////////////////////////////////////////////////////////////////////////////
//
// COPYRIGHT (C):     :-))
// PROJECT:           Object Oriented Finite XC::Element Program
// FILE:              EightNodeBrick_u_p_U.cpp
// CLASS:             EightNodeBrick_u_p_U
// MEMBER FUNCTIONS:
//
// MEMBER VARIABLES
//
// PURPOSE:           Finite XC::Element Class for coupled system
//  "Coupled system": Solid and fluid coexist.
//                    u-- Solid displacement
//                    p-- Pore pressure
//                    U-- Absolute fluid displacement
//
// RETURN:
// VERSION:
// LANGUAGE:          C++
// TARGET OS:         DOS || UNIX || . . .
// DESIGNER:          Boris Jeremic, Zhao Cheng
// PROGRAMMER:        Boris Jeremic, Zhaohui Yang, Xiaoyan Wu, Zhao Cheng
// DATE:              Aug. 2001
// UPDATE HISTORY:    Modified from XC::EightNodeBrick.cpp  reorganized a lot by Xiaoyan
//                    01/24/2002    Xiaoyan
//                    Add the permeability XC::BJtensor and ks, kf to the constructor  Xiaoyan
//
//
//                    31Oct2003. Qing fixed small inconsistencies in basic theory
//                               related to permeability...
//
//
//                    Clean-up and re-write by Zhao Cheng, 10/20/2004
//
///////////////////////////////////////////////////////////////////////////////
//
#ifndef EIGHTNODEBRICK_U_P_U_CPP
#define EIGHTNODEBRICK_U_P_U_CPP

#include <domain/mesh/element/volumetric/upU/EightNodeBrick_u_p_U.h>
#include <utility/matrix/Vector.h>
#include <utility/matrix/Matrix.h>
#include <utility/matrix/nDarray/stresst.h>
#include <utility/matrix/nDarray/straint.h>
#include <utility/matrix/nDarray/BJtensor.h>
#include <domain/mesh/element/utils/Information.h>
#include <utility/recorder/response/ElementResponse.h>
#include <domain/load/ElementalLoad.h>
#include <domain/domain/Domain.h>
#include <domain/mesh/node/Node.h>
#include <utility/actor/objectBroker/FEM_ObjectBroker.h>
#include <material/nD/NDMaterial.h>
#include "domain/load/volumetric/BrickSelfWeight.h"

const int XC::EightNodeBrick_u_p_U::Num_IntegrationPts = 2;
const int XC::EightNodeBrick_u_p_U::Num_TotalGaussPts = 8;
const int XC::EightNodeBrick_u_p_U::Num_Nodes = 8;
const int XC::EightNodeBrick_u_p_U::Num_Dim = 3;
const int XC::EightNodeBrick_u_p_U::Num_Dof = 7;
const int XC::EightNodeBrick_u_p_U::Num_ElemDof = 56;
const double XC::EightNodeBrick_u_p_U::pts[2] = {-0.577350269189626, +0.577350269189626};
const double XC::EightNodeBrick_u_p_U::wts[2] = {1.0, 1.0};
 XC::Matrix XC::EightNodeBrick_u_p_U::K(Num_ElemDof, Num_ElemDof);
 XC::Matrix XC::EightNodeBrick_u_p_U::C(Num_ElemDof, Num_ElemDof);
 XC::Matrix XC::EightNodeBrick_u_p_U::M(Num_ElemDof, Num_ElemDof);
 XC::Vector XC::EightNodeBrick_u_p_U::P(Num_ElemDof);
 XC::BJtensor XC::EightNodeBrick_u_p_U::perm(def_dim_2,0.0);


//======================================================================
XC::EightNodeBrick_u_p_U::EightNodeBrick_u_p_U(int element_number,
                                           int node_numb_1,
                                           int node_numb_2,
                                           int node_numb_3,
                                           int node_numb_4,
                                           int node_numb_5,
                                           int node_numb_6,
                                           int node_numb_7,
                                           int node_numb_8,
                                           NDMaterial *Globalmmodel,
                                           const BodyForces3D &bForces,
                                           double nn,
                                           double alf,
                                           double rs,
                                           double rf,
                                           double permb_x,
                                           double permb_y,
                                           double permb_z,
                                           double kks,
                                           double kkf,
                                           double pp)
: BrickBase(element_number, ELE_TAG_EightNodeBrick_u_p_U,node_numb_1,node_numb_2,node_numb_3,node_numb_4,node_numb_5,node_numb_6,node_numb_7,node_numb_8,NDMaterialPhysicalProperties(8,Globalmmodel)),
   bf(bForces), poro(nn), alpha(alf), rho_s(rs), rho_f(rf),
   ks(kks), kf(kkf), pressure(pp), eleQ(0), Ki(0)
  {
    // permeability
    perm(1,1) = permb_x;
    perm(2,2) = permb_y;
    perm(3,3) = permb_z;
  }

//======================================================================
XC::EightNodeBrick_u_p_U::EightNodeBrick_u_p_U(void)
  : BrickBase(0,ELE_TAG_EightNodeBrick_u_p_U,NDMaterialPhysicalProperties(8,nullptr)),
   poro(0.0), alpha(1.0), rho_s(0.0),rho_f(0.0), ks(0.0), kf(0.0), pressure(0.0),
   eleQ(nullptr), Ki(nullptr)
  {}

//! @brief Virtual constructor.
XC::Element *XC::EightNodeBrick_u_p_U::getCopy(void) const
  { return new EightNodeBrick_u_p_U(*this); }

//======================================================================
XC::EightNodeBrick_u_p_U::~EightNodeBrick_u_p_U(void)
  {
     if(eleQ) delete eleQ;
     if(Ki) delete Ki;
  }

//======================================================================
int XC::EightNodeBrick_u_p_U::getNumDOF(void) const
  { return Num_ElemDof; }

//======================================================================
void XC::EightNodeBrick_u_p_U::setDomain(Domain *theDomain)
  {
    BrickBase::setDomain(theDomain);
    theNodes.checkNumDOF(Num_Dof,getTag());
  }


//======================================================================
const XC::Matrix &XC::EightNodeBrick_u_p_U::getTangentStiff(void) const
  {
    static Matrix retval;
    retval= getStiff(1);
    if(isDead())
      retval*= dead_srf;
    return retval;
  }

//======================================================================
const XC::Matrix &XC::EightNodeBrick_u_p_U::getInitialStiff(void) const
  {
    static Matrix retval;
    retval= getStiff(0);
    if(isDead())
      retval*= dead_srf;
    return retval;
  }

//======================================================================
const XC::Matrix &XC::EightNodeBrick_u_p_U::getDamp(void) const
  {
    BJtensor tC = getDampTensorC123();
    //tC.print("C","\n");
    int i, j, m, n;

    double Ctemp = 0.0;
    BJtensor CRm;
    BJtensor CRk;
    if(rayFactors.getAlphaM() != 0.0)
      CRm = getMassTensorMsf() *((1.0-poro)*rho_s);
    if(rayFactors.getBetaK() != 0.0)
      CRk = getStiffnessTensorKep();
    if(rayFactors.getBetaK0() != 0.0 || rayFactors.getBetaKc() != 0.0) {
          std::cerr << "Warning: EightNodeBrick-XC::u_p_U:: betaK0 or rayFactors.getBetaKc() are not used" << "\n";
    }

    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        for( m=0; m<Num_Dim; m++) {
          for( n=0; n<Num_Dim; n++)
            {
              Ctemp = tC(i+1, m+1, n+1, j+1);
              //C1
              C(i*Num_Dof+m, j*Num_Dof+n) = Ctemp *(poro*poro);
              if(rayFactors.getAlphaM() != 0.0)
                 C(i*Num_Dof+m, j*Num_Dof+n) += CRm(i+1, j+1) * rayFactors.getAlphaM();
              if(rayFactors.getBetaK() != 0.0)
                 C(i*Num_Dof+m, j*Num_Dof+n) += CRk(i+1, m+1, n+1, j+1) * rayFactors.getBetaK();
              //C3
              C(i*Num_Dof+m+4, j*Num_Dof+n+4) = Ctemp *(poro*poro);
              //C2 and C2^T
              C(i*Num_Dof+m, j*Num_Dof+n+4) = -Ctemp *(poro*poro);
              C(j*Num_Dof+n+4, i*Num_Dof+m) = -Ctemp *(poro*poro);
            }
        }
      }
    }
    if(isDead())
      C*=dead_srf;
    return C;
  }

//======================================================================
const XC::Matrix &XC::EightNodeBrick_u_p_U::getMass (void) const
  {
    BJtensor tM = getMassTensorMsf();
    //tM.print("M","\n");
    M.Zero();

    int i, j;
    double Mtemp = 0.0;

    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        Mtemp = tM(i+1, j+1);
        //Ms, Note *(1.0-poro)*rho_s here!
        M(i*Num_Dof+0, j*Num_Dof+0) = Mtemp *(1.0-poro)*rho_s;
        M(i*Num_Dof+1, j*Num_Dof+1) = Mtemp *(1.0-poro)*rho_s;
        M(i*Num_Dof+2, j*Num_Dof+2) = Mtemp *(1.0-poro)*rho_s;
        //Mf, Note *poro*rho_f here!
        M(i*Num_Dof+4, j*Num_Dof+4) = Mtemp *poro*rho_f;
        M(i*Num_Dof+5, j*Num_Dof+5) = Mtemp *poro*rho_f;
        M(i*Num_Dof+6, j*Num_Dof+6) = Mtemp *poro*rho_f;
      }
    }
    if(isDead())
      M*=dead_srf;

    return M;
  }

//======================================================================
void XC::EightNodeBrick_u_p_U::zeroLoad(void)
  {
    BrickBase::zeroLoad();
    if(eleQ)
      eleQ->Zero();
  }

//======================================================================
int XC::EightNodeBrick_u_p_U::addLoad(ElementalLoad *theLoad, double loadFactor)
  {
    BrickSelfWeight *brkLoad= dynamic_cast<BrickSelfWeight *>(theLoad);
    if(brkLoad)
      {
        if(eleQ==0)
          eleQ = new Vector(Num_ElemDof);
        *eleQ = (this->getExForceS() + this->getExForceF() )*loadFactor;
      }
    else
      {
        std::cerr << "XC::EightNodeBrick_u_p_U::addLoad() " << this->getTag() << ", load type unknown\n";
        return -1;
      }
    return 0;
  }

//======================================================================
int XC::EightNodeBrick_u_p_U::addInertiaLoadToUnbalance(const XC::Vector &accel)
{
  static XC::Vector ra(Num_ElemDof);

  int i, ik;

  for(i=0; i<Num_Nodes; i++) {
    const XC::Vector &RA = theNodes[i]->getRV(accel);

    if( RA.Size() != Num_Dof ) {
      std::cerr << "XC::EightNodeBrick_u_p_U::addInertiaLoadToUnbalance matrix and vector sizes are incompatible\n";
      return (-1);
    }

    ik = i*Num_Dof;

    ra(ik +0) = RA(0);
    ra(ik +1) = RA(1);
    ra(ik +2) = RA(2);
    ra(ik +3) = 0.0;
    ra(ik +4) = RA(4);
    ra(ik +5) = RA(5);
    ra(ik +6) = RA(6);
  }

  if(load.isEmpty())
    load.reset(Num_ElemDof);

    load.addMatrixVector(1.0, M, ra, -1.0);

  return 0;
}

//========================================================================
const XC::Vector &XC::EightNodeBrick_u_p_U::getResistingForce(void) const
  {
    P.Zero();

    int i, j;
    Vector u(Num_ElemDof);

    // Using K*u as the internal nodal forces
    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector &disp = theNodes[i]->getTrialDisp();
      if( disp.Size() != Num_Dof ) {
        std::cerr << "XC::EightNode_Brick_u_p_U::getResistingForce(): matrix and vector sizes are incompatible \n";
        exit(-1);
      }
      for(j=0; j<Num_Dof; j++) {
        u(i*Num_Dof +j) = disp(j);
      }
    }

    this->getTangentStiff();
    P.addMatrixVector(0.0, K, u, 1.0);

    if(!load.isEmpty())
      P.addVector(1.0, load, -1.0);

    if(eleQ != 0)
      P.addVector(1.0, *eleQ, -1.0);

    if(isDead())
      P*=dead_srf;
    return P;
  }

//========================================================================
const XC::Vector &XC::EightNodeBrick_u_p_U::getResistingForceIncInertia(void) const
  {
    int i, j;
    Vector a(Num_ElemDof);

    this->getResistingForce();

    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector &acc = theNodes[i]->getTrialAccel();
      if( acc.Size() != Num_Dof ) {
        std::cerr << "XC::EightNode_Brick_u_p_U::getResistingForceIncInertia matrix and vector sizes are incompatible \n";
        exit(-1);
      }
      for(j=0; j<Num_Dof; j++) {
        a(i*Num_Dof +j) = acc(j);
      }
    }

    this->getMass();
    P.addMatrixVector(1.0, M, a, 1.0);

    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector &vel = theNodes[i]->getTrialVel();
      if( vel.Size() != Num_Dof ) {
        std::cerr << "XC::EightNode_Brick_u_p_U::getResistingForceIncInertia matrix and vector sizes are incompatible \n";
        exit(-1);
      }
      for(j=0; j<Num_Dof; j++) {
        a(i*Num_Dof +j) = vel(j);
      }
    }

    this->getDamp();
    P.addMatrixVector(1.0, C, a, 1.0);

    if(isDead())
      P*=dead_srf;
    return P;
  }

//=============================================================================
int XC::EightNodeBrick_u_p_U::sendSelf(Communicator &comm)
  {
     // Not implemtented yet
     return 0;
  }

//=============================================================================
int XC::EightNodeBrick_u_p_U::recvSelf(const Communicator &comm)
{
     // Not implemtented yet
     return 0;
}

//=============================================================================
XC::Response* XC::EightNodeBrick_u_p_U::setResponse(const std::vector<std::string> &argv, Information &eleInfo)
  {
    if(argv[0] == "force" || argv[0] == "forces")
      return new ElementResponse(this, 1, P);
    else if(argv[0] == "stiff" || argv[0] == "stiffness")
      return new ElementResponse(this, 2, K);
    else if(argv[0] == "mass")
      return new ElementResponse(this, 3, M);
    else if(argv[0] == "damp")
      return new ElementResponse(this, 4, C);
    else if(argv[0] == "material" || argv[0] == "integrPoint")
      {
        const int pointNum = atoi(argv[1]);
        if(pointNum > 0 && pointNum <= Num_TotalGaussPts)
          return setMaterialResponse(physicalProperties[pointNum-1],argv,2,eleInfo);
        else
          return 0;
      }
    else if(argv[0] == "stresses")
      return new ElementResponse(this, 5, Vector(Num_TotalGaussPts*6) );
    else if(argv[0] == "gausspoint" || argv[0] == "GaussPoint")
      return new ElementResponse(this, 6, Vector(Num_TotalGaussPts*Num_Dim) );
    else
     return 0;
  }

//=============================================================================
int XC::EightNodeBrick_u_p_U::getResponse(int responseID, Information &eleInfo)
{
  if(responseID == 1)
    return eleInfo.setVector(getResistingForce());

  else if(responseID == 2)
    return eleInfo.setMatrix(getTangentStiff());

  else if(responseID == 3)
    return eleInfo.setMatrix(getMass());

  else if(responseID == 4)
    return eleInfo.setMatrix(getDamp());

  else if(responseID == 5) {
    static XC::Vector stresses(Num_TotalGaussPts*6);
    stresstensor sigma;
    int cnt = 0;
    int i;
    for(i=0; i<Num_TotalGaussPts; i++)
      {
        sigma = physicalProperties[i]->getStressTensor();
        stresses(cnt++) = sigma(1,1);  //xx
        stresses(cnt++) = sigma(2,2);  //yy
        stresses(cnt++) = sigma(3,3);  //zz
        stresses(cnt++) = sigma(2,3);  //yz
        stresses(cnt++) = sigma(3,1);  //zx
        stresses(cnt++) = sigma(2,3);  //xy
      }
    return eleInfo.setVector(stresses);
  }

  else if(responseID == 6) {
    static XC::Vector Gpts(Num_TotalGaussPts*Num_Dim);
    BJtensor GCoord;
    int cnt = 0;
    int i,j;
    GCoord = getGaussPts();
    for(i=0; i<Num_TotalGaussPts; i++) {
      for(j=0; j<Num_Dim; j++) {
        Gpts(cnt++) = GCoord(i+1,j+1);     //fixed '+1's, ZC 12/01/04
      }
    }
    return eleInfo.setVector(Gpts);
  }

  else
    return (-1);
}

//=============================================================================
void XC::EightNodeBrick_u_p_U::Print(std::ostream &s, int flag) const
  {
    s << "EightNodeBrick_u_p_U, element id:  " << this->getTag() << "\n";
    s << "Connected external nodes:  " << theNodes << "\n";

    s << "Node 1: " << theNodes.getTagNode(0) << "\n";
    s << "Node 2: " << theNodes.getTagNode(1) << "\n";
    s << "Node 3: " << theNodes.getTagNode(2) << "\n";
    s << "Node 4: " << theNodes.getTagNode(3) << "\n";
    s << "Node 5: " << theNodes.getTagNode(4) << "\n";
    s << "Node 6: " << theNodes.getTagNode(5) << "\n";
    s << "Node 7: " << theNodes.getTagNode(6) << "\n";
    s << "Node 8: " << theNodes.getTagNode(7) << "\n";

    s << "Material model:  " << "\n";

    int GP_c_r, GP_c_s, GP_c_t, where;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts ; GP_c_r++ ) {
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts ; GP_c_s++ ) {
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts ; GP_c_t++ ) {
          where = (GP_c_r*Num_IntegrationPts+GP_c_s)*Num_IntegrationPts+GP_c_t;
          s << "\n where = " << where+1 << "\n";
          s << " r= " << GP_c_r << " s= " << GP_c_s << " t= " << GP_c_t << "\n";
          physicalProperties[where]->Print(s);
        }
      }
    }

}

//======================================================================
int XC::EightNodeBrick_u_p_U::update(void)
  {
    int ret = 0;

    double r  = 0.0;
    double s  = 0.0;
    double t  = 0.0;

    std::vector<int> Tdisp_dim({Num_Nodes,Num_Dof});
    BJtensor total_displacements(Tdisp_dim,0.0);
    std::vector<int> tdisp_dim({Num_Nodes,Num_Dim});
    BJtensor total_disp(tdisp_dim,0.0);

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    straintensor eps;

    BJtensor dhGlobal;

    total_displacements = getNodesDisp();
    int i;
    for(i=1; i<=Num_Nodes; i++) {
      total_disp(i,1) = total_displacements(i,1);
      total_disp(i,2) = total_displacements(i,2);
      total_disp(i,3) = total_displacements(i,3);
    }

    int GP_c_r, GP_c_s, GP_c_t, where;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ )
      {
        r = pts[GP_c_r];
        for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ )
          {
            s = pts[GP_c_s];
            for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ )
              {
                t = pts[GP_c_t];
                where = (GP_c_r*Num_IntegrationPts+GP_c_s)*Num_IntegrationPts+GP_c_t;
                dh = shapeFunctionDerivative(r,s,t);
                dhGlobal = dh_Global(dh);
                eps = total_disp("ia") * dhGlobal("ib");
                eps.null_indices();
                eps.symmetrize11();
                if( (physicalProperties[where]->setTrialStrain(eps) ) )
                  std::cerr << "XC::TwentyNodeBrick_u_p_U::update(tag: " << this->getTag() << "), not converged\n";
              }
           }
      }
    return ret;
  }


//======================================================================
 XC::Vector XC::EightNodeBrick_u_p_U::getExForceS ()
{
    Vector PExS(Num_Nodes*Num_Dof);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;
    double det_of_Jacobian = 0.0;

    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim, 0.0);
    BJtensor Pexs(hp_dim, 0.0);

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    BJtensor Jacobian;

    int GP_c_r, GP_c_s, GP_c_t, i, j;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ ) {
          t = pts[GP_c_t];
          tw = wts[GP_c_t];
          hp = shapeFunction(r,s,t);
          dh = shapeFunctionDerivative(r,s,t);
          Jacobian = Jacobian_3D(dh);
          det_of_Jacobian = Jacobian.determinant();
          weight = rw * sw * tw * det_of_Jacobian;
          Pexs += hp *weight;
        }
      }
    }

    for(i=0; i<Num_Nodes; i++) {
      for(j=0; j<Num_Dim; j++) {
        PExS(i*Num_Dof+j) += Pexs(i+1)*bf(j) * ((1.0-poro)*rho_s);
      }
    }

    return PExS;

}

//======================================================================
 XC::Vector XC::EightNodeBrick_u_p_U::getExForceF ()
{
    Vector PExF(Num_Nodes*Num_Dof);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;
    double det_of_Jacobian = 0.0;

    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim, 0.0);
    BJtensor Pexf(hp_dim, 0.0);
    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    BJtensor Jacobian;

    int GP_c_r, GP_c_s, GP_c_t, i, j;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ ) {
          t = pts[GP_c_t];
          tw = wts[GP_c_t];
          hp = shapeFunction(r,s,t);
          dh = shapeFunctionDerivative(r,s,t);
          Jacobian = Jacobian_3D(dh);
          det_of_Jacobian = Jacobian.determinant();
          weight = rw * sw * tw * det_of_Jacobian;
          Pexf += hp *weight;
        }
      }
    }

    for(i=0; i<Num_Nodes; i++) {
      for(j=0; j<Num_Dim; j++) {
        PExF(i*Num_Dof+j+4) += Pexf(i+1)*bf(j) * (poro*rho_f);
      }
    }

    return PExF;
}

//======================================================================
const XC::Matrix &XC::EightNodeBrick_u_p_U::getStiff(int Ki_flag) const
  {
    if(Ki_flag != 0 && Ki_flag != 1)
     {
       std::cerr << "Error XC::EightNodeBrick_u_p_U::getStiff() - illegal use\n";
       exit(-1);
     }

    if(Ki_flag == 0 && Ki != 0)
      return *Ki;

    BJtensor tKep = getStiffnessTensorKep();
    BJtensor tG   = getStiffnessTensorG12();
    BJtensor tP   = getStiffnessTensorP();

    int i, j, m, n;

    //Kep
    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        for( m=0; m<Num_Dim; m++) {
          for( n=0; n<Num_Dim; n++)
            {
              K(i*Num_Dof+m, j*Num_Dof+n) = tKep(i+1, m+1, n+1, j+1);
            }
        }
      }
    }

    //G1 and G1^T, Note *(alpha-poro) here!
    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        for( m=0; m<Num_Dim; m++)
          {
            K(i*Num_Dof+m, j*Num_Dof+3) = -tG(i+1, m+1, j+1) *(alpha-poro);
            K(j*Num_Dof+3, i*Num_Dof+m) = -tG(i+1, m+1, j+1) *(alpha-poro);
          }
      }
    }

    //P
    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        K(i*Num_Dof+3, j*Num_Dof+3) = -tP(i+1, j+1);
      }
    }

    //G2 and G2^T, Note *poro here!
    for( i=0 ; i<Num_Nodes; i++ ) {
      for( j=0; j<Num_Nodes; j++ ) {
        for( m=0; m<Num_Dim; m++)
          {
            K(i*Num_Dof+m+4, j*Num_Dof+3) = -tG(i+1, m+1, j+1) *poro;
            K(j*Num_Dof+3, i*Num_Dof+m+4) = -tG(i+1, m+1, j+1) *poro;
          }
      }
    }

    if( Ki_flag == 1)
      return K;

    Ki = new Matrix(K);

    if(Ki == 0)
      {
        std::cerr << "Error XC::EightNodeBrick_u_p_U::getStiff() -";
        std::cerr << "ran out of memory\n";
        exit(-1);
      }
    return *Ki;
  }

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::getStiffnessTensorKep(void) const
{
    std::vector<int> K_dim({Num_Nodes,Num_Dim,Num_Dim,Num_Nodes});
    BJtensor Kep(K_dim,0.0);
    BJtensor Kkt(K_dim,0.0);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    int where = 0;
    double weight = 0.0;
    double det_of_Jacobian = 0.0;

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    BJtensor Constitutive;

    BJtensor Jacobian;
    BJtensor dhGlobal;

    int GP_c_r, GP_c_s, GP_c_t;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ )
          {
            t = pts[GP_c_t];
            tw = wts[GP_c_t];
            where = (GP_c_r*Num_IntegrationPts+GP_c_s)*Num_IntegrationPts+GP_c_t;
            dh = shapeFunctionDerivative(r,s,t);
            Jacobian = Jacobian_3D(dh);
            det_of_Jacobian = Jacobian.determinant();
            dhGlobal = dh_Global(dh);
            weight = rw * sw * tw * det_of_Jacobian;
            Constitutive = physicalProperties[where]->getTangentTensor();
            Kkt = dhGlobal("kj")*Constitutive("ijml");
            Kkt = Kkt("kiml")*dhGlobal("pl")*weight;
            Kep = Kep + Kkt;
          }
      }
    }

    return Kep;
}

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::getStiffnessTensorG12(void) const
{
    // This is for G1 and G2
    // G1 = (alpha-poro) *G;
    // G2 = poro *G;

    std::vector<int> G_dim({Num_Nodes,Num_Dim,Num_Nodes});
    BJtensor G(G_dim,0.0);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim,0.0);

    double det_of_Jacobian = 0.0;

    BJtensor Jacobian;
    BJtensor dhGlobal;

    int GP_c_r, GP_c_s, GP_c_t;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ )
          {
            t = pts[GP_c_t];
            tw = wts[GP_c_t];
            dh = shapeFunctionDerivative(r,s,t);
            hp= shapeFunction(r,s,t);
            Jacobian = Jacobian_3D(dh);
            dhGlobal = dh_Global(dh);
            det_of_Jacobian = Jacobian.determinant();
            weight = rw * sw * tw * det_of_Jacobian;
            G += dhGlobal("ki")*hp("m") * weight;
          }
      }
    }

    return G;
}

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::getDampTensorC123(void) const
{
    // This is for C1, C2 and C3, C1 = C2 = c3
    // Since solid and fluid shape function the same

    if(perm(1,1)==0.0 || perm(2,2)==0.0 || perm(3,3)==0.0) {
       std::cerr<<" Error, XC::EightNodeBrick_u_p_U::getDampTensorC123 -- permeability (x/y/z) is zero\n";
       exit(-1);
    }

    BJtensor perm_inv = perm.inverse();

    std::vector<int> C_dim({Num_Nodes,Num_Dim,Num_Dim,Num_Nodes});
    BJtensor C123(C_dim,0.0);
    std::vector<int> c_dim({Num_Nodes,Num_Dim,Num_Dim});
    BJtensor c123(c_dim,0.0);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;
    double det_of_Jacobian = 0.0;

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim,0.0);

    BJtensor Jacobian;

    int GP_c_r, GP_c_s, GP_c_t;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ ) {
          t = pts[GP_c_t];
          tw = wts[GP_c_t];
          hp = shapeFunction(r,s,t);
          dh = shapeFunctionDerivative(r,s,t);
          Jacobian = Jacobian_3D(dh);
          det_of_Jacobian = Jacobian.determinant();
          weight = rw * sw * tw * det_of_Jacobian;
          c123 = hp("k")*perm_inv("ij");
          C123 += c123("kij")*hp("m") *weight;
          }
       }
    }

    return C123;
}

//======================================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::getMassTensorMsf(void) const
{
    // This is for Ms and Mf -> M_kl
    // Ms = Msf * (1.0-poro)*rho_s
    // Mf = Msf * poro*rho_f

    std::vector<int> M_dim({Num_Nodes,Num_Nodes});
    BJtensor Msf(M_dim,0.0);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;
    double det_of_Jacobian = 0.0;

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);
    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim,0.0);

    BJtensor Jacobian;

    int GP_c_r, GP_c_s, GP_c_t;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ ) {
          t = pts[GP_c_t];
          tw = wts[GP_c_t];
          hp = shapeFunction(r,s,t);
          dh = shapeFunctionDerivative(r,s,t);
          Jacobian = Jacobian_3D(dh);
          det_of_Jacobian = Jacobian.determinant();
          weight = rw * sw * tw * det_of_Jacobian;
          Msf += hp("m")*hp("n")*weight;
          }
       }
    }

    return Msf;
}

//======================================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::getStiffnessTensorP(void) const
{
    if(ks == 0.0 || kf == 0.0) {
       std::cerr<<" Error, XC::EightNodeBrick_u_p_U::getStiffnessTensorP -- solid and/or fluid bulk modulus is zero\n";
       exit(-1);
    }
    double  oneOverQ = poro/kf + (alpha-poro)/ks;

    std::vector<int> Pp_dim({Num_Nodes,Num_Nodes});
    BJtensor Pp(Pp_dim,0.0);

    double r  = 0.0;
    double rw = 0.0;
    double s  = 0.0;
    double sw = 0.0;
    double t  = 0.0;
    double tw = 0.0;
    double weight = 0.0;

    std::vector<int> dh_dim({Num_Nodes,Num_Dim});
    BJtensor dh(dh_dim, 0.0);

    std::vector<int> hp_dim({Num_Nodes});
    BJtensor hp(hp_dim,0.0);

    double det_of_Jacobian = 0.0;

    BJtensor Jacobian;

    int GP_c_r, GP_c_s, GP_c_t;

    for( GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ ) {
      r = pts[GP_c_r];
      rw = wts[GP_c_r];
      for( GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ ) {
        s = pts[GP_c_s];
        sw = wts[GP_c_s];
        for( GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ ) {
          t = pts[GP_c_t];
          tw = wts[GP_c_t];
          dh = shapeFunctionDerivative(r,s,t);
          hp= shapeFunction(r,s,t);
          Jacobian = Jacobian_3D(dh);
          det_of_Jacobian = Jacobian.determinant();
          weight = rw * sw * tw * det_of_Jacobian;
          Pp += hp("m")*hp("n") * weight;
        }
      }
    }

    return Pp * oneOverQ;
}

//======================================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::Jacobian_3D(const BJtensor &dh) const
  {
     BJtensor N_C = getNodesCrds();
     BJtensor J3D = N_C("ki") * dh("kj");
     J3D.null_indices();
     return J3D;
  }

//======================================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::Jacobian_3Dinv(const BJtensor &dh) const
  { return Jacobian_3D(dh).inverse(); }

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::dh_Global(const BJtensor &dh) const
{
     BJtensor  JacobianINV0 = Jacobian_3Dinv(dh);
     BJtensor  dhGlobal_0 = dh("ik") * JacobianINV0("kj");
       dhGlobal_0.null_indices();
     return dhGlobal_0;
}

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::getNodesCrds(void) const
  {
    int i,j;
    std::vector<int> dimX({Num_Nodes,Num_Dim});
    BJtensor N_coord(dimX, 0.0);

    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector&TNodesCrds = theNodes[i]->getCrds();
      for(j=0; j<Num_Dim; j++) {
        N_coord(i+1,j+1) = TNodesCrds(j);
      }
    }

    return N_coord;

  }

//======================================================================
 XC::BJtensor XC::EightNodeBrick_u_p_U::getNodesDisp(void) const
  {
    int i,j;
    std::vector<int> dimU({Num_Nodes,Num_Dof});
    BJtensor total_disp(dimU, 0.0);

    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector&TNodesDisp = theNodes[i]->getTrialDisp();
      for(j=0; j<Num_Dof; j++) {
        total_disp(i+1,j+1) = TNodesDisp(j);
      }
    }

    return total_disp;
  }

//======================================================================
double XC::EightNodeBrick_u_p_U::getPorePressure(double x1, double x2, double x3)
{
    double pp = 0.0;
    int i;

    for(i=0; i<Num_Nodes; i++) {
      const XC::Vector& T_disp = theNodes[i]->getTrialDisp();
      pp += shapeFunction(x1,x2,x3)(i+1) * T_disp(3);
    }

    return pp;
}

//======================================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::shapeFunction(double r1, double r2, double r3) const
  {
    std::vector<int> Hfun({Num_Nodes});
    BJtensor h(Hfun, 0.0);

    h(8)=(1.0+r1)*(1.0-r2)*(1.0-r3)*0.125;
    h(7)=(1.0-r1)*(1.0-r2)*(1.0-r3)*0.125;
    h(6)=(1.0-r1)*(1.0+r2)*(1.0-r3)*0.125;
    h(5)=(1.0+r1)*(1.0+r2)*(1.0-r3)*0.125;
    h(4)=(1.0+r1)*(1.0-r2)*(1.0+r3)*0.125;
    h(3)=(1.0-r1)*(1.0-r2)*(1.0+r3)*0.125;
    h(2)=(1.0-r1)*(1.0+r2)*(1.0+r3)*0.125;
    h(1)=(1.0+r1)*(1.0+r2)*(1.0+r3)*0.125;

    return h;
  }


//==============================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::shapeFunctionDerivative(double r1, double r2, double r3) const
  {
    std::vector<int> DHfun({Num_Nodes,Num_Dim});
    BJtensor dh(DHfun, 0.0);

      //  node number 8
    dh(8,1)= (1.0-r2)*(1.0-r3)*0.125;
    dh(8,2)=-(1.0+r1)*(1.0-r3)*0.125;
    dh(8,3)=-(1.0+r1)*(1.0-r2)*0.125;
      //  node number 7
    dh(7,1)=-(1.0-r2)*(1.0-r3)*0.125;
    dh(7,2)=-(1.0-r1)*(1.0-r3)*0.125;
    dh(7,3)=-(1.0-r1)*(1.0-r2)*0.125;
      //  node number 6
    dh(6,1)=-(1.0+r2)*(1.0-r3)*0.125;
    dh(6,2)= (1.0-r1)*(1.0-r3)*0.125;
    dh(6,3)=-(1.0-r1)*(1.0+r2)*0.125;
      //  node number 5
    dh(5,1)= (1.0+r2)*(1.0-r3)*0.125;
    dh(5,2)= (1.0+r1)*(1.0-r3)*0.125;
    dh(5,3)=-(1.0+r1)*(1.0+r2)*0.125;
      //  node number 4
    dh(4,1)= (1.0-r2)*(1.0+r3)*0.125;
    dh(4,2)=-(1.0+r1)*(1.0+r3)*0.125;
    dh(4,3)= (1.0+r1)*(1.0-r2)*0.125;
      //  node number 3
    dh(3,1)=-(1.0-r2)*(1.0+r3)*0.125;
    dh(3,2)=-(1.0-r1)*(1.0+r3)*0.125;
    dh(3,3)= (1.0-r1)*(1.0-r2)*0.125;
      //  node number 2
    dh(2,1)=-(1.0+r2)*(1.0+r3)*0.125;
    dh(2,2)= (1.0-r1)*(1.0+r3)*0.125;
    dh(2,3)= (1.0-r1)*(1.0+r2)*0.125;
      //  node number 1
    dh(1,1)= (1.0+r2)*(1.0+r3)*0.125;
    dh(1,2)= (1.0+r1)*(1.0+r3)*0.125;
    dh(1,3)= (1.0+r1)*(1.0+r2)*0.125;

    return dh;
  }

//==============================================================
XC::BJtensor XC::EightNodeBrick_u_p_U::getGaussPts(void)
  {
    std::vector<int> dimensions1({Num_TotalGaussPts,Num_Dim});
    BJtensor Gs(dimensions1, 0.0);
    std::vector<int> dimensions2({Num_Nodes});
    BJtensor shp(dimensions2, 0.0);

    double r = 0.0;
    double s = 0.0;
    double t = 0.0;
    int i, j, where;


    for(int GP_c_r = 0 ; GP_c_r < Num_IntegrationPts; GP_c_r++ )
      {
	r = pts[GP_c_r];
	for(int GP_c_s = 0 ; GP_c_s < Num_IntegrationPts; GP_c_s++ )
	  {
	    s = pts[GP_c_s];
	    for(int GP_c_t = 0 ; GP_c_t < Num_IntegrationPts; GP_c_t++ )
	      {
		t = pts[GP_c_t];
		where = (GP_c_r*Num_IntegrationPts+GP_c_s)*Num_IntegrationPts+GP_c_t;
		shp = shapeFunction(r,s,t);
		for(i=0; i<Num_Nodes; i++)
		  {
		    const Vector& T_Crds = theNodes[i]->getCrds();
		    for(j=0; j<Num_Dim; j++)
		      { Gs(where+1, j+1) += shp(i+1) * T_Crds(j); }
		  }
	      }
	  }
      }
    return Gs;
  }


#endif



