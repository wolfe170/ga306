from PySide2 import QtWidgets
from PySide2 import QtGui
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken2

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(pointer), QtWidgets.QWidget)







###CHECK FOR EXISTING WINDOW###


myWindow = 'myWin'

if cmds.window('myWin', exists = True):
    cmds.deleteUI('myWin', wnd = True)

    
    
    
    
    
    
    
###SET GLOBAL VIDEOS###



lowPolyMainGroup = []
highPolyMainGroup = []

lpName = ''
hpName = ''

lowPolyAllChildren = []
highPolyAllChildren = []











### CREATE FUNCTIONS ###



#SELECT GROUPS


def selectLPGroup():
    global lowPolyAllChildren
    global lowPolyMainGroup
    global lpName

    lowPolyMainGroup = cmds.ls(selection=True)
    lpName = lowPolyMainGroup[0]
    lowPolyAllChildren = cmds.listRelatives(lowPolyMainGroup, ad=True)
    
    for n in lowPolyAllChildren:
        if n[-5:] == 'Shape':
            lowPolyAllChildren.remove(n)

    LPTextField.setText(lpName)

    
def selectHPGroup():
    global highPolyAllChildren
    global highPolyMainGroup
    global hpName  
    
    highPolyMainGroup = cmds.ls(selection=True)
    hpName = highPolyMainGroup[0]
    highPolyAllChildren = cmds.listRelatives(highPolyMainGroup, ad=True)
    
    for n in highPolyAllChildren:
        if n[-5:] == 'Shape':
            highPolyAllChildren.remove(n)
    
    HPTextField.setText(hpName)
    
      
        
        
#REDEFINE GROUP LISTS


def resetGroupItems():
    global lowPolyAllChildren
    global highPolyAllChildren
    global lowPolyMainGroup
    global highPolyMainGroup

    lowPolyAllChildren = cmds.listRelatives(lowPolyMainGroup, ad=True)
    
    for n in lowPolyAllChildren:
        if n[-5:] == 'Shape':
            lowPolyAllChildren.remove(n)
    highPolyAllChildren = cmds.listRelatives(highPolyMainGroup, ad=True)
    
    for n in highPolyAllChildren:
        if n[-5:] == 'Shape':
            highPolyAllChildren.remove(n)
            


            
            
#CLEAR GROUPS


def clearLP():
    global lowPolyAllChildren
    global lowPolyMainGroup
    global lpName

    lowPolyMainGroup = []
    lpName = ''
    lowPolyAllChildren = []

    LPTextField.setText('Select LP Group and hit the button')
    

def clearHP():
    global highPolyAllChildren
    global highPolyMainGroup
    global hpName

    highPolyMainGroup = []
    hpName = ''
    highPolyAllChildren = []

    HPTextField.setText('Select HP Group and hit the button')
    
    
    

#ERROR PREFIX


def errorLP():
    global lowPolyAllChildren
    global highPolyAllChildren

    for n in lowPolyAllChildren:
        if (n[:10]) != 'NOT_IN_HP_':
            if n in highPolyAllChildren:
                print(n + ' exists in high poly group')
            elif n[:-4] in highPolyAllChildren:
                print(n + ' exists in high poly group')
            elif (n+'_high') in highPolyAllChildren:
                print(n + ' exists in high poly group')
            elif (n[:-4]+'_high') in highPolyAllChildren:
                print(n + ' exists in high poly group')
            else:
                cmds.rename(n, 'NOT_IN_HP_'+n)          
    resetGroupItems()

        
def errorHP():
    global lowPolyAllChildren
    global highPolyAllChildren

    for n in highPolyAllChildren:
        if (n[:10]) != 'NOT_IN_LP_':
            if n in lowPolyAllChildren:
                print(n + ' exists in low poly group')
            elif n[:-5] in lowPolyAllChildren:
                print(n + ' exists in low poly group')
            elif (n+'_low') in lowPolyAllChildren:
                print(n + ' exists in low poly group')
            elif (n[:-5]+'_low') in lowPolyAllChildren:
                print(n + ' exists in low poly group')
            else:
                cmds.rename(n, 'NOT_IN_LP_'+n)           
    resetGroupItems()
    
    
    
    
