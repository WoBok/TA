##########################################################################################
# these code is test against UE 5.0. It doesn't guarantee to be functional in other versions
##########################################################################################


import os
import unreal
from importlib import reload

import UnrealUtils

reload(UnrealUtils)
from UnrealUtils import (
    get_package_from_path,
    asset_tools,
    get_asset_by_path,
    editor_level_subsystem,
    get_bp_class_by_path,
    editor_subsystem
)


def get_cb_selection():
    """
    get asset selection list from content browser selection
    :return:
    """
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    for a in assets:
        unreal.log(a)
    return assets
    #######################################################################
    # alternative
    # utility_base = unreal.GlobalEditorUtilityBase.get_default_object()
    # return utility_base.get_selected_assets()
    #######################################################################


def show_assets_in_cb(paths=None):
    """
    :param paths: Asset paths
    :return:
    """
    if paths is None:
        paths = []
    elif type(paths) is str:
        paths = [paths]
    elif type(paths) is list:
        pass
    else:
        raise Exception(f'Unknown value {paths} in parameter paths')
    unreal.EditorAssetLibrary.sync_browser_to_objects(asset_paths=paths)


def show_current_level_in_cb():
    """
    show current level in content browser
    :return:
    """
    level_path = editor_level_subsystem.get_current_level().get_path_name()
    show_assets_in_cb([level_path])
    return level_path


def open_assets_in_editor(paths=None):
    """
    :param paths: Asset paths
    :return:
    """
    if paths is None:
        paths = []
    elif type(paths) is str:
        paths = [paths]
    elif type(paths) in [list, tuple, set]:
        pass
    else:
        raise Exception(f'Unknown value {paths} in parameter paths')
    loaded_assets = [get_asset_by_path(x) for x in paths]
    asset_tools.open_editor_for_assets(assets=loaded_assets)


def asset_exists(path=''):
    """
    example py EditorAssetUtils.py --asset_exists (/Game/LevelPrototyping/Textures/T_GridChecker_A.T_GridChecker_A)
    :param path: Asset path
    :return: True if the asset exists
    """
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path=path)


def get_material_instance_constant_parameter(mi_asset_path, parameter_name):
    """
    example:
    py EditorAssetUtils.py --get_material_instance_constant_parameter (/Game/LevelPrototyping/Materials/M_Solid_Red.M_Solid_Red,BaseColor)
    :param mi_asset_path: the path to material instance asset
    :param parameter_name: name of parameter to get value from
    :return:
    """
    mi_asset = get_asset_by_path(mi_asset_path)
    #######################################################################
    # get all parameters first and use it for looking up
    #######################################################################
    scalars = unreal.MaterialEditingLibrary.get_scalar_parameter_names(mi_asset)
    switches = unreal.MaterialEditingLibrary.get_static_switch_parameter_names(mi_asset)
    textures = unreal.MaterialEditingLibrary.get_texture_parameter_names(mi_asset)
    vectors = unreal.MaterialEditingLibrary.get_vector_parameter_names(mi_asset)

    #######################################################################
    # try to get the correct type of parameter. If not valid type found raise exception
    #######################################################################
    if parameter_name in scalars:
        getter = unreal.MaterialEditingLibrary.get_material_instance_scalar_parameter_value
    elif parameter_name in switches:
        getter = unreal.MaterialEditingLibrary.get_material_instance_static_switch_parameter_value
    elif parameter_name in textures:  # unreal.Texture
        getter = unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value
    elif parameter_name in vectors:
        getter = unreal.MaterialEditingLibrary.get_material_instance_vector_parameter_value
    else:
        raise Exception(f'Unsupported type of parameter name {parameter_name}')
    parameter_value = getter(instance=mi_asset, parameter_name=parameter_name)
    # unreal.log(f'{mi_asset_path}.{parameter_name} is {parameter_value}')
    return parameter_value


