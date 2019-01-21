'''
VorModel

Creates a VORLAX input file based on parametric inputs...

Version for Discoidal wing, a-la Vought XF5U and V-173.

Wing definition with six control stations. Sweep and camber can vary between 
control stations.

Customize as needed to reflect the basic configuration of interest.
Customization may entail addition/deletion of surfaces, or modification of
existing surfaces. 

Note! Reads path to Vorlax .exe in "path.txt" file that must reside
in same directory as vorModel.py. The path in that file must be on the 
first line and begin with drive letter + colon, or "\". and must point
to directory with Vorlax executable. Will write input file there. 
Assumes C-drive if path begins with "\".

'''
import math
# START Changing Inputs Here ***************************
inputGeo = {'acProject': 'Parametric_Discoidal_Wing',
# WING DEFINITION:
    'sRefInFt2': 7.07,
    'arWing': 1.2732,
    'taperWingInDecimal': 0.5708,
    'sweepLeWingInDeg': 0,
    'dihedralWingInDeg': 0,
    'xDistWingApexInIn': 0,
    'mrpMacPct': 15,
    #"TIP"
    'spanTipInIn': 6.25,
    'chordTipInIn': 4,
    'tipIncidenceDeg': 0,
    # Spanwise location of wing control stations
    'bSta1OverHalfSpan': 0.0, # Spanwise Location of station #1 as fraction of half span (width of fuse)
    'bSta2OverHalfSpan': 0.309, # Spanwise location of station #2 as fraction of half span 
    'bSta3OverHalfSpan': 0.588, # Spanwise location of station #3 as fraction of half span 
    'bSta4OverHalfSpan': 0.809, # Spanwise location of station #4 as fraction of half span 
    'bSta5OverHalfSpan': 0.951, # Spanwise location of station #5 as fraction of half span 
    # Variation of chord from trapazoidal wing at control stations 
    'ratioCSta1OverCtrap': 1., # Ratio of actual chord at station #1 over reference chord of equivalent trapezoidal wing
    'ratioCSta2OverCtrap': 1.096485, # Ratio of actual chord at station #2 over reference chord of equivalent trapezoidal wing
    'ratioCSta3OverCtrap': 1.081978, # Ratio of actual chord at station #3 over reference chord of equivalent trapezoidal wing
    'ratioCSta4OverCtrap': 0.900452, # Ratio of actual chord at station #4 over reference chord of equivalent trapezoidal wing
    'ratioCSta5OverCtrap': 0.522162, # Ratio of actual chord at station #5 over reference chord of equivalent trapezoidal wing
    'ratioCSta6OverCtrap': 0.2, # Ratio of actual chord at station #6 over reference chord of equivalent trapezoidal wing
    # Variation of sweep from reference value at control stations 
    'sweepIncrDegSta1': 4.5, # Increment in actual sweep above reference sweep from station #1 to station #2 
    'sweepIncrDegSta2': 13.5, # Increment in actual sweep above reference sweep from station #2 to station #3
    'sweepIncrDegSta3': 22.5, # Increment in actual sweep above reference sweep from station #3 to station #4
    'sweepIncrDegSta4': 31.5, # Increment in actual sweep above reference sweep from station #4 to station #5
    'sweepIncrDegSta5': 40.5, # Increment in actual sweep above reference sweep from station #5 to station #6
    # Incidence at control stations, positive equal wash-OUT (TE up)
    'incidenceDegSta1': 0, # Incidence at station #1 
    'incidenceDegSta2': 0, # Incidence at station #2 
    'incidenceDegSta3': 0, # Incidence at station #3 
    'incidenceDegSta4': 0, # Incidence at station #4 
    'incidenceDegSta5': 0, # Incidence at station #5
    'incidenceDegSta6': 0, # Incidence at station #6
     # Vertical shear at control stations, positive equal up from dihedral line
    'zShearInInSta1': 0, # Vertical displacement above dihedral line at station #1 
    'zShearInInSta2': 0, # Vertical displacement above dihedral line at station #2
    'zShearInInSta3': 0, # Vertical displacement above dihedral line at station #3  
    'zShearInInSta4': 0, # Vertical displacement above dihedral line at station #4
    'zShearInInSta5': 0, # Vertical displacement above dihedral line at station #5
    'zShearInInSta6': 0, # Vertical displacement above dihedral line at station #6
    # FUSELAGE DEFINITION: NOTE! NOT USED IN CURRENT MODEL!
#    'lengthFuseInIn': 30.03,
#    'heightFuseInIn': 3.08,
#    'noseTopAngle': 25.0,
#    'noseSideAngle': 25.0,
#    'tailTopAngle': 60.0,
#    'tailSideAngle': 60.0,
#    'widthFuseInIn': 3.08,
    # HORIZONTAL TAIL (AILEVATOR) DEFINITION:
    'isHTailOn': -1, # 0 = off, 1 = collective deflection, -1 = asymmetric deflection
    'sRefHTailInFt2': 0.3,
    'arHTail': 1.1,
    'taperHTailInDecimal': 0.8,
    'sweepLeHTailInDeg': 0,
    'dihedralHTailInDeg': 0,
    'hTailIncidenceInDeg': 0, # Positive = TE UP on RIGHT SIDE
    'mrpMacHTailPct': 25,
    # VERTICAL TAIL DEFINITION:
    'isVTailOn': 1, # OFF=0, ON (DORSAL)=1, ON (VENTRAL)=-1
    'sRefVTailInFt2': .2,
    'arVTail': 2,
    'taperVTailInDecimal': 0.493,
    'sweepLeVTailInDeg': 20,
    'tiltVTailInDeg': 0,
    'xDistVTailBaseInIn': 1,
    'mrpMacVTailPct': 25,
    # ELEVATOR
    'fracRootElevatorBreak': 0.75,
    'elevDeflectionInDeg': 0, # Positive = TE UP
    'zElevOffset': 0.1, # Needed to enable convergence
# (ADD EXTRA COMPONENTS AS NEEDED)
}
# Read path to working directory
fout = open("path.txt", 'r')
userExePath=fout.readline()
fout.close()

