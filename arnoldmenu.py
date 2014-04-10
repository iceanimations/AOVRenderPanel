# pieces of code picked up from
# http://therenderblog.com/loading-render-passesaovs-inside-maya-renderview-with-python/

import pymel.core as pc
import maya.cmds as cmds

    
def selectedAOV(): return cmds.optionMenu('aovsListMenu',q=1,v=1)

def aovUI():

    aovsList = cmds.optionMenu('com.iceanimations.arnold.aovs'
                               ,w=95,label='AOV',cc=loadAOV,
                               p = 'renderViewToolbar')
    activeAOVS = cmds.ls(et='aiAOV')
    aovsNames = ['beauty'] + [i.split('_', 1)[1] for i in activeAOVS]
    
    for i, item in enumerate(aovsNames):
        cmds.menuItem(label=item)
        if item == selectedAOV():
            cmds.optionMenu('rendererSelOptionMenu', edit = True, select = i + 2)

def loadAOV():

	activeAOVS = cmds.ls(et='aiAOV')
	aovsNames = [i.split('_', 1)[1] for i in activeAOVS]

	if activeAOVS == []:
		cmds.warning("No aov's setup")
	else:
		CurrentProject = cmds.workspace(q=1,fullName=1)
		rview = cmds.getPanel( sty = 'renderWindowPanel' )
		selectedAOV = cmds.optionMenu('aovsListMenu',q=1,v=1)
                pc.setAttr("defaultArnoldRenderOptions.displayAOV", selectedAOV)

		ImgTempPath = CurrentProject + '/images/tmp/'
		latest_file = max(all_files_under(ImgTempPath), key=os.path.getmtime)
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
