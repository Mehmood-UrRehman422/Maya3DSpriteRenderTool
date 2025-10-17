import maya.cmds as cmds
import maya.mel as mel
import os
import subprocess
import math


TextWidth = 180 # Width Of Text in ButtonLayoutFrame

# DEFAULT CONSTANTS #
# ----------------- #
defaultDirection = 1
defaultDirectionCount = 4

defaultCamStartAngle = 0
defaultCamMaxAngle = 360

defaultCamProximity = 5
defaultCamHeight = 2

defaultCamResolutionX = 256
defaultCamResolutionY = 256

defaultCamMaxResolution = 8192

default_path = ""


# MODIFIED VARIABLES #
# ------------------ #
camDirection = 0
camDirectionCount = 0

camStartAngle = 0.0
camMaxAngle = 0.0

camProximity = 0.0
camHeight = 0.0

PerRenderRotation = 0.0

camResolutionX = 0
camResolutionY = 0


# Function To Setup Camera initially when SetupCam is pressed #
def SetupCam(*args):
    UpdateTempOutputPath()

    if cmds.objExists("renderCamera1"):
        cmds.delete("renderCamera1")
    
    renderCam = cmds.camera(name="renderCamera")
    print("Camera Spawned")

    # Reset Existing Fields #
    cmds.intField("DirectionCountField", value=defaultDirectionCount, e=True)
    cmds.floatField("StartAngleField", value=defaultCamStartAngle, e=True)
    cmds.floatField("MaxAngleField", value=defaultCamMaxAngle, e=True)
    cmds.floatField("CameraProximityField", value=defaultCamProximity, e=True)
    cmds.floatField("CameraHeightField", value=defaultCamHeight, e=True)

    cmds.checkBox("SplitByDirectionField", value=True, e=True)
    cmds.checkBox("CombineToSpritesheetField", value=True, e=True)

    cmds.intField("ResolutionField1", value=defaultCamResolutionX, e=True)
    cmds.intField("ResolutionField2", value=defaultCamResolutionY, e=True)

    UpdateCameraDirectionCount()
    UpdateCameraHeight()
    UpdateCameraProximity()
    UpdateCameraStartAngle()
    UpdateCameraMaxAngle()
    UpdatePerRenderRotation()
    UpdatePreviewRotation()
    UpdateCameraPosition()
    ResolutionChanged()
    RefreshPreview()

def CheckCameraExists(Camera):
    if not cmds.objExists(Camera):
        cmds.warning("Render Camera not found! Please initialize first.")
        return








def UpdateTempOutputPath():
    global default_path
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "sprite_preview", type="string")
    cmds.setAttr("defaultRenderGlobals.enableDefaultLight", 1)
    default_project_images = cmds.workspace(expandName="images")
    #default_project_images = cmds.workspace(expandName="tmp")
    default_path = os.path.normpath(os.path.join(default_project_images, "tmp", "sprite_preview.jpg")).replace("\\", "/")
    #default_path = os.path.join(default_project_images, "sprite_preview.jpg")

def fix_path(path):
    """
    Ensures file paths are compatible with Maya across Windows/macOS/Linux.
    Converts all slashes to forward (/) and expands environment variables.
    """
    if not path:
        return ""
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    return path.replace("/", "\\")

def RefreshPreview():
    global default_path
    CheckCameraExists("renderCamera1")
    cmds.render("renderCamera1", x=camResolutionX, y=camResolutionY)
    #cmds.render("renderCamera1", x=256, y=256, writeImage=preview_path)
    #mel.eval("render 'renderCamera1' -x 256 -y 256 -rd '{preview_path}'")
    #mel.eval(f'render "renderCamera1" -x 256 -y 256 -l {preview_path}')
    cmds.image("PreviewImage", e=True, image=default_path)
    print(cmds.image("PreviewImage", q=True, image=True))
    print(f"Preview updated: {default_path}")
#"C:\\Users\\MRehm\\Documents\\maya\\projects\\default\\images\\tmp\\sprite_preview.jpg"
#RefreshPreview()






