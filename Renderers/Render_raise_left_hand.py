import sys
sys.path.append("/usr/autodesk/maya2017/lib/python2.7/site-packages/")
import maya.standalone
import maya.cmds
print dir(maya.cmds)

maya.cmds.sphere(radius=4)