def build_skm_import_options(skeleton_path=None):
    """
    :param skeleton_path: Skeleton asset path of the skeleton that will be used to bind the mesh
    :return: Import option object. The basic import options for importing a skeletal mesh
    """
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.import_mesh = True
    options.import_as_skeletal = True
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    options.import_textures = False
    options.import_materials = False
    options.create_physics_asset = False
    if skeleton_path is None:
        options.skeleton = skeleton_path
    else:
        options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    import_data = options.skeletal_mesh_import_data
    import_data.import_translation = unreal.Vector(0.0, 0.0, 0.0)
    import_data.import_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    import_data.import_uniform_scale = 1.0

    #######################################################################
    # unreal.FbxSkeletalMeshImportData
    # Calling the FbxSkeletalMeshImportData properties with . doesn't work in UE5.0
    # TODO: try the following code again in UE 5.1+ and see if it is fixed
    # import_data.import_morph_targets = True
    # import_data.update_skeleton_reference_pose = False
    #######################################################################
    import_data.set_editor_property('import_morph_targets', True)
    import_data.set_editor_property('update_skeleton_reference_pose', False)
    return options


def example_import_skm_asset():
    source = r"D:\zuobiao\Graphics\human_rig.fbx"
    directory = '/Game/Gameplay'
    option = build_skm_import_options(skeleton_path='/Game/Gameplay/human_rig_Skeleton.human_rig_Skeleton')
    task = build_import_task(source, directory, dest_name='New_Human', options=option)
    asset_paths = execute_import_tasks([task])
    show_assets_in_cb(asset_paths)


def example_import_csv_asset():
    source = r"D:\zuobiao\Python\UnrealPython\example.csv"
    directory = '/Game/Gameplay'
    struct_path = '/Game/Gameplay/Struct_Example.Struct_Example'
    datatable_task = build_import_task(source, directory)
    factory = unreal.CSVImportFactory()
    factory.automated_import_settings.import_row_struct = get_asset_by_path(struct_path)
    datatable_task.factory = factory
    asset_paths = execute_import_tasks([datatable_task])
    show_assets_in_cb(asset_paths)


def build_anim_import_options(skeleton_path=None):
    """
    :param skeleton_path: Skeleton asset path of the skeleton that will be used to bind the animation
    :return: Import option object. The basic import options for importing an animation
    """
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.import_animations = True
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
    if skeleton_path is None:
        options.skeleton = skeleton_path
    else:
        options.skeleton = unreal.load_asset(skeleton_path)
    # unreal.FbxMeshImportData
    import_data.import_translation = unreal.Vector(0.0, 0.0, 0.0)
    import_data.import_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    import_data.import_uniform_scale = 1.0

    #######################################################################
    # unreal.FbxAnimSequenceImportData
    # Calling the FbxAnimSequenceImportData properties with . doesn't work in UE5.0
    # TODO: try the following code again in UE 5.1+ and see if it is fixed
    # import_data.animation_length = unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME
    # import_data.remove_redundant_keys = False
    #######################################################################
    import_data = options.anim_sequence_import_data
    import_data.set_editor_property(
        'animation_length',
        unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME
    )
    import_data.set_editor_property('remove_redundant_keys', False)
    return options


def regenerate_skeletal_mesh_lods(skeletal_mesh_path, num_of_lods=4):
    """
    regenerate lods for given skeletal mesh
    :param skeletal_mesh_path: skeletal mesh path
    :param num_of_lods:
    :return:
    """
    asset = get_asset_by_path(skeletal_mesh_path)
    result = asset.regenerate_lod(num_of_lods)
    if not result:
        unreal.log_warning(f'Unable to generate lods for {skeletal_mesh_path}')


def create_directory(path=''):
    """
    :param path: Directory path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.make_directory(directory_path=path)


def duplicate_directory(from_dir='', to_dir=''):
    """
    :param from_dir: Directory path to duplicate
    :param to_dir: Duplicated directory path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.duplicate_directory(
        source_directory_path=from_dir,
        destination_directory_path=to_dir
    )


