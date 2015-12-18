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
///////////////////////////////////////////////////////////////////////////////
//
// COPYRIGHT (C):     :-))
// PROJECT:           Object Oriented Finite Element Program
// FILE:             EightNodeBrick_u_p_U.h
// CLASS:            EightNodeBrick_u_p_U
// MEMBER FUNCTIONS:
//
// MEMBER VARIABLES
//
// PURPOSE:           Finite Element Class for coupled system
//  "Coupled system": Solid and fluid coexist.
//                    u-- Solid displacement
//                    p-- Pore pressure
//                    U-- Absolute fluid displacement
// RETURN:
// VERSION:
// LANGUAGE:          C++.ver >= 3.0
// TARGET OS:         DOS || UNIX || . . .
// DESIGNER:          Boris Jeremic, Xiaoyan Wu, Chao Cheng (main for last revision)
// PROGRAMMER:        Boris Jeremic, Xiaoyan Wu, Zhaohui Yang, Zhao Cheng (main for last revision)
// DATE:              Sept. 2001
// UPDATE HISTORY:    Modified from EightNodeBrick.h.  Reorganized a lot by Xiaoyan
//                    01/24/2002    Xiaoyan
//                    Add the permeability tensor and ks, kf  to the constructor  Xiaoyan
//
//
//
//                    Clean-up and re-write by Zhao Cheng, 10/20/2004
//
//
///////////////////////////////////////////////////////////////////////////////


#ifndef EIGHTNODEBRICK_U_P_U_H
#define EIGHTNODEBRICK_U_P_U_H

#include <domain/mesh/element/volumen/BrickBase.h>
#include "domain/mesh/element/body_forces/BodyForces3D.h"

namespace XC {
  class BJtensor;
  class NDMaterial;

//! \ingroup ElemVol
//
//! @brief Hexaedro de ocho nodos.
class EightNodeBrick_u_p_U: public BrickBase
  {
  private:
    static Matrix K; //!< Stiffness
    static Matrix C; //!< Damping
    static Matrix M; //!< Mass
    static Vector P; //!< Residual

    static const int  Num_IntegrationPts;
    static const int  Num_TotalGaussPts;
    static const int  Num_Nodes;
    static const int  Num_Dim;
    static const int  Num_Dof;
    static const int  Num_ElemDof;
    static const double pts[2]; //!< Stores quadrature points
    static const double wts[2]; //!< Stores quadrature weights
    static BJtensor perm; //!< Permeability = k/(rho_f*g)

    BodyForces3D bf; //!< Body forces
    double poro; //!< Porosity
    double alpha; //!< Coefficient for soil (approximate equal 1)
    double rho_s; //!< Solid density
    double rho_f; //!< Fluid density
    double ks; //!< Bulk modulus of solid
    double kf; //!< Bulk modulus of fluid
    double pressure; //!< Normal surface traction (pressure) over entire element  //?

    Vector *eleQ;
    mutable Matrix *Ki;
  public:
    EightNodeBrick_u_p_U(int element_number,
                   int node_numb_1, int node_numb_2, int node_numb_3, int node_numb_4,
                   int node_numb_5, int node_numb_6, int node_numb_7, int node_numb_8,
                   NDMaterial *Globalmmodel,  const BodyForces3D &,
                   double nn, double alf, double rs,double rf,
                   double permb_x, double permb_y, double permb_z,
                   double kks, double kkf, double pp);
    EightNodeBrick_u_p_U(void);
    Element *getCopy(void) const;
    ~EightNodeBrick_u_p_U(void);
    // public methods to obtain information about dof & connectivity
    int getNumDOF(void) const;
    void setDomain(Domain *theDomain);

    // public methods to set the state of the element    
    int update(void);

    // public methods to obtain stiffness, mass, damping and residual information
    const Matrix &getTangentStiff(void) const;
    const Matrix &getInitialStiff(void) const;
    const Matrix &getDamp(void) const;
    const Matrix &getMass(void) const;

    void zeroLoad(void);
    int addLoad(ElementalLoad *theLoad, double loadFactor);
    int addInertiaLoadToUnbalance(const Vector &accel);
    const Vector &getResistingForce(void) const;
    const Vector &getResistingForceIncInertia(void) const;

    int sendSelf(CommParameters &);
    int recvSelf(const CommParameters &);

    void Print(std::ostream &s, int flag =0);

    Response *setResponse(const std::vector<std::string> &argv, Information &eleInfo);
    int getResponse(int responseID, Information &eleInformation);

    //int setParameter(const std::vector<std::string> &argv, Parameter &param);
    //int updateParameter (int parameterID, Information &info);

  private:
    BJtensor shapeFunction(double, double, double) const;
    BJtensor shapeFunctionDerivative(double, double, double) const;
    BJtensor getGaussPts(void);
    BJtensor getNodesCrds(void) const;
    BJtensor getNodesDisp(void) const;
    BJtensor Jacobian_3D(BJtensor dh) const;
    BJtensor Jacobian_3Dinv(BJtensor dh) const;
    BJtensor dh_Global(BJtensor dh) const;

    BJtensor getStiffnessTensorKep() const;
    BJtensor getStiffnessTensorG12() const;
    BJtensor getStiffnessTensorP() const;
    BJtensor getMassTensorMsf() const;
    BJtensor getDampTensorC123(void) const;
    const Matrix &getStiff(int Ki_flag) const;
    double getPorePressure(double, double, double);
    Vector getExForceS();
    Vector getExForceF();
  };
} // end of XC namespace


#endif

