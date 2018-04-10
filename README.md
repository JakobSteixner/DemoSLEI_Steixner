Introduction
============

This package demonstrates a simple interface between a GUI input console
and scripts that implement scene changes in `.ma` and `.mb` files using
Autodesk Maya's Python interpreter.

Requirements
============

Software
--------

Python 2.7.(>=11), Autodesk Maya 2017, Autodesk Maya's Python interpreter 
needs to be in $PATH

Operating Systems
-----------------

The package has been developed under Ubuntu 16.04 and partially tested under 
MacOS, though without the link to Autodesk Maya -- I failed to install Maya on
my (old) MacBook. It *should* work under Windows -- paths are ensured to be OS-
specific, etc. -- but without any warranty.


Installation
============

Make sure that the true location of mayapy(.exe) -- Autodesk Maya's Python 
interpreter -- is in your system $PATH! On MacOS and Linux, it is found 
under `/usr/autodesk/maya2017/bin/`. Symlinking it e. g. `/usr/local/bin`
can break its ability to import required modules provided by Autodesk.

The only modules that actually use `mayapy` are the ones in the 
`Renderers/render__<GESTURE>` family. Since they are only accessed by 
`Renderers/RPreprocessor`, an alternative would be to hardcode mayapy's 
location there.

With these prerequisites, all you need to do is extract the package into a 
place of your choosing. It does not need to be on Python's path unless you 
want to access it from outside. Relative import within the package has been 
tested to work (at least under Linux and Mac).

Usage
=====

The nexus of the package is the module `Checker.py`, which interacts with the
GUI and sends the result to Maya. It can be called from the command line with
the following call:

$ python Checker.py  <path/to/input/file> <path/to/file/to/modify>

The input file is expected to be a text file with one German sentence and it's 
translation into sign language glosses together in a line, separated with a TAB.
The file to modify is any Maya ascii (`.ma`) or binary (`.mb`). Note that in the
current implementation, the modified scenes are stored in the package's subdirectory
`corrected_scenes` with irrespective of their origin!

Implementation status
=====================

The only implemented GESTURES at the moment are "NOD", linked to the GLOSS "CONFIRM",
and "RAISE_HEAD", linked to "YES". To see an effect, after calling `Checker.py`, submit
once with and once without changing the gloss from "CONFIRM" to "YES", and compare the 
output files.

Core components
==============

GUI for sign language experts
------

The interface is meant for sign language experts, you can quality check
and correct the output of the machine translation system at SiMAX.

The Interface allows users to:

* Change the suggested word orders by klicking on the buttons marked `=>`/
`<=` below and above the bold Glosses.

* Exchange suggested glosses against other registered glosses

* Suggest additions of missing glosses to the database

* View an extended context beyond the current sentence in a pop-up

It does *not* allow to add or remove words, however, if the most natural 
sign language translation is shorter or longer than the one the MT system 
suggests.

Interface to Autodesk Maya
--------------------------

The interface to Autodesk Maya allows (simple) scene changes (currently
implemented: changing the inclination of a head in a sample scene via 
`render__NOD` and `render__RAISE_HEAD`, the only gestures actually implemented.

It does so by grabbing the nodes identifying the head and its subparts by their 
name and then rotating them all around the origin.

When fed an unimplemented gesture, the system currently graciously skips it.

Logging utilities
----------

All transformations that are sent to Maya are logged in the directory `logs`, one 
line per transformation, one file per day.

User requests for improvements and additions are logged separately in 
`requested_additions`

Credits
=======

All Maya files were created with a free student version of Autodesk Maya and are 
for non-commercial use only.

The file `Head_Model.ma` is from [here:](https://www.dropbox.com/s/vtdo9ekju4cggao/Head_Model.ma?dl=0#)
in what I hope constitutes fair use. I found it through the author's very helpfull 
[Youtube channel](https://www.youtube.com/watch?v=1dLYqlm95Cc).
[This guide](https://gist.github.com/borgfriend/b83467639cb8039dc79974bf780a4994) was 
very helpful to get Maya Autodesk successfully installed under Debian/Ubuntu.
