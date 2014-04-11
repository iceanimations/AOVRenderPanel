# pieces of code picked up from
# http://therenderblog.com/loading-render-passesaovs-inside-maya-renderview-with-python/

import os
import pymel.core as pc
import maya.cmds as cmds
op = os.path

def aovUI():

    aovsList = cmds.optionMenu('com_iceanimations_arnold_aovs',
                               w = 125, h = 26, label = 'AOV',
                               cc = loadAOV, p = 'renderViewToolbar')

    activeAOVS = cmds.ls(et='aiAOV')
    aovsNames = ['beauty'] + [i.split('_', 1)[1] for i in activeAOVS]
    
    for i, item in enumerate(aovsNames):
        cmds.menuItem(label=item)
        if item == pc.getAttr("defaultArnoldRenderOptions.displayAOV"):
            cmds.optionMenu('com_iceanimations_arnold_aovs', edit = True, select = i + 1)

def loadAOV(*args):

	activeAOVS = cmds.ls(et='aiAOV')
	aovsNames = [i.split('_', 1)[1] for i in activeAOVS]

	if activeAOVS == []:
            cmds.warning("No aov's setup")
	else:

            rview = cmds.getPanel( sty = 'renderWindowPanel' )
            selectedAOV = cmds.optionMenu('com_iceanimations_arnold_aovs',q=1,v=1)
            pc.setAttr("defaultArnoldRenderOptions.displayAOV", selectedAOV)
            
            img = pc.renderSettings(fin = True, lut = True, fpt = True)[0]
            if '<RenderPass>' not in img:
                gin = pc.renderSettings(gin = 1, lut =1)[0]
                imgTillTmp = img[:img.find(gin)]
                img = op.join(imgTillTmp, selectedAOV, gin)
            pathToImg = img.replace('<RenderPass>', selectedAOV)
            print pathToImg
            cmds.renderWindowEditor(rview, e=True, li=pathToImg)

def drawMenu():
    if pc.mel.currentRenderer().lower() != "arnold":
        return False

        currentAOV = pc.getAttr("defaultArnoldRenderOptions.displayAOV")
    aovUI()
    
drawMenu()
