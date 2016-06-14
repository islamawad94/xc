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

#include "ElementEdge.h"
#include "Element.h"
#include "domain/mesh/node/Node.h"
#include <iostream>
#include "domain/mesh/MeshEdge.h"

//! @brief Constructor.
XC::ElementEdge::ElementEdge(Element *eptr,const int &i)
  :elem(eptr),iedge(i) {}

//! @brief Returns a pointer to the element that "owns" the edge.
const XC::Element *XC::ElementEdge::getElementPtr(void) const
  { return elem; }

//! @brief Returns the index of the edge in its owner element.
const int &XC::ElementEdge::getEdgeIndex(void) const
  { return iedge; }

//! @brief Get the the element indexes of the edge nodes. 
XC::ID XC::ElementEdge::getLocalIndexNodes(void) const
  { return elem->getLocalIndexNodesEdge(iedge); }

//! @brief Returns the edge nodes. 
XC::ElementEdge::NodesEdge XC::ElementEdge::getNodes(void) const
  { return elem->getNodesEdge(iedge); }

//! @brief Returns the corresponding mesh edge. 
XC::MeshEdge XC::ElementEdge::getMeshEdge(void) const
  { return MeshEdge(getNodes()); }