####################################################################################################
# def create_generic_asset_example():
#     base_path = '/Game/GenericAssets/'
#     generic_assets = [
#         [base_path + 'sequence',        unreal.LevelSequence,  unreal.LevelSequenceFactoryNew()],
#         [base_path + 'material',        unreal.Material,       unreal.MaterialFactoryNew()], # for parent material
#         [base_path + 'world',           unreal.World,          unreal.WorldFactory()],
#         [base_path + 'particle_system', unreal.ParticleSystem, unreal.ParticleSystemFactoryNew()],
#         [base_path + 'paper_flipbook',  unreal.PaperFlipbook,  unreal.PaperFlipbookFactory()],
#         [base_path + 'data_struct',  unreal.UserDefinedStruct, unreal.StructureFactory()]
#     ]
#     for asset in generic_assets:
#         print create_generic_asset(asset[0], asset[1], asset[2])
####################################################################################################
def create_generic_asset(asset_path='', asset_class=None, asset_factory=None, unique_name=True):
    """
    :param asset_path: Path of asset to create
    :param asset_class: The asset class
    :param asset_factory: The associated factory of the class.
    :param unique_name: If True, will add a number at the end of the asset name until unique
    :return: The created asset
    """
    if unique_name:
        asset_path, asset_name = asset_tools.create_unique_asset_name(
            base_package_name=asset_path, suffix=''
        )
    if asset_exists(asset_path):
        result = unreal.load_asset(asset_path)
    else:
        _path_ = os.path.dirname(asset_path)
        _name_ = os.path.basename(asset_path)
        result = asset_tools.create_asset(
            asset_name=_name_, package_path=_path_,
            asset_class=asset_class,
            factory=asset_factory
        )
    show_assets_in_cb([asset_path])
    return result


def example_create_datatable_asset(asset_path='', data_struct=''):
    """
    example_create_datatable_asset('/Game/Gameplay/dt_Example', '/Game/Gameplay/Struct_Example')
    :param asset_path:
    :param data_struct:
    :return:
    """
    row_struct = create_generic_asset(data_struct, unreal.UserDefinedStruct, unreal.StructureFactory())
    datatable_factory = unreal.DataTableFactory()
    datatable_factory.struct = row_struct
    create_generic_asset(asset_path, unreal.DataTable, datatable_factory)


def create_material_instance_constant(parent_material_path, mi_asset_name=None):
    """
    create a material instance in the same directory of parent material
    :param mi_asset_name: the material instance name
    :param parent_material_path: the parent material path
    :return:
    """
    parent_material = get_asset_by_path(parent_material_path)
    #######################################################################
    #  if no name is given it will use the parent name + inst
    #######################################################################
    if not mi_asset_name:
        parent_material_basename = os.path.basename(parent_material_path)
        parent_material_basename = parent_material_basename.split('.')[0]
        mi_asset_name = parent_material_basename + '_inst'
    mi_asset_directory = os.path.dirname(parent_material_path)
    mi_asset_path = '/'.join([mi_asset_directory, mi_asset_name])
    mi_asset = create_generic_asset(
        asset_path=mi_asset_path,
        asset_class=unreal.MaterialInstanceConstant,
        asset_factory=unreal.MaterialInstanceConstantFactoryNew()
    )
    unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, parent_material)
    #######################################################################
    # optional auto saving
    # unreal.EditorAssetLibrary.save_asset(mi_asset_path)
    #######################################################################
    return mi_asset_path


def example_create_material_instances():
    import random
    for i in range(10):
        mi_asset_path = create_material_instance_constant(
            '/Game/LevelPrototyping/Materials/M_Solid.M_Solid',
            f'M_Solid_colored_{i}'
        )
        set_material_instance_constant_parameter(
            mi_asset_path,
            'BaseColor',
            (random.random(), random.random(), random.random())
        )


def duplicate_asset(from_path='', to_path=''):
    """
    example:
    duplicate_asset(
    '/Game/LevelPrototyping/Textures/T_GridChecker_A.T_GridChecker_A',
    '/Game/Gameplay/T_Grid')
    :param from_path: Asset path to duplicate
    :param to_path: Duplicated asset path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.duplicate_asset(
        source_asset_path=from_path,
        destination_asset_path=to_path
    )


def rename_asset(from_path='', to_path=''):
    """
    example:
    rename_asset('/Game/Gameplay/T_Grid.T_Grid', '/Game/Gameplay/T_Grid1')
    :param from_path: Asset path to rename
    :param to_path: Renamed asset path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.rename_asset(
        source_asset_path=from_path,
        destination_asset_path=to_path
    )


