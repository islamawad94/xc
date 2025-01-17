# ----------------------------------------------------------------------------
#   XC program; finite element analysis code
#   for structural analysis and design.
# 
#   Copyright (C)  Luis C. Pérez Tato
# 
#   Except for the restrictions that may arise from the copyright
#   of the original program (see copyright below if any)
#   XC is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or 
#   (at your option) any later version.
# 
#   This software is distributed in the hope that it will be useful, but 
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details. 
# 
# 
#  You should have received a copy of the GNU General Public License 
#  along with this program.
#  If not, see <http:// www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
MESSAGE(STATUS "************* find packages begins ****************")
find_package(X11 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(VTK REQUIRED)
find_package(GTK2 REQUIRED)
find_package(CGAL REQUIRED COMPONENTS Qt5 Core)
find_package(GNUGTS REQUIRED)
find_package(CImg REQUIRED)
find_package(MySQL REQUIRED)
find_package(GLIB2 REQUIRED)
find_package(Python COMPONENTS Interpreter Development)
find_package(Boost 1.62 REQUIRED)
if(Boost_FOUND)
  INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
  SET(Boost_USE_STATIC_LIBS OFF)
  SET(Boost_USE_MULTITHREADED ON)
  SET(Boost_USE_STATIC_RUNTIME OFF)
  SET(Boost_DETAILED_FAILURE_MSG ON)
  if (PYTHON_VERSION_MAJOR EQUAL 3)
     find_package(Boost COMPONENTS python${PYTHON_VERSION_SUFFIX})
     find_package(PythonInterp 3)
     find_package(PythonLibs 3 REQUIRED)
  else()
     find_package(Boost COMPONENTS python)
     find_package(PythonInterp)
     find_package(PythonLibs REQUIRED)
  endif()
  set(XC_UTILS_BOOST_PYTHON_LIBRARIES ${Boost_LIBRARIES})
  find_package(Boost COMPONENTS system regex filesystem thread math_c99 math_c99f math_c99l math_tr1 math_tr1f math_tr1l REQUIRED)
elseif(NOT Boost_FOUND)
  MESSAGE(FATAL_ERROR "Unable to find correct Boost version. Did you set BOOST_ROOT?")
endif()
message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
#MESSAGE(STATUS "boost libraries: " ${Boost_LIBRARIES})
find_package(F2C REQUIRED)
find_package(ExecInfo)
find_package(Plot REQUIRED)
find_package(Gnuplot REQUIRED)
find_package(MPFR)
find_package(GMP)
find_package(SQLITE3 REQUIRED)
find_package(MPI REQUIRED)
find_package(Arpack REQUIRED)
find_package(ArpackPP REQUIRED)
find_package(Umfpack REQUIRED)
find_package(MUMPS REQUIRED)
find_package(Petsc)
find_package(LAPACK REQUIRED)
find_package(BLAS REQUIRED)
find_package(SuperLU REQUIRED)
find_package(BerkeleyDB REQUIRED)
find_package(METIS REQUIRED)
find_package(TCL REQUIRED)
find_package(ORACLE)
find_package(OpenMP REQUIRED)
find_package(GMSH 4.8 REQUIRED)
find_package(SuiteSparse REQUIRED)
MESSAGE(STATUS "************* find packages ends ****************")
