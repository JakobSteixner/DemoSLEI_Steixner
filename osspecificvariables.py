import sys
import subprocess

if sys.platform.startswith("win"):
    mayapy = "mayapy.exe"
    python = "python.exe"
    
    
else:
    # on UNIX-like systems including MacOS
    mayapy = subprocess.check_output((r"echo $(which mayapy)"), shell=True).strip()
    python = "python"

if mayapy == "":
    print ("Cannot seem to find an executable Maya-Python binary")


#print mayapy



