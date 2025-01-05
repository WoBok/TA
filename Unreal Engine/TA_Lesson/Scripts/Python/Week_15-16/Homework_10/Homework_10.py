import unreal
import argparse
import types
import os

#####################################################################
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_utility = unreal.EditorUtilityLibrary

#####################################################################


# ---------------------------------------create_data_table_with_selected_assets---------------------------------------
"""
1. 首先加载用于创建Data Table的Structure，若不存在则创建
2. 使用加载的Structure创建Data Table
3. 生成所选择的SkeletalMesh路径的csv字符串
4. 将csv字符串导入到已创建的Data Table中
"""


def create_data_table_with_selected_assets():
    struct_asset = load_struct()
    datatable = create_data_table(struct_asset)
    csv_str = get_skeletal_assets_path_csv_string()
    datatable.fill_from_csv_string(csv_str)  # Unreal Engine 5.4之后才有的API


# 创建用存储路径的Data Table
def create_data_table(struct_asset):
    assert struct_asset, "Failed to load or create Data Table"

    package_name, asset_name = asset_tools.create_unique_asset_name('/Game/Data/SkeletalAssetTable', '')
    datatable_factory = unreal.DataTableFactory()
    datatable_factory.struct = struct_asset
    datatable_asset = asset_tools.create_asset(asset_name=asset_name, package_path=os.path.dirname(package_name),
                                               asset_class=unreal.DataTable, factory=datatable_factory)

    unreal.log("The created Data Table has been stored at the path '/Content/Data'.")

    # EditorAssetLibrary.sync_browser_to_objects(asset_paths=['/Game/Data/SkeletalAssetTable'])
    # Unreal Engine 5.5中存在的两个问题：（Unreal Engine 5.3测试无此问题）
    # 1. 如果文件夹之前没有创建，则无法显示文件
    # 2. 如果文件夹已经创建，会成功定位，但是文件内容会消失

    return datatable_asset


# 加载用于创建Data Table的结构体，若没有则创建
def load_struct():
    custom_struct = unreal.load_asset("/Game/Scripts/SkeletalAssetStruct")
    if not custom_struct:
        custom_struct = asset_tools.create_asset(asset_name='SkeletalAssetStruct', package_path='/Game/Scripts',
                                                 asset_class=unreal.UserDefinedStruct,
                                                 factory=unreal.StructureFactory())

        # 此处使用了插件TAPython为Structure添加字段
        # Github Release: https://github.com/cgerchenhp/UE_TAPython_Plugin_Release/releases
        # Document: https://www.tacolor.xyz/pages/PythonEditorLib/PythonStructLib.html#add_variable
        unreal.PythonStructLib.add_variable(custom_struct, "string", "", None, 0, False, "Path")
        unreal.PythonStructLib.remove_variable_by_name(custom_struct,
                                                       unreal.PythonStructLib.get_variable_names(custom_struct)[0])
    return custom_struct


# 创建导入到Data Table中的csv字符串
def get_skeletal_assets_path_csv_string():
    assets = editor_utility.get_selected_assets()
    skeletal_assets = [skeletal for skeletal in assets if isinstance(skeletal, unreal.SkeletalMesh)]
    csv_str = "---,Path\n"
    count = 1
    for skeletal_asset in skeletal_assets:
        path = skeletal_asset.get_path_name()
        csv_str += f"{count},{path}\n"
        count += 1
    return csv_str


# --------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------select_assets_in_data_table---------------------------------------------
"""
1. 从Data Table中获取路径
2. 在Content Browser中显示
"""


def select_assets_in_data_table():
    path = get_skeletal_path_from_datatable()
    unreal.EditorAssetLibrary.sync_browser_to_objects(path)


# 从Data Table中获取SkeletalMesh的路径，若选择多个Data Table，则默认获取多选中第一个Data Table中的路径
def get_skeletal_path_from_datatable():
    assets = editor_utility.get_selected_assets()
    datatable_asset = [datatable for datatable in assets if isinstance(datatable, unreal.DataTable)][0]
    return datatable_asset.get_column_as_string('Path')


