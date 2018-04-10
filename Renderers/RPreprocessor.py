#!/bin/python
import sys, os, subprocess
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("."))
#print sys.path
if __name__ != '__main__':
    submodule =  __name__[:__name__.rfind(".")]
else:
    submodule = ""

from osspecificvariables import *


#print mayapy
#exit()
import subprocess, sys, os, string
import time
sp = os.sep


class Render(object):
    """Calls function `render__<GESTURE>` if implemented,
    passes otherwise; arguments:
    * filepath: string, path to file to be modified (without filename)
    * filename: string, name of source file
    * gesture: string, conventionally capitalised
    * degrees: int or float, required for some gestures, ignored elsewhere
    
    """
    
    def __init__(self, filepath, oldfilename, gesture, degrees=30, timestamp=None):
        try:
            self.degrees = degrees
        except NameError:
            pass
        if isinstance(filepath, basestring):
            self.path_to_file = filepath.split(sp)
        else: self.path_to_file = filepath
        self.copy_ma(oldfilename)
        self.render_gloss(gesture)
    def copy_ma(self, filename):
        """Copies the input file via subprecess and
        returns the name of the new file as a string
        format: old_file_name.timestamp.ext;
        assumes that the old file has no "n" in its
        filename proper - any part between dots
        will be ignored!"""
        filenamebase = filename.split(".")[0]
        fileext = filename.split(".")[-1]
        current_time = time.strftime("%Y%m%d_%H%M%S")
        new_filename = string.join([filenamebase, current_time,fileext], ".")
        self.newpath = string.join(self.path_to_file[:-1] + ["corrected_scenes", new_filename],sp)
        # create copy of sample scene in folder `corrected_scenes`
        subprocess.call(["cp", string.join(self.path_to_file + [filename],sp), self.newpath])
    def render_gloss(self, gesture):
        try:
            print "gesture "+gesture+": It looks like we're succeeding sending stuff oof to maya"
            subprocess.call([mayapy, os.path.abspath(".")+sp+submodule+sp+"render__"+gesture+".py", self.newpath, str(self.degrees)])
        except OSError:
            print "mayapy seems not to be found on path, failed to execute", "render__"+gesture+".py"
            pass



if __name__ == '__main__':
    gesture = sys.argv[1]
    try: degrees = sys.argv[2]
    except IndexError: degrees = 30
    Render(os.path.abspath, "Head_Model.ma", gesture, degrees)

else:
    def run(**args):
        """
        required params:
        - filepath
        - oldfilename
        - gesture
        -degrees
        optional: timestamp
        """
        
        Render(**args)

