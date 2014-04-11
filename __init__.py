import arnoldmenu
import pymel.core as pc
import os
op = os.path
SPRT_FOR = map(str,[2013,
                    2014,
                    2015])
VER = pc.about(v = True)
for ver in SPRT_FOR:
    if ver in VER:
        renderWindowPanel = op.join(op.dirname(arnoldmenu.__file__ ),
                                    'renderWindowPanel'+ '_' + ver + '.mel')
        with open(renderWindowPanel, 'r') as r:
            arnoldmenu_file = arnoldmenu.__file__.replace('\\', '/')
            print arnoldmenu_file
            if (arnoldmenu_file.endswith('.pyc') and
                op.exists(arnoldmenu_file[:-1])):
                arnoldmenu_file = arnoldmenu_file[:-1]
            pc.mel.eval(r.read().replace(r'arnoldmenu',
                                         arnoldmenu_file))
