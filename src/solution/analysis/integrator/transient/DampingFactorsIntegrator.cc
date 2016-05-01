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
//DampingFactors.cpp

#include "DampingFactorsIntegrator.h"


//! @brief Constructor.
XC::DampingFactorsIntegrator::DampingFactorsIntegrator(SoluMethod *owr,int classTag)
  : TransientIntegrator(owr,classTag), rayFactors() {}

//! @brief Constructor.
XC::DampingFactorsIntegrator::DampingFactorsIntegrator(SoluMethod *owr,int classTag,const RayleighDampingFactors &rF)
  : TransientIntegrator(owr,classTag), rayFactors(rF) {}

void XC::DampingFactorsIntegrator::setRayleighDampingFactors(void)
  {
    // if damping factors exist set them in the ele & node of the domain
    if(!rayFactors.Nulos())
      Integrator::setRayleighDampingFactors(rayFactors);
  }

void XC::DampingFactorsIntegrator::Print(std::ostream &s, int flag)
  {
    TransientIntegrator::Print(s,flag);
    s << "  Rayleigh Damping: " << rayFactors << std::endl;
  }

//! @brief Envía los miembros del objeto a través del canal que se pasa como parámetro.
int XC::DampingFactorsIntegrator::sendData(CommParameters &cp)
  {
    int res= TransientIntegrator::sendData(cp);
    res+= cp.sendMovable(rayFactors,getDbTagData(),CommMetaData(2));
    return res;
  }

//! @brief Recibe los miembros del objeto a través del canal que se pasa como parámetro.
int XC::DampingFactorsIntegrator::recvData(const CommParameters &cp)
  {
    int res= TransientIntegrator::recvData(cp);
    res+= cp.receiveMovable(rayFactors,getDbTagData(),CommMetaData(2));
    return res;
  }