def delete_asset(path=''):
    """
    example:
    delete_asset('/Game/Gameplay/T_Grid1.T_Grid1')
    :param path: Asset path
    :return: True if the operation succeeds
    """
    if not path:
        return
    elif asset_exists(path):
        return unreal.EditorAssetLibrary.delete_asset(asset_path_to_delete=path)


def duplicate_asset_dialog(from_path='', to_path='', show_dialog=True):
    """
    example:
    duplicate_asset_dialog(
        '/Game/LevelPrototyping/Textures/T_GridChecker_A.T_GridChecker_A',
        '/Game/LevelPrototyping/Textures/T_Grid'
    )
    This function will also work on assets of the type level. (But might be really slow if the level is huge)
    :param from_path: Asset path to duplicate
    :param to_path: Duplicate asset path
    :param show_dialog: True if you want to show the confirm pop-up
    :return: True if the operation succeeds
    """
    splitted_path = to_path.rsplit('/', 1)
    asset_path = splitted_path[0]
    asset_name = splitted_path[1]
    if show_dialog:
        return asset_tools.duplicate_asset_with_dialog(
            asset_name=asset_name,
            package_path=asset_path,
            original_object=get_asset_by_path(from_path)
        )
    else:
        return asset_tools.duplicate_asset(
            asset_name=asset_name, package_path=asset_path,
            original_object=get_asset_by_path(from_path)
        )


def rename_asset_dialog(from_path='', to_path='', show_dialog=True):
    """
    This function will also work on assets of the type level.
     (But might be really slow if the level is huge)
    :param from_path: Asset path to rename
    :param to_path: Renamed asset path
    :param show_dialog: True if you want to show the confirm pop-up
    :return: True if the operation succeeds
    """
    asset_path = os.path.dirname(to_path)
    asset_name = os.path.basename(to_path)
    rename_data = unreal.AssetRenameData(
        asset=get_asset_by_path(from_path),
        new_package_path=asset_path,
        new_name=asset_name
    )
    if show_dialog:  # this currently doesn't work in UE 5.0 TODO: test it in 5.1+
        return asset_tools.rename_assets_with_dialog(assets_and_names=[rename_data])
    else:
        return asset_tools.rename_assets(assets_and_names=[rename_data])


def save_asset(path='', force_save=True):
    """
    :param path: Asset path
    :param force_save:
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.save_asset(
        asset_to_save=path,
        only_if_is_dirty=not force_save
    )


def save_directory(path='', force_save=True, recursive=True):
    """
    :param path: Directory path
    :param force_save:
    :param recursive:
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.save_directory(
        directory_path=path,
        only_if_is_dirty=not force_save,
        recursive=recursive
    )


def get_all_dirty_packages():
    """
    :return: The assets that need to be saved
    """
    packages = []
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages


def save_all_dirty_packages(show_dialog=False):
    """
    :param show_dialog: True if you want to see the confirm pop-up
    :return: True if the operation succeeds
    """
    if bool(show_dialog):
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(
            save_map_packages=True,
            save_content_packages=True
        )
    else:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
            save_map_packages=True,
            save_content_packages=True
        )


def save_packages(packages_path=None, show_dialog=False):
    """
    save the given packages that is dirty only
    :type packages_path: list[str]
    :param show_dialog: True if you want to see the confirm pop-up
    :return: True if the operation succeeds
    """
    if packages_path is None:
        packages_path = []
    packages = [get_package_from_path(p) for p in packages_path]
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_packages_with_dialog(
            packages_to_save=packages,
            only_dirty=False  # note that only_dirty=False
        )
    else:
        return unreal.EditorLoadingAndSavingUtils.save_packages(
            packages_to_save=packages,
            only_dirty=False
        )


