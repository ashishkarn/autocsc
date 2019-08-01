from tkinter import *
import re
import os
from subprocess import check_output
import subprocess
from threading import Thread
import threading

def callback(textInput,rootdir):
    sourcecode=textInput.get()
    print("Input code generated...")
    if not sourcecode or len(sourcecode.strip())==0:
        print("Empty File...")
        return
    buildname=extractNamespace(sourcecode)
    directoryname=buildDirectories(rootdir,buildname,sourcecode)
    os.chdir(directoryname)
    compilesource(directoryname)
    runsource(directoryname)
    
def compilationthread(a,textInput,rootdir):
    subthread=Thread(target=callback,args=(textInput,rootdir))
    b=a[0]+1
    a[0]=b
    print("Executing on thread : {0}".format(a[0]))
    subthread.start()
        
def main():
    rootdir=os.getcwd()
    root = Tk()
    label1 = Label( root, text="Compile and Run")
    textInput = Entry(root, bd=5)
    a=[0]
    submit = Button(root, text ="Submit", command = lambda: compilationthread(a,textInput,rootdir))
    label1.pack()
    textInput.pack()
    submit.pack(side =BOTTOM)
    root.mainloop()

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
        
def compilesource(directoryname):
    print("Compiling..")
    compilecode="csc -out:executable.exe source.cs"
    try:
        os.system(compilecode)
    except:
        print("Error in compiling")
        

def runsource(directoryname):
    if(os.path.exists("executable.exe")):
        try:
            print("Executing..")
            executecode="cmd.exe /K executable.exe"
            os.system(executecode)            
        except Exception as e:
            print("Error")
            print(e.returncode)
    else:
        print("Executable not found at "+directoryname)
    print("\n############################\n")
                
main()





            
    
    
