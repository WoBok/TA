import os
import unreal
import argparse
import types

editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
editor_level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor_utility_subsystem = unreal.EditorUtilitySubsystem()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
get_asset_by_path = lambda a: unreal.EditorAssetLibrary.find_asset_data(a).get_asset()
get_package_from_path = lambda path: unreal.load_package(path)
get_bp_class_by_path = lambda bp_path: unreal.EditorAssetLibrary.load_blueprint_class(bp_path)
asset_registery = unreal.AssetRegistryHelpers.get_asset_registry()


def get_path_to_uasset(asset):
    """
    Given an unreal asset, return the path of uasset in dir
    :type asset: str or unreal.Name or uneal.Object
    :return:
    """
    if type(asset) is str:
        str_asset = asset
    elif type(asset) is unreal.Name:
        str_asset = str(asset)
    else:
        str_asset = asset.get_path_name()
    if str_asset.startswith('/Game/'):
        asset_path = str_asset.replace('\\', '/').replace('/Game/', 'Content/')
        return os.path.join(unreal.Paths.project_dir(), asset_path.split('.')[0] + '.uasset')
    else:
        return str_asset


def run_editor_utility_widget(path_to_widget):
    if path_to_widget.endswith('_C'):
        path_to_widget = path_to_widget[:-2]
    asset = unreal.EditorAssetLibrary.load_asset(path_to_widget)
    editor_utility_subsystem.spawn_and_register_tab(asset)


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
