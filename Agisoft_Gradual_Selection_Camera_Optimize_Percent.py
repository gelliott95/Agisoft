import Metashape
import sys

"""
Metashape Sparse Point Cloud Filter Script (v 2.0)
Matjaz Mori, CPA, June 2019
Adapted to include optimize camera alignment -Grant Elliott, Aug 2020
Usage:
Workflow -> Batch Process -> Add -> Run script
In the row "Argumets" we enter exactly 4 values ​​without spaces for: ReprojectionError, ReconstructionUncertainty, ImageCount, ProjectionAccuracy in this order.
ex: 1 15 3 5
or
leave the "Arguments" line blank, in which case the default values ​​will be used,
which can also be modified in the script itself under the variables def_reperr, def_recunc, def_imgcount and def_projacc.
When using, it is advisable to monitor the Console (View -> Console).
"""


def_reperr=10 #Percentage value
def_recunc=15
def_imgcount=0
def_projacc=50 #Percentage value

def_fit_f=True
def_fit_k1=True
def_fit_k2=True
def_fit_k3=True
def_fit_k4=True
def_fit_cx=True
def_fit_cy=True
def_fit_p1=True
def_fit_p2=True
def_fit_p3=True
def_fit_p4=True
def_fit_b1=True
def_fit_b2=True

paramNo=len(sys.argv)

reperr=float(sys.argv[1] if paramNo == 5 else def_reperr)
recunc=float(sys.argv[2] if paramNo == 5 else def_recunc)
imgcount=float(sys.argv[3] if paramNo == 5 else def_imgcount)
projacc=float(sys.argv[4] if paramNo == 5 else def_projacc)
fit_f=float(sys.argv[5] if paramNo == 5 else def_fit_f)
fit_k1=float(sys.argv[6] if paramNo == 5 else def_fit_k1)
fit_k2=float(sys.argv[7] if paramNo == 5 else def_fit_k2)
fit_k3=float(sys.argv[8] if paramNo == 5 else def_fit_k3)
fit_k4=float(sys.argv[9] if paramNo == 5 else def_fit_k4)
fit_cx=float(sys.argv[10] if paramNo == 5 else def_fit_cx)
fit_cy=float(sys.argv[11] if paramNo == 5 else def_fit_cy)
fit_p1=float(sys.argv[12] if paramNo == 5 else def_fit_p1)
fit_p2=float(sys.argv[13] if paramNo == 5 else def_fit_p2)
fit_p3=float(sys.argv[14] if paramNo == 5 else def_fit_p3)
fit_p4=float(sys.argv[15] if paramNo == 5 else def_fit_p4)
fit_b1=float(sys.argv[16] if paramNo == 5 else def_fit_b1)
fit_b2=float(sys.argv[17] if paramNo == 5 else def_fit_b2)



for chunk in Metashape.app.document.chunks:
    f = Metashape.TiePoints.Filter()
    f.init(chunk,Metashape.TiePoints.Filter.ReconstructionUncertainty)
    f.removePoints(recunc)
    
    
chunk.optimizeCameras(fit_f, fit_cx, fit_cy, fit_k1, fit_k2, fit_k3, fit_p1, fit_p2)
    
	
for chunk in Metashape.app.document.chunks:
    f = Metashape.TiePoints.Filter()
    f.init(chunk,Metashape.TiePoints.Filter.ProjectionAccuracy)
    values = f.values.copy()
    values.sort()
    projaccper = values[int(len(values)* (1-projacc/100))]
    f.selectPoints(projaccper)
    f.removePoints(projaccper)
    
chunk.optimizeCameras(fit_f, fit_cx, fit_cy, fit_k1, fit_k2, fit_k3, fit_p1, fit_p2)    
    
for chunk in Metashape.app.document.chunks:
    f = Metashape.TiePoints.Filter()
    f.init(chunk,Metashape.TiePoints.Filter.ReprojectionError)
    values = f.values.copy()
    values.sort()
    reperrper = values[int(len(values)* (1-reperr/100))]
    f.selectPoints(reperrper)
    f.removePoints(reperrper)
    

chunk.optimizeCameras(fit_f, fit_cx, fit_cy, fit_b1, fit_b2, fit_k1, fit_k2, fit_k3, fit_k4, fit_p1, fit_p2, fit_p3, fit_p4)

	

if paramNo == 5:
    print ("Number of entered arguments: " +str(paramNo-1)+". Used values:")
else:
    print ("Number of entered arguments: " +str(paramNo-1)+". Default values were used:")
	
print ("ReprojectionError Level: ")
print (reperr)
print ("ReconstructionUncertainty Level: ")
print (recunc)
print ("ImageCount Level: ")
print (imgcount)
print ("ProjectionAccuracy Level: ")
print (projacc)