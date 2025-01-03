##########################################################################################
# these code is test against UE 5.0. It doesn't guarantee to be functional in other versions
##########################################################################################


import unreal
from importlib import reload
import UnrealUtils
import re

reload(UnrealUtils)
from UnrealUtils import (
    editor_subsystem,
    editor_actor_subsystem,
    get_asset_by_path
)


def get_actors_by_class(actor_class):
    """
    :type actor_class: unreal.Actor
    :return:
    """
    world = editor_subsystem.get_editor_world()
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
    return actors


def example_get_actors_by_class():
    actors = get_actors_by_class(unreal.StaticMeshActor)
    for actor in actors:
        unreal.log((actor.get_actor_label(), actor))


def get_actors_by_class_name(actor_class_name):
    """
    :type actor_class_name: str
    :return:
    """
    actor_class = getattr(unreal, actor_class_name)
    world = editor_subsystem.get_editor_world()
    actors = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class)
    return actors


def get_actors_by_classes(actor_classes):
    actors = []
    for klass in actor_classes:
        actors.extend(get_actors_by_class(klass))
    return actors


def get_all_actors():
    return get_actors_by_class(unreal.Actor)


def get_actors_by_selection():
    actors = editor_actor_subsystem.get_selected_level_actors()
    return actors


def select_actors_by_class(actor_classes):
    """
    :type actor_classes: unreal.Actor
    :return:
    """
    if type(actor_classes) is list:
        actors = get_actors_by_classes(actor_classes)
    else:
        actors = get_actors_by_class(actor_classes)
    editor_actor_subsystem.set_selected_level_actors(actors)
    return actors


def select_actors_by_class_name(actor_classes_name):
    """
    :type actor_classes_name: str
    :return:
    """
    actors = get_actors_by_class_name(actor_classes_name)
    editor_actor_subsystem.set_selected_level_actors(actors)
    return actors


def get_actors_by_label(keyword):
    actors = get_all_actors()
    filtered_actors = [a for a in actors if re.search(keyword, a.get_actor_label())]
    return filtered_actors


def get_actors_by_tags(tags):
    if not type(tags) is list:
        tags = [tags]
    world = editor_subsystem.get_editor_world()
    actors = []
    for tag in tags:
        actors.extend(unreal.GameplayStatics.get_all_actors_with_tag(world, tag))
    return actors


def select_actors_by_tags(tags):
    actors = get_actors_by_tags(tags)
    editor_actor_subsystem.set_selected_level_actors(actors)
    return actors


def select_actors_by_label(keywold):
    actors = get_actors_by_label(keywold)
    editor_actor_subsystem.set_selected_level_actors(actors)
    return actors


def log_selected_actors():
    """
    This works for both generic actor properties and bluperint actors custom variables
    :return:
    """
    actors = get_actors_by_selection()
    for actor in actors:
        unreal.log('-' * 100)
        unreal.log(f'actor label: {actor.get_actor_label()}')
        unreal.log(f'actor name: {actor.get_name()}')
        unreal.log(f'actor instance name: {actor.get_fname()}')
        unreal.log(f'actor path name: {actor.get_path_name()}')
        unreal.log(f'actor full name: {actor.get_full_name()}')
        unreal.log(f'actor owner: {actor.get_owner()}')
        unreal.log(f'actor parent actor: {actor.get_parent_actor()}')
        unreal.log(f'actor attach parent actor: {actor.get_attach_parent_actor()}')
        unreal.log(f'actor attached actors: {actor.get_attached_actors()}')
        unreal.log(f'actor folder path: {actor.get_folder_path()}')
        unreal.log(f'actor level: {actor.get_level()}')
        unreal.log(f'actor location: {actor.get_actor_location()}')
        unreal.log(f'actor rotation: {actor.get_actor_rotation()}')
        unreal.log(f'actor hidden: {actor.get_editor_property("bHidden")}')
        unreal.log(f'actor BaseColor: {actor.get_editor_property("BaseColor")}')
        root_component = actor.get_editor_property("RootComponent")
        unreal.log(f'actor root component: {root_component}')
        if type(root_component) is unreal.StaticMeshComponent:
            unreal.log(f'component visible: {root_component.get_editor_property("bVisible")}')
            unreal.log(f'component materials override: {root_component.get_editor_property("OverrideMaterials")}')
            unreal.log(f'component materials override: {root_component.get_editor_property("override_materials")}')
            # unreal.log(f'component materials override: {root_component.override_materials}')#this doesn't work in UE5.0
            unreal.log(f'component materials: {root_component.get_materials()}')
            unreal.log(f'component cast shadow: {root_component.get_editor_property("CastShadow")}')


def set_selected_actors_location():
    for actor in get_actors_by_selection():
        actor_location = actor.get_actor_location()
        actor_location.y += 100
        actor.set_actor_location(actor_location, sweep=False, teleport=True)


def set_selected_actors_property(property_name, property_value):
    """
    This works for both generic actor properties and bluperint actors custom variables
    example:
    set_selected_actors_property('BaseColor', (0, 255, 0))
    :param property_name:
    :param property_value:
    :return:
    """
    for actor in get_actors_by_selection():
        try:
            actor.set_editor_property(property_name, property_value)
            continue
        except:
            pass
        for component in actor.get_components_by_class(unreal.ActorComponent):
            try:
                component.set_editor_property(property_name, property_value)
                continue
            except:
                pass


def set_selected_actors_assets(property_name, assets_path):
    """
    :type property_name: str
    :type assets_path: list[str]
    :return:
    """
    assets = [get_asset_by_path(a) for a in assets_path]
    set_selected_actors_property(property_name, assets)


def set_selected_actors_material_parameter(parameter_name, parameter_value):
    """
    :type parameter_name: str
    :type parameter_value: any
    :return:
    """
    for actor in get_actors_by_selection():
        for component in actor.get_components_by_class(unreal.MeshComponent):
            if type(parameter_value) in [int, float]:
                setter = component.set_scalar_parameter_value_on_materials
            elif type(parameter_value) in [tuple, list]:
                parameter_value = unreal.Vector(*parameter_value)
                setter = component.set_vector_parameter_value_on_materials
            elif type(parameter_value) is unreal.Vector:
                setter = component.set_vector_parameter_value_on_materials
            else:
                unreal.log_warning(f'Unsupported type of parameter {parameter_value}')
                break
            setter(parameter_name, parameter_value)


def spawn_actor_from_class(klass, actor_label=''):
    actor_location = unreal.Vector(0, 0, 0)
    actor_rotation = unreal.Rotator(0, 0, 0)
    actor = editor_actor_subsystem.spawn_actor_from_class(
        klass, actor_location, actor_rotation
    )
    if actor_label:
        actor.set_actor_label(actor_label)
    return actor


def spawn_static_mesh_actor_from_asset(asset_path, actor_label=''):
    actor = spawn_actor_from_class(unreal.StaticMeshActor, actor_label)
    asset = get_asset_by_path(asset_path)
    # sm_component = asset.get_component_by_class(unreal.StaticMeshComponent)
    # sm_component.set_editor_property('StaticMesh', asset)
    actor.static_mesh_component.set_static_mesh(asset)


def destroy_actor_by_label(label):
    actors = get_actors_by_label(label)
    for actor in actors:
        actor.destroy_actor()
    return actors


#######################################################################
# copy the following code to your script
#######################################################################
from UnrealUtils import _run

if __name__ == '__main__':
    unreal.log(_run(locals()))
