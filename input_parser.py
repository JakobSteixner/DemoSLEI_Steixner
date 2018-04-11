#!/usr/bin/python
from collections import OrderedDict, namedtuple

def ParseSentence(from_file):
    """for reading the input sentences"""
    sentences = OrderedDict()
    for line in open(from_file).read().strip().split("\n"):
        try:
            sentences[line.split("\t")[0]] = line.split("\t")[1]
        except IndexError:
            pass
    return sentences



class Gloss_list_parser():
    """provides the information in "glossslist.csv" in handy
    formats to other classes"""
    def __init__(self, from_file, sep =""):
        self.indices, self.glosses, self.types, self.gesture_lists = [],[],[], []
        inputfile = open(from_file).read().strip()
        sep = sep.strip(" ") # to avoid problems with " " as sep
        for line in inputfile.split("\n")[1:]:
            try: splitline = line.strip().split(sep)
            except: splitline = line.strip().split()
            self.indices.append(splitline[0])
            self.glosses.append(splitline[1])
            self.types.append(splitline[2])
            try:
                self.gesture_lists.append(splitline[3])
            except IndexError:
                self.gesture_lists.append(None)
                

def glosses(from_file = "glosslist.csv"):
    """function to return a list of glosses, consider using
    Gloss_list parser directly if you also need gestures and/or
    types to minimize file handling."""
    reader = Gloss_list_parser(from_file)
    return reader.glosses

def gestures (from_file = "glosslist.csv"):
    """function to return a list of gestures, consider using
    Gloss_list parser directly if you also need glosses and/or
    types to minimize file handling."""
    reader = Gloss_list_parser(from_file)
    def forcesplit(stringornone, sep=" "):
        try:
            return stringornone.split(sep)
        except AttributeError:
            return stringornone
    return [forcesplit(line, ":") for line in reader.gesture_lists]

def types(from_file= "glosslist.csv"):
    """function to return a list of types, consider using
    Gloss_list parser directly  if you also need gestures
    and/or glosses to minimize file handling."""
    reader = Gloss_list_parser(from_file)
    return reader.types


