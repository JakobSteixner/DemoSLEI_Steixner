#SampleScene.py
"""
Maya-Python script to rotate 
"""
import sys
import maya.standalone as std                                                                                                 
std.initialize(name='python') 
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds
		
maya.cmds.file(sys.argv[1], open=True)

print ("opening file ", sys.argv[1])
		
allface = "R_Eye_Ball L_Eye_Ball L_Gum L_Teeth U_Gum U_Teeth Tongue Head2 Cap".split()

print ("selecting parts ", allface)
	
for part in allface:
    maya.cmds.rotate(str(360-int(sys.argv[2])) + "deg", 0, 0, part, pivot = (0,0,0),translate=True)

print "rotation completed"
maya.cmds.file( save=True, type='mayaAscii' )

exit()