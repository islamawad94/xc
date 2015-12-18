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
** ****************************************************************** */

// $Revision: 1.4 $
// $Date: 2003/02/14 23:01:25 $
// $Source: /usr/local/cvs/OpenSees/SRC/material/nD/J2Plasticity.h,v $

#ifndef J2Plasticity_h
#define J2Plasticity_h

// Written: Ed "C++" Love
//
// J2 isotropic hardening material class
//
//  Elastic Model
//  sigma = K*trace(epsilion_elastic) + (2*G)*dev(epsilon_elastic)
//
//  Yield Function
//  phi(sigma,q) = || dev(sigma) ||  - sqrt(2/3)*q(xi)
//
//  Saturation Isotropic Hardening with linear term
//  q(xi) = simga_0 + (sigma_infty - sigma_0)*exp(-delta*xi) + H*xi
//
//  Flow Rules
//  \dot{epsilon_p} =  gamma * d_phi/d_sigma
//  \dot{xi}        = -gamma * d_phi/d_q
//
//  Linear Viscosity
//  gamma = phi / eta  ( if phi > 0 )
//
//  Backward Euler Integration Routine
//  Yield condition enforced at time n+1
//
//  set eta := 0 for rate independent case
//


#include <utility/matrix/Vector.h>
#include <utility/matrix/Matrix.h>
#include <material/nD/NDMaterial.h>


namespace XC{

//! @ingroup NDMat
//
//
//! @defgroup J2NDMat J2 Isotropic hardening materials.
//
//! @ingroup J2NDMat
//
//! @brief J2 Isotropic hardening material class.
class J2Plasticity: public NDMaterial
  {
  protected :
    //this is mike's problem
    static Tensor rank2;
    static Tensor rank4;

    //material parameters
    double bulk; //!< bulk modulus
    double shear; //!< shear modulus
    double sigma_0; //!< initial yield stress
    double sigma_infty; //!< final saturation yield stress
    double delta; //!< exponential hardening parameter
    double Hard; //!< linear hardening parameter
    double eta; //!< viscosity

    //internal variables
    Matrix epsilon_p_n; //!< plastic strain time n
    Matrix epsilon_p_nplus1; //!< plastic strain time n+1
    double xi_n; //!< xi time n
    double xi_nplus1; //!< xi time n+1

    //material response
    Matrix stress; //!< stress tensor
    double tangent[3][3][3][3]; //!< material tangent
    static double initialTangent[3][3][3][3]; //!< material tangent
    static double IIdev[3][3][3][3]; //!< rank 4 deviatoric
    static double IbunI[3][3][3][3]; //!< rank 4 I bun I

    //material input
    Matrix strain; //!< strain tensor

    //parameters
    static const double one3;
    static const double two3;
    static const double four3;
    static const double root23;


    void zero( );//zero internal variables
    void plastic_integrator( );//plasticity integration routine
    void doInitialTangent(void) const;

    double q( double xi );//hardening function
    double qprime( double xi );//hardening function derivative

    //matrix index to tensor index mapping
    virtual void index_map( int matrix_index, int &i, int &j ) const;

    int sendData(CommParameters &);
    int recvData(const CommParameters &);
  public:
    //null constructor
    J2Plasticity();
    //full constructor
    J2Plasticity(int tag, int classTag,
                     double K,
                     double G,
                     double yield0,
                     double yield_infty,
                     double d,
                     double H,
                     double viscosity = 0 );
    J2Plasticity(int tag, int classTag);
    //elastic constructor
    J2Plasticity( int tag, int classTag, double K, double G );

    virtual NDMaterial* getCopy(const std::string &) const;

    //swap history variables
    virtual int commitState(void);
    //revert to last saved state
    virtual int revertToLastCommit(void);
    //revert to start
    virtual int revertToStart(void);

    //sending and receiving
    virtual int sendSelf(CommParameters &);
    virtual int recvSelf(const CommParameters &);

    //print out material data
    void Print(std::ostream &s, int flag = 0);

    virtual NDMaterial *getCopy(void) const;
    virtual const std::string &getType(void) const;
    virtual int getOrder(void) const;
  };

} //end of XC namespace

#endif