#REMOVE ERROR PREFIX


def errorLP_undo():
    global lowPolyAllChildren

    for n in lowPolyAllChildren:
        if (n[:10]) == 'NOT_IN_HP_':
            cmds.rename(n, n[10:])
    resetGroupItems()


def errorHP_undo():
    global highPolyAllChildren

    for n in highPolyAllChildren:
        if (n[:10]) == 'NOT_IN_LP_':
            cmds.rename(n, n[10:])
    resetGroupItems()

    
    
    
    
#ADD SUFFIXES


#THIS ONE ALLOWS FUNCTION TO RENAME THROUGH NESTED GROUPS

def addSuffix(previousGroup, previousGroupName, previousChildren, suffix):
    
    suffixValue = len(suffix)
    counter=0
    
    for i in range(len(previousChildren)):
        cmds.select(previousGroupName+previousChildren[i])
        currentGroup = cmds.ls(selection=True)
        currentChildren = cmds.listRelatives(currentGroup, children=True)
        currentGroupName = currentGroup[0]+'|'
        
        if currentChildren[0][-5:] == 'Shape':
            if (previousChildren[counter][-suffixValue:]) != suffix:
                cmds.rename(previousGroupName+previousChildren[counter], previousChildren[counter]+suffix)  
            counter+=1
        else:
            addSuffix(currentGroup, currentGroupName, currentChildren, suffix)
            if (previousChildren[counter][-suffixValue:]) != suffix:
                cmds.rename(previousGroupName+previousChildren[counter], previousChildren[counter]+suffix)
            counter+=1
            
            
            
def suffixLP():
    global lowPolyMainGroup
    global lowPolyAllChildren
    global lpName
    
    currentChildren = cmds.listRelatives(lowPolyMainGroup, children=True)
    currentGroupName = lowPolyMainGroup[0]+'|'
    
    
    addSuffix(lowPolyMainGroup, currentGroupName, currentChildren, '_low')
    cmds.select(lowPolyMainGroup)
    if (lowPolyMainGroup[0][-4:]) != '_low':
        cmds.rename(lowPolyMainGroup[0], lowPolyMainGroup[0]+'_low')
    selectLPGroup()    
    resetGroupItems()
    
    
    
def suffixHP():
    global highPolyMainGroup
    global highPolyAllChildren
    global hpName
    
    currentChildren = cmds.listRelatives(highPolyMainGroup, children=True)
    currentGroupName = highPolyMainGroup[0]+'|'
    
    
    addSuffix(highPolyMainGroup, currentGroupName, currentChildren, '_high')
    cmds.select(highPolyMainGroup)
    if (highPolyMainGroup[0][-5:]) != '_high':
        cmds.rename(highPolyMainGroup[0], highPolyMainGroup[0]+'_high')
    selectHPGroup()    
    resetGroupItems()
    
    
    
    
#REMOVE SUFFIXES


def suffixLP_undo():
    global lowPolyAllChildren
    
    for k in lowPolyAllChildren:
        if (k[-4:]) == '_low':
            cmds.rename(k, k[:-4])
    cmds.select(lowPolyMainGroup)
    if (lowPolyMainGroup[0][-4:]) == '_low':
        cmds.rename(lowPolyMainGroup[0], lowPolyMainGroup[0][:-4])
    selectLPGroup()    
    resetGroupItems()


def suffixHP_undo():
    global highPolyAllChildren
    
    for k in highPolyAllChildren:
        if (k[-5:]) == '_high':
            cmds.rename(k, k[:-5])
    cmds.select(highPolyMainGroup)
    if (highPolyMainGroup[0][-5:]) == '_high':
        cmds.rename(highPolyMainGroup[0], highPolyMainGroup[0][:-5])
    selectHPGroup()   
    resetGroupItems()
    

    
    
    
