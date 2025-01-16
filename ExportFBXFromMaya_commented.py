import maya.cmds as cmds
import os
from maya import OpenMayaUI
from shiboken6 import wrapInstance
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ExportToolUI(QWidget):  
   #creates gui window for the tool
   
   def __init__(self, parent = None):
      super(ExportToolUI, self).__init__(parent)

      self.setWindowFlags(Qt.Window)

      self.setObjectName('ExportToolUI_uniqueID') #set the object name

      #customize the UI window
      self.setWindowTitle("Animation FBX Export")
      self.setGeometry(50,50,250,150)

      #add widgets to your window
      self.build_ui()
      self.connect_ui()
    
   def build_ui(self): 
      #create a button 

      vlayout = QVBoxLayout()
      self.runScriptButton = QPushButton("Export Animation as FBX", self) 
      vlayout.addWidget(self.runScriptButton) 

   def connect_ui(self): 
      # the button will run the script when pressed
      self.runScriptButton.clicked.connect(self.exportAnimation) 
   
   def exportAnimation(self): 
      #here is the purpose of the tool.  This function will ask the user to name the file and then export it as an fbx 

      text, ok = QInputDialog.getText(self, "QInputDialog.getText()", #creates a pop up asking the user to input a name for the file
                                "User name:", QLineEdit.Normal,
                                QDir.home().dirName())
      fileName = text 
      filePath = f'D://Dropbox//Personal//FrankieAnims//MayaExports//{fileName}.fbx' 
      #the file path is hardcoded because this tool is meant to be used for specific project pipeline, this is where the exported animations will live
       
      cmds.file( filePath, force=True, type="FBX export", preserveReferences=False, exportSelected=True, constraints=True) 
      # determines where the file will be exported, it will override an existing file with the same name if needed, won't preserve references, 
      # will only export selected objects, and will maintain constraints.

def getMainWindow():
       ptr = OpenMayaUI.MQtUtil.mainWindow()
       maya_window = wrapInstance(int(ptr), QWidget)
       return maya_window
   
maya_window = getMainWindow()
try:
   tool.close()
except NameError:
   pass
tool = ExportToolUI(maya_window)
tool.show()