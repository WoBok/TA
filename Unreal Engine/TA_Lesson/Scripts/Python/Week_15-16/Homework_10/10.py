import unreal
import argparse
import types
import os

#####################################################################
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


#####################################################################

# csv_str = """---,SkeletalAssets
# NewRow1,'/Engine/EngineMeshes/SkeletalCube.SkeletalCube'"""


def create_data_table_with_selected_assets():
    datatable = create_data_table()
    csv_str = get_skeletal_assets_path_csv_string()

    datatable.fill_from_csv_string(csv_str)


def create_data_table():
    package_name, asset_name = asset_tools.create_unique_asset_name('/Game/Week15-16/Blueprint/S_SkeletalAssetTable',
                                                                    '')
    struct_path = '/Game/Week15-16/Blueprint/S_SkeletalAssets'
    struct_asset = unreal.load_asset(struct_path)
    datatable_factory = unreal.DataTableFactory()
    datatable_factory.struct = struct_asset
    return asset_tools.create_asset(asset_name=asset_name, package_path=os.path.dirname(package_name),
                                    asset_class=unreal.DataTable, factory=datatable_factory)


def get_skeletal_assets_path_csv_string():
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    skeletal_assets = [skeletal for skeletal in assets if isinstance(skeletal, unreal.SkeletalMesh)]
    csv_str = "---,SkeletalAssets\n"
    count = 1
    for skeletal_asset in skeletal_assets:
        path = skeletal_asset.get_path_name()
        csv_str += f"{count},'{path}'\n"
        count += 1
    print(csv_str)


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
