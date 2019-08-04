from tkinter import *
import re
import os
from subprocess import check_output
import subprocess
from threading import Thread
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown

def main():
    Window.clearcolor = rgba(222, 222, 222, 1)
    AutoCSC().run()
    
#GUI Container and main thread
def callback(textInput,rootdir,outputArea):
    sourcecode=textInput.text
    outputArea.text = "Input code generated..."
    if not sourcecode or len(sourcecode.strip())==0:
        outputArea.text = "Empty File..."
        return
    buildname=extractNamespace(sourcecode)
    directoryname=buildDirectories(rootdir,buildname,sourcecode)
    os.chdir(directoryname)
    dllflag=check_for_dll(sourcecode)
    compilesource(dllflag,directoryname,outputArea)
    runsource(directoryname,outputArea)
    
def compilationthread(threadCount,textInput,rootdir,outputArea):
    subthread=Thread(target=callback,args=(textInput,rootdir,outputArea))
    b=threadCount[0]+1
    threadCount[0]=b
    print("Executing on thread : {0}".format(threadCount[0]))
    subthread.start()
    threadCount[0]=threadCount[0]-1

def rgba(R, G, B, A):
    return (R/255, G/255, B/255, A)

class Container(GridLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.rows = 4
        self.threadCount=[0]
        self.rootdir=os.getcwd()

        self.menuBar = GridLayout(cols = 5, size_hint_y = None, height = 20)
        self.textArea = TextInput(multiline = True, background_color = rgba(255, 255, 255, 1))
        self.buttonLayout = GridLayout(cols = 3, size_hint_y = 0.05, spacing = 1)
        self.outputLabel = Label(text = 'Output:', color = rgba(1, 1, 1, 1))
        self.executeButton = Button(text = 'Execute', background_normal = '', background_color = rgba(32, 170, 14, 1), size_hint_x = 0.25, on_press=lambda x: compilationthread(self.threadCount,self.textArea,self.rootdir,self.outputArea))
        self.outputArea = TextInput(multiline = True, background_color = rgba(222, 222, 222, 1), size_hint_y = 0.35)

        self.add_widget(self.menuBar)
        self.add_widget(self.textArea)
        self.buttonLayout.add_widget(self.outputLabel)
        self.buttonLayout.add_widget(self.executeButton)
        self.add_widget(self.buttonLayout)
        self.add_widget(self.outputArea)

class AutoCSC(App):
    def build(self):
        return Container()

#Compilation and execution specific routines
def extractNamespace(sourcecode):
    buildnames=re.findall(r"\nnamespace \S+", sourcecode)
    if len(buildnames)==0:
        print("No namespace found, Generating a new name...")
        buildnames.append("\nnamespace genr")
    print("buildName = "+buildnames[0].strip('\n'))
    return buildnames[0]

def buildDirectories(rootdir,buildname,sourcecode):
    os.chdir(rootdir)
    print("Present Working dir changed to: {0}".format(os.getcwd()))
    if not os.path.exists("builds/"):
        os.mkdir("builds/")
    directoryname="builds/" + re.sub('[^A-Za-z0-9]+', '_', buildname)
    if not os.path.exists(directoryname):
        os.mkdir(directoryname)
    else:
        #iterate with different names suffixed with natural numbers
        for i in range(1,1000):
            if not os.path.exists(directoryname+str(i)):
                directoryname=directoryname+str(i)
                os.mkdir(directoryname)
                break
            else:
                continue
    print("Directory created at: "+ directoryname)
    #create source file
    sourcefile=open(directoryname+"/source.cs","w+")
    sourcefile.write(sourcecode)
    sourcefile.close()
    return directoryname

def check_for_dll(sourcecode):
    mainPresence=re.findall(r"static void Main", sourcecode)
    if(len(mainPresence)==0):
        return True
    return False

def compilesource(dllflag, directoryname, outputArea):
    outputArea.text = "Compiling..."
    compilecode="csc -out:executable.exe source.cs"
    compilecode2="csc -target:library -out:library.dll source.cs"
    try:
        if(dllflag==True):
            print("Compiling library.dll")
            os.system(compilecode2)
        else:
            print("Compiling executable.exe")
            os.system(compilecode)
    except:
        print("Error in compiling")
        
def runsource(directoryname,outputArea):
    if(os.path.exists("executable.exe")):
        outputArea.text = "Executing..."
        executecode='start cmd.exe /K executable.exe'
        os.system(executecode)
    else:
        print("Executable not found at "+directoryname)
    print("\n############################\n")
                
main()





            
    
    
