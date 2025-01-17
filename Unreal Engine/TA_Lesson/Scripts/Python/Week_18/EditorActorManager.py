import re
from functools import reduce
import unreal

from Reference.UnrealStructure import WidgetAMStructure

Category = 'Actor Manager Editor BP Function Library'
editor_utility_subsystem = unreal.EditorUtilitySubsystem()
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
get_asset_by_path = lambda a: unreal.EditorAssetLibrary.find_asset_data(a).get_asset()


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


@unreal.uclass()  # decorator used to define UClass types from Python
class EditorActorManager(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(static=True, params=[unreal.Actor], meta=dict(Category=Category))
    # unreal.ufunction(meta=None, ret=None, params=None, override=None, static=None, pure=None, getter=None, setter=None)
    # decorator used to define UFunction fields from Python
    def select_actor(actor):
        """
        :type actor: unreal.Actor
        :return:
        """
        editor_actor_subsystem.set_selected_level_actors([actor])
        # return actor.get_actor_label()

    @unreal.ufunction(
        static=True,
        params=[unreal.Array(unreal.Actor), unreal.Set(str)],
        ret=unreal.Array(unreal.Actor),
        meta=dict(Category=Category))
    def filter_actors_by_labels(actors, keywords):
        """
        :type actor: list[unreal.Actor]
        :return:
        """
        if not keywords:
            return actors
        _filter = lambda k: [a for a in actors if re.search(k.lower(), a.get_actor_label().lower())]
        filtered_actors = [_filter(k) for k in keywords if k.strip()]
        if not filtered_actors:
            return actors
        filtered_actors = reduce(lambda a, b: a + b, filtered_actors)
        return list(set(filtered_actors))

    @unreal.ufunction(
        static=True,
        params=[unreal.Actor, str],
        ret=str,
        meta=dict(Category=Category))
    def rename_actor_label(actor, new_label):
        """
        :param actor:
        :param new_label:
        :return:
        """
        old_label = actor.get_actor_label()
        if not old_label == new_label:
            actor.set_actor_label(new_label)
        return new_label

    @unreal.ufunction(
        static=True,
        params=[unreal.Array(unreal.Actor), unreal.Array(unreal.EditableTextBox)],
        meta=dict(Category=Category))
    def batch_rename_actors_label(actors, text_boxes):
        """
        :type actor: list[unreal.Actor]
        :type text_boxes: list[unreal.EditableTextBox]
        :return:
        """
        for index, actor in enumerate(actors):
            new_label = ''
            for tb in text_boxes:
                text = str(tb.get_text())
                if re.search('^#+$', text):
                    # new_label += f'%0{len(text)}i' % (index + 1)
                    new_label += f"{(index + 1):0{len(text)}d}"
                else:
                    new_label += text
            if not new_label:
                return
            actor.set_actor_label(new_label)

    @unreal.ufunction(
        static=True,
        params=[unreal.ComboBoxString, unreal.Array(unreal.Actor)],
        ret=unreal.Array(str),
        meta=dict(Category=Category))
    def setup_combo_box_str_options(box, actors):
        """
        :type box: unreal.ComboBoxString
        :type actors: list[unreal.Actor]
        :return:
        """
        if not actors:
            return []
        mesh_components = actors[0].get_components_by_class(unreal.MeshComponent)
        if not mesh_components:
            return []
        um = unreal.MaterialEditingLibrary
        scalars = []
        switches = []
        vectors = []
        results = []
        for component in mesh_components:
            mi_dynamic = component.get_materials()
            for mi in mi_dynamic:
                scalars.extend(um.get_scalar_parameter_names(mi))
                switches.extend(um.get_static_switch_parameter_names(mi))
                vectors.extend(um.get_vector_parameter_names(mi))
        results.extend([f'<scalar> {a}' for a in scalars])
        results.extend([f'<switch> {a}' for a in switches])
        results.extend([f'<color> {a}' for a in vectors])
        unreal.log(results)
        box.clear_options()
        for option in results:
            box.add_option(option)
        return results

    @unreal.ufunction(
        static=True,
        params=[unreal.Array(unreal.Actor), str],
        ret=WidgetAMStructure,
        meta=dict(Category=Category))
    def randomize_bp_mi_parameters(actors, parameter):
        """
        :type actors: list[unreal.Actor]
        :type parameter: str
        :return:
        """
        results = WidgetAMStructure()
        results.scalar_values = []
        results.switch_values = []
        results.color_values = []
        results.successful = False
        from random import random
        if parameter.startswith('<scalar>'):
            parameter = parameter[8:].strip()
            value_generator = lambda: random()
            value_container = results.scalar_values
        elif parameter.startswith('<switch>'):
            parameter = parameter[8:].strip()
            value_generator = lambda: random() >= 0.5
            value_container = results.switch_values
        elif parameter.startswith('<color>'):
            parameter = parameter[7:].strip()
            value_generator = lambda: [random() * 255, random() * 255, random() * 255]
            value_container = results.color_values
        else:
            unreal.log('Please select a parameter from the list')
            return results
        for actor in actors:
            value = value_generator()
            value_container.append(value)
            actor.set_editor_property(parameter, value)
            unreal.log(f'{actor.get_actor_label()}.{parameter} = {value}')
        results.successful = True
        return results

    @unreal.ufunction(
        static=True,
        params=[unreal.Set(str)],
        ret=bool,
        meta=dict(Category=Category))
    def get_user_edit_permission(names):
        """
        get the permission of current user for editing the blueprint
        :return:
        """
        return os.getlogin().lower() in [x.strip().lower() for x in names]

    @unreal.ufunction(
        static=True,
        params=[unreal.Widget],
        ret=unreal.Class,
        meta=dict(Category=Category))
    def open_bp_widget_editor(bp_reference):
        """
        given the reference to bp widget, open the bp editor for it
        :return:
        """
        bp_object = unreal.load_object(None, bp_reference.get_path_name())
        bp_class = bp_object.get_class()
        bp_path = bp_class.get_path_name()
        open_assets_in_editor(bp_path.split('.')[0])
        return bp_class