# STOP Changing Inputs Here ************************
# Useful degree conversions
radToDeg = 180 / math.pi
degToRad = 1 / radToDeg

# Determine wing characteristics 
sRefInIn2 = 144 * inputGeo['sRefInFt2']
bInIn = (sRefInIn2 * inputGeo['arWing'])**0.5
bOver2InIn = bInIn / 2
tanDihedralWing = math.tan(inputGeo['dihedralWingInDeg'] * degToRad)
tanSweepLeWing = math.tan(inputGeo['sweepLeWingInDeg'] * degToRad)
halfFuseInIn = inputGeo['bSta1OverHalfSpan'] * bOver2InIn
cRootInIn = 2 * sRefInIn2 / bInIn / (1 + inputGeo['taperWingInDecimal'])
cMacInIn = 2 / 3 * cRootInIn * (1 + inputGeo['taperWingInDecimal'] + \
                                inputGeo['taperWingInDecimal']**2) / \
                                (1 + inputGeo['taperWingInDecimal']) 
cTipInIn = cRootInIn * inputGeo['taperWingInDecimal']
sweepQtrChordWingInDeg = radToDeg * math.atan((bOver2InIn * tanSweepLeWing + \
                         cTipInIn / 4 - cRootInIn / 4) / bOver2InIn)
yMacInIn = bInIn / 6 * ((1 + 2 * inputGeo['taperWingInDecimal']) / \
                        (1 + inputGeo['taperWingInDecimal'])) 
zMrpInIn = (yMacInIn - halfFuseInIn) * tanDihedralWing
xLeMacInIn = inputGeo['xDistWingApexInIn'] + bOver2InIn * tanSweepLeWing * \
             1 / 3 * (1 + 2 * inputGeo['taperWingInDecimal']) / \
             (1 + inputGeo['taperWingInDecimal']) 
xMrpInIn = xLeMacInIn + \
           cMacInIn * inputGeo['mrpMacPct'] / 100 
cWingFuseInIn = cRootInIn - \
                inputGeo['bSta1OverHalfSpan'] * (cRootInIn - cTipInIn) 
xWingFuseInIn = inputGeo['xDistWingApexInIn'] + halfFuseInIn * tanSweepLeWing 
xTipInIn = inputGeo['xDistWingApexInIn'] + bOver2InIn * tanSweepLeWing
zTipInIn = (bOver2InIn - halfFuseInIn) * tanDihedralWing

# Determine spanwise location of wing control stations 
ySta1InIn = inputGeo['bSta1OverHalfSpan'] * bInIn / 2
ySta2InIn = inputGeo['bSta2OverHalfSpan'] * bInIn / 2
ySta3InIn = inputGeo['bSta3OverHalfSpan'] * bInIn / 2
ySta4InIn = inputGeo['bSta4OverHalfSpan'] * bInIn / 2
ySta5InIn = inputGeo['bSta5OverHalfSpan'] * bInIn / 2
ySta6InIn = bInIn / 2

# Determine chord lengths at wing control stations
chordSta1InIn = (cRootInIn - inputGeo['bSta1OverHalfSpan'] * \
                (cRootInIn - cTipInIn)) * inputGeo['ratioCSta1OverCtrap'] 
chordSta2InIn = (cRootInIn - inputGeo['bSta2OverHalfSpan'] * \
                (cRootInIn - cTipInIn)) * inputGeo['ratioCSta2OverCtrap'] 
chordSta3InIn = (cRootInIn - inputGeo['bSta3OverHalfSpan'] * \
                (cRootInIn - cTipInIn)) * inputGeo['ratioCSta3OverCtrap'] 
chordSta4InIn = (cRootInIn - inputGeo['bSta4OverHalfSpan'] * \
                (cRootInIn - cTipInIn)) * inputGeo['ratioCSta4OverCtrap'] 
chordSta5InIn = (cRootInIn - inputGeo['bSta5OverHalfSpan'] * \
                (cRootInIn - cTipInIn)) * inputGeo['ratioCSta5OverCtrap'] 
chordSta6InIn = cTipInIn * inputGeo['ratioCSta6OverCtrap']

# Determine horizontal tail characteristics
tanHTailIncidence = math.tan(inputGeo['hTailIncidenceInDeg'] * degToRad)
cosHTailIncidence = math.cos(inputGeo['hTailIncidenceInDeg'] * degToRad)
tanDihedralHTail = math.tan(inputGeo['dihedralHTailInDeg'] * degToRad)
tanSweepLeHTail = math.tan(inputGeo['sweepLeHTailInDeg'] * degToRad)
sRefHTailInIn2 = 144 * inputGeo['sRefHTailInFt2'] 
bHTailInIn = (sRefHTailInIn2 * inputGeo['arHTail'])**0.5 
bOver2HTailInIn = bHTailInIn / 2
cRootHTailInIn = 2 * sRefHTailInIn2 / bHTailInIn / \
                 (1 + inputGeo['taperHTailInDecimal'])
cMacHTailInIn = 2 / 3 * cRootHTailInIn * (1 + inputGeo['taperHTailInDecimal'] \
                + inputGeo['taperHTailInDecimal']**2) / \
                (1 + inputGeo['taperHTailInDecimal']) 
cTipHTailInIn = cRootHTailInIn * inputGeo['taperHTailInDecimal'] 
sweepQtrChordHTailWingInDeg = radToDeg * math.atan((bOver2HTailInIn * \
   tanSweepLeHTail + cTipHTailInIn / 4 - cRootHTailInIn / 4) / bOver2HTailInIn)
yMacHTailInIn = bHTailInIn / 6 * ((1 + 2 * inputGeo['taperHTailInDecimal']) / \
                (1 + inputGeo['taperHTailInDecimal'])) 
