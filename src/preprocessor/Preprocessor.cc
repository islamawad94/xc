//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
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
//Preprocessor.cc

#include "Preprocessor.h"
#include "FEProblem.h"
#include "domain/domain/Domain.h"
#include "domain/mesh/node/Node.h"
#include "domain/mesh/element/Element.h"
#include "preprocessor/set_mgmt/SetEstruct.h"
#include "preprocessor/set_mgmt/Set.h"
#include "preprocessor/multi_block_topology/matrices/ElemPtrArray3d.h"
#include "boost/lexical_cast.hpp"


#include "utility/matrix/ID.h"

//! @brief Default constructor.
XC::Preprocessor::Preprocessor(CommandEntity *owr,DataOutputHandler::map_output_handlers *oh)
  : CommandEntity(owr), MovableObject(0), domain(nullptr), materialHandler(this), transf(this), beamIntegrators(this), 
    nodes(this), elements(this), loads(this), constraints(this),
    mbt(this),sets(this)
  { domain= new Domain(this,oh); }

//! @brief Copy constructor (prohibited).
XC::Preprocessor::Preprocessor(const Preprocessor &other)
  : CommandEntity(other), MovableObject(other), domain(nullptr), materialHandler(this), transf(this), beamIntegrators(this),
    nodes(this), elements(this), loads(this), constraints(this),
    mbt(this),sets(this)
  {
    std::cerr << getClassName() << "::" << __FUNCTION__
	      << "; this object must no be copied." << std::endl;
  }

//! @brief Assignment operator (prohibited).
XC::Preprocessor &XC::Preprocessor::operator=(const Preprocessor &other)
  {
    std::cerr << getClassName() << "::" << __FUNCTION__
	      << "; can't assign a preprocessor object." << std::endl;
    return *this;
  }

//! @brief Insert the pointer to the node in the "total" set and in the 
//! sets that are currently opened.
void XC::Preprocessor::updateSets(Node *new_node)
  {
    sets.get_set_total()->addNode(new_node);
    MapSet::map_sets &open_sets= sets.get_open_sets();
    for(MapSet::map_sets::iterator i= open_sets.begin();i!= open_sets.end();i++)
      {
        Set *ptr_set= dynamic_cast<Set *>((*i).second);
        assert(ptr_set);
        ptr_set->addNode(new_node);
      }
  }

//! @brief Insert the pointer to the element in the "total" set and in the 
//! sets that are currently opened.
void XC::Preprocessor::updateSets(Element *new_elem)
  {
    sets.get_set_total()->addElement(new_elem);
    MapSet::map_sets &open_sets= sets.get_open_sets();
    for(MapSet::map_sets::iterator i= open_sets.begin();i!= open_sets.end();i++)
      {
        Set *ptr_set= dynamic_cast<Set *>((*i).second);
        assert(ptr_set);
        ptr_set->addElement(new_elem);
      }
  }

//! @brief Insert the pointer to the constraint in the "total" set and in the 
//! sets that are currently opened.
void XC::Preprocessor::updateSets(Constraint *new_constraint)
  {
    sets.get_set_total()->GetConstraints().push_back(new_constraint);
    MapSet::map_sets &open_sets= sets.get_open_sets();
    for(MapSet::map_sets::iterator i= open_sets.begin();i!= open_sets.end();i++)
      {
        Set *ptr_set= dynamic_cast<Set *>((*i).second);
        assert(ptr_set);
        ptr_set->GetConstraints().push_back(new_constraint);
      }
  }

//! @brief Destructor.
XC::Preprocessor::~Preprocessor(void)
  {
    mbt.clearAll();
    if(domain) delete domain;
    domain= nullptr;
  }

//! @brief Return a pointer to the problem that owns this preprocessor.
XC::FEProblem *XC::Preprocessor::getProblem(void)
  {
    FEProblem *retval= dynamic_cast<FEProblem *>(Owner());
    return retval;
  }

//! @brief Return a const pointer to the problem that owns this preprocessor.
const XC::FEProblem *XC::Preprocessor::getProblem(void) const
  {
    Preprocessor *this_no_const= const_cast<Preprocessor *>(this);
    return this_no_const->getProblem(); 
  }

//! @brief Assign Stress Reduction Factor for element deactivation.
void XC::Preprocessor::setDeadSRF(const double &d)
  { Element::setDeadSRF(d); }

//! @brief Return a pointer to the set or geometric entity with
//! the name being passed as a parameter.
XC::SetEstruct *XC::Preprocessor::find_struct_set(const std::string &nmb)
  {
    SetEstruct *retval= sets.find_struct_set(nmb);
    if(!retval)
      retval= mbt.find_struct_set(boost::lexical_cast<size_t>(nmb));
    return retval;
  }

