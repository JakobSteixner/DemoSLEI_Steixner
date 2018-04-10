#!/usr/bin/python
# -*- coding: utf8 -*-
#
# TODO: replace the string literals in label texts
# with dictionary calls for a polyglot version

import Tkinter as tk
import input_parser, string, os
import tkFont
import time


class Lodge_Request:
    """Window to lodge a request for a GLOSS to be implemented"""
    def __init__(self, master=None):
        #tk.Frame.__init__(self, master)
        self.master = master
        self.build()
        #self.source_text = source_text
    def createWidgets(self):
        self.displbox = tk.Label(self.top,
            text="Bitte benennen Sie die fehlende Glosse\nin einer eigenen Zeile.\nBeschreiben Sie außerdem gerne die dazugehörige\n Gebärde kurz; Links und Quellen willkommen!")
        self.textfield = tk.Text(self.top, height=5, width=50)
        self.cancel_button = tk.Button(master=self.top, text="Abbrechen", command=self.top.destroy)
        self.OK_button = tk.Button(master=self.top, text="Absenden", command=self.record)
    def build(self):
        top = self.top = tk.Toplevel(self.master)
        top.geometry("400x200+100+100")
        self.createWidgets()
        self.top.title(u"Ergänzungsanfrage")
        self.top.grid()
        self.displbox.grid(columnspan=2, row=0)
        self.textfield.grid(columnspan=2, row=1)
        self.OK_button.grid(column=1, row=2)
        self.cancel_button.grid(column=0, row=2)
    def record(self):
        request = self.textfield.get("1.0","end")
        with open(string.join([os.path.abspath("."),"requested_additions","request"+time.strftime("%Y%m%d_%H%M%S")], os.sep), "w") as record:
            record.write(request)
        self.top.destroy()
        


class DisplayContext:
    """Window to display additional context, can be toggled from the main window"""
    def __init__(self, source_text, master=None, ondisplay=False):
        #tk.Frame.__init__(self, master)
        self.master = master
        self.ondisplay = ondisplay
        self.source_text = source_text
    def createWidgets(self):
        displayfont = tkFont.Font(size = 16, weight="bold")
        self.displbox = tk.Label(self.top, text=string.join(self.source_text,"\n"), font=displayfont)
        #
        self.OK_button = tk.Button(master=self.top, text="OK", command=self.top.destroy)
    def build(self):
        top = self.top = tk.Toplevel(self.master)
        top.geometry("300x200+120+120")
        self.createWidgets()
        self.top.title(u"Kontext")
        self.top.grid()
        self.displbox.grid(column=0, row=0)
        self.OK_button.grid(column=0, row=1)