zMrpHTailInIn = yMacHTailInIn * tanDihedralHTail
#cFuseHTailInIn = cRootHTailInIn - inputGeo['bSta1OverHalfSpan'] * \
#                bOver2InIn / bOver2HTailInIn * (cRootHTailInIn - cTipHTailInIn) 
#xFuseHTailInIn = inputGeo['xDistHTailApexInIn'] + halfFuseInIn * tanSweepLeHTail 
xTipHTailInIn = bOver2HTailInIn * tanSweepLeHTail
zTipHTailInIn = bOver2HTailInIn * tanDihedralHTail

# Determine vertical tail characteristics 
tanSweepLeVTail = math.tan(inputGeo['sweepLeVTailInDeg'] * degToRad)
sRefVTailInIn2 = 144 * inputGeo['sRefVTailInFt2'] 
bVTailInIn = (sRefVTailInIn2 * inputGeo['arVTail'])**0.5 
cRootVTailInIn = 2 * sRefVTailInIn2 / bVTailInIn / \
                 (1 + inputGeo['taperVTailInDecimal']) 
cMacVTailInIn = 2 / 3 * cRootVTailInIn * \
                (1 + inputGeo['taperVTailInDecimal'] + \
                inputGeo['taperVTailInDecimal']**2) / \
                (1 + inputGeo['taperVTailInDecimal'])
cTipVTailInIn = cRootVTailInIn * inputGeo['taperVTailInDecimal'] 
sweepQtrChordVTailWingInDeg = radToDeg*math.atan((bVTailInIn*tanSweepLeVTail+ \
                        cTipVTailInIn / 4 - cRootVTailInIn / 4) / bVTailInIn)
zBaseVTailInIn = 0 
zMacVTailInIn = bVTailInIn / 3 * ((1 + 2 * inputGeo['taperVTailInDecimal']) / \
                (1 + inputGeo['taperVTailInDecimal'])) + zBaseVTailInIn
xLeMacVTailInIn = inputGeo['xDistVTailBaseInIn']+bVTailInIn*tanSweepLeVTail * \
              1 / 3 * (1 + 2 * inputGeo['taperVTailInDecimal']) / \
              (1 + inputGeo['taperVTailInDecimal']) 
xMrpVTailInIn = xLeMacVTailInIn + cMacVTailInIn*inputGeo['mrpMacVTailPct'] /100 
# Slave to second wing station
yBaseVTailInIn = ySta3InIn
yTipVTailInIn = yBaseVTailInIn + \
                bVTailInIn * math.tan(inputGeo['tiltVTailInDeg'] * degToRad) 
vTailVolCoeff = (xMrpVTailInIn - xMrpInIn) * sRefVTailInIn2 / \
                (bInIn * sRefInIn2) 
zTipVTailInIn = bVTailInIn 
if inputGeo['isVTailOn'] < 0: 
    zTipVTailInIn = -zTipVTailInIn 
    zMacVTailInIn = -zMacVTailInIn
iQuantVTail = 2

# Elevator quantities
tanElevDeflection = math.tan(inputGeo['elevDeflectionInDeg'] * degToRad) 
cosElevDeflection = math.cos(inputGeo['elevDeflectionInDeg'] * degToRad) 
    
# Write VORLAX input file **************
# Split drive letter from path
drive, exePath = userExePath.split("\\", 1)
# Handle case where user doesn't include drive in path... 
# we will assume it's on the C drive
if not drive: drive = "C:"
# Open input file for write
fin = open(drive + "\\" + exePath + "\\vorlax.in", 'w')
# Write line 1 inputs
fin.write('Auto Generated VORLAX Case\n')
# Echo Parametric Inputs
fin.write('*\n')
fin.write('********* Begin Echo Parametric Inputs *********\n')
fin.write('*** WING ***\n')
fin.write('* mrpMacPct: ' + "{:10.3f}".format(inputGeo['mrpMacPct']) + '\n')
fin.write('* sRefInFt2: ' + "{:10.3f}".format(inputGeo['sRefInFt2']) + '\n')
fin.write('* arWing: ' + "{:13.3f}".format(inputGeo['arWing']) + '\n')
fin.write('* taperWingInDecimal: ' + \
          "{:9.3f}".format(inputGeo['taperWingInDecimal']) + '\n')
fin.write('* sweepLeWingInDeg: ' + \
          "{:11.3f}".format(inputGeo['sweepLeWingInDeg']) + '\n')
fin.write('* dihedralWingInDeg: ' + \
          "{:10.3f}".format(inputGeo['dihedralWingInDeg']) + '\n')
fin.write('* xDistWingApexInIn: ' + \
          "{:10.3f}".format(inputGeo['xDistWingApexInIn']) + '\n')
fin.write('*\n')

fin.write('*Spanwise location of control stations:\n')
fin.write('* bSta1OverHalfSpan: ' + \
          "{:10.3f}".format(inputGeo['bSta1OverHalfSpan']) + \
          ' #Fraction of half span, station 1 (fuse)\n')
fin.write('* bSta2OverHalfSpan: ' + \
          "{:10.3f}".format(inputGeo['bSta2OverHalfSpan']) + \
          ' #Fraction of half span, station 2\n')
fin.write('* bSta3OverHalfSpan: ' + \
          "{:10.3f}".format(inputGeo['bSta3OverHalfSpan']) + \
          ' #Fraction of half span, station 3\n') 
fin.write('* bSta4OverHalfSpan: ' + \
          "{:10.3f}".format(inputGeo['bSta4OverHalfSpan']) + \
          ' #Fraction of half span, station 4\n') 
fin.write('* bSta5OverHalfSpan: ' + \
          "{:10.3f}".format(inputGeo['bSta5OverHalfSpan']) + \
          ' #Fraction of half span, station 5\n') 
fin.write('*\n')

fin.write('*Variation of chord from trapazoidal wing at control stations:\n')
fin.write('* ratioCSta1OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta1OverCtrap']) + \
          ' #Ratio actual to ref chord, station 1\n')
fin.write('* ratioCSta2OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta2OverCtrap']) + \
          ' #Ratio actual to ref chord, station 2\n') 
fin.write('* ratioCSta3OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta3OverCtrap']) + \
          ' #Ratio actual to ref chord, station 3\n')
