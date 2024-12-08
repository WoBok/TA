__author__ = 'Nathan.Chen'

import os
from pymel.core import *
from functools import reduce, partial
import logging

logger = logging.getLogger('MeshSelectToolLogger')

for handler in logger.handlers:
    logger.removeHandler(handler)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(os.path.dirname(__file__) + '/app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class Colors:
    RED = [1, 0, 0]
    GREEN = [0.5, 1, 0.5]
    BLUE = [0.5, 0.7, 1]
    LIGHTGREY = [0.7] * 3
    MIDGREY = [0.4] * 3
    DARKGREY = [0.23] * 3


class Selector:
    """
    this is a tool that allows artists select mesh faces by materials assignment
    """

    def __init__(self):
        self.winTitle = 'Select Mesh Face'
        self.winName = 'MeshSelectTool'
        self.selectionSetName = 'MeshSelectTool_Set'
        self.objects = list()
        self.frames = list()
        if 'MeshSelectTool_SelectMode' not in optionVar:
            optionVar['MeshSelectTool_SelectMode'] = 0
        if 'MeshSelectTool_LoadMode' not in optionVar:
            optionVar['MeshSelectTool_LoadMode'] = False
        if 'MeshSelectTool_AutoLoad' not in optionVar:
            optionVar['MeshSelectTool_AutoLoad'] = False
        if 'MeshSelectTool_AutoLoadMemory' not in optionVar:
            optionVar['MeshSelectTool_AutoLoadMemory'] = False
        self.logger = logging.getLogger('MeshSelectToolLogger')
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(__file__)

    @property
    def select_set(self):
        try:
            return PyNode(self.selectionSetName)
        except MayaNodeError:
            self.logger.debug(f'object set {self.selectionSetName} not exist, creating a new one.')
            return createNode('objectSet', name=self.selectionSetName)

    def init_UI(self):
        with formLayout() as self.mainForm:
            with menuBarLayout() as self.menuBar:
                self.add_menus()
            self.nameField = textFieldButtonGrp(
                label='Objects',
                columnWidth3=[50, 140, 5],
                adjustableColumn=2,
                editable=False,
                buttonLabel='<',
                placeholderText='Please select meshes in the viewport',
                buttonCommand=self.insert_selection
            )
            with scrollLayout(childResizable=True) as self.mainScroll:
                pass

        self.mainForm.attachForm(self.menuBar.name(), 'top', 0)
        self.mainForm.attachForm(self.menuBar.name(), 'left', 0)
        self.mainForm.attachForm(self.menuBar.name(), 'right', 0)
        self.mainForm.attachForm(self.nameField.name(), 'left', 0)
        self.mainForm.attachForm(self.nameField.name(), 'right', 0)
        self.mainForm.attachForm(self.mainScroll.name(), 'left', 0)
        self.mainForm.attachForm(self.mainScroll.name(), 'right', 0)
        self.mainForm.attachForm(self.mainScroll.name(), 'bottom', 0)
        self.mainForm.attachControl(self.mainScroll.name(), 'top', 0, self.nameField.name())
        self.mainForm.attachControl(self.nameField.name(), 'top', 0, self.menuBar.name())

        scriptJob(event=['SelectionChanged', self.auto_load], parent=self.mainForm, rp=True)
        scriptJob(event=['SceneOpened', self.scene_opened], parent=self.mainScroll, rp=True)
    def add_menus(self):
        with menu(label='Window') as self.windowMenu:
            menuItem(label='Refresh', image='refresh.png', command=self.refresh)
            menuItem(label='Clear', image='clearAll.png', command=self.clear)
            menuItem(label='Collapse All', image='dot.png',
                     command=lambda *a: [f.setCollapse(True) for f in self.frames])
            menuItem(label='Expand All', image='dot.png',
                     command=lambda *a: [f.setCollapse(False) for f in self.frames])
            menuItem(label='Close', image='closeTabButton.png',
                     command=lambda *a: workspaceControl(self.winTitle, edit=True, close=True))

        with menu(label='Edit', tearOff=True) as self.editMenu:
            menuItem(divider=True, dividerLabel='Selection Mode')
            self.modeRadios = radioMenuItemCollection()
            menuItem(
                label='Exclusive',
                radioButton=not bool(optionVar['MeshSelectTool_SelectMode']),
                command=lambda *a: optionVar.update({'MeshSelectTool_SelectMode': 0})
            )
            menuItem(
                label='Additive',
                radioButton=bool(optionVar['MeshSelectTool_SelectMode']),
                command=lambda *a: optionVar.update({'MeshSelectTool_SelectMode': 1})
            )
            menuItem(divider=True, dividerLabel='Loading Mode')
            menuItem(
                label='Load Dependencies',
                checkBox=optionVar['MeshSelectTool_LoadMode'],
                command=self.change_load_mode,
                ann='Load child objects when a group node is selected'
            )
            menuItem(
                label='Auto Load Selection',
                checkBox=optionVar['MeshSelectTool_AutoLoad'],
                command=self.change_auto_select,
                ann='Automatically load selected objects'
            )
            menuItem(
                label='Auto Load Memory',
                checkBox=optionVar['MeshSelectTool_AutoLoadMemory'],
                command=self.change_auto_load_memory,
                ann='Automatically load last selected objects in current scene when opened'
            )

        with menu(label='Help') as self.helpMenu:
            menuItem(label='help', image='help.png',
                     command=lambda *a: showHelp('http://www.autodesk.com/', absolute=True))

    def add_buttons(self, obj, frame):
        self.logger.debug(f'Mesh - {obj}')
        shape = obj.getShape()
        shading_engine_nodes = shape.inputs(type='shadingEngine')
        for shading_group in list(set(shading_engine_nodes)):
            surface_shader = shading_group.surfaceShader.inputs()[0]
            btn_label = surface_shader.name()
            faces = shading_group.members()[0]
            btn = iconTextButton(
                style='textOnly',
                label=f'{btn_label} ({len(faces)})',
                parent=frame,
                enableBackground=True,
            )
            btn.setCommand(partial(self.cmd_btn_select, btn))
            self.btns.append(btn)
            btn.data = faces
            btn.isHighlighted = False
            self.setBtnBgColor(btn)
            self.logger.debug(f'shader - {surface_shader}')

    def cmd_btn_select(self, btn, *args):
        a = optionVar['MeshSelectTool_SelectMode']
        if optionVar['MeshSelectTool_SelectMode'] == 0:
            self.cmd_btn_select_exclusive(btn)
        else:
            self.cmd_btn_select_additive(btn)

    def cmd_btn_select_additive(self, btn):
        if not any([b.isHighlighted for b in self.btns]):
            select(clear=True)
        if btn.isHighlighted:
            select(btn.data, deselect=True)
            btn.isHighlighted = False
        else:
            select(btn.data, add=True)
            btn.isHighlighted = True
        self.setBtnBgColor(btn)

    def cmd_btn_select_exclusive(self, btn):
        if btn.isHighlighted:
            select(btn.data, deselect=True)
            btn.isHighlighted = False
        else:
            select(btn.data, replace=True)
            for b in self.btns:
                b.isHighlighted = False
            btn.isHighlighted = True

        for b in self.btns:
            self.setBtnBgColor(b)

    def setBtnBgColor(self, btn):
        btn.setBackgroundColor(Colors.BLUE if btn.isHighlighted else Colors.DARKGREY)

    def refresh(self, *args):
        select(clear=True)
        self.insert_objects()

    def clear(self, *args):
        self.objects = []
        self.refresh()
        
    def insert_selection(self, *args):
        validate_method = self.validate_selection_grp if optionVar[
            'MeshSelectTool_LoadMode'] else self.validate_selection_meshes
        if validate_method():
            pass
        self.insert_objects()

    def insert_objects(self):
        self.mainScroll.clear()
        self.nameField.setText('')
        self.frames = []
        self.btns = []
        self.select_set.clear()
        ann = []
        for obj in self.objects:
            self.nameField.setText(obj.name())
            ann.append(obj.name())
            with frameLayout(
                    label=obj.getShape().name(),
                    collapsable=True,
                    parent=self.mainScroll
            ) as frame:
                self.frames.append(frame)
                self.add_buttons(obj, frame)
            self.select_set.add(obj)
        self.nameField.setAnnotation('\n'.join(ann))

    def validate_selection_meshes(self):
        selected_objects = selected(type='transform')
        self.objects = [n for n in selected_objects if n.getShape()]
        if self.objects:
            return True
        else:
            return False

    def validate_selection_grp(self):
        selected_objects = selected(type='transform')
        dependencies = [n.getChildren(ad=True, type='transform') for n in selected_objects]
        dependencies.append(selected_objects)
        dependencies = reduce(lambda x, y: x + y, dependencies)
        self.objects = [n for n in set(dependencies) if n.getShape()]
        if self.objects:
            return True
        else:
            return False

    def auto_load(self, *args):
        if optionVar['MeshSelectTool_AutoLoad']:
            self.insert_selection()

    def change_load_mode(self, value):
        optionVar['MeshSelectTool_LoadMode'] = value
        self.insert_selection()

    def change_auto_select(self, value):
        optionVar['MeshSelectTool_AutoLoad'] = value

    def change_auto_load_memory(self, value):
        optionVar['MeshSelectTool_AutoLoadMemory'] = value

    def scene_opened(self, *args):
        if optionVar['MeshSelectTool_AutoLoadMemory']:
            self.logger.info(
                'Automatically loading last selected objects. To turn it off, uncheck Edit>Auto Load Memory')
            self.objects = self.select_set.members()
            self.insert_objects()
if __name__ == '__main__':
    Tool = Selector()
    
    # Tool.init_UI()
    
    if workspaceControl(Tool.winTitle, exists=True):
        workspaceControl(Tool.winTitle, edit=True, close=True)
    
    workspaceControl(Tool.winTitle, retain=False, floating=True, uiScript='Tool.init_UI()')
