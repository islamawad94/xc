# -*- coding: utf-8 -*-
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) "
__copyright__= "Copyright 2018, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es "


''' Test of PySimple1 uniaxial material object.'''
import os
import geom
import xc
import math
import numpy as np
from misc_utils import log_messages as lmsg

feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
materials= preprocessor.getMaterialHandler
pyS1= materials.newMaterial('py_simple1','pyS1')
pyS1.soilType= 1 #Soft clay.
pyS1.ultimateCapacity= 1958.0
pyS1.y50= 0.125
pyS1.dashPot= 0
pyS1.dragResistanceFactor= 0.0
pyS1.initialize()

epsMin= 0.0
epsMax= 3*pyS1.y50
incEps=(epsMax-epsMin)/25.0
range= np.arange(epsMin,epsMax,incEps)
strains= list()
for s in range:
    strains.append(s)
for s in reversed(range):
    strains.append(s)
for s in range:
    strains.append(-s)
for s in reversed(range):
    strains.append(-s)

strains.extend(strains)
strains.extend(strains)


stresses= list()
for eps in strains:
    pyS1.setTrialStrain(eps, 0.0)
    pyS1.commitState()
    stresses.append(pyS1.getStress())

#Stresses computed 16/09/2018
sample_stresses= [0.0, 232.066212579952, 464.17336571492723, 688.0472346752966, 744.5053098493206, 798.6475316758975, 850.5338511951642, 900.2263049518612, 947.7886560108125, 993.2860369355008, 1036.7845995535506, 1078.3511758180753, 1118.0529534939542, 1155.9571697807833, 1192.130825354454, 1226.6404206891393, 1259.5517159290414, 1290.929515029113, 1320.8374743867125, 1352.5900240569913, 1380.783267726669, 1406.894443267383, 1431.500798139636, 1454.8220253987065, 1476.9764592114107, 1476.9764592114107, 1256.0119819294146, 1039.8607840663046, 831.0564451180041, 633.7036231169193, 453.97782861872633, 299.1618547187666, 173.20742177677155, 71.4993433253018, -18.252059042872304, -111.16437662927576, -221.71018193189016, -359.56122106874756, -501.48830128768924, -559.4441057525867, -616.0998710711984, -671.2598147105111, -724.7903499626988, -776.604651216099, -826.6509668298781, -874.9039316533459, -921.3581330549903, -966.023323892261, -1008.9208273592889, -1050.0808044724583, -1050.0808044724583, -1089.540149739222, -1127.3408488906864, -1163.5286808223084, -1198.1521796809373, -1231.2617966494847, -1262.9092175088697, -1293.1468036745684, -1322.0271326177315, -1349.6026194289605, -1375.9252054797282, -1401.0461031795078, -1425.015588056451, -1447.8828310451836, -1469.6957651129158, -1490.5009813111374, -1510.3436500863627, -1529.267464277279, -1547.3146007078387, -1564.525697684919, -1580.9873755034525, -1596.6778371538426, -1611.632312475442, -1625.8895200796742, -1639.4851306284515, -1639.4851306284515, -1416.7715265198233, -1198.045334881564, -985.3523261868654, -782.0902331809687, -593.7986296614683, -428.532965150772, -294.66576915338425, -195.02659035581306, -123.90681264308499, -71.72550164925875, -30.04536668560323, 7.4460294643371725, 45.96153749945579, 90.99378375079283, 149.63978902308867, 231.1227450908931, 344.26133587487976, 490.21795380091794, 547.2980957784665, 603.4566351563574, 658.3865445635175, 711.8768475850376, 763.7864075327248, 814.0248937067389, 814.0248937067389, 862.5391653497411, 909.3035389804602, 954.312781769253, 997.5770084485847, 1039.1179119564529, 1078.965936628713, 1117.1581254280352, 1153.736455990113, 1188.7465366914448, 1222.236572268399, 1254.2565346940794, 1284.8574930275822, 1314.091068440679, 1342.0089893673567, 1368.662727897933, 1394.1032029471853, 1418.3805389091162, 1441.5438708373767, 1463.6411889148806, 1484.7192162742533, 1504.8233152245152, 1523.997417714137, 1542.283976476092, 1559.723933798861, 1559.723933798861, 1338.255729908771, 1121.3903246933496, 911.5765243287584, 712.8807685146311, 531.767418596687, 376.8783741156434, 255.35467375881066, 166.88493728929228, 103.61962212207546, 56.02830787350816, 16.479748095341918, -20.794039884734005, -60.94563191130422, -109.90037673891688, -175.54981111325108, -267.50123304172126, -393.0062959325293, -510.64786152151225, -567.4420564454634, -623.1921863659159, -677.6289898729243, -730.5689847588739, -781.8910116546069, -831.519329129677, -831.519329129677, -879.4115386815131, -925.5499375988763, -969.9352704019722, -1012.5821559059214, -1053.5156913713631, -1092.7688917677408, -1130.3807291093983, -1166.3946093157106, -1200.8571731788104, -1233.8173414528571, -1265.3255469674662, -1295.4331124584849, -1324.1917437957113, -1351.653116000697, -1377.868534918039, -1402.888661322668, -1426.7632870881444, -1449.5411551283116, -1471.2698163802459, -1491.995518274225, -1511.763120043894, -1530.6160309419313, -1548.5961679961677, -1565.7504947991192, -1565.7504947991192, -1344.2124445917302, -1127.2430067037894, -917.2695366162712, -718.32535671583, -536.8381643112837, -381.4583495669424, -259.463296556191, -170.76335743856254, -107.64573106784229, -60.62856100916325, -22.15981957820739, 13.330673393487912, 50.60227607848518, 94.9053561889422, 153.2261911092582, 234.7357606463153, 348.15966878431533, 491.7211581600477, 548.7405037309528, 604.8413298019602, 659.7158408956969, 713.1526462087879, 765.0103881801145, 815.1986214348727, 815.1986214348727, 863.6641485927676, 910.3812606371094, 955.3447149503188, 998.5646233893148, 1040.0626778141116, 1079.8693203414045, 1118.021588935987, 1154.5614526132233, 1189.5345071554596, 1222.9889406882887, 1254.9747047082205, 1285.5428442024702, 1314.7449530172512, 1342.6327293872137, 1369.257612725279, 1394.6704871867014, 1418.921440709151, 1442.0595705603748, 1464.132828151991, 1485.1878971778983, 1505.2701001309485, 1524.423329027309, 1542.6899967842357, 1560.1110061959123, 1560.1110061959123, 1338.6672032091667, 1121.839458181943, 912.0864504836871, 713.4927313580315, 532.5529189098331, 377.94622727121856, 256.8331330814262, 168.89523848931083, 106.29660644065244, 59.57822271283563, 21.247187392169234, -14.230341639919768, -51.61008774673009, -96.17166358640422, -154.95795319421094, -237.17995823848742, -351.4785885627079, -493.16968115911436, -550.1705934143697, -606.2437585728619, -661.0842097143515, -714.4826157716243, -766.2991141428819, -816.4443493320719, -816.4443493320719, -864.8659249206822, -911.5387258732628, -956.4579537654222, -999.6340547984936, -1041.0889734089433, -1080.8533424773889, -1118.964343289918, -1155.4640512440349, -1190.3981393668194, -1223.814849784143, -1255.7641692758284, -1286.2971629327499, -1315.4654323337693, -1343.3206733390098, -1369.9143147293362, -1395.2972232996526, -1419.5194641759592, -1442.6301074378966, -1464.677073842818, -1485.7070137383444, -1505.76521423905, -1524.8955305140264, -1543.1403376449518, -1560.5409591932164, -1560.5409591932164, -1339.0920499891902, -1122.2566898775144, -912.4919765415121, -713.8800115128686, -532.9126794668477, -378.2697250662675, -257.1213903193426, -169.16505308827192, -106.5742125348312, -59.89275548223153, -21.63251065153264, 13.727857686168894, 50.91873406252903, 95.17531733623987, 153.47725926642605, 234.99250212863058, 348.440079798046, 491.8299885444374, 548.8451091880474, 604.9418788694417, 659.8124628476395, 713.2454514509072, 765.0994787866069, 815.2840965195209, 815.2840965195209, 863.7461069520109, 910.4598019375306, 955.4199401333881, 998.6366346554124, 1040.1315783843718, 1079.9352141084837, 1118.084580067083, 1154.621645142052, 1189.592004584645, 1223.0438456147137, 1255.0271184784788, 1285.592866602201, 1314.792681996006, 1342.6782608190665, 1369.3010402044442, 1394.7119018567757, 1418.9609311241527, 1442.0972225754701, 1464.1687248416156, 1485.2221187788978, 1505.3027240083316, 1524.454429660243, 1542.7196457699706, 1560.1392722694275, 1560.1392722694275, 1338.6971091421888, 1121.8718957404149, 912.1229759666485, 713.5361203707647, 532.6079835923616, 378.0202865859873, 256.93479262021924, 169.03257945092835, 106.47852457341152, 59.81822588581865, 21.567727936744085, -13.791728510706053, -50.99027218086127, -95.26517772432088, -153.6001271259918, -235.1659674129171, -348.6758302838455, -491.93318325365357, -548.9470002425152, -605.0418060511016, -659.9099682301, -713.3402244206529, -765.1913156427185, -815.3728714950025, -815.3728714950025, -863.8317515465244, -910.5422901133101, -955.4992776036546, -998.7128510304295, -1040.2047213263863, -1080.0053449140316, -1118.1517702769431, -1154.685973902201, -1189.6535565649174, -1223.1027093486334, -1255.0833850266013, -1285.6466284681621, -1314.8440322431827, -1342.7272923489052, -1369.34784516686, -1394.7565711697264, -1419.003554084368, -1442.137886545901, -1464.2075150038545, -1485.2591179408473, -1505.3380124589748, -1524.4880850646066, -1542.7517430983646, -1560.169916438674, -1560.169916438674, -1338.7273887656859, -1121.9016316568511, -912.1518760288993, -713.5637174041866, -532.633615030092, -378.04332733349105, -256.95531382645703, -169.05177646326536, -106.49826374683812, -59.84057766239182, -21.59509543736127, 13.75605835259949, 50.94121936702238, 95.19451532987694, 153.4951318255774, 235.0107978862252, 348.4600792900079, 491.8377539442329, 548.8525739996298, 604.9490548480854, 659.8193590278568, 713.252075575949, 765.1058380431283, 815.2901979093693]

error= 0.0
for s1, s2 in zip(stresses,sample_stresses):
    error+= (s1-s2)**2

error= math.sqrt(error)

'''
print('error= ', error)
print(strains)
print(stresses)
'''

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if(error<1e-10):
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')

###   FIGURES & REPORTS
#import matplotlib.pyplot as plt
#plt.plot(strains,stresses)
#plt.show()