fin.write('* ratioCSta4OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta4OverCtrap']) + \
          ' #Ratio actual to ref chord, station 4\n')
fin.write('* ratioCSta5OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta5OverCtrap']) + \
          ' #Ratio actual to ref chord, station 5\n')
fin.write('* ratioCSta6OverCtrap: ' + \
          "{:10.3f}".format(inputGeo['ratioCSta6OverCtrap']) + \
          ' #Ratio actual to ref chord, station 6\n')
fin.write('*\n')

fin.write('*Variation of sweep from reference value at control stations:\n')
fin.write('* sweepIncrDegSta1: ' + \
          "{:10.3f}".format(inputGeo['sweepIncrDegSta1']) + \
          ' #Increment in sweep, station 1 to 2\n')
fin.write('* sweepIncrDegSta2: ' + \
          "{:10.3f}".format(inputGeo['sweepIncrDegSta2']) + \
          ' #Increment in sweep, station 2 to 3\n')
fin.write('* sweepIncrDegSta3: ' + \
          "{:10.3f}".format(inputGeo['sweepIncrDegSta3']) + \
          ' #Increment in sweep, station 3 to 4\n')
fin.write('* sweepIncrDegSta4: ' + \
          "{:10.3f}".format(inputGeo['sweepIncrDegSta4' ]) + \
          ' #Increment in sweep, station 4 to 5\n')
fin.write('* sweepIncrDegSta5: ' + \
          "{:10.3f}".format(inputGeo['sweepIncrDegSta5' ]) + \
          ' #Increment in sweep, station 5 to 6\n')
fin.write('*\n')

fin.write('*Incidence at control stations - positive = wash-OUT (TE UP):\n')
fin.write('* incidenceDegSta1: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta1']) + \
          ' #Incidence at station 1\n')
fin.write('* incidenceDegSta2: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta2']) + \
          ' #Incidence at station 2\n') 
fin.write('* incidenceDegSta3: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta3']) + \
          ' #Incidence at station 3\n')
fin.write('* incidenceDegSta4: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta4']) + \
          ' #Incidence at station 4\n')
fin.write('* incidenceDegSta5: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta5']) + \
          ' #Incidence at station 5\n')
fin.write('* incidenceDegSta6: ' + \
          "{:10.3f}".format(inputGeo['incidenceDegSta6']) + \
          ' #Incidence at station 6\n')
fin.write('*\n')

fin.write('*Vertical shear at stations, positive = UP from dihedral line:\n')
fin.write('* zShearInInSta1: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta1']) + \
          ' #Vertical displacement at station 1\n')
fin.write('* zShearInInSta2: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta2']) + \
          ' #Vertical displacement at station 2\n') 
fin.write('* zShearInInSta3: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta3']) + \
          ' #Vertical displacement at station 3\n')
fin.write('* zShearInInSta4: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta4']) + \
          ' #Vertical displacement at station 4\n')
fin.write('* zShearInInSta5: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta5']) + \
          ' #Vertical displacement at station 5\n')
fin.write('* zShearInInSta6: ' + \
          "{:10.3f}".format(inputGeo['zShearInInSta6']) + \
          ' #Vertical displacement at station 6\n')
fin.write('*\n')

#fin.write('*** FUSELAGE ***\n') 
#fin.write('* heightFuseInIn: ' + \
#          "{:10.3f}".format(inputGeo['heightFuseInIn']) + '\n') 
#fin.write('* lengthFuseInIn: ' + \
#          "{:10.3f}".format(inputGeo['lengthFuseInIn']) + '\n') 
#fin.write('* noseTopAngle: ' + \
#          "{:12.3f}".format(inputGeo['noseTopAngle']) + '\n')
#fin.write('* noseSideAngle: ' + \
#          "{:11.3f}".format(inputGeo['noseSideAngle']) + ' \n')
#fin.write('* tailTopAngle: ' + \
#          "{:12.3f}".format(inputGeo['tailTopAngle']) + '\n')
#fin.write('* tailSideAngle: ' + \
#          "{:11.3f}".format(inputGeo['tailSideAngle']) + '\n')
#fin.write('*\n')

fin.write('*** HORIZONTAL TAIL/AILEVATORS ***\n')
fin.write('* isHTailOn: ' + \
          "{:19d}".format(inputGeo['isHTailOn']) + ' # OFF=0; ON/COLLECTIVE=1; ON/ASYMMETRIC=2\n')
fin.write('* mrpMacHTailPct: ' + \
          "{:14.3f}".format(inputGeo['mrpMacHTailPct']) + '\n')
fin.write('* sRefHTailInFt2: ' + \
          "{:14.3f}".format(inputGeo['sRefHTailInFt2']) + '\n')
fin.write('* arHTail: ' + \
          "{:21.3f}".format(inputGeo['arHTail']) + '\n')
fin.write('* taperHTailInDecimal:' + \
          "{:10.3f}".format(inputGeo['taperHTailInDecimal']) + '\n')
fin.write('* sweepLeHTailInDeg: ' + \
          "{:11.3f}".format(inputGeo['sweepLeHTailInDeg']) + '\n')
fin.write('* dihedralHTailInDeg: ' + \
          "{:10.3f}".format(inputGeo['dihedralHTailInDeg']) + '\n')
fin.write('* hTailIncidenceInDeg:' + \
          "{:10.3f}".format(inputGeo['hTailIncidenceInDeg']) + \
          ' # Positive = TE down\n')
fin.write('*\n')

fin.write('*** VERTICAL TAIL ***\n')
fin.write('* isVTailOn: ' + \
          "{:19d}".format(inputGeo['isVTailOn']) + \
          ' # OFF=0; ON,UPPER=1, ON,LOWER=-1\n')
fin.write('* mrpMacVTailPct: ' + \
          "{:14.3f}".format(inputGeo['mrpMacVTailPct']) + '\n')
fin.write('* sRefVTailInFt2: ' + \
          "{:14.3f}".format(inputGeo['sRefVTailInFt2']) + '\n')
