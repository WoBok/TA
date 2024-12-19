import pymel.core as pm
from functools import partial


class Colors:
    SELECTED_COLOR = (0.5, 0.5, 0.5)
    DEFAULT_COLOR = (0.3647, 0.3647, 0.3647)


class MaterialExplorer:

    def __init__(self):
        self.winTitle = 'Material Explorer'
        self.window = None
        self.material_ui = None
        self.selected_btn = None
        self.selected_materials = []

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
                                 backgroundColor=Colors.SELECTED_COLOR) as self.material_inspector_layout:
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

    def obj_button_selected(self, btn, *args):
        pm.select(btn.shape, replace=True)
        btn.parent.setBackgroundColor(Colors.SELECTED_COLOR)

        if self.selected_btn:
            self.selected_btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            self.delete_last_material_ui()
            self.material_inspector_layout.setVisible(False)
            self.selected_materials.clear()  # = [x for x in self.selected_materials if
            # x not in self.selected_btn.selected_materials]

        if btn.is_selected:
            self.selected_btn = None
            btn.is_selected = False
        else:
            if self.selected_btn:
                self.selected_btn.is_selected = False
            btn.is_selected = True
            self.selected_btn = btn
            self.selected_materials += btn.selected_materials
            self.create_materials_ui(btn.shape.name(), btn.parent)

    def get_shape_materials(self, shape):
        shading_engines = shape.outputs(type='shadingEngine')
        all_materials = []
        for shadingEngine in shading_engines:
            materials = shadingEngine.surfaceShader.inputs()
            for material in materials:
                all_materials.append(material)

        return all_materials

    def create_materials_ui(self, shape_name, parent):
        self.delete_last_material_ui()

        with pm.formLayout(parent=parent) as formLayout:
            with pm.frameLayout(label=f"The material of {shape_name}", collapsable=True,
                                backgroundColor=Colors.SELECTED_COLOR) as self.material_ui:
                for material in self.selected_materials:
                    pm.button(label=material.name(), command=partial(self.creat_material_inspector_ui, material))
        formLayout.attachForm(self.material_ui, 'top', 0)
        formLayout.attachForm(self.material_ui, 'left', 10)
        formLayout.attachForm(self.material_ui, 'right', 10)
        formLayout.attachForm(self.material_ui, 'bottom', 5)

    def delete_last_material_ui(self):
        if self.material_ui:
            self.material_ui.delete()
            self.material_ui = None

    def creat_material_inspector_ui(self, material, *args):
        parent = self.material_inspector_layout
        parent.setVisible(True)
        parent.clear()

        self.create_mi_base_color_ui(material, parent)
        self.create_mi_specular_color_ui(material, parent)
        self.create_mi_bump_depth_ui(material, parent)
        self.create_mi_metallic_and_roughness_ui(material, parent)

    def create_mi_base_color_ui(self, material, parent):
        # base color
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