# Update Camera Direction Count #
def UpdateCameraDirectionCount(*args):
    CheckCameraExists("renderCamera1")
    global camDirectionCount
    camDirectionCount = cmds.intField("DirectionCountField", q=True, value=True)
    cmds.intSlider("PreviewSlider", e=True, max=camDirectionCount, value=camDirection)
    UpdateCameraPosition()
    UpdatePerRenderRotation()
    RefreshPreview()

# Update Camera Proximity #
def UpdateCameraProximity(*args):
    CheckCameraExists("renderCamera1")
    global camProximity
    camProximity = cmds.floatField("CameraProximityField", q=True, value=True)
    #cmds.setAttr("renderCamera1.translateX", camProximity)
    UpdateCameraPosition()
    RefreshPreview()

def UpdateCameraPosition():
    global camStartAngle
    global PerRenderRotation
    global camDirection
    global camProximity
#    S=O/H
#    SIN(ANGLE) = OPPOSITE / HYPOTENUSE
#    SIN(ANGLE) * HYPOTENUSE = OPPOSITE
#    SIN(Rotation) * CamDistance = CamLocationY

#    C=A/H
#    COS(ANGLE) = ADJACENT / HYPOTENUSE
#    COS(ANGLE) * HYPOTENUSE = ADJECENT
#    COS(Rotation) * CamDistance = CamLocationX

#    T=O/A
    CamPosX = math.sin(math.radians(camStartAngle + (PerRenderRotation * (camDirection-1)))) * camProximity
    CamPosZ = math.cos(math.radians(camStartAngle + (PerRenderRotation * (camDirection-1)))) * camProximity
    cmds.setAttr("renderCamera1.rotateY", (camStartAngle + ((camDirection-1) * PerRenderRotation)))
    cmds.setAttr("renderCamera1.translateX", CamPosX)
    cmds.setAttr("renderCamera1.translateZ", CamPosZ)

# Update Camera Height #
def UpdateCameraHeight(*args):
    CheckCameraExists("renderCamera1")
    global camHeight
    camHeight = cmds.floatField("CameraHeightField", q=True, value=True)
    cmds.setAttr("renderCamera1.translateY", camHeight)
    RefreshPreview()

# Update Camera Start Angle #
def UpdateCameraStartAngle(*args):
    CheckCameraExists("renderCamera1")
    global camStartAngle
    camStartAngle = cmds.floatField("StartAngleField", q=True, value=True)
    #cmds.setAttr("renderCamera1.rotateY", (camStartAngle + (camDirection * PerRenderRotation)))
    UpdatePerRenderRotation()
    UpdateCameraPosition()
    RefreshPreview()

# Update Camera Max Angle #
def UpdateCameraMaxAngle(*args):
    CheckCameraExists("renderCamera1")
    global camMaxAngle
    camMaxAngle = cmds.floatField("MaxAngleField", q=True, value=True)
    UpdatePerRenderRotation()
    UpdateCameraPosition()
    RefreshPreview()

def UpdatePerRenderRotation():
    global PerRenderRotation
    PerRenderRotation = (camMaxAngle-camStartAngle)/camDirectionCount
    print(PerRenderRotation)

def UpdatePreviewRotation(*args):
    global camDirection
    camDirection = cmds.intSlider("PreviewSlider", q=True, value=True)
    UpdateCameraPosition()
    RefreshPreview()


# Rotation Per Direction #
# (camMaxAngle - camStartAngle) / camDirectionCount

def ResolutionChanged(*args):
    global camResolutionX
    global camResolutionY
    camResolutionX = cmds.intField("ResolutionField1", q=True, value=True)
    camResolutionY = cmds.intField("ResolutionField2", q=True, value=True)
    RefreshPreview()

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

cmds.window("RenderTool", title="3D to Spritesheet Tool", widthHeight=(600,450))
cmds.paneLayout("MasterLayout", parent="RenderTool", configuration="vertical2", paneSize=[1,70,100], separatorThickness=6)

#cmds.columnLayout("ButtonLayout", parent=MasterLayout, columnOffset=["both", 15])
cmds.frameLayout("ButtonLayout", parent="MasterLayout", marginWidth=15, marginHeight=15, label="Options/Settings", collapsable=True, collapse=False)