fin.write('* arVTail: ' + \
          "{:21.3f}".format(inputGeo['arVTail']) + '\n')
fin.write('* taperVTailInDecimal:' + \
          "{:10.3f}".format(inputGeo['taperVTailInDecimal']) + '\n')
fin.write('* sweepLeVTailInDeg: ' + \
          "{:11.3f}".format(inputGeo['sweepLeVTailInDeg']) + '\n')
fin.write('* tiltVTailInDeg: ' + \
          "{:14.3f}".format(inputGeo['tiltVTailInDeg']) + \
          ' # Vertical=0, Tilt Out=+, Tilt In=-\n')
fin.write('* xDistVTailBaseInIn: ' + \
          "{:10.3f}".format(inputGeo['xDistVTailBaseInIn']) + '\n')
fin.write('*\n')
fin.write('********* End Echo Parametric Inputs *********\n')
fin.write('\n')
fin.write('\n')
fin.write('********* Begin VORLAX Input Deck *********\n')
'''
See NASA CR BEFORE CHANGING HARDWIRED INPUTS

'''
fin.write('*ISOLV       LAX       LAY    REXPAR      ')
fin.write('HAG    FLOATX    FLOATY    ITRMAX\n')
fin.write('     0         0         1      0.10')
fin.write('      0.00      0.00      0.00        99\n')

# Run single AoA & Mach in VORLAX
# Mach sweep
fin.write('*NMACH          MACH\n')
fin.write('     1           0.1\n')
# AoA sweep (AoA in degrees)
fin.write('*NALPHA        ALPHA\n')
fin.write('    16           -2. -1. 0. 1. 2. 3. 4. 6. 8. 10. 12. 14. 16. 18. 20. 22.\n')
#fin.write('    13           13. 14. 15. 16. 17. 18. 19. 20. 21. 22. 23. 24. 25.\n')
#fin.write('     1            0.\n')
fin.write('*    LATRL       PSI    PITCHQ     ROLLQ      YAWQ      VINF\n')
fin.write('         0      0.00      0.00      0.00      0.00       1.0\n')

nPan = 7 + 2 * abs(inputGeo['isHTailOn']) + abs(inputGeo['isVTailOn'])
fin.write('*NPAN           SREF      CBAR      XBAR      ZBAR     WSPAN\n')
fin.write('{:2d}'.format(nPan) +
          '        ' +
          "{:10.2f}".format(sRefInIn2) +
          "{:10.2f}".format(cMacInIn) +
          "{:10.2f}".format(xMrpInIn) +
          "{:10.2f}".format(zMrpInIn) +
          "{:10.2f}".format(bInIn) + '\n')
fin.write('*\n')

fin.write('*** FUSELAGE PANELS ***\n')
#fin.write('*VORLAX inputs for fuselage:\n')
## Vertical fuselage panel ***
#fin.write('*       X1        Y1        Z1     CORD1')
#fin.write(' COMMENT: VERTICAL FUSELAGE PANEL\n')
#fin.write("{:10.3f}".format(0) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(inputGeo['lengthFuseInIn']) + '\n')
#fin.write('*       X2        Y2        Z2     CORD2\n')
#xFuseTopEdgeInIn = inputGeo['heightFuseInIn'] * \
#                   math.tan((inputGeo['noseTopAngle']) * degToRad)
#chordFuseTopEdgeInIn = inputGeo['lengthFuseInIn'] - xFuseTopEdgeInIn - \
#                       inputGeo['heightFuseInIn'] * \
#                       math.tan((inputGeo['tailTopAngle']) * degToRad)
#fin.write("{:10.3f}".format(xFuseTopEdgeInIn) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(inputGeo['heightFuseInIn']) + 
#          "{:10.3f}".format(chordFuseTopEdgeInIn) + '\n')
#fin.write('*     NVOR      RNCV       SPC       PDL\n')
#fin.write('        10     15.00      1.00      0.00\n')
#fin.write('*    AINC1     AINC2       ITS       NAP    ')
#fin.write('IQUANT     ISYNT       NPP\n')
#fin.write("{:10.5f}".format(0) +
#          "{:10.5f}".format(0) +
#          '         0         0         1         0         0\n')
#fin.write('*\n')

## Horizontal fuselage panel ***
#fin.write('*       X1        Y1        Z1     CORD1')
#fin.write(' COMMENT: HORIZONTAL FUSELAGE PANEL\n') 
#fin.write("{:10.3f}".format(0) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(inputGeo['lengthFuseInIn']) + '\n')
#fin.write('*       X2        Y2        Z2     CORD2\n')
#xFuseSideEdgeInIn = ySta1InIn * math.tan((inputGeo['noseSideAngle'])*degToRad)
#chordFuseSideEdgeInIn = inputGeo['lengthFuseInIn'] - xFuseSideEdgeInIn - \
#                   ySta1InIn * math.tan((inputGeo['tailSideAngle']) * degToRad)
#fin.write("{:10.3f}".format(xFuseSideEdgeInIn) +
#          "{:10.3f}".format(inputGeo['widthFuseInIn']) +
#          "{:10.3f}".format(0) +
#          "{:10.3f}".format(chordFuseSideEdgeInIn) + '\n')
#fin.write('*     NVOR      RNCV       SPC       PDL\n')
#fin.write('        10     15.00      1.00      0.00\n')
#fin.write('*    AINC1     AINC2       ITS       NAP    ')
#fin.write('IQUANT     ISYNT       NPP\n')
#fin.write("{:10.5f}".format(0) +
#          "{:10.5f}".format(0) +
#          '         0         0         2         0         0\n')
#fin.write('*\n')

# Wing panels
fin.write('*** WING PANELS ***\n')
fin.write('*Derived Geometric Data for Reference Wing:\n') 
fin.write('* Wing Span (in):' +
          "{:10.3f}".format(bInIn) + '\n') 
fin.write('* Root Chord (in):' +
          "{:9.3f}".format(cRootInIn) + '\n') 
fin.write('* Tip Chord (in):' +
          "{:10.3f}".format(cTipInIn) + '\n') 