//! @brief Domain setup to solve for a new load pattern.
void XC::Preprocessor::resetLoadCase(void)
  { 
    getLoadHandler().removeAllFromDomain();
    if(domain)
      domain->resetLoadCase();
    else
      std::cerr << getClassName() << "::" << __FUNCTION__
		<< "; domain not defined (null ptr)."
                << std::endl;
  }


//! @brief Delete all preprocessor entities.
void XC::Preprocessor::clearAll(void)
  {
    sets.reset();
    mbt.clearAll();
    transf.clearAll();
    beamIntegrators.clearAll();
    nodes.clearAll();
    elements.clearAll();
    if(domain)
      domain->clearAll();
    loads.clearAll();
    constraints.clearAll();
    materialHandler.clearAll();
  }

//! @brief Return a pointer to the database.
XC::FE_Datastore *XC::Preprocessor::getDataBase(void)
  {
    FE_Datastore *retval= nullptr;
    FEProblem *prb= getProblem();
    if(prb)
      retval= prb->getDataBase();
    return retval;
  }

//! @brief Return a vector to store the dbTags
//! of the class members
XC::DbTagData &XC::Preprocessor::getDbTagData(void) const
  {
    static DbTagData retval(10);
    return retval;
  }

//! @brief Send data through the communicator argument.
int XC::Preprocessor::sendData(Communicator &comm)
  {
    //res+= comm.sendMovable(materialHandler,getDbTagData(),CommMetaData(0));
    //res+= comm.sendMovable(transf,getDbTagData(),CommMetaData(1));
    //res+= comm.sendMovable(beamIntegrators,getDbTagData(),CommMetaData(2));
    //res+= comm.sendMovable(nodes,getDbTagData(),CommMetaData(3));
    //res+= comm.sendMovable(elements,getDbTagData(),CommMetaData(4));
    int res= comm.sendMovable(loads,getDbTagData(),CommMetaData(5));
    //res+= comm.sendMovable(constraints,getDbTagData(),CommMetaData(6));
    res+= comm.sendMovable(mbt,getDbTagData(),CommMetaData(7));
    assert(domain);
    res+= sendDomain(*domain,8,getDbTagData(),comm);
    res+= comm.sendMovable(sets,getDbTagData(),CommMetaData(9));
    return res;
  }

//! @brief Receive data through the communicator argument.
int XC::Preprocessor::recvData(const Communicator &comm)
  {
    //res+= comm.receiveMovable(materialHandler,getDbTagData(),CommMetaData(0));
    //res+= comm.receiveMovable(transf,getDbTagData(),CommMetaData(1));
    //res+= comm.receiveMovable(beamIntegrators,getDbTagData(),CommMetaData(2));
    //res+= comm.receiveMovable(nodes,getDbTagData(),CommMetaData(3));
    //res+= comm.receiveMovable(elements,getDbTagData(),CommMetaData(4));
    int res= comm.receiveMovable(loads,getDbTagData(),CommMetaData(5));
    //res+= comm.receiveMovable(constraints,getDbTagData(),CommMetaData(6));
    res+= comm.receiveMovable(mbt,getDbTagData(),CommMetaData(7));
    assert(domain);
    res+= receiveDomain(*domain,8,getDbTagData(),comm);
    res+= comm.receiveMovable(sets,getDbTagData(),CommMetaData(9));
    return res;
  }

//! @brief Send object through the communicator argument.
int XC::Preprocessor::sendSelf(Communicator &comm)
  {
    setDbTag(comm);
    const int dataTag= getDbTag();
    inicComm(10);
    int res= sendData(comm);

    res+= comm.sendIdData(getDbTagData(),dataTag);
    if(res < 0)
      std::cerr << getClassName() << "::" << __FUNCTION__
		<< "; failed to send data\n";
    return res;
  }

//! @brief Receive object through the communicator argument.
int XC::Preprocessor::recvSelf(const Communicator &comm)
  {
    inicComm(10);
    const int dataTag= getDbTag();
    int res= comm.receiveIdData(getDbTagData(),dataTag);

    if(res<0)
      std::cerr << getClassName() << "::" << __FUNCTION__
		<< "; failed to receive ids.\n";
    else
      {
        //setTag(getDbTagDataPos(0));
        res+= recvData(comm);
        if(res<0)
          std::cerr << getClassName() << "::" << __FUNCTION__
		    << "; failed to receive data.\n";
      }
    return res;
  }

