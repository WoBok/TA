import pymel.core as pm
import maya.cmds as cmds


class MaterialExplorer:

    def __init__(self):
        self.winTitle = 'Material Explorer'

    def create_dockable_window(self):
        if pm.workspaceControl(self.winTitle, exists=True):
            pm.deleteUI(self.winTitle)
        self.window = pm.workspaceControl(self.winTitle, retain=False, floating=True)
        print(self.window)
        self.create_ui()
        self.bind_jobs()

    def bind_jobs(self):
        pm.scriptJob(event=['SelectionChanged', self.load_materials], parent=self.window, rp=True)

    def create_ui(self):
        with pm.columnLayout(adjustableColumn=True):
            self.create_menu()

    def create_menu(self):
        with pm.menuBarLayout():
            with pm.menu(label='View'):
                pm.menuItem(label='Refresh')
                pm.menuItem(label='Clear')

    def load_materials(self):
        print('loading materials')


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