fin.write('* MAC Chord (in):' +
          "{:10.3f}".format(cMacInIn) + '\n') 
fin.write('* x MRP (in):' +
          "{:14.3f}".format(xMrpInIn) + '\n') 
fin.write('* z MRP (in):' +
          "{:14.3f}".format(zMrpInIn) + '\n') 
fin.write('* y (in):' +
          "{:18.3f}".format(yMacInIn) + '\n') 
fin.write('* Sweep 1/4C (deg):' +
          "{:8.3f}".format(sweepQtrChordWingInDeg) + '\n')
fin.write('*\n')
fin.write('*VORLAX inputs for Wing:\n')

# Inboard-most wing panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: INBOARD-MOST WING PANEL\n') 
xSta1InIn = xLeMacInIn + ySta1InIn * tanSweepLeWing
mainChordSta1InIn = chordSta1InIn * inputGeo['fracRootElevatorBreak']
fin.write("{:10.3f}".format(xSta1InIn) +
          "{:10.3f}".format(ySta1InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta1InIn + inputGeo['zShearInInSta1']) +
          "{:10.3f}".format(mainChordSta1InIn) + '\n')
fin.write('*       X2        Y2        Z2     CORD2\n')
xSta2InIn = xSta1InIn + (ySta2InIn-ySta1InIn) * \
            math.tan((inputGeo['sweepLeWingInDeg'] + \
            inputGeo['sweepIncrDegSta1']) * degToRad)    
mainChordSta2InIn = mainChordSta1InIn - xSta2InIn
fin.write("{:10.3f}".format(xSta2InIn) +
          "{:10.3f}".format(ySta2InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta2InIn + inputGeo['zShearInInSta2']) +
          "{:10.3f}".format(mainChordSta2InIn) + '\n')
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(math.tan(inputGeo['incidenceDegSta1'] * degToRad))+ 
         "{:10.5f}".format(math.tan(inputGeo['incidenceDegSta2'] * degToRad)) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Second-most inboard wing panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: SECOND INBOARD WING PANEL\n') 
fin.write("{:10.3f}".format(xSta2InIn) +
          "{:10.3f}".format(ySta2InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta2InIn + inputGeo['zShearInInSta2']) +
          "{:10.3f}".format(mainChordSta2InIn) + '\n') 
fin.write('*       X2        Y2        Z2     CORD2\n')
xSta3InIn = xSta2InIn + (ySta3InIn-ySta2InIn) * \
            math.tan((inputGeo['sweepLeWingInDeg'] + \
            inputGeo['sweepIncrDegSta2']) * degToRad)
mainChordSta3InIn = mainChordSta1InIn - xSta3InIn    
fin.write("{:10.3f}".format(xSta3InIn) + \
          "{:10.3f}".format(ySta3InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta3InIn + inputGeo['zShearInInSta3']) +
          "{:10.3f}".format(mainChordSta3InIn) + '\n') 
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(math.tan(inputGeo['incidenceDegSta2'] * degToRad))+ 
         "{:10.5f}".format(math.tan(inputGeo['incidenceDegSta3'] * degToRad)) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Middle wing panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: MIDDLE WING PANEL\n') 
fin.write("{:10.3f}".format(xSta3InIn) +
          "{:10.3f}".format(ySta3InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta3InIn + inputGeo['zShearInInSta3']) +
          "{:10.3f}".format(chordSta3InIn) + '\n')
fin.write('*       X2        Y2        Z2     CORD2\n')
xSta4InIn = xSta3InIn + (ySta4InIn-ySta3InIn) * \
            math.tan((inputGeo['sweepLeWingInDeg'] + \
            inputGeo['sweepIncrDegSta3']) * degToRad)
#fin.write("{:10.3f}".format(xSta4InIn) +
#          "{:10.3f}".format(ySta4InIn) +
# "{:10.3f}".format(tanDihedralAngle * ySta4InIn + inputGeo['zShearInInSta4']) +
#          "{:10.3f}" .format(chordSta4InIn) + '\n') 
fin.write("{:10.3f}".format(xSta4InIn) +
          "{:10.3f}".format(ySta4InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta4InIn + inputGeo['zShearInInSta4']) +
          "{:10.3f}" .format(chordSta3InIn) + '\n') 
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(math.tan(inputGeo['incidenceDegSta3'] * degToRad))+ 
         "{:10.5f}".format(math.tan(inputGeo['incidenceDegSta4'] * degToRad)) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Second-most outboard wing panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: SECOND-MOST OUTBOARD WING PANEL\n') 
fin.write("{:10.3f}".format(xSta4InIn) +
          "{:10.3f}".format(ySta4InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta4InIn + inputGeo['zShearInInSta4']) +
          "{:10.3f}".format(chordSta4InIn) + '\n') 
fin.write('*       X2        Y2        Z2     CORD2\n')
xSta5InIn = xSta4InIn + (ySta5InIn-ySta4InIn) * \
math.tan((inputGeo['sweepLeWingInDeg'] + \
          inputGeo['sweepIncrDegSta4']) * degToRad) 
fin.write("{:10.3f}".format(xSta5InIn) +
          "{:10.3f}".format(ySta5InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta5InIn + inputGeo['zShearInInSta5']) +
          "{:10.3f}".format(chordSta5InIn) + '\n')
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(math.tan(inputGeo['incidenceDegSta4'] * degToRad))+ 
         "{:10.5f}".format(math.tan(inputGeo['incidenceDegSta5'] * degToRad)) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Outboard-most wing panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: MOST OUTBOARD WING PANEL\n') 
fin.write("{:10.3f}".format(xSta5InIn) +
          "{:10.3f}".format(ySta5InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta5InIn + inputGeo['zShearInInSta5']) +
          "{:10.3f}".format(chordSta5InIn) + '\n')
fin.write('*       X2        Y2        Z2     CORD2\n')
xSta6InIn = xSta5InIn + (ySta6InIn-ySta5InIn) * \
            math.tan((inputGeo['sweepLeWingInDeg'] + \
            inputGeo['sweepIncrDegSta5']) * degToRad) 
