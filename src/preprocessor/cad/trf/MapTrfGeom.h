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
//MapTrfGeom.h

#ifndef MAPTrfGeom_H
#define MAPTrfGeom_H

#include "preprocessor/cad/MapCadMember.h"
#include "TrfGeom.h"
#include "boost/lexical_cast.hpp"


namespace XC {

//! @ingroup Cad
//
//! @brief Contenedor de puntos del modelo.
class MapTrfGeom: public MapCadMember<TrfGeom>
  {
  protected:


  public:
    MapTrfGeom(Cad *cad= NULL);

    template <class T>
    TrfGeom *Nueva(void);
    TrfGeom *newTransformation(const std::string &type);


  };

//! @brief Crea una nueva transformación geométrica.
template <class T>
XC::TrfGeom *XC::MapTrfGeom::Nueva(void)
  {
    TrfGeom *retval= busca(getTag());
    if(!retval) //La transformación es nueva.
      {
        Preprocessor *preprocessor= getPreprocessor();
        retval= new T(preprocessor);
        if(retval)
          {
            retval->Nombre()= "t"+boost::lexical_cast<std::string>(getTag());
            (*this)[getTag()]= retval;
            tag++;
	  }
      }
    return retval;
  }

} //end of XC namespace
#endif
