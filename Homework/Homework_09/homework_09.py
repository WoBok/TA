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
        self.selected_obj_button_layout = None

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
                    pm.button(label=obj.name(), command=partial(self.obj_button_selected, obj.getShape(), cl))

    def obj_button_selected(self, obj, parent, *args):
        pm.select(obj, replace=True)
        parent.setBackgroundColor(Colors.SELECTED_COLOR)

        if self.selected_obj_button_layout:
            self.selected_obj_button_layout.setBackgroundColor(Colors.DEFAULT_COLOR)
            self.delete_last_material_ui()
            self.material_inspector_layout.setVisible(False)

        if self.selected_obj_button_layout != parent:
            self.create_materials_ui(obj, parent)
            self.selected_obj_button_layout = parent
        else:
            self.selected_obj_button_layout = None

    def create_materials_ui(self, obj, parent):
        shading_engines = obj.outputs(type='shadingEngine')
        all_materials = []
        for shadingEngine in shading_engines:
            materials = shadingEngine.surfaceShader.inputs()
            for material in materials:
                all_materials.append(material)
        self.delete_last_material_ui()
        with pm.formLayout(parent=parent) as formLayout:
            with pm.frameLayout(label=obj.name(), collapsable=True,
                                backgroundColor=Colors.SELECTED_COLOR) as self.material_ui:
                for material in all_materials:
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

        # Todo: 优化变量名，加入容错判断

        # base color
        ai_multiply = material.inputs(type='aiMultiply')[0]
        color_constant = ai_multiply.inputs(type='colorConstant')[0]
        base_color = pm.getAttr(color_constant + '.inColor')
        pm.colorSliderButtonGrp(label='Base Color', buttonLabel='Reset', adjustableColumn=3,
                                columnAttach=(1, 'right', 5),
                                rgb=base_color, parent=parent)
        # specular color
        mat_specular_color = pm.getAttr(material + '.specularColor')
        pm.colorSliderButtonGrp(label='Specular Color', buttonLabel='Reset', adjustableColumn=3,
                                columnAttach=(1, 'right', 5),
                                rgb=mat_specular_color, parent=parent)

        # bump depth
        bump2d = material.inputs(type='bump2d')[0]
        mat_bump_depth = pm.getAttr(bump2d + '.bumpDepth')
        pm.floatSliderButtonGrp(label='Bump Depth', field=True, buttonLabel='Reset', minValue=-5, maxValue=5,
                                sliderStep=0.001,
                                adjustableColumn=3,
                                columnAttach=(1, 'right', 5), value=mat_bump_depth, parent=parent)
        # metallic and roughness
        multiply_divides = material.inputs(type='multiplyDivide')
        metallic_strength_constant = None
        roughness_strength_constant = None
        for multiplyDivide in multiply_divides:
            if multiplyDivide.inputs(type='floatConstant')[0].name() == 'metallic_strength':
                metallic_strength_constant = multiplyDivide.inputs(type='floatConstant')[0]
            if multiplyDivide.inputs(type='floatConstant')[0].name() == 'roughness_strength':
                roughness_strength_constant = multiplyDivide.inputs(type='floatConstant')[0]
        # metallic strength
        metallic_strength = pm.getAttr(metallic_strength_constant + '.inFloat')
        pm.floatSliderButtonGrp(label='Metallic Strength', field=True, buttonLabel='Reset', minValue=0, maxValue=1,
                                sliderStep=0.001,
                                adjustableColumn=3,
                                columnAttach=(1, 'right', 5), value=metallic_strength, parent=parent)
        # roughness strength
        roughness_strength = pm.getAttr(roughness_strength_constant + '.inFloat')
        pm.floatSliderButtonGrp(label='Roughness Strength', field=True, buttonLabel='Reset', minValue=0, maxValue=1,
                                sliderStep=0.001,
                                adjustableColumn=3,
                                columnAttach=(1, 'right', 5), value=roughness_strength, parent=parent)
        print(metallic_strength_constant)
        print(roughness_strength_constant)


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