fin.write("{:10.3f}".format(xSta6InIn) +
          "{:10.3f}".format(ySta6InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta6InIn + inputGeo['zShearInInSta6']) +
          "{:10.3f}".format(chordSta6InIn) + '\n')
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(math.tan(inputGeo['incidenceDegSta5'] * degToRad))+ 
         "{:10.5f}".format(math.tan(inputGeo['incidenceDegSta6'] * degToRad)) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

## Tip Panel ***
#fin.write('*       X1        Y1        Z1     CORD1')
#fin.write(' COMMENT: TIP\n') 
#fin.write("{:10.3f}".format(xSta6InIn) +
#          "{:10.3f}".format(ySta6InIn) +
# "{:10.3f}".format(tanDihedralWing * ySta6InIn + inputGeo['zShearInInSta6']) +
#          "{:10.3f}".format(inputGeo['chordTipInIn']) + '\n')
#fin.write('*       X2        Y2        Z2     CORD2\n')
#fin.write("{:10.3f}".format(xSta6InIn) +
#          "{:10.3f}".format(ySta6InIn+inputGeo['spanTipInIn']) +
# "{:10.3f}".format(tanDihedralWing * ySta6InIn + inputGeo['zShearInInSta6']) +
#          "{:10.3f}".format(inputGeo['chordTipInIn']) + '\n')
#fin.write('*     NVOR      RNCV       SPC       PDL\n')
#fin.write('        10     15.00      1.00      0.00\n')
#fin.write('*    AINC1     AINC2       ITS       NAP    ')
#fin.write('IQUANT     ISYNT       NPP\n')
#fin.write("{:10.5f}".format(math.tan(inputGeo['tipIncidenceDeg'] * degToRad))+ 
#         "{:10.5f}".format(math.tan(inputGeo['tipIncidenceDeg'] * degToRad)) + 
#         '         0        0          2         0         0\n')
#fin.write('*\n')

# Horizontal tail (ailevator) panel ***
if inputGeo['isHTailOn'] != 0:  
    xRootHTailInIn = xSta4InIn + chordSta3InIn - cRootHTailInIn
    xLeMacHTailInIn = xRootHTailInIn + \
                  bOver2HTailInIn * tanSweepLeHTail * 1 / 3 * \
                  (1 + 2 * inputGeo['taperHTailInDecimal']) / \
                  (1 + inputGeo['taperHTailInDecimal']) 
    xMrpHTailInIn = xLeMacHTailInIn + \
                    cMacHTailInIn * inputGeo['mrpMacHTailPct'] / 100 
    hTailVolCoeff = (xMrpHTailInIn - xMrpInIn) * sRefHTailInIn2 / \
                    (cMacInIn * sRefInIn2)      
                    
    fin.write('*** HORIZONTAL TAIL PANEL ***\n')
    fin.write('*Derived Geometric Data for Horizontal Tail:\n') 
    fin.write('* Span (in):' +
              "{:15.3f}".format(bHTailInIn) + '\n')
    fin.write('* Root Chord (in):' +
              "{:9.3f}".format(cRootHTailInIn) + '\n')
    fin.write('* Tip Chord (in):' +
              "{:10.3f}".format(cTipHTailInIn) + '\n')
    fin.write('* MAC Chord (in):' +
              "{:10.3f}".format(cMacHTailInIn) + '\n')
    fin.write('* x MRP (in):' +
              "{:14.3f}".format(xMrpHTailInIn) + '\n')
    fin.write('* y MAC (in):' +
              "{:14.3f}".format(yMacHTailInIn) + '\n')
    fin.write('* Sweep 1/4C (deg):' +
              "{:8.3f}".format(sweepQtrChordHTailWingInDeg) + '\n') 
    fin.write('* Tail Volume Coefficient:' +
              "{:12.5f}".format(hTailVolCoeff) + '\n')
    fin.write('*\n')
    fin.write('*VORLAX inputs for Horizontal Tails:\n')
    fin.write('*       X1        Y1        Z1     CORD1')
    fin.write(' COMMENT: RIGHT HORIZONTAL TAIL PANEL\n')
    fin.write("{:10.3f}".format(xRootHTailInIn) +
              "{:10.3f}".format(ySta4InIn) +
              "{:10.3f}".format(0) +
              "{:10.3f}".format(cRootHTailInIn * cosHTailIncidence) + '\n')
    fin.write('*       X2        Y2        Z2     CORD2\n')
    fin.write("{:10.3f}".format(xRootHTailInIn + xTipHTailInIn) +
              "{:10.3f}".format(ySta4InIn + bOver2HTailInIn) +
              "{:10.3f}".format(zTipHTailInIn) +
              "{:10.3f}".format(cTipHTailInIn * cosHTailIncidence) + '\n')         
    fin.write('*     NVOR      RNCV       SPC       PDL\n')
    fin.write('        10     15.00      1.00      0.00\n')
    fin.write('*    AINC1     AINC2       ITS       NAP    ')
    fin.write('IQUANT     ISYNT       NPP\n')
    fin.write("{:10.5f}".format(tanHTailIncidence)+ 
          "{:10.5f}".format(tanHTailIncidence) + 
          '         0        0          1         0         0\n')
    fin.write('*\n')
    
    fin.write('*       X1        Y1        Z1     CORD1')
    fin.write(' COMMENT: LEFT HORIZONTAL TAIL PANEL\n')
    fin.write("{:10.3f}".format(xRootHTailInIn) +
              "{:10.3f}".format(-ySta4InIn) +
              "{:10.3f}".format(0) +
              "{:10.3f}".format(cRootHTailInIn * cosHTailIncidence) + '\n')
    fin.write('*       X2        Y2        Z2     CORD2\n')
    fin.write("{:10.3f}".format(xRootHTailInIn + xTipHTailInIn) +
              "{:10.3f}".format(-ySta4InIn - bOver2HTailInIn) +
              "{:10.3f}".format(zTipHTailInIn) +
              "{:10.3f}".format(cTipHTailInIn * cosHTailIncidence) + '\n')         
    fin.write('*     NVOR      RNCV       SPC       PDL\n')
    fin.write('        10     15.00      1.00      0.00\n')
    fin.write('*    AINC1     AINC2       ITS       NAP    ')
    fin.write('IQUANT     ISYNT       NPP\n')
    fin.write("{:10.5f}".format(-1 * inputGeo['isHTailOn'] * tanHTailIncidence) + 
          "{:10.5f}".format(-1 * inputGeo['isHTailOn'] * tanHTailIncidence) + 
          '         0        0          1         0         0\n')
    fin.write('*\n')

