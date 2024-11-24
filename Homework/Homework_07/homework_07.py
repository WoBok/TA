import pymel.core as pm


class MeshSelector:
    def __init__(self):
        self.main_win_name = 'MeshSelector'
        self.main_win_title = 'Mesh Selector'
        self.rbtn_names = ['Poly meshes', 'Nurb meshes', 'Nurb curves']

    # 显示UI
    def show_ui(self):
        self.window = self._create_window()

    # 创建主窗口
    def _create_window(self):
        if pm.window(self.main_win_name, exists=True):
            pm.deleteUI(self.main_win_name, window=True)
        win = pm.window(self.main_win_name, title=self.main_win_title, sizeable=False)
        self._create_layout()
        win.show()

    # 创建主窗口布局
    def _create_layout(self):
        with pm.columnLayout(adjustableColumn=True, rowSpacing=10, width=255) as self.col_layout:
            pm.separator(height=10)
            self._create_buttons()
            pm.separator(height=10)

    # 创建主窗口按钮
    def _create_buttons(self):
        pm.radioCollection()
        for btn_name in self.rbtn_names:
            pm.radioButton(btn_name, label=btn_name,
                           onCommand=eval(self._get_rbtn_command(btn_name)),  # 当按钮被选择时，获取按钮执行逻辑函数名称，并赋值给onCommand
                           offCommand=lambda *args: pm.select(clear=True))  # 当按钮取消选择时，清除所有的选择状态

    # Poly meshes按钮执行逻辑
    def _poly_meshes_rbtn(self, *args):
        self._select_rbtn('mesh', self.rbtn_names[0])

    # Nurb meshes按钮执行逻辑
    def _nurb_meshes_rbtn(self, *args):
        self._select_rbtn('nurbsSurface', self.rbtn_names[1])

    # Nurb curves按钮执行逻辑
    def _nurb_curves_rbtn(self, *args):
        self._select_rbtn('nurbsCurve', self.rbtn_names[2])

    # 选择物体并判断，如果没有当前选择类型的物体则弹出警告
    def _select_rbtn(self, type_name, btn_name):
        if not self._selector(type_name):
            self._show_warning_win(btn_name.lower())

    # 选择对应类型物体执行逻辑
    def _selector(self, type_name):
        nodes = pm.ls(type=type_name)
        if not nodes:
            return False
        pm.select(nodes)
        return True

    # 根据按钮名称创建按钮执行逻辑的函数名称
    def _get_rbtn_command(self, rbtn_name):
        return f"self._{rbtn_name.lower().replace(' ', '_')}_rbtn"

    # 警告提示窗口
    def _show_warning_win(self, rbtn_name):
        if pm.window('WarningWindow', exists=True):
            pm.deleteUI('WarningWindow', window=True)
        win = pm.window('WarningWindow', title='Warning!', widthHeight=(255, 30), sizeable=False)
        with pm.rowLayout(adjustableColumn=True):
            pm.text(f'Warning: No {rbtn_name} in the scene.')
        win.show()


mesh_selector = MeshSelector()
mesh_selector.show_ui()
