/* pltsvv.f -- translated by f2c (version 20160102).
   You must link the resulting object file with libf2c:
	on Microsoft Windows system, link with libf2c.lib;
	on Linux or Unix systems, link with .../path/to/libf2c.a -lm
	or, if you install libf2c.a in a standard place, with -lf2c -lm
	-- in that order, at the end of the command line, as in
		cc *.o -lf2c -lm
	Source for libf2c is in /netlib/f2c/libf2c.zip, e.g.,

		http://www.netlib.org/f2c/libf2c.zip
*/

#ifdef __cplusplus
extern "C" {
#endif
#include "paving.h"

/* Common Block Declarations */

struct {
    xc_float devcap[23], defout[7];
} status_;

#define status_1 status_

struct {
    xc_float devp[5];
} device_;

#define device_1 device_

struct {
    xc_float colp[3], palett[48]	/* was [3][16] */;
} color_;

#define color_1 color_

struct {
    xc_float textp[40];
} text_;

#define text_1 text_

struct {
    xc_float vectp[5], xcur, ycur;
} vectrc_;

#define vectrc_1 vectrc_

struct {
    integer idex[400]	/* was [200][2] */, nvect[400]	/* was [200][2] */;
    xc_float xsize[400]	/* was [200][2] */, ysize[400]	/* was [200][2] */, 
	    x0[4600]	/* was [2300][2] */, y0[4600]	/* was [2300][2] */, 
	    x1[4600]	/* was [2300][2] */, y1[4600]	/* was [2300][2] */;
} font_;

#define font_1 font_

struct {
    xc_float graphp[100];
} graph_;

#define graph_1 graph_

struct {
    xc_float mapp[11];
} mappar_;

#define mappar_1 mappar_

struct {
    integer memory[1000];
} storag_;

#define storag_1 storag_

struct {
    xc_float tdevp[50]	/* was [5][10] */, ttextp[400]	/* was [40][10] */, 
	    tvectp[50]	/* was [5][10] */, tgraph[1000]	/* was [100][10] */, 
	    tmapp[110]	/* was [11][10] */;
    integer ipopd, ipopt, ipopv, ipopg, ipopm;
} psave_;

#define psave_1 psave_

/* Table of constant values */

static integer c__3 = 3;

/* Copyright(C) 1999-2020 National Technology & Engineering Solutions */
/* of Sandia, LLC (NTESS).  Under the terms of Contract DE-NA0003525 with */
/* NTESS, the U.S. Government retains certain rights in this software. */

/* See packages/seacas/LICENSE for details */
/* ======================================================================= */
/* Subroutine */ int pltsvv_()
{
    extern /* Subroutine */ int pltflu_(), siorpt_(char *, char *, integer *, 
	    ftnlen, ftnlen);

    if (psave_1.ipopv == 10) {
	pltflu_();
	siorpt_("PLTSVV", "Too many calls to PLTSVV.", &c__3, (ftnlen)6, (
		ftnlen)25);
	return 0;
    }
    ++psave_1.ipopv;
    psave_1.tvectp[psave_1.ipopv * 5 - 5] = vectrc_1.vectp[0];
    psave_1.tvectp[psave_1.ipopv * 5 - 4] = vectrc_1.vectp[1];
    psave_1.tvectp[psave_1.ipopv * 5 - 3] = vectrc_1.vectp[2];
    psave_1.tvectp[psave_1.ipopv * 5 - 2] = vectrc_1.vectp[3];
    psave_1.tvectp[psave_1.ipopv * 5 - 1] = vectrc_1.vectp[4];
    return 0;
} /* pltsvv_ */

#ifdef __cplusplus
	}
#endif