# Vertical tail panel *** 
if inputGeo['isVTailOn'] != 0: 
    fin.write('*** VERTICAL TAIL PANEL ***\n')
    fin.write('*Derived Geometric Data for Vertical Tail:\n')
    fin.write('* Span (in):' +
              "{:15.3f}".format(bVTailInIn) + '\n')
    fin.write('* Root Chord (in):' +
              "{:9.3f}".format(cRootVTailInIn) + '\n')
    fin.write('* Tip Chord (in):' +
              "{:10.3f}".format(cTipVTailInIn) + '\n')
    fin.write('* MAC Chord (in):' +
              "{:10.3f}".format(cMacVTailInIn) + '\n')
    fin.write('* x MRP (in):' +
              "{:14.3f}".format(xMrpVTailInIn) + '\n')
    fin.write('* z MAC (in):' +
              "{:14.3f}".format(zMacVTailInIn) + '\n')
    fin.write('* Sweep 1/4C (deg):' +
              "{:8.3f}".format(sweepQtrChordVTailWingInDeg) + '\n')
    fin.write('* Tail Volume Coefficient:' + 
              "{:12.5f}".format(vTailVolCoeff) + '\n')
    fin.write('*\n')
    fin.write('*VORLAX inputs for Vertical Tail:\n')
    fin.write('*       X1        Y1        Z1     CORD1')
    fin.write(' COMMENT: VERTICAL TAIL PANEL\n')
    xBaseVtailInIn = xSta3InIn + chordSta3InIn - cRootVTailInIn
    fin.write("{:10.3f}".format(xBaseVtailInIn) +
              "{:10.3f}".format(yBaseVTailInIn) +
              "{:10.3f}".format(zBaseVTailInIn) +
              "{:10.3f}".format(cRootVTailInIn) + '\n')
    fin.write('*       X2        Y2        Z2     CORD2\n')
    xTipVTailInIn = xBaseVtailInIn + bVTailInIn * tanSweepLeVTail 
    fin.write("{:10.3f}".format(xTipVTailInIn) +
              "{:10.3f}".format(yTipVTailInIn) +
              "{:10.3f}".format(zTipVTailInIn) +
              "{:10.3f}".format(cTipVTailInIn) + '\n')
    fin.write('*     NVOR      RNCV       SPC       PDL\n')
    fin.write('        10     15.00      1.00      0.00\n')
    fin.write('*    AINC1     AINC2       ITS       NAP    ')
    fin.write('IQUANT     ISYNT       NPP\n')
    fin.write("{:10.5f}".format(0) +
              "{:10.5f}".format(0) +
              '         0         0' +
              "{:10d}".format(iQuantVTail) +
              '         0         0\n')

# Inboard elevator panel ***
fin.write('*\n')	
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: INBOARD ELEVATOR PANEL\n') 
fin.write("{:10.3f}".format(xSta1InIn + mainChordSta1InIn) +
          "{:10.3f}".format(ySta1InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta1InIn + inputGeo['zShearInInSta1'] + inputGeo['zElevOffset']) +
          "{:10.3f}".format(cosElevDeflection * (chordSta1InIn - mainChordSta1InIn)) + '\n') 
fin.write('*       X2        Y2        Z2     CORD2\n')
            
fin.write("{:10.3f}".format(xSta2InIn + mainChordSta2InIn) + \
          "{:10.3f}".format(ySta2InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta2InIn + inputGeo['zShearInInSta2'] + inputGeo['zElevOffset']) +
          "{:10.3f}".format(cosElevDeflection * (chordSta2InIn - mainChordSta2InIn)) + '\n') 
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(tanElevDeflection)+ 
         "{:10.5f}".format(tanElevDeflection) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Outboard elevator panel ***
fin.write('*       X1        Y1        Z1     CORD1')
fin.write(' COMMENT: OUTBOARD ELEVATOR PANEL\n') 
fin.write("{:10.3f}".format(xSta2InIn + mainChordSta2InIn) +
          "{:10.3f}".format(ySta2InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta2InIn + inputGeo['zShearInInSta2'] + inputGeo['zElevOffset']) +
          "{:10.3f}".format(cosElevDeflection * (chordSta2InIn - mainChordSta2InIn)) + '\n') 
fin.write('*       X2        Y2        Z2     CORD2\n')
            
fin.write("{:10.3f}".format(xSta3InIn + mainChordSta3InIn) + \
          "{:10.3f}".format(ySta3InIn) +
 "{:10.3f}".format(tanDihedralWing * ySta3InIn + inputGeo['zShearInInSta3'] + inputGeo['zElevOffset']) +
          "{:10.3f}".format(cosElevDeflection * (chordSta3InIn - mainChordSta3InIn)) + '\n') 
fin.write('*     NVOR      RNCV       SPC       PDL\n')
fin.write('        10     15.00      1.00      0.00\n')
fin.write('*    AINC1     AINC2       ITS       NAP    ')
fin.write('IQUANT     ISYNT       NPP\n')
fin.write("{:10.5f}".format(tanElevDeflection)+ 
         "{:10.5f}".format(tanElevDeflection) + 
         '         0        0          2         0         0\n')
fin.write('*\n')

# Stations that define survey grid (0=No survey, not used)
fin.write('*\n')
fin.write('* NXS   NYS   NZS\n')
fin.write('     0       0      0\n')
fin.write('* END\n')
fin.write('********* End VORLAX Input Deck *********\n')
fin.close()