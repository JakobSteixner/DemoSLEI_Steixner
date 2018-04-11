#!/usr/bin/python

import input_parser, prepare_expert_GUI, Renderers.RPreprocessor, sys, os, string, time
sp = os.sep

class Checker_backend():
    def __init__(self, filename, index, context_range):
        input_sentences = self.input_sentences = input_parser.ParseSentence("input_sentences.txt")
        self.source_text = [key for key in input_sentences]
        self.suggested_translation = [input_sentences[key].split() for key in input_sentences]
        self.setcontextrange(context_range)
        self.index = index
    def setcontextrange(self, Range):
        """not currently used"""
        self.setcontextrange = Range
    def send_to_gui(self, **kwargs):
        self.result = prepare_expert_GUI.run(**kwargs)
        self.record()
    def record(self):
        with open("logs"+sp+"changelog"+time.strftime("%Y%m%d")+".log", "a") as log:
            log.write(string.join ([ time.strftime("%Y%m%d%H%M%S"),
                                    "FROM", string.join(self.suggested_translation[self.index], ":"),
                                    "TO", string.join(self.result, ":")], "\t") + "\n")
    def send_to_maya(self, result, targetscene):
        folderpath = string.join(targetscene.split(os.sep)[:-1], os.sep)
        filename = targetscene.split(os.sep)[-1]
        # take reading the lexicon out of the loop
        glosses, gestures = input_parser.glosses(), input_parser.gestures()
        for gloss in self.result:
            idx = glosses.index(gloss)
            # was: idx = input_parser.glosses().index(gloss)
            if glosses[idx] != None:
            # was: if input_parser.gestures()[idx] != None:
                for gesture in gestures[idx]:
                #for gesture in input_parser.gestures()[idx]:
                    #try:
                        success = Renderers.RPreprocessor.run(**{"filepath":folderpath, "oldfilename":filename, "gesture":gesture, "degrees":20})
                        if success == 0:
                            print "we seem to have success rendering"
                            print gesture + " as part of the gloss "+ gloss
                        else:
                            print "Something went wrong trying to copy and render scene."
                            print "Check the stated sample file exists and mayapy is "
                            print "found in your system $PATH"
                    # except:
                    #     print ""
                    #     print "Failure while trying `Renderers.RPreprocessor.run(gesture='%s')`"% gesture
                    #     print "Unable to execute rendering instruction"
                    #     print "for "+gesture+"."
                    #     print "This usually either means that Maya's python"
                    #     print "interpreter is not properly installed/not"
                    #     print "found in $PATH, or that no rendering instruction"
                    #     print 'has been implemented for the gesture ' +gesture
            else:
                print "no gestures currently associated with gloss "+gloss
                print "skipping"
                pass

if __name__ == '__main__':
    if len(sys.argv) < 3: 
        print """"
        In command line usage, this package requires two arguments:
        - the full path to a machine-translated text ready for corrections
        - the full path to a Maya scene to be modified
        """
        exit()
    inputsentences, targetscene = sys.argv[1:]
    checker = Checker_backend(inputsentences,1,1)
    checker.send_to_gui(longinput=inputsentences, index=1)
    print checker.result
    checker.send_to_maya(checker.result, targetscene)

