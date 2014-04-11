# pieces of code picked up from
# http://therenderblog.com/loading-render-passesaovs-inside-maya-renderview-with-python/

import os
import pymel.core as pc
import maya.cmds as cmds


def all_files_under(path):
    for cur_path, dirnames, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(cur_path, filename)
    
def selectedAOV(): return cmds.optionMenu('aovsListMenu',q=1,v=1)

# def activeRenderLayerName():
#     return ("masterLayer"
#             if pc.mel.eval("editRenderLayerGlobals -q -crl")
#             == "defaultRenderLayer" else
#             pc.mel.eval("editRenderLayerGlobals -q -crl"))

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
            CurrentProject = cmds.workspace(q=1,fullName=1)
            rview = cmds.getPanel( sty = 'renderWindowPanel' )
            selectedAOV = cmds.optionMenu('com_iceanimations_arnold_aovs',q=1,v=1)
            pc.setAttr("defaultArnoldRenderOptions.displayAOV", selectedAOV)
            
            # prefixMapping = {"<RenderLayer>": activeRenderLayerName(),
            #                  "<Scene>": "untitled" if not cmds.file(q=True, sn=True)
            #                  else cmds.file(q=True, sn=True),
            #                  "<RenderPass>": selectedAOV}
            
            
            ImgTempPath = CurrentProject + '/images/tmp/'
            latest_file = max(all_files_under(ImgTempPath),
                              key=os.path.getmtime)
            splitPath = latest_file.replace('/','\\')

            splitPath = splitPath.split(os.sep)

            for n, i in enumerate(splitPath):
                if i in aovsNames or i == 'beauty':
                    splitPath[n] = selectedAOV

            splitPath[0] = splitPath[0] + '\\'
            pathToImg = os.path.join(*splitPath)

            print pathToImg
            cmds.renderWindowEditor(rview, e=True, li=pathToImg)

def drawMenu():
    if pc.mel.currentRenderer().lower() != "arnold":
        return False

    currentAOV = pc.getAttr("defaultArnoldRenderOptions.displayAOV")
    aovUI()
    
drawMenu()
