import pymel.core as pm


class MaterialExplorer:

    def __init__(self):
        self.winTitle = 'Material Explorer'

    def create_dockable_window(self):
        if pm.workspaceControl(self.winTitle, exists=True):
            pm.deleteUI(self.winTitle)
        pm.workspaceControl(self.winTitle, retain=False, floating=True)
        self.create_ui()

    def create_ui(self):
        with pm.columnLayout(adjustableColumn=True):
            self.create_menu()

    def create_menu(self):
        with pm.menuBarLayout():
            with pm.menu(label='View'):
                pm.menuItem(label='Refresh')
                pm.menuItem(label='Clear')


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