#######################################################################
# def import_my_assets_example():
#     texture_task = build_import_task('C:/Path/To/Assets/Texture.TGA', '/Game/Textures')
#     sound_task = build_import_task('C:/Path/To/Assets/Sound.WAV', '/Game/Sounds')
#     static_mesh_task = build_import_task(
#         'C:/Path/To/Assets/StaticMesh.FBX',
#         '/Game/StaticMeshes',
#         options=build_sm_import_options()
#     )
#     skeletal_mesh_task = build_import_task(
#         'C:/Path/To/Assets/SkeletalMesh.FBX',
#         '/Game/SkeletalMeshes',
#         options=build_skm_import_options('/Game/SkeletalMeshes/skeleton')
#     )
#     animation_task = build_import_task(
#         'C:/Path/To/Assets/Animation.FBX',
#         '/Game/Animations',
#         options=build_anim_import_options('/Game/SkeletalMeshes/skeleton')
#     )
#     unreal.log(execute_import_tasks([texture_task, sound_task, static_mesh_task, skeletal_mesh_task]))
#     # Not executing the animation_task at the same time of the skeletal_mesh_task because it look
#     # like it does not work if it's the case. Pretty sure it's not normal.
#     unreal.log(execute_import_tasks([animation_task]))
#######################################################################
def build_import_task(filename='', dest_path='', dest_name=None, options=None):
    """
    :param filename: Windows file fullname of the asset you want to import
    :param dest_path: Asset path
    :param dest_name: Asset name
    :param options: Import option object. Can be None for assets that does not usually
     have a pop-up when importing. (e.g. Sound, Texture, etc.)
    :return: The import task object
    """
    task = unreal.AssetImportTask()
    task.automated = True  # no UI

    #######################################################################
    # if destination is not specified it will use the source name
    #######################################################################
    if dest_name is not None:
        task.destination_name = dest_name
    task.destination_path = dest_path
    task.filename = filename

    #######################################################################
    # in this case the import will always override existed mesh if the name of asset already occupied
    # Alternatively this can be changed to additive importing
    #######################################################################
    task.replace_existing = True

    #######################################################################
    # optional auto saving the asset after finishing importing
    # which will trigger source control actions if there is any
    # task.save = True
    #######################################################################
    task.set_editor_property('options', options)
    return task


def execute_import_tasks(tasks=None):
    """
    :param tasks: The import tasks object. You can get them from buildImportTask()
    :return: The paths of successfully imported assets
    """
    if tasks is None:
        tasks = []
    asset_tools.import_asset_tasks(tasks)
    imported_asset_paths = []
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            imported_asset_paths.append(path)
    return imported_asset_paths


def example_import_texture_asset():
    source = r"D:\zuobiao\Graphics\T_Color.tga"
    directory = '/Game/Gameplay'
    task = build_import_task(source, directory)
    asset_paths = execute_import_tasks([task])
    show_assets_in_cb(asset_paths)


def build_sm_import_options():
    """
    :return: Import option object. The basic import options for importing a static mesh
    """
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.import_mesh = True
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    options.import_textures = False
    options.import_materials = False
    options.import_as_skeletal = False
    # unreal.FbxMeshImportData
    import_data = options.static_mesh_import_data
    import_data.import_translation = unreal.Vector(0.0, 0.0, 0.0)
    import_data.import_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    import_data.import_uniform_scale = 1.0

    #######################################################################
    # unreal.FbxStaticMeshImportData
    # Calling the FbxStaticMeshImportData properties with . doesn't work in UE5.0
    # TODO: try the following code again in UE 5.1+ and see if it is fixed
    # import_data.combine_meshes = True
    # import_data.generate_lightmap_u_vs = True
    # import_data.auto_generate_collision = True
    #######################################################################
    import_data.set_editor_property('combine_meshes', True)
    import_data.set_editor_property('generate_lightmap_u_vs', True)
    import_data.set_editor_property('auto_generate_collision', True)
    return options


