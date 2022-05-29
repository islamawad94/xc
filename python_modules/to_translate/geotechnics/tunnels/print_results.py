# -*- coding: utf-8 -*-
from __future__ import print_function

def processPolyhedralAngle(nmbAng,nmbTunel):
    print("\n\\subsection{Polyhedral angle: ",nmbAng,"}\n")
    print("\n\\begin{alltt}\n")
    if(not(JPvacio)):
        if(containsTunnelAxis):
            print("  Contains tunnel axis= Yes.\n")
            print("\\end{alltt}\n")
        else:
            print("  Contains tunnel axis= No.\n")
            print("  Vectores externos:\n")
            print("    I1= ",I1," I2= ",I2,"\n")
            print("    angI1= ",rad2deg(angI1),"\n")
            print("    angI2= ",rad2deg(angI2),"\n")
            print("    angI1I2= ",rad2deg(angI1I2),"\n")
            if(angI1I2>=PI):
                print("  La cuña abarca toda la sección (bloque inamovible).\n")
                print("\\end{alltt}\n")
            else:
                print("  Pirámide:\n")
                print("    points of tangency= ",ptsTang,"\n")
                print("    cúspide= ",p3,"\n")
                psplot.pageSize("letter")
                #outputFile= open(nmbTunel+nmbAng+".ps")
                psplot.fspace(0.0, 0.0, 30.0, 30.0) # specify user coor system
                psplot.lineWidth(0.1) # line thickness in user coordinates
                psplot.penColorName("blue")  # path will be drawn in red
                psplot.erase() # erase Plotter's graphics display
                nv= tunnelSection.getNumVertices
                ptPlot= tunnelSection.at(1)
                psplot.moveTo(ptPlot.x,ptPlot.y)
                i= 0
                for i in range(2,nv+1):
                    ptPlot= tunnelSection.at(i)
                    psplot.cont(ptPlot.x,ptPlot.y)
                ptPlot= tunnelSection.at(1)
                psplot.cont(ptPlot.x,ptPlot.y)
                psplot.penColorName("red")  # path will be drawn in red
                psplot.moveTo(p1.x,p1.y)
                psplot.cont(p3.x,p3.y)
                psplot.cont(p2.x,p2.y)
                psplot.flush()
                psplot.close()
                print("\\end{alltt}\n")
                print("\\begin{figure}\n")
                print("  \\centering\n")
                print("  \\includegraphics[width=40mm]{",nmbTunel+nmbAng+".ps","}\n")
                print("  \\caption{",caption+" Pirámide "+ nmbAng,"}\n")
                print("\\end{figure}\n")
    else:
        print("  El bloque generado es inamovible.\n")
        print("\\end{alltt}\n")

def print_results_jps():
    processPolyhedralAngle(nmbAng= JP0000)
    processPolyhedralAngle(nmbAng= JP0001)
    processPolyhedralAngle(nmbAng= JP0010)
    processPolyhedralAngle(nmbAng= JP0011)
    processPolyhedralAngle(nmbAng= JP0100)
    processPolyhedralAngle(nmbAng= JP0101)
    processPolyhedralAngle(nmbAng= JP0110)
    processPolyhedralAngle(nmbAng= JP0111)
    processPolyhedralAngle(nmbAng= JP1000)
    processPolyhedralAngle(nmbAng= JP1001)
    processPolyhedralAngle(nmbAng= JP1010)
    processPolyhedralAngle(nmbAng= JP1011)
    processPolyhedralAngle(nmbAng= JP1100)
    processPolyhedralAngle(nmbAng= JP1101)
    processPolyhedralAngle(nmbAng= JP1110)
    processPolyhedralAngle(nmbAng= JP1111)
    
def print_results_jps_3planes(caption):
    print("\\section{",caption," Análisis cinemático de cuñas y bloques.}\n")
    print("\\begin{center}\n")
    print("\\begin{tabular}{|l|c|c|}\n")
    print("\\hline\n")
    print("Familia & Buzamiento & Dir. buzamiento\\\\\n")
    print("\\hline\n")
    print("P1 &", rad2deg(alpha1)," & ",rad2deg(beta1),"\\\\\n")
    print("P2 &", rad2deg(alpha2)," & ",rad2deg(beta2),"\\\\\n")
    print("P3 &", rad2deg(alpha3)," & ",rad2deg(beta3),"\\\\\n")
    print("\\hline\n")
    print("\\multicolumn{3}{|l|}{Tunnel axis: ",tunnelAxisVector,"}\\\\\n")
    print("\\hline\n")
    print("\\end{tabular}\n")
    print("\\end{center}\n")
    processPolyhedralAngle(nmbAng= JP000,nmbTun)
    processPolyhedralAngle(nmbAng= JP001,nmbTun)
    processPolyhedralAngle(nmbAng= JP010,nmbTun)
    processPolyhedralAngle(nmbAng= JP011,nmbTun)
    processPolyhedralAngle(nmbAng= JP100,nmbTun)
    processPolyhedralAngle(nmbAng= JP101,nmbTun)
    processPolyhedralAngle(nmbAng= JP110,nmbTun)
    processPolyhedralAngle(nmbAng= JP111,nmbTun)
   
def print_results_jps_4planes(caption):
    print("\\section{",caption," Análisis cinemático de cuñas y bloques.}\n")
    print("\\begin{center}\n")
    print("\\begin{tabular}{|l|c|c|}\n")
    print("\\hline\n")
    print("Familia & Buzamiento & Dir. buzamiento\\\\\n")
    print("\\hline\n")
    print("P1 &", rad2deg(alpha1)," & ",rad2deg(beta1),"\\\\\n")
    print("P2 &", rad2deg(alpha2)," & ",rad2deg(beta2),"\\\\\n")
    print("P3 &", rad2deg(alpha3)," & ",rad2deg(beta3),"\\\\\n")
    print("\\hline\n")
    print("\\multicolumn{3}{|l|}{Tunnel axis: ",tunnelAxisVector,"}\\\\\n")
    print("\\hline\n")
    print("\\end{tabular}\n")
    print("\\end{center}\n")

    processPolyhedralAngle(nmbAng= JP0000,nmbTun)
    processPolyhedralAngle(nmbAng= JP0001,nmbTun)
    processPolyhedralAngle(nmbAng= JP0010,nmbTun)
    processPolyhedralAngle(nmbAng= JP0011,nmbTun)
    processPolyhedralAngle(nmbAng= JP0100,nmbTun)
    processPolyhedralAngle(nmbAng= JP0101,nmbTun)
    processPolyhedralAngle(nmbAng= JP0110,nmbTun)
    processPolyhedralAngle(nmbAng= JP0111,nmbTun)
    processPolyhedralAngle(nmbAng= JP1000,nmbTun)
    processPolyhedralAngle(nmbAng= JP1001,nmbTun)
    processPolyhedralAngle(nmbAng= JP1010,nmbTun)
    processPolyhedralAngle(nmbAng= JP1011,nmbTun)
    processPolyhedralAngle(nmbAng= JP1100,nmbTun)
    processPolyhedralAngle(nmbAng= JP1101,nmbTun)
    processPolyhedralAngle(nmbAng= JP1110,nmbTun)
    processPolyhedralAngle(nmbAng= JP1111,nmbTun)
