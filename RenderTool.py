import maya.cmds as cmds
import os
import subprocess


TextWidth = 180 # Width Of Text in ButtonLayoutFrame

# Function To Setup Camera initially when SetupCam is pressed #
def SetupCam(*args):
    if cmds.objExists("renderCamera1"):
        cmds.delete("renderCamera1")
    
    renderCam = cmds.camera(name="renderCamera")
    print("Camera Spawned")

    # Reset Existing Fields #
    cmds.intField("DirectionCountField", value=1, e=True)
    cmds.floatField("StartAngleField", value=0, e=True)
    cmds.floatField("MaxAngleField", value=360, e=True)
    cmds.floatField("CameraOffsetField1", value=5, e=True)
    cmds.floatField("CameraOffsetField2", value=10, e=True)

    cmds.checkBox("SplitByDirectionField", value=True, e=True)
    cmds.checkBox("CombineToSpritesheetField", value=True, e=True)

    cmds.intField("ResolutionField1", value=256, e=True)
    cmds.intField("ResolutionField2", value=256, e=True)
    
# Function to Browse Save Folder for the outputs #    
def browseOutputFolder(*args):
    folder = cmds.fileDialog2(dialogStyle=2, fileMode=3, caption="Select Output Folder")
    if folder:
        cmds.textField("OutputFolderField", e=True, text=folder[0])
        print("Output folder set to:", folder[0])

def openSelectedOutputFolder(*args):
    folder = cmds.textField("OutputFolderField", text=True, q=True)
    if cmds.about(nt=True):  # Windows
        os.startfile(folder)
    elif cmds.about(macOS=True):  # macOS
        subprocess.Popen(["open", folder])
    else:  # Linux
        subprocess.Popen(["xdg-open", folder])

# Delete any old tool windows if already open #
if cmds.window("RenderTool", exists=True):
    cmds.deleteUI("RenderTool", window=True)

cmds.window("RenderTool", title="3D to Spritesheet Tool", widthHeight=(300,150))
cmds.paneLayout("MasterLayout", parent="RenderTool", configuration="vertical2", paneSize=[1,70,100], separatorThickness=6)

#cmds.columnLayout("ButtonLayout", parent=MasterLayout, columnOffset=["both", 15])
cmds.frameLayout("ButtonLayout", parent="MasterLayout", marginWidth=15, marginHeight=15, label="Options/Settings", collapsable=True, collapse=False)

#cmds.columnLayout("PreviewLayout", parent=MasterLayout, columnOffset=["both", 15])
cmds.frameLayout("PreviewLayout", parent="MasterLayout", marginWidth=15, marginHeight=15, label="Preview")

cmds.button("InitializeButton", parent="ButtonLayout", label="Initialize", command=SetupCam)
cmds.scrollLayout("ButtonLayoutScrollbar", parent="ButtonLayout", childResizable=True)



# Frame for Camera Setup
cmds.frameLayout("CameraSetupLayout", parent="ButtonLayoutScrollbar", marginWidth=5, marginHeight=5, label="Camera Setup", collapsable=True, collapse=False)
cmds.columnLayout("CameraSetupColumn", parent="CameraSetupLayout", adjustableColumn=True)

