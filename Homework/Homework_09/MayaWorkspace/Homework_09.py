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
        self.selected_obj_btn = None
        self.selected_obj_btns = []
        self.selected_mat_btns = []
        self.init_option_vars()

    def init_option_vars(self):
        if 'MaterialExplorer_SelectMode' not in pm.optionVar:
            pm.optionVar['MaterialExplorer_SelectMode'] = 1

    # ------------------------------window------------------------------
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
                                 backgroundColor=Colors.OBJ_BTN_SELECTED_COLOR) as self.mi_layout:  # mi:material inspector
                self.mi_layout.sliders = {}
                self.create_mi_control_ui()
            with pm.scrollLayout(childResizable=True) as scrollLayout:
                self.create_obj_buttons()

        formLayout.attachForm(menuBarLayout, 'top', 0)
        formLayout.attachForm(menuBarLayout, 'left', 0)
        formLayout.attachForm(menuBarLayout, 'right', 0)
        formLayout.attachForm(self.mi_layout, 'left', 0)
        formLayout.attachForm(self.mi_layout, 'right', 0)
        formLayout.attachForm(scrollLayout, 'left', 0)
        formLayout.attachForm(scrollLayout, 'right', 0)
        formLayout.attachForm(scrollLayout, 'bottom', 0)
        formLayout.attachControl(self.mi_layout, 'top', 0, menuBarLayout)
        formLayout.attachControl(scrollLayout, 'top', 0, self.mi_layout)

    # ------------------------------menu------------------------------
    def create_menu(self):
        with pm.menu(label='Selection Mode', tearOff=True) as self.editMenu:
            pm.menuItem(divider=True, dividerLabel='Selection Mode')
            pm.radioMenuItemCollection()
            pm.menuItem(
                label='Exclusive',
                radioButton=not bool(pm.optionVar['MaterialExplorer_SelectMode']),
                command=self.exclusive_menu_command
            )
            pm.menuItem(
                label='Additive',
                radioButton=bool(pm.optionVar['MaterialExplorer_SelectMode']),
                command=self.additive_menu_command
            )

    def exclusive_menu_command(self, *args):
        self.set_btns_default()
        pm.optionVar.update({'MaterialExplorer_SelectMode': 0})

    def additive_menu_command(self, *args):
        self.set_btns_default()
        pm.optionVar.update({'MaterialExplorer_SelectMode': 1})

    def set_btns_default(self):
        pm.select(clear=True)
        for btn in self.selected_obj_btns:
            btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            btn.material_ui.delete()
            btn.is_selected = False
        self.selected_obj_btns.clear()
        for btn in self.selected_mat_btns:
            btn.is_selected = False
        self.selected_mat_btns.clear()
        self.mi_layout.setVisible(False)

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

        if self.selected_obj_btns:
            self.selected_obj_btns[0].parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            self.selected_obj_btns[0].material_ui.delete()
            self.mi_layout.setVisible(False)

        if btn.is_selected:
            self.selected_obj_btns.remove(btn)
            btn.is_selected = False
        else:
            if self.selected_obj_btns:
                self.selected_obj_btns[0].is_selected = False
                self.selected_obj_btns[0] = btn
            else:
                self.selected_obj_btns.append(btn)
            btn.is_selected = True
            self.create_materials_ui(btn)

    def obj_button_selected_additive(self, btn):
        if btn.is_selected:
            pm.select(btn.shape, deselect=True)
            btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            btn.material_ui.delete()
            btn.is_selected = False
            self.selected_obj_btns.remove(btn)
        else:
            pm.select(btn.shape, add=True)
            btn.parent.setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)
            self.create_materials_ui(btn)
            btn.is_selected = True
            self.selected_obj_btns.append(btn)

        if not self.selected_obj_btns:
            self.mi_layout.setVisible(False)

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
                    mat_btn.mat_attrs = {}

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
        self.mi_layout.setVisible(True)
        btn.setBackgroundColor(Colors.MAT_BTN_SELECTED_COLOR)

        if self.selected_mat_btns:
            self.selected_mat_btns[0].setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)

        if btn.is_selected:
            self.selected_mat_btns.remove(btn)
            btn.is_selected = False
            self.mi_layout.setVisible(False)
        else:
            if self.selected_mat_btns:
                self.selected_mat_btns[0].is_selected = False
                self.selected_mat_btns[0] = btn
            else:
                self.selected_mat_btns.append(btn)
            btn.is_selected = True
            self.set_mi_control_value(btn)

    def mat_button_selected_additive(self, btn):
        self.mi_layout.setVisible(True)

        if btn.is_selected:
            self.selected_mat_btns.remove(btn)
            btn.setBackgroundColor(Colors.OBJ_BTN_SELECTED_COLOR)
            btn.is_selected = False

        else:
            self.selected_mat_btns.append(btn)
            btn.setBackgroundColor(Colors.MAT_BTN_SELECTED_COLOR)
            btn.is_selected = True

        self.set_mi_control_value(btn)

        if not self.selected_mat_btns:
            self.mi_layout.setVisible(False)

    # ------------------------------mat control ui------------------------------
    def set_mi_control_value(self, btn):
        self.set_mi_base_color_value(btn)
        self.set_mi_specular_color_value(btn)
        self.set_mi_bump_depth_value(btn)
        self.set_mi_metallic_and_roughness_value(btn)

    def set_mi_base_color_value(self, btn):
        if 'Base Color' in self.mi_layout.sliders:
            mat_ai_multiplies = btn.material.inputs(type='aiMultiply')
            if mat_ai_multiplies:
                mat_ai_multiply = mat_ai_multiplies[0]
                mat_color_constants = mat_ai_multiply.inputs(type='colorConstant')
                if mat_color_constants:
                    mat_base_color_constant = mat_color_constants[0]
                    self.set_color_slider_value(mat_base_color_constant, 'inColor', 'Base Color')
                    btn.mat_attrs['Base Color'] = f'{mat_base_color_constant}.inColor'

    def set_mi_specular_color_value(self, btn):
        if 'Specular Color' in self.mi_layout.sliders:
            if pm.hasAttr(btn.material, 'specularColor'):
                self.set_color_slider_value(btn.material, 'specularColor', 'Specular Color')
                btn.mat_attrs['Specular Color'] = f'{btn.material}.specularColor'

    def set_color_slider_value(self, node, attr, slider_name):
        color = pm.getAttr(f'{node}.{attr}')
        slider = self.mi_layout.sliders[slider_name]
        slider.setRgbValue(color)

    def set_mi_bump_depth_value(self, btn):
        if 'Bump Depth' in self.mi_layout.sliders:
            mat_bump2ds = btn.material.inputs(type='bump2d')
            if mat_bump2ds:
                mat_bump2d = mat_bump2ds[0]
                self.set_float_slider_value(mat_bump2d, 'bumpDepth', 'Bump Depth')
                btn.mat_attrs['Bump Depth'] = f'{mat_bump2d}.bumpDepth'

    def set_mi_metallic_and_roughness_value(self, btn):
        if 'Metallic Strength' in self.mi_layout.sliders and 'Roughness Strength' in self.mi_layout.sliders:
            mat_multiply_divides = btn.material.inputs(type='multiplyDivide')
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

                if mat_metallic_strength_constant:
                    self.set_float_slider_value(mat_metallic_strength_constant, 'inFloat', 'Metallic Strength')
                    btn.mat_attrs['Metallic Strength'] = f'{mat_metallic_strength_constant}.inFloat'
                if mat_roughness_strength_constant:
                    self.set_float_slider_value(mat_roughness_strength_constant, 'inFloat', 'Roughness Strength')
                    btn.mat_attrs['Roughness Strength'] = f'{mat_roughness_strength_constant}.inFloat'

    def set_float_slider_value(self, node, attr, slider_name):
        value = pm.getAttr(f'{node}.{attr}')
        slider = self.mi_layout.sliders[slider_name]
        slider.setValue(value)

    def create_mi_control_ui(self):
        color_control_info = {'Base Color': (1, 1, 1), 'Specular Color': (1, 1, 1)}
        float_control_info = {'Bump Depth': 1, 'Metallic Strength': 1, 'Roughness Strength': 1}
        for label, node in color_control_info.items():
            self.create_mi_color_slider_ui(label, node)
        for label, node in float_control_info.items():
            self.create_mi_float_slider_ui(label, node)

    def create_mi_color_slider_ui(self, label, value):
        node_color_slider = pm.colorSliderButtonGrp(label=label, buttonLabel='Reset',
                                                    adjustableColumn=3,
                                                    columnAttach=(1, 'right', 5), rgb=value)
        node_color_slider.changeCommand(partial(self.set_mat_color_attr, label))
        self.mi_layout.sliders[label] = node_color_slider

    def create_mi_float_slider_ui(self, label, value):
        node_float_slider = pm.floatSliderButtonGrp(label=label, field=True, buttonLabel='Reset', minValue=0,
                                                    maxValue=1, sliderStep=0.001, adjustableColumn=3,
                                                    columnAttach=(1, 'right', 5), value=value)
        node_float_slider.changeCommand(partial(self.set_mat_float_attr, label))
        self.mi_layout.sliders[label] = node_float_slider

    def set_mat_float_attr(self, label, *args):
        for btn in self.selected_mat_btns:
            if label in btn.mat_attrs:
                slider = self.mi_layout.sliders[label]
                mat_attr = btn.mat_attrs[label]
                pm.setAttr(mat_attr, slider.getValue())

    def set_mat_color_attr(self, label, *args):
        for btn in self.selected_mat_btns:
            if label in btn.mat_attrs:
                slider = self.mi_layout.sliders[label]
                mat_attr = btn.mat_attrs[label]
                pm.setAttr(mat_attr, slider.getRgbValue())


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
