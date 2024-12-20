__author__ = 'WoBok'

import pymel.core as pm
from functools import partial


class Colors:
    DEFAULT_COLOR = (0.3647, 0.3647, 0.3647)
    OBJ_BTN_SELECTED_COLOR = (0.5, 0.5, 0.5)
    MAT_BTN_SELECTED_COLOR = (0.7, 0.7, 0.7)


class MaterialExplorer:

    def __init__(self):
        self.winTitle = 'Material Explorer'
        self.window = None
        self.selected_btn = None
        self.selected_obj_btns = []
        self.selected_mat_btns = []
        self.init_option_vars()

    def init_option_vars(self):
        if 'MaterialExplorer_SelectMode' not in pm.optionVar:
            pm.optionVar['MaterialExplorer_SelectMode'] = 1
        pm.optionVar['MaterialExplorer_SelectMode'] = 1

    def create_dockable_window(self):
        if pm.workspaceControl(self.winTitle, exists=True):
            pm.deleteUI(self.winTitle)
        self.window = pm.workspaceControl(self.winTitle, retain=False, floating=True, initialWidth=350,
                                          initialHeight=800)
        self.create_ui()
        self.bind_jobs()

    def bind_jobs(self):
        pm.scriptJob(event=['SceneOpened', self.create_dockable_window], parent=self.window, rp=True)

    def create_ui(self):
        with pm.formLayout() as formLayout:
            with pm.menuBarLayout() as menuBarLayout:
                self.create_menu()
            with pm.columnLayout(adjustableColumn=True, visible=False,
                                 backgroundColor=Colors.OBJ_BTN_SELECTED_COLOR) as self.material_inspector_layout:
                pass
            with pm.scrollLayout(childResizable=True) as scrollLayout:
                self.create_obj_buttons()

        formLayout.attachForm(menuBarLayout, 'top', 0)
        formLayout.attachForm(menuBarLayout, 'left', 0)
        formLayout.attachForm(menuBarLayout, 'right', 0)
        formLayout.attachForm(self.material_inspector_layout, 'left', 0)
        formLayout.attachForm(self.material_inspector_layout, 'right', 0)
        formLayout.attachForm(scrollLayout, 'left', 0)
        formLayout.attachForm(scrollLayout, 'right', 0)
        formLayout.attachForm(scrollLayout, 'bottom', 0)
        formLayout.attachControl(self.material_inspector_layout, 'top', 0, menuBarLayout)
        formLayout.attachControl(scrollLayout, 'top', 0, self.material_inspector_layout)

    def create_menu(self):
        with pm.menu(label='View'):
            pm.menuItem(label='Refresh')
            pm.menuItem(label='Clear')

    # ------------------------------obj btn------------------------------
    def create_obj_buttons(self):
        transform_nodes = pm.ls(type='transform')
        objs = [o for o in transform_nodes if isinstance(o.getShape(), pm.nt.Mesh)]
        with pm.columnLayout(adjustableColumn=True, rowSpacing=5):
            for obj in objs:
                with pm.columnLayout(adjustableColumn=True) as cl:
                    shape = obj.getShape()
                    btn = pm.button(label=obj.name())
                    btn.setCommand(partial(self.obj_button_selected, btn))
                    btn.selected_materials = self.get_shape_materials(shape)
                    btn.is_selected = False
                    btn.shape = shape
                    btn.parent = cl

    def get_shape_materials(self, shape):
        shading_engines = shape.outputs(type='shadingEngine')
        all_materials = []
        for shadingEngine in shading_engines:
            materials = shadingEngine.surfaceShader.inputs()
            for material in materials:
                all_materials.append(material)

        return all_materials

    def obj_button_selected(self, btn, *args):
        if pm.optionVar['MaterialExplorer_SelectMode'] == 0:
            self.obj_button_selected_exclusive(btn)
        else:
            self.obj_button_selected_additive(btn)

    def obj_button_selected_exclusive(self, btn):
        pm.select(btn.shape, replace=True)
        btn.parent.setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)

        if self.selected_btn:
            self.selected_btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            self.selected_btn.material_ui.delete()
            self.material_inspector_layout.setVisible(False)

        if btn.is_selected:
            self.selected_btn = None
            btn.is_selected = False
        else:
            if self.selected_btn:
                self.selected_btn.is_selected = False
            btn.is_selected = True
            self.selected_btn = btn
            self.create_materials_ui(btn)

    def obj_button_selected_additive(self, btn):
        if btn.is_selected:
            pm.select(btn.shape, add=True)
            btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            btn.material_ui.delete()
            btn.is_selected = False
            self.material_inspector_layout.setVisible(False)  # Todo
        else:
            pm.select(btn.shape, deselect=True)
            btn.parent.setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)
            self.create_materials_ui(btn)
            btn.is_selected = True

    # ------------------------------mat btn------------------------------
    def create_materials_ui(self, btn):
        with pm.formLayout(parent=btn.parent) as formLayout:
            with pm.frameLayout(label=f"The material of {btn.shape.name()}", collapsable=True,
                                backgroundColor=Colors.OBJ_BTN_SELECTED_COLOR) as btn.material_ui:
                for material in btn.selected_materials:
                    mat_btn = pm.button(label=material.name())
                    mat_btn.setCommand(partial(self.mat_button_selected, mat_btn))
                    mat_btn.material = material
                    mat_btn.is_selected = False
                    # self.selected_mat_btns.append(mat_btn)

        formLayout.attachForm(btn.material_ui, 'top', 0)
        formLayout.attachForm(btn.material_ui, 'left', 10)
        formLayout.attachForm(btn.material_ui, 'right', 10)
        formLayout.attachForm(btn.material_ui, 'bottom', 5)

    def mat_button_selected(self, btn, *args):
        if pm.optionVar['MaterialExplorer_SelectMode'] == 0:
            self.mat_button_selected_exclusive(btn)
        else:
            self.mat_button_selected_additive(btn)

    def mat_button_selected_exclusive(self, btn):
        material = btn.material
        parent = self.material_inspector_layout
        parent.setVisible(True)
        parent.clear()
        self.create_mi_control_ui(material, parent)

    def mat_button_selected_additive(self, btn):
        material = btn.material
        parent = self.material_inspector_layout
        parent.setVisible(True)

        if btn.is_selected:
            self.selected_mat_btns.remove(btn)
            btn.setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)
            btn.is_selected = False

        else:
            self.selected_mat_btns.append(btn)
            btn.setBackgroundColor(Colors.MAT_BTN_SELECTED_COLOR)
            btn.is_selected = True

            # if len(self.selected_mat_btns) >= 2:
            #     if type(self.selected_mat_btns[-1]) is not type(self.selected_mat_btns[-2]):
            #         parent.clear()
            #         parent.setVisible(False)

        if len(self.selected_mat_btns) == 1:
            self.create_mi_control_ui(material, parent)

        if not self.selected_mat_btns:
            parent.clear()
            parent.setVisible(False)

        # if not btn.is_selected:
        #     print(len(self.selected_mat_btns))
        #     if len(self.selected_mat_btns) >= 2:
        #         if type(self.selected_mat_btns[-1]) is not type(self.selected_mat_btns[-2]):
        #             parent.clear()
        #             parent.setVisible(False)

    # ------------------------------mat control ui------------------------------
    # mi:material inspector
    def create_mi_control_ui(self, material, parent):
        self.create_mi_base_color_ui(material, parent)
        self.create_mi_specular_color_ui(material, parent)
        self.create_mi_bump_depth_ui(material, parent)
        self.create_mi_metallic_and_roughness_ui(material, parent)

    def create_mi_base_color_ui(self, material, parent):
        mat_ai_multiplies = material.inputs(type='aiMultiply')
        if mat_ai_multiplies:
            mat_ai_multiply = mat_ai_multiplies[0]
            mat_color_constants = mat_ai_multiply.inputs(type='colorConstant')
            if mat_color_constants:
                mat_base_color_constant = mat_color_constants[0]
                self.create_mi_color_slider_ui('Base Color', mat_base_color_constant, 'inColor', parent)

    def create_mi_specular_color_ui(self, material, parent):
        if pm.hasAttr(material, 'specularColor'):
            self.create_mi_color_slider_ui('Specular Color', material, 'specularColor', parent)

    def create_mi_color_slider_ui(self, label, node, attr, parent):
        attr_color = pm.getAttr(f"{node}.{attr}")
        node_color_slider = pm.colorSliderButtonGrp(label=label, buttonLabel='Reset',
                                                    adjustableColumn=3,
                                                    columnAttach=(1, 'right', 5), rgb=attr_color,
                                                    parent=parent)
        node_color_slider.node = node
        node_color_slider.attr = attr
        node_color_slider.changeCommand(partial(self.set_mat_color_attr, node_color_slider))

    def create_mi_bump_depth_ui(self, material, parent):
        mat_bump2ds = material.inputs(type='bump2d')
        if mat_bump2ds:
            mat_bump2d = mat_bump2ds[0]
            self.create_mi_float_slider_ui('Bump Depth', mat_bump2d, 'bumpDepth', parent)

    def create_mi_metallic_and_roughness_ui(self, material, parent):
        mat_multiply_divides = material.inputs(type='multiplyDivide')
        if mat_multiply_divides:
            mat_metallic_strength_constant = None
            mat_roughness_strength_constant = None
            for multiply_divide in mat_multiply_divides:
                mat_float_constants = multiply_divide.inputs(type='floatConstant')
                if mat_float_constants:
                    if mat_float_constants[0].name() == 'metallic_strength':
                        mat_metallic_strength_constant = multiply_divide.inputs(type='floatConstant')[0]
                    if mat_float_constants[0].name() == 'roughness_strength':
                        mat_roughness_strength_constant = multiply_divide.inputs(type='floatConstant')[0]

            self.create_mi_float_slider_ui('Metallic Strength', mat_metallic_strength_constant, 'inFloat', parent)
            self.create_mi_float_slider_ui('Roughness Strength', mat_roughness_strength_constant, 'inFloat', parent)

    def create_mi_float_slider_ui(self, label, node, attr, parent):
        if node:
            attr_strength = pm.getAttr(f"{node}.{attr}")
            node_float_slider = pm.floatSliderButtonGrp(label=label, field=True, buttonLabel='Reset', minValue=0,
                                                        maxValue=1, sliderStep=0.001, adjustableColumn=3,
                                                        columnAttach=(1, 'right', 5), value=attr_strength,
                                                        parent=parent)
            node_float_slider.node = node
            node_float_slider.attr = attr
            node_float_slider.changeCommand(partial(self.set_mat_float_attr, node_float_slider))

    def set_mat_float_attr(self, slider, *args):
        node = slider.node
        attr = slider.attr
        if pm.hasAttr(node, attr):
            pm.setAttr(f"{node}.{attr}", slider.getValue())

    def set_mat_color_attr(self, slider, *args):
        node = slider.node
        attr = slider.attr
        if pm.hasAttr(node, attr):
            pm.setAttr(f"{node}.{attr}", slider.getRgbValue())


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