cmds.rowLayout("DirectionCountRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("DirectionCountText", parent="DirectionCountRow", label="Number Of Directions: ", width=TextWidth, align="right")
cmds.intField("DirectionCountField", parent="DirectionCountRow", value=1, minValue=1, maxValue=360)

cmds.rowLayout("StartAngleRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("StartAngleText", parent="StartAngleRow", label="Start Angle: ", width=TextWidth, align="right")
cmds.floatField("StartAngleField", parent="StartAngleRow", value=0, minValue=0, maxValue=360)

cmds.rowLayout("MaxAngleRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("MaxAngleText", parent="MaxAngleRow", label="Maximum Angle: ", width=TextWidth, align="right")
cmds.floatField("MaxAngleField", parent="MaxAngleRow", value=360, minValue=0, maxValue=360)

cmds.rowLayout("CameraOffsetFieldRow", parent="CameraSetupColumn", numberOfColumns=3)
cmds.text("CameraOffsetFieldText", parent="CameraOffsetFieldRow", label="Camera Offset (x/y): ", width=TextWidth, align="right")
cmds.floatField("CameraOffsetField1", parent="CameraOffsetFieldRow", value=5, minValue=0)
cmds.floatField("CameraOffsetField2", parent="CameraOffsetFieldRow", value=10, minValue=0)
#cmds.floatFieldGrp("CameraOffsetField", parent="CameraSetupLayout", label="Camera Offset (X,Y): ", numberOfFields=2, value1=5.0, value2=10.0)



# Frame for Spritesheet Settings
cmds.frameLayout("SpritesheetSettingsLayout", parent="ButtonLayoutScrollbar", marginWidth=5, marginHeight=5, label="Spritesheet Settings", collapsable=True, collapse=False)

cmds.rowLayout("SplitByDirectionRow", parent="SpritesheetSettingsLayout", numberOfColumns=3)
cmds.text("SplitByDirectionText", parent="SplitByDirectionRow", label="Split Spritesheet By Direction: ", width=TextWidth, align="right")
cmds.checkBox("SplitByDirectionField", parent="SplitByDirectionRow", label="", value=True)

# 
# ADD COLLUMN INTFIELD HERE LATER
# 

cmds.rowLayout("CombineToSpritesheetRow", parent="SpritesheetSettingsLayout", numberOfColumns=2)
cmds.text("CombineToSpritesheetText", parent="CombineToSpritesheetRow", label="Combine Sprites to Spritesheet: ", width=TextWidth, align="right")
cmds.checkBox("CombineToSpritesheetField", parent="CombineToSpritesheetRow", label="", value=True)

cmds.separator(parent="SpritesheetSettingsLayout")

cmds.button("PreviewSheetButton", parent="SpritesheetSettingsLayout", label="Preview Spritesheet")



#Frame for Render Settings
cmds.frameLayout("RenderSettingsLayout", parent="ButtonLayoutScrollbar", marginWidth=5, marginHeight=5, label="Render Settings", collapsable=True, collapse=False)

cmds.rowLayout("ResolutionRow", parent="RenderSettingsLayout", numberOfColumns=3)
cmds.text("ResolutionText", parent="ResolutionRow", label="Sprite Resolution (W x H): ", width=TextWidth, align="right")
cmds.intField("ResolutionField1", parent="ResolutionRow", value=256, minValue=1)
cmds.intField("ResolutionField2", parent="ResolutionRow", value=256, minValue=1)

#
# ADD BACKGROUND TYPE OPTION MENU HERE
#

#
# ADD LIGHTING PRESET OPTION MENU HERE
#

#
# ADD RENDER METHOD RADIOBUTTONGRP HERE
#

cmds.rowLayout("OutputFolderRow", parent="RenderSettingsLayout", numberOfColumns=3, adjustableColumn=2)
cmds.text("OutputFolderText", parent="OutputFolderRow", label="Output Folder: ", width=TextWidth, align="right")
cmds.textField("OutputFolderField", parent="OutputFolderRow", text="")
cmds.button("BrowseButton", parent="OutputFolderRow", label="Browse", command=browseOutputFolder)




cmds.rowLayout("RenderButtonsRow", parent="ButtonLayout", numberOfColumns=3)
cmds.button("RenderSpriteButton", parent="ButtonLayout", label="Render Sprite")
cmds.button("RenderSheetButton", parent="ButtonLayout", label="Render Sheet")
cmds.button("OpenFolderButton", parent="ButtonLayout", label="Open Folder", command=openSelectedOutputFolder)


cmds.showWindow("RenderTool")



# INPUTS NEEDED #
#---------------#
# Initialize Button #
# Target Mesh (to render/scan) #

# Direction Count # IntField #
# Start Angle # FloatField #
# Max Angle # FloatField #
# Camera Offset # FloatField #

# SplitByDirection # Checkbox #
# Columns # IntField (if SplitByDirection is Off) #
# CombineToSpritesheet # Checkbox #
# PreviewSheet # Button #

# ImageSize/Resolution # intField #
# BackgroundType # OptionMenu #
# LightingPreset # OptionMenu #
# RenderMethod # RadioButtonGrp #
# Output Folder #

# Generate Sprites #
# Generate Sheet #
# Open Folder #