class main():
    """Creates an interface for expert input,
        allowing to move positions of glosses or change
        glosses. Not currently implemented: adding
        or removing glosses.
        
        Known shortcomings: 
        """
    def __init__(self, longinput = None, master=None, index=0, width=0, tk=tk):
        self.tk = tk
        self.width = width
        self.master = master
        self.source = input_parser.ParseSentence(longinput)
        self.original = [entry for entry in self.source]
        self.translation = [self.source[key] for key in self.source]
        #self.suggested_translation = [gloss for gloss in self.translation]
        self.index = index
        self.as_glosses = as_glosses = self.translation[self.index].strip(""" '" """).split()
        self.original_glosses = [gloss for gloss in as_glosses]
    def build(self):
        self.root = self.tk.Tk()
        #self.root.geometry("800x400+300+300")
        self.root.title(u"Bitte verbessern Sie die Übersetzung")
        self.frame = frame = self.tk.Frame()
        self.frame.grid()
        self.createWidgets()
    def set_context(self, text_and_width = None):
        if text_and_width == None:
            text_and_width = (self.original, self.width)
        sourcetext, Range = text_and_width
        context = sourcetext[self.index-self.width:self.index+self.width]
        self.context_textbox = DisplayContext(sourcetext,
                                              master=None)
        
    def createWidgets(self):
        """General setup: Tkinter.Canvas with various Buttons and
        Labels, and drop-down-menues to replace words"""
        self.canvas = self.tk.Canvas(self.frame)
        self.canvas.grid()
        self.sentencelength = sentencelength = len(self.as_glosses)
        displayfont = tkFont.Font(size = 14)
        
        
        """Some helper functions defined here:
        Shifting glosses..."""
        def shift_word_right(position):
            word = self.as_glosses.pop(position)
            self.as_glosses.insert(position+1, word)
            self.redraw()
        def shift_word_left(position):
            word = self.as_glosses.pop(position)
            self.as_glosses.insert(position-1, word)
            self.redraw()
            
        """Displaying/hiding context."""
        def showhide_context():
            #context_ondisplay = status
            if self.context_ondisplay:
                self.context_textbox.top.destroy()
            else:
                self.display_context()
            self.context_ondisplay = not self.context_ondisplay
            self.context_button.destroy()
            self.context_button = refresh_context_button()
    
        def refresh_context_button():
            context_button_labels = ["show context", "hide context"]
            context_button = self.tk.Button(master=self.canvas,text=context_button_labels[self.context_ondisplay],command=showhide_context)
            context_button.grid(columnspan = sentencelength, row=6, pady=6)
            return context_button
        
        """Here comes the actual widgets:"""
        # source of translation
        self.tk.Label(self.canvas, text="Ausgangstext", font=tkFont.Font(size = 16, weight="bold")).grid(columnspan=sentencelength,row=0)
        displcurrentoriginal = self.tk.Label(self.canvas, text=self.original[self.index], font=displayfont)
        displcurrentoriginal.grid(columnspan=sentencelength, row=1)
        #
        displayfont = tkFont.Font(size = 20, weight="bold") #bold type for the actual glosses
        
        # duplicate as_glosses list to store tk.StringVar-results
        # from exchanging glosses, saves us some ugly
        # exec-hacking:
        self.stringvars = stringvars = [gloss for gloss in self.as_glosses]
        
        for column, gloss in enumerate(self.as_glosses):
            
            # left error except for first position:
            if column > 0:
                currentcol = str(column)
                # eval-hack to avoid overwriting
                shift_word_left_button = self.tk.Button(master=self.canvas,text='<=',command=eval("lambda: shift_word_left("+currentcol+")", locals()))
                #exec("shift_word_%d_leftbutton = self.tk.Button(master=self,text='<=',command=shift_left%d)" % (column, column))
                shift_word_left_button.grid(column=column, row=2)
                
            # the actual gloss:
            displaygloss = self.tk.Label(self.canvas, text=gloss,font=displayfont)
            displaygloss.grid(column=column, row=3)
            
            # right arrow except for last position
            if column < sentencelength - 1:
                currentcol = str(column)
                shift_word_right_button = self.tk.Button(master=self.canvas,text='=>',command=eval("lambda: shift_word_right("+currentcol+")", locals()))
                shift_word_right_button.grid(column=column, row=4)
            
            # drop-down menues to select another word
            # formerly implemented as exec-hack
            optionList = (input_parser.glosses())
            v = self.tk.StringVar()
            #exec("self.gloss_chosen%d = v = self.tk.StringVar()" % column, locals())
            v.set(gloss)
            stringvars[column] = v
            self.om= self.tk.OptionMenu (self.canvas, v, *optionList , command=self.redraw_from_om)
            self.om.grid(column=column,row=5)
        
        # context display button
        self.context_ondisplay = False
        self.context_button = refresh_context_button()
        
        # last not least, we want to be able to submit our results
        submit_button = self.tk.Button(master=self.canvas, text=u"Übersetzung akzeptieren", command=self.submit)
        submit_button.grid(columnspan=sentencelength/2, column=(sentencelength+1)/2, row=7, pady=6)
        request_addition_button = self.tk.Button(master=self.canvas, text=u"Glossen-Implementierung anfordern", command=self.request_addition)
        request_addition_button.grid(columnspan=sentencelength/2, row=7, pady=7)
    def request_addition(self):
        entryfield = Lodge_Request(master=None)
    def redraw_from_om(self, event):
        self.update_glosses()
        self.redraw()
    def redraw(self):
        """Draw a new canvas with updated input"""
        self.canvas.destroy()
        self.createWidgets()
        pass
    def update_glosses(self):
        self.as_glosses = [var.get() for var in self.stringvars]
    def display_context(self):
        context = (string.join([entry for entry in self.original]),self.width)
        self.set_context()
        self.context_textbox.build()
    def submit(self):
        """
        The submit function stores the updated glosses and their
        positions in the property `self.as_glosses` (list type).
        This is what the calling object should be requesting!
        
        It then proceeds to tear down the GUI.
        """
        self.update_glosses()
        self.root.destroy()

def run(longinput = "input_sentences.txt", index=1, width=1):
    app = main( longinput, master = None, index=index, width=width)
    app.build()
    app.root.wait_window()
    result = app.as_glosses
    return result



if __name__ == '__main__':
    print "=== RESULT ==="
    print run()

#print app
#app.context_textbox.mainloop()

        