def example_import_sm_asset():
    source = r"D:\zuobiao\Graphics\tree.fbx"
    directory = '/Game/Gameplay'
    task = build_import_task(source, directory, options=build_sm_import_options())
    asset_paths = execute_import_tasks([task])
    show_assets_in_cb(asset_paths)


def delete_directory(path=''):
    """
    :param path: Directory path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.delete_directory(directory_path=path)


def directory_exists(path=''):
    """
    :param path: Directory path
    :return: True if the directory exists
    """
    return unreal.EditorAssetLibrary.does_directory_exist(directory_path=path)


def rename_directory(from_dir='', to_dir=''):
    """
    :param from_dir: Directory path to rename
    :param to_dir: Renamed directory path
    :return: True if the operation succeeds
    """
    return unreal.EditorAssetLibrary.rename_directory(
        source_directory_path=from_dir,
        destination_directory_path=to_dir
    )


#######################################################################
# copy the following code to your script
#######################################################################
from UnrealUtils import _run

if __name__ == '__main__':
    unreal.log(_run(locals()))


def set_material_instance_constant_parameter(mi_asset_path, parameter_name, parameter_value):
    """
    example:
    EditorAssetUtils.set_material_instance_constant_parameter('/Game/LevelPrototyping/Materials/M_Solid_Red.M_Solid_Red', 'BaseColor', (0,1,0))
    :param mi_asset_path: the path to material instance asset
    :param parameter_name: name of parameter to change
    :param parameter_value: value of parameter to set
    :return:
    """
    mi_asset = get_asset_by_path(mi_asset_path)
    #######################################################################
    # get all parameters first and use it for looking up
    #######################################################################
    scalars = unreal.MaterialEditingLibrary.get_scalar_parameter_names(mi_asset)
    switches = unreal.MaterialEditingLibrary.get_static_switch_parameter_names(mi_asset)
    textures = unreal.MaterialEditingLibrary.get_texture_parameter_names(mi_asset)
    vectors = unreal.MaterialEditingLibrary.get_vector_parameter_names(mi_asset)

    #######################################################################
    # try to get the correct type of parameter. If not valid type found raise exception
    #######################################################################
    if parameter_name in scalars:
        setter = unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value
    elif parameter_name in switches:
        setter = unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value
    elif parameter_name in textures:  # unreal.Texture
        setter = unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value
        parameter_value = get_asset_by_path(parameter_value)
    elif parameter_name in vectors:
        setter = unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value
        parameter_value = unreal.LinearColor(*parameter_value, 1.0)
    else:
        raise Exception(f'Unsupported type of parameter name {parameter_name}')
    original_value = get_material_instance_constant_parameter(mi_asset_path, parameter_name)
    setter(instance=mi_asset, parameter_name=parameter_name, value=parameter_value)
    unreal.log(f'{mi_asset_path}.{parameter_name} is changed from {original_value} to {parameter_value}')
    #######################################################################
    # optional auto saving
    # unreal.EditorAssetLibrary.save_asset(mi_asset_path)
    #######################################################################

    #######################################################################
    # update the material viewport when it's opened
    #######################################################################
    unreal.MaterialEditingLibrary.update_material_instance(mi_asset)


def set_asset_property(asset_path, property_name, property_value):
    """
    this only works for non-bp assets
    :param asset_path: path of asset
    :param property_name: name of property to set
    :param property_value:
    :return:
    """
    asset = get_asset_by_path(asset_path)
    original_value = asset.get_editor_property(property_name)
    asset.set_editor_property(property_name, property_value)
    unreal.log(f'{asset_path}.{property_name} is changed from {original_value} to {property_value}')

    #######################################################################
    # optional auto saving
    # unreal.EditorAssetLibrary.save_asset(asset_path)
    #######################################################################
    return property_value


def get_asset_property(asset_path, property_name):
    """
    this only works for non-bp assets
    :param asset_path: path of asset
    :param property_name: name of property to set
    :return:
    """
    asset = get_asset_by_path(asset_path)
    property_value = asset.get_editor_property(property_name)
    unreal.log(f'{asset_path}.{property_name} = {property_value}')
    return property_value
