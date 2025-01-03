__author__ = 'WoBok'

import pymel.core as pm
from functools import partial


class Colors:
    DEFAULT_COLOR = (0.3647, 0.3647, 0.3647)
    MOD_BTN_SELECTED_COLOR = (0.5, 0.5, 0.5)
    MAT_BTN_SELECTED_COLOR = (0.7, 0.7, 0.7)


class MaterialExplorer:

    def __init__(self):
        self.winTitle = 'Material Explorer'
        self.window = None
        self.selected_mod_btns = []  # 当前正在被选择模型的button
        self.selected_mat_btns = []  # 当前正在被选择材质的button
        self.init_option_vars()

    # 初始化optionVar
    def init_option_vars(self):
        if 'MaterialExplorer_SelectMode' not in pm.optionVar:
            pm.optionVar['MaterialExplorer_SelectMode'] = 1

    # ------------------------------window------------------------------

    # 创建可以dock的window
    def create_dockable_window(self):
        if pm.workspaceControl(self.winTitle, exists=True):
            pm.deleteUI(self.winTitle)
        self.window = pm.workspaceControl(self.winTitle, retain=False, floating=True, initialWidth=350,
                                          initialHeight=800)
        self.create_ui_layout()
        self.bind_jobs()

    # 绑定场景打开时的任务
    def bind_jobs(self):
        pm.scriptJob(event=['SceneOpened', self.create_dockable_window], parent=self.window, rp=True)

    # 创建ui布局
    def create_ui_layout(self):
        with pm.formLayout() as formLayout:
            with pm.menuBarLayout() as menuBarLayout:  # 创建菜单布局
                self.create_menu()
            with pm.columnLayout(adjustableColumn=True, visible=False,
                                 backgroundColor=Colors.MOD_BTN_SELECTED_COLOR) as self.mi_layout:  # 创建材质属性布局 # mi:material inspector
                self.mi_layout.sliders = {}  # 被创建的slider将缓存至此列表
                self.create_mi_slider_ui()
            with pm.scrollLayout(childResizable=True) as scrollLayout:  # 创建模型按钮布局
                self.create_mod_buttons()

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

    # 创建菜单
    def create_menu(self):
        with pm.menu(label='Selection Mode', tearOff=True) as self.editMenu:
            pm.menuItem(divider=True, dividerLabel='Selection Mode')
            pm.radioMenuItemCollection()
            pm.menuItem(label='Exclusive', radioButton=not bool(pm.optionVar['MaterialExplorer_SelectMode']),
                        command=self.exclusive_menu_command)
            pm.menuItem(label='Additive', radioButton=bool(pm.optionVar['MaterialExplorer_SelectMode']),
                        command=self.additive_menu_command)

    # 单选菜单命令
    def exclusive_menu_command(self, *args):
        self.set_btns_default()
        pm.optionVar.update({'MaterialExplorer_SelectMode': 0})

    # 多选菜单命令
    def additive_menu_command(self, *args):
        self.set_btns_default()
        pm.optionVar.update({'MaterialExplorer_SelectMode': 1})

    # 选择单选或多选菜单时将所有button设置为初始状态
    def set_btns_default(self):
        pm.select(clear=True)

        for btn in self.selected_mod_btns:
            btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)
            btn.material_ui.delete()
            btn.is_selected = False

        self.selected_mod_btns.clear()

        self.selected_mat_btns.clear()

        self.mi_layout.setVisible(False)

    # ------------------------------mod btn------------------------------

    # 创建所有模型的button
    def create_mod_buttons(self):
        transform_nodes = pm.ls(type='transform')
        mods = [
            mod for mod in transform_nodes
            if isinstance(mod.getShape(), pm.nt.Mesh)
        ]
        with pm.columnLayout(adjustableColumn=True, rowSpacing=5):
            for mod in mods:
                with pm.columnLayout(adjustableColumn=True) as cl:
                    shape = mod.getShape()
                    btn = pm.button(label=mod.name())
                    btn.setCommand(partial(self.mod_button_selected, btn))
                    btn.materials = self.get_shape_materials(shape)  # 模型按钮关联的材质
                    btn.is_selected = False
                    btn.shape = shape  # 模型按钮关联的shape
                    btn.parent = cl

    # 获取当前选择模型的shape的所有材质
    def get_shape_materials(self, shape):
        shading_engines = shape.outputs(type='shadingEngine')
        all_materials = []
        for shadingEngine in shading_engines:
            materials = shadingEngine.surfaceShader.inputs()
            for material in materials:
                all_materials.append(material)

        return all_materials

    # 判断当模型按钮被选择时需要执行的命令
    def mod_button_selected(self, btn, *args):
        if pm.optionVar['MaterialExplorer_SelectMode'] == 0:
            self.mod_button_selected_exclusive(btn)
        else:
            self.mod_button_selected_additive(btn)

    """
    按钮被选择后会创建对应模型关联材质的button并高亮，
    按钮被选择后会被缓存入self.selected_mod_btns列表中，
    当被缓存的按钮再次被点击时删除其对应模型关联材质的button并取消高亮，
    当其他按钮被选择会删除缓存按钮对应模型关联材质的button并取消高亮，
    当按钮被取消选择时若材质属性面板打开则将其隐藏
    """

    # 单选模式下模型按钮被选择时执行的命令
    def mod_button_selected_exclusive(self, btn):
        pm.select(btn.shape, replace=True)
        btn.parent.setBackgroundColor(
            Colors.MOD_BTN_SELECTED_COLOR)  # 高亮被选择的按钮
        self.selected_mat_btns.clear()  # 清除被选择的材质按钮缓存

        if self.selected_mod_btns:
            self.selected_mod_btns[0].parent.setBackgroundColor(
                Colors.DEFAULT_COLOR)  # 取消缓存按钮的高亮
            self.selected_mod_btns[0].material_ui.delete()  # 删除缓存按钮关联材质的button
            self.mi_layout.setVisible(False)  # 隐藏材质属性面板

        if btn.is_selected:
            self.selected_mod_btns.remove(btn)  # 清除按钮缓存
            btn.is_selected = False
        else:
            if self.selected_mod_btns:
                self.selected_mod_btns[0].is_selected = False
                self.selected_mod_btns[0] = btn  # 替换缓存按钮为当前选择按钮
            else:
                self.selected_mod_btns.append(btn)  # 将按钮加入缓存
            btn.is_selected = True
            self.create_mat_buttons(btn)  # 创建对应模型关联材质的button

    """
    当按钮被选择或加选时创建对应模型关联材质的button并高亮，
    当按钮被取消选择时删除对应模型关联材质的button并取消高亮，
    当所有按钮被取消选择时若材质属性面板打开则将其隐藏
    """

    # 多选模式下模型按钮被选择时执行的命令
    def mod_button_selected_additive(self, btn):
        if btn.is_selected:  # 若按钮已经被选择
            pm.select(btn.shape, deselect=True)
            btn.parent.setBackgroundColor(Colors.DEFAULT_COLOR)  # 取消按钮高亮
            btn.is_selected = False

            # 从材质按钮缓存中删除与当前按钮关联的材质按钮
            btn_mat_names = [mat.name() for mat in btn.materials]
            self.selected_mat_btns = list(
                filter(lambda mat_btn: mat_btn.getLabel() not in btn_mat_names, self.selected_mat_btns))

            self.selected_mod_btns.remove(btn)  # 从模型按钮缓存中删除当前按钮
            btn.material_ui.delete()  # 删除模型按钮关联的材质按钮
            self.check_slider_enable()  # 检查材质面板中的属性是否需要开启
        else:
            pm.select(btn.shape, add=True)
            btn.parent.setBackgroundColor(Colors.MOD_BTN_SELECTED_COLOR)  # 高亮按钮
            self.create_mat_buttons(btn)  # 创建模型按钮关联的材质按钮
            btn.is_selected = True
            self.selected_mod_btns.append(btn)  # 将当前按钮加入模型按钮缓存中

        # 若已没有模型按钮被选择，则关闭材质属性面板
        if not self.selected_mod_btns:
            self.mi_layout.setVisible(False)

    # ------------------------------mat btn------------------------------

    # 创建模型按钮关联的所有材质按钮
    def create_mat_buttons(self, btn):
        with pm.formLayout(parent=btn.parent) as formLayout:
            with pm.frameLayout(label=f"The material of {btn.shape.name()}", collapsable=True,
                                backgroundColor=Colors.MOD_BTN_SELECTED_COLOR) as btn.material_ui:
                for material in btn.materials:
                    mat_btn = pm.button(label=material.name())
                    mat_btn.setCommand(partial(self.mat_button_selected, mat_btn))
                    mat_btn.material = material  # 材质按钮关联的材质
                    mat_btn.is_selected = False
                    mat_btn.mat_attrs = {}  # 材质按钮关联的材质属性

        formLayout.attachForm(btn.material_ui, 'top', 0)
        formLayout.attachForm(btn.material_ui, 'left', 10)
        formLayout.attachForm(btn.material_ui, 'right', 10)
        formLayout.attachForm(btn.material_ui, 'bottom', 5)

    # 判断当材质按钮被选择时需要执行的命令
    def mat_button_selected(self, btn, *args):
        if pm.optionVar['MaterialExplorer_SelectMode'] == 0:
            self.mat_button_selected_exclusive(btn)
        else:
            self.mat_button_selected_additive(btn)

    """
    按钮被选择时显示当前按钮关联材质的属性并将按钮高亮，
    按钮被选择后被缓存入self.selected_mat_btns列表中，
    当被缓存的按钮再次被点击时隐藏属性面板并将按钮取消高亮，
    当其他按钮被选择时取消缓存按钮的高亮状态，并显示被选择按钮关联材质的属性且高亮被选择按钮，
    当按钮被取消选择时关闭材质属性面板，
    根据check_slider_enable()函数的逻辑判断是否需要显示材质的属性
    """

    # 单选模式下材质按钮被选择时执行的命令
    def mat_button_selected_exclusive(self, btn):
        self.mi_layout.setVisible(True)  # 显示材质属性面板
        btn.setBackgroundColor(Colors.MAT_BTN_SELECTED_COLOR)  # 高亮被选择的按钮

        if self.selected_mat_btns:
            self.selected_mat_btns[0].setBackgroundColor(Colors.MOD_BTN_SELECTED_COLOR)  # 取消缓存按钮的高亮

        if btn.is_selected:
            self.selected_mat_btns.remove(btn)  # 清除按钮缓存
            btn.is_selected = False
            self.mi_layout.setVisible(False)  # 隐藏材质属性面板
        else:
            if self.selected_mat_btns:
                self.selected_mat_btns[0].is_selected = False
                self.selected_mat_btns[0] = btn  # 替换缓存按钮为当前选择按钮
            else:
                self.selected_mat_btns.append(btn)  # 将按钮加入缓存
            btn.is_selected = True
            self.set_mi_control_value(btn)  # 对材质面板的属性赋值

        self.check_slider_enable()  # 检查材质面板中的属性是否需要开启

    """
    当按钮被选择或加选时显示并更新材质属性并高亮，
    当按钮被取消选择时更新材质属性并取消高亮，
    当所有按钮被取消选择时关闭材质属性面板
    根据check_slider_enable()函数的逻辑判断是否需要显示和更新材质的属性，
    """

    # 多选模式下模型按钮被选择时执行的命令
    def mat_button_selected_additive(self, btn):
        self.mi_layout.setVisible(True)  # 显示材质属性面板

        if btn.is_selected:
            self.selected_mat_btns.remove(btn)  # 从材质按钮缓存中删除当前按钮
            btn.setBackgroundColor(Colors.MOD_BTN_SELECTED_COLOR)  # 取消按钮高亮
            btn.is_selected = False
        else:
            self.selected_mat_btns.append(btn)
            btn.setBackgroundColor(Colors.MAT_BTN_SELECTED_COLOR)  # 高亮按钮
            btn.is_selected = True

        self.set_mi_control_value(btn)  # 对材质面板的属性赋值

        # 若已没有材质按钮被选择，则关闭材质属性面板
        if not self.selected_mat_btns:
            self.mi_layout.setVisible(False)

        self.check_slider_enable()  # 检查材质面板中的属性是否需要开启

    # ------------------------------mat control ui------------------------------

    # 创建材质属性面板slider控件
    def create_mi_slider_ui(self):
        color_control_info = {
            'Base Color': (1, 1, 1),
            'Specular Color': (1, 1, 1)
        }
        float_control_info = {
            'Bump Depth': 1,
            'Metallic Strength': 1,
            'Roughness Strength': 1
        }
        for attr_name, node in color_control_info.items():
            self.create_mi_color_slider_ui(attr_name, node)
        for attr_name, node in float_control_info.items():
            self.create_mi_float_slider_ui(attr_name, node)

    # color slider控件创建逻辑
    def create_mi_color_slider_ui(self, attr_name, value):
        node_color_slider = pm.colorSliderGrp(label=attr_name, adjustableColumn=3, columnAttach=(1, 'right', 5),
                                              height=25, rgb=value)
        node_color_slider.changeCommand(partial(self.set_mat_color_attr, attr_name))
        self.mi_layout.sliders[attr_name] = node_color_slider

    # float slider控件创建逻辑
    def create_mi_float_slider_ui(self, attr_name, value):
        node_float_slider = pm.floatSliderGrp(label=attr_name, field=True, minValue=0, maxValue=1, sliderStep=0.001,
                                              adjustableColumn=3, columnAttach=(1, 'right', 5), height=25, value=value)
        node_float_slider.changeCommand(partial(self.set_mat_float_attr, attr_name))
        self.mi_layout.sliders[attr_name] = node_float_slider

    # 材质float属性赋值逻辑
    def set_mat_float_attr(self, attr_name, *args):
        for btn in self.selected_mat_btns:
            if attr_name in btn.mat_attrs:
                slider = self.mi_layout.sliders[attr_name]
                mat_attr = btn.mat_attrs[attr_name]
                pm.setAttr(mat_attr, slider.getValue())

    # 材质color属性赋值逻辑
    def set_mat_color_attr(self, attr_name, *args):
        for btn in self.selected_mat_btns:
            if attr_name in btn.mat_attrs:
                slider = self.mi_layout.sliders[attr_name]
                mat_attr = btn.mat_attrs[attr_name]
                pm.setAttr(mat_attr, slider.getRgbValue())

    # 对材质属性面板的属性赋值
    def set_mi_control_value(self, btn):
        self.set_mi_base_color_value(btn)
        self.set_mi_specular_color_value(btn)
        self.set_mi_bump_depth_value(btn)
        self.set_mi_metallic_and_roughness_value(btn)

    # 对材质属性面板的base color属性赋值
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

    # 对材质属性面板的specular color属性赋值
    def set_mi_specular_color_value(self, btn):
        if 'Specular Color' in self.mi_layout.sliders:
            if pm.hasAttr(btn.material, 'specularColor'):
                self.set_color_slider_value(btn.material, 'specularColor', 'Specular Color')
                btn.mat_attrs['Specular Color'] = f'{btn.material}.specularColor'

    # color slider赋值逻辑
    def set_color_slider_value(self, node, attr, slider_name):
        color = pm.getAttr(f'{node}.{attr}')
        slider = self.mi_layout.sliders[slider_name]
        slider.setRgbValue(color)

    # 对材质属性面板的bump depth属性赋值
    def set_mi_bump_depth_value(self, btn):
        if 'Bump Depth' in self.mi_layout.sliders:
            mat_bump2ds = btn.material.inputs(type='bump2d')
            if mat_bump2ds:
                mat_bump2d = mat_bump2ds[0]
                self.set_float_slider_value(mat_bump2d, 'bumpDepth', 'Bump Depth')
                btn.mat_attrs['Bump Depth'] = f'{mat_bump2d}.bumpDepth'

    # 对材质属性面板的metallic和roughness属性赋值
    def set_mi_metallic_and_roughness_value(self, btn):
        if 'Metallic Strength' in self.mi_layout.sliders and 'Roughness Strength' in self.mi_layout.sliders:
            mat_multiply_divides = btn.material.inputs(type='multiplyDivide')
            if mat_multiply_divides:
                mat_metallic_strength_constant = None
                mat_roughness_strength_constant = None
                for multiply_divide in mat_multiply_divides:
                    mat_float_constants = multiply_divide.inputs(type='floatConstant')
                    if mat_float_constants:
                        if mat_float_constants[0].name().startswith('metallic_strength'):
                            mat_metallic_strength_constant = multiply_divide.inputs(type='floatConstant')[0]
                        if mat_float_constants[0].name().startswith('roughness_strength'):
                            mat_roughness_strength_constant = multiply_divide.inputs(type='floatConstant')[0]

                if mat_metallic_strength_constant:
                    self.set_float_slider_value(mat_metallic_strength_constant, 'inFloat', 'Metallic Strength')
                    btn.mat_attrs['Metallic Strength'] = f'{mat_metallic_strength_constant}.inFloat'
                if mat_roughness_strength_constant:
                    self.set_float_slider_value(mat_roughness_strength_constant, 'inFloat', 'Roughness Strength')
                    btn.mat_attrs['Roughness Strength'] = f'{mat_roughness_strength_constant}.inFloat'

    # float slider赋值逻辑
    def set_float_slider_value(self, node, attr, slider_name):
        value = pm.getAttr(f'{node}.{attr}')
        slider = self.mi_layout.sliders[slider_name]
        slider.setValue(value)

    """
    材质属性slider开启逻辑：
    共有Base Color、Specular Color、Bump Depth、Metallic和Roughness五个属性显示，
    若所有材质均有这五个属性，则所有属性的slider全部开启，
    若任意一个材质缺少某个属性，则这个属性的slider关闭,
    如材质1有以上五个属性，材质2仅有Specular Color和Bump Depth属性，
    则材质属性面板中仅开始Specular Color和Bump Depth两个Slider
    """

    # 检查材质属性面板的slider是否需要开启
    def check_slider_enable(self):
        sliders = list(self.mi_layout.sliders.values())
        for slider in sliders:
            slider.setEnable(True)

        slider_attr_names = list(self.mi_layout.sliders.keys())
        for btn in self.selected_mat_btns:
            btn_attr_names = btn.mat_attrs.keys()
            for slider_attr_name in slider_attr_names:
                if slider_attr_name not in btn_attr_names:
                    self.mi_layout.sliders[slider_attr_name].setEnable(False)


materialExplorer = MaterialExplorer()
materialExplorer.create_dockable_window()
