# -*- coding: utf-8 -*-

import os
import shutil

template = """
\\documentclass{beamer}

\\mode<presentation>
{
\\usetheme{Warsaw}
\\setbeamercovered{transparent}
}

\\usepackage[english]{babel}
\\usepackage[latin1]{inputenc}
\\usepackage{mathptmx}
\\usepackage[scaled=.90]{helvet}
\\usepackage{courier}


\\usepackage[T1]{fontenc}

\\begin{document}

\\begin{frame}
\\begin{center}
{\\LARGE \\textbf{%s}}
\\end{center}
\\end{frame}

%s
\\end{document}
"""

framestring = """
\\begin{frame}
\\frametitle{%s}
\\includegraphics[height=0.8\\textheight]{%s}
\\end{frame}
"""

sectionstring = """
\\begin{frame}
    \\begin{center}
      \\Large
      \\textbf{%s}
    \\end{center}
\\end{frame}
"""


class PyTeX(object):
    
    WorkingFolder = '/tmp'
    
    def __init__(self, title, pdffilepath):
        self.__pdffilepath = os.path.abspath(pdffilepath)
        self.__title = title
        self.__body = ""
        
    def addfig(self, figtitle, figpath):
        self.__body += framestring % (figtitle, figpath)
        
    def addSection(self, sectionName):
        self.__body += sectionstring % sectionName
        
    def addToBody(self, string):
        self.__body += string
        
    def compile(self):
        f = open(self.WorkingFolder + '/workfile.tex', 'w')
        f.write(template % (self.__title, self.__body))
        f.flush()
        f.close()
        os.chdir('/tmp')
        os.system('bash --login -c "pdflatex ' + self.WorkingFolder + '/workfile.tex"')
        os.system('bash --login -c "pdflatex ' + self.WorkingFolder + '/workfile.tex"')
        if os.path.isfile(self.WorkingFolder + '/workfile.pdf'):
            print self.WorkingFolder + '/workfile.pdf -> ' + self.__pdffilepath
            shutil.copy(self.WorkingFolder + '/workfile.pdf', self.__pdffilepath)
            os.remove(self.WorkingFolder + '/workfile.pdf')
        else:
            print 'pdf creation failed'