###CREATE GUI    
    
    
    
    
#CREATE MAIN WINDOW

parent = getMayaWindow()
window = QtWidgets.QMainWindow(parent)
window.setObjectName(myWindow)
window.setWindowTitle('Export Manager')
window.setMinimumSize(500,275)
window.setMaximumSize(500,275)


#CREATE MAIN WIDGET
mainWidget = QtWidgets.QWidget()
window.setCentralWidget(mainWidget)


#CREATE FONT

font = QtGui.QFont()
font.setPointSize(8)
font.setBold(True)


#CREATE SPACERS

spacer1 = QtWidgets.QSpacerItem(40,0)
spacer2 = QtWidgets.QSpacerItem(30,0)
spacerVert = QtWidgets.QSpacerItem(0,15)


#CREATE MAIN VERTICLE LAYOUT

mainLayout = QtWidgets.QVBoxLayout(mainWidget)


#CREATE LOW POLY GROUP LAYOUT

LPGrpLayout = QtWidgets.QHBoxLayout()
mainLayout.addLayout(LPGrpLayout)

LPGButton = QtWidgets.QPushButton('Low Poly Group')
LPGrpLayout.addWidget(LPGButton)
LPGButton.setMinimumWidth(150)
LPGButton.setMaximumWidth(150)
LPGButton.setFont(font)
LPGButton.clicked.connect(selectLPGroup)

LPTextField = QtWidgets.QLineEdit()
LPGrpLayout.addWidget(LPTextField)
LPTextField.setText('Select LP Group and hit the button')
LPTextField.setMinimumWidth(200)
LPTextField.setMaximumWidth(200)

LPClearButton = QtWidgets.QPushButton('Clear')
LPGrpLayout.addWidget(LPClearButton)
LPClearButton.setMinimumWidth(100)
LPClearButton.setMaximumWidth(100)
LPClearButton.setFont(font)
LPClearButton.clicked.connect(clearLP)


#CREATE HIGH POLY GROUP LAYOUT

HPGrpLayout = QtWidgets.QHBoxLayout()
mainLayout.addLayout(HPGrpLayout)
mainLayout.addSpacerItem(spacerVert)

HPGButton = QtWidgets.QPushButton('High Poly Group')
HPGrpLayout.addWidget(HPGButton)
HPGButton.setMinimumWidth(150)
HPGButton.setMaximumWidth(150)
HPGButton.setFont(font)
HPGButton.clicked.connect(selectHPGroup)

HPTextField = QtWidgets.QLineEdit()
HPGrpLayout.addWidget(HPTextField)
HPTextField.setText('Select HP Group and hit the button')
HPTextField.setMinimumWidth(200)
HPTextField.setMaximumWidth(200)

HPClearButton = QtWidgets.QPushButton('Clear')
HPGrpLayout.addWidget(HPClearButton)
HPClearButton.setMinimumWidth(100)
HPClearButton.setMaximumWidth(100)
HPClearButton.setFont(font)
HPClearButton.clicked.connect(clearHP)


#CREATE HORIZONTAL ERROR LAYOUT

errorLayout = QtWidgets.QHBoxLayout()
mainLayout.addLayout(errorLayout)
errorLabel = QtWidgets.QLabel('Check for Errors:')
errorLabel.setFont(font)
errorLayout.addSpacerItem(spacer1)
errorLayout.addWidget(errorLabel)
mainLayout.addSpacerItem(spacerVert)


#CREATE CHECK ERRORS BUTTON

checkErrorsLayout = QtWidgets.QVBoxLayout()
errorLayout.addLayout(checkErrorsLayout)