#cmds.columnLayout("PreviewLayout", parent=MasterLayout, columnOffset=["both", 15])
cmds.frameLayout("PreviewLayout", parent="MasterLayout", marginWidth=15, marginHeight=15, label="Preview")





# BUTTON LAYOUT #
# ------------- #
cmds.button("InitializeButton", parent="ButtonLayout", label="Initialize", command=SetupCam)
cmds.scrollLayout("ButtonLayoutScrollbar", parent="ButtonLayout", childResizable=True)

# Frame for Camera Setup
cmds.frameLayout("CameraSetupLayout", parent="ButtonLayoutScrollbar", marginWidth=5, marginHeight=5, label="Camera Setup", collapsable=True, collapse=False)
cmds.columnLayout("CameraSetupColumn", parent="CameraSetupLayout", adjustableColumn=True)

cmds.rowLayout("DirectionCountRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("DirectionCountText", parent="DirectionCountRow", label="Number Of Directions: ", width=TextWidth, align="right")
cmds.intField("DirectionCountField", parent="DirectionCountRow", value=defaultDirectionCount, minValue=1, maxValue=360, changeCommand=UpdateCameraDirectionCount)

cmds.separator(parent="CameraSetupColumn")

cmds.rowLayout("StartAngleRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("StartAngleText", parent="StartAngleRow", label="Start Angle: ", width=TextWidth, align="right")
cmds.floatField("StartAngleField", parent="StartAngleRow", value=defaultCamStartAngle, minValue=0, maxValue=360, changeCommand=UpdateCameraStartAngle)

cmds.rowLayout("MaxAngleRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("MaxAngleText", parent="MaxAngleRow", label="Maximum Angle: ", width=TextWidth, align="right")
cmds.floatField("MaxAngleField", parent="MaxAngleRow", value=defaultCamMaxAngle, minValue=0, maxValue=360, changeCommand=UpdateCameraMaxAngle)

cmds.separator(parent="CameraSetupColumn")

cmds.rowLayout("CameraProximityFieldRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("CameraProximityFieldText", parent="CameraProximityFieldRow", label="Camera Proximity: ", width=TextWidth, align="right")
cmds.floatField("CameraProximityField", parent="CameraProximityFieldRow", value=defaultCamProximity, minValue=0, changeCommand=UpdateCameraProximity)

cmds.rowLayout("CameraHeightFieldRow", parent="CameraSetupColumn", numberOfColumns=2)
cmds.text("CameraHeightFieldText", parent="CameraHeightFieldRow", label="Camera Height: ", width=TextWidth, align="right")
cmds.floatField("CameraHeightField", parent="CameraHeightFieldRow", value=defaultCamHeight, changeCommand=UpdateCameraHeight)

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
cmds.intField("ResolutionField1", parent="ResolutionRow", value=defaultCamResolutionX, minValue=1, maxValue=defaultCamMaxResolution, changeCommand=ResolutionChanged)
cmds.intField("ResolutionField2", parent="ResolutionRow", value=defaultCamResolutionY, minValue=1, maxValue=defaultCamMaxResolution, changeCommand=ResolutionChanged)

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









# PREVIEW PANEL #
# ------------- #
cmds.columnLayout("PreviewColumn", parent="PreviewLayout", adjustableColumn=True)

cmds.image("PreviewImage", parent="PreviewColumn", image="")

cmds.rowLayout("PreviewSliderRow", parent="PreviewColumn", numberOfColumns=3, adjustableColumn=2)
cmds.text("PreviewSliderText", parent="PreviewSliderRow", label="Preview Direction: ", width=TextWidth, align="right")
cmds.intSlider("PreviewSlider", parent="PreviewSliderRow", min=1, max=defaultDirectionCount, value=defaultDirection, changeCommand=UpdatePreviewRotation)
#cmds.intSliderGrp("PreviewAngleSlider", parent="PreviewColumn", label="Preview Angle", field=True, min=1, max=defaultDirectionCount, value=camDirection)

#cmds.modelPanel("PreviewPanel", parent="PreviewLayout", label="Camera Preview", camera="renderCamera1")






if CheckCameraExists("renderCamera1"):
    UpdatePreviewRotation()
    UpdateTempOutputPath()
    ResolutionChanged()
    RefreshPreview()



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