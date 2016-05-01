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
//DiscretBase.h

#ifndef DiscretBase_h 
#define DiscretBase_h 


#include "xc_utils/src/nucleo/EntConNmb.h"

namespace XC {
  class Material;

//! @ingroup MATSCC
//
//! @defgroup MATSCCRepres Representación de una sección.
//
//! @ingroup MATSCCRepres
//!
//! @brief Base para los objetos empleados para discretizar la sección.
class DiscretBase: public EntConNmb
  {
  private:
    Material *mat; //!< Puntero al material que constituye el elemento de la discretización.
  protected:

  public:
    DiscretBase(Material *mat);

    virtual double getMaxY(void) const= 0;
    virtual double getMaxZ(void) const= 0;
    virtual double getMinY(void) const= 0;
    virtual double getMinZ(void) const= 0;

    void setMaterialPtr(Material *mat);
    Material *getMaterialPtr(void) const;

  };
} // end of XC namespace


#endif