LPErrorsButton = QtWidgets.QPushButton('Check for LP Errors')
checkErrorsLayout.addWidget(LPErrorsButton)
LPErrorsButton.setMinimumWidth(150)
LPErrorsButton.setMaximumWidth(150)
LPErrorsButton.setFont(font)
LPErrorsButton.clicked.connect(errorLP)

HPErrorsButton = QtWidgets.QPushButton('Check for HP Errors')
checkErrorsLayout.addWidget(HPErrorsButton)
HPErrorsButton.setMinimumWidth(150)
HPErrorsButton.setMaximumWidth(150)
HPErrorsButton.setFont(font)
HPErrorsButton.clicked.connect(errorHP)


#CREATE UNDO CHECK ERRORS BUTTON

removeErrorsLayout = QtWidgets.QVBoxLayout()
errorLayout.addLayout(removeErrorsLayout)

removeLPErrorsButton = QtWidgets.QPushButton('Remove Error Marks')
removeErrorsLayout.addWidget(removeLPErrorsButton)
removeLPErrorsButton.setMinimumWidth(150)
removeLPErrorsButton.setMaximumWidth(150)
removeLPErrorsButton.setFont(font)
removeLPErrorsButton.clicked.connect(errorLP_undo)

removeHPErrorsButton = QtWidgets.QPushButton('Remove Error Marks')
removeErrorsLayout.addWidget(removeHPErrorsButton)
removeHPErrorsButton.setMinimumWidth(150)
removeHPErrorsButton.setMaximumWidth(150)
removeHPErrorsButton.setFont(font)
removeHPErrorsButton.clicked.connect(errorHP_undo)


#CREATE SUFFIX HORIZONTAL LAYOUT

suffixLayout = QtWidgets.QHBoxLayout()
mainLayout.addLayout(suffixLayout)
suffixLabel = QtWidgets.QLabel('Add/Remove Suffix:')
suffixLabel.setFont(font)
suffixLayout.addSpacerItem(spacer2)
suffixLayout.addWidget(suffixLabel)
mainLayout.addSpacerItem(spacerVert)


#CREATE ADD SUFFIX BUTTON

addSuffixLayout = QtWidgets.QVBoxLayout()
suffixLayout.addLayout(addSuffixLayout)

LPSuffixButton = QtWidgets.QPushButton('Add _low')
addSuffixLayout.addWidget(LPSuffixButton)
LPSuffixButton.setMinimumWidth(150)
LPSuffixButton.setMaximumWidth(150)
LPSuffixButton.setFont(font)
LPSuffixButton.clicked.connect(suffixLP)

HPSuffixButton = QtWidgets.QPushButton('Add _high')
addSuffixLayout.addWidget(HPSuffixButton)
HPSuffixButton.setMinimumWidth(150)
HPSuffixButton.setMaximumWidth(150)
HPSuffixButton.setFont(font)
HPSuffixButton.clicked.connect(suffixHP)


#CREATE REMOVE SUFFIX BUTTON

removeSuffixLayout = QtWidgets.QVBoxLayout()
suffixLayout.addLayout(removeSuffixLayout)

removeLPSuffixButton = QtWidgets.QPushButton('Remove Suffix')
removeSuffixLayout.addWidget(removeLPSuffixButton)
removeLPSuffixButton.setMinimumWidth(150)
removeLPSuffixButton.setMaximumWidth(150)
removeLPSuffixButton.setFont(font)
removeLPSuffixButton.clicked.connect(suffixLP_undo)

removeHPSuffixButton = QtWidgets.QPushButton('Remove Suffix')
removeSuffixLayout.addWidget(removeHPSuffixButton)
removeHPSuffixButton.setMinimumWidth(150)
removeHPSuffixButton.setMaximumWidth(150)
removeHPSuffixButton.setFont(font)
removeHPSuffixButton.clicked.connect(suffixHP_undo)








#SHOW WINDOW AKA RUN THIS SHIT


window.show()