# --------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------generate_lods----------------------------------------------------
"""
1. 创建Lod Settings并设置相关参数
2. 从Data Table中存储的路径中加载SkeletalMesh
3. 为SkeletalMesh赋值Lod Settings属性并重新生成Lod
"""


def generate_lods():
    lod_group_settings_lod0 = generate_lod_setting(0.8, 0.8, 4)
    lod_group_settings_lod1 = generate_lod_setting(0.5, 0.5, 3)
    lod_group_settings_lod2 = generate_lod_setting(0.25, 0.25, 2)

    path = get_skeletal_path_from_datatable()
    for p in path:
        lod_settings = unreal.SkeletalMeshLODSettings()
        lod_settings.set_editor_property('lod_groups',
                                         [lod_group_settings_lod0, lod_group_settings_lod1, lod_group_settings_lod2])
        skeletal_mesh = unreal.load_asset(p)
        skeletal_mesh.set_editor_property('lod_settings', lod_settings)
        skeletal_mesh.regenerate_lod(3)


# 创建用于生成Lod的设置
def generate_lod_setting(screen_size, num_of_triangles_percentage, max_bones_per_vertex):
    lod_group_settings_lod = unreal.SkeletalMeshLODGroupSettings()
    lod_group_settings_lod.set_editor_property('screen_size', unreal.PerPlatformFloat(screen_size))

    reduction_settings_lod = unreal.SkeletalMeshOptimizationSettings()
    reduction_settings_lod.set_editor_property('termination_criterion',
                                               unreal.SkeletalMeshTerminationCriterion.SMTC_NUM_OF_TRIANGLES)
    reduction_settings_lod.set_editor_property('num_of_triangles_percentage', num_of_triangles_percentage)
    reduction_settings_lod.set_editor_property('max_bones_per_vertex', max_bones_per_vertex)
    lod_group_settings_lod.set_editor_property('reduction_settings', reduction_settings_lod)

    return lod_group_settings_lod


# --------------------------------------------------------------------------------------------------------------------

def _run(input_locals):
    """
    example code:
    from UnrealUtils import _run
    if __name__ == '__main__':
        unreal.log(_run(locals()))
    :param input_locals: the output from locals
    :type input_locals: dict
    :return: the dict of returns from all invoked functions
    """
    parser = argparse.ArgumentParser()
    funcs = []
    results = {}
    for name, var in input_locals.items():
        if type(var) not in [types.FunctionType, types.LambdaType]:
            continue
        parser.add_argument('--' + name, help=var.__doc__)
        funcs.append(name)
    sys_args = parser.parse_args()
    for func_name in funcs:
        arg_value = getattr(sys_args, func_name)
        if not arg_value:
            continue
        assert arg_value.startswith('(') and arg_value.endswith(')'), \
            f'Insufficient function arguments found for function {func_name}.' \
            f' Needs to match regular expression ^(.*)$'
        if arg_value == '()':
            results[func_name] = input_locals[func_name]()
        else:
            arguments = arg_value[1:-1].split(',')
            #######################################################################
            # try to convert commonly used data from string to Python data types
            # more smart jobs can be done here for example using eval to compile the string
            #######################################################################
            converted_args = []
            for arg in arguments:
                if arg == 'None':
                    converted_args.append(None)
                elif arg == 'True':
                    converted_args.append(True)
                elif arg == 'False':
                    converted_args.append(False)
                elif arg.startswith('[') and arg.endswith(']'):
                    converted_args.append(arg[1:-1].split('/'))
                elif arg.startswith('(') and arg.endswith(')'):
                    converted_args.append(tuple(arg[1:-1].split('/')))
                else:
                    converted_args.append(arg)

            results[func_name] = input_locals[func_name](*converted_args)
    return results


if __name__ == '__main__':
    unreal.log(_run(locals()))
