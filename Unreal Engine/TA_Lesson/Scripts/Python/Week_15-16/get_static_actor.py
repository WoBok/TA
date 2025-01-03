import unreal

editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def get_actors_by_type(actor_type):
    world = editor_subsystem.get_editor_world()
    actor = unreal.GameplayStatics.get_all_actors_of_class(world, actor_type)
    return actor


def get_actors_by_selection():
    actor = editor_actor_subsystem.get_selected_level_actors()
    return actor


def select_static_actors_by_type():
    actors = get_actors_by_type(unreal.StaticMeshActor)  # 通过父类unreal.Actor可以找到所有Actor
    editor_actor_subsystem.set_selected_level_actors(actors)


def log_actors():
    # actors = get_actors_by_type(unreal.StaticMeshActor)
    actors = get_actors_by_selection()
    for actor in actors:
        unreal.log("-" * 100)
        unreal.log(f"actor label:{actor.get_actor_label()}")
        unreal.log(f"actor name:{actor.get_name()}")
        unreal.log(f"actor instance name: {actor.get_fname()}")
        unreal.log(f"actor path name:{actor.get_path_name()}")
        unreal.log(f"actor full name: {actor.get_full_name()}")
        unreal.log(f"actor owner:{actor.get_owner()}")
        unreal.log(f"actor parent actor:{actor.get_parent_actor()}")
        unreal.log(f"actor attach parent actor: {actor.get_attach_parent_actor}")
        unreal.log(f"actor attached actors: {actor.get_attached_actors()}")
        unreal.log(f"actor folder path:{actor.get_folder_path()}")
        unreal.log(f"actor level:{actor.get_level()}")
        unreal.log(f"actor location:{actor.get_actor_location()}")
        unreal.log(f"actor rotation: {actor.get_actor_rotation()}")
        unreal.log(f"actor hidden: {actor.get_editor_property('bHidden')}")
        root_component = actor.get_editor_property('RootComponent')
        unreal.log(f"actor root_component: {root_component}")
        unreal.log(f"component visible: {root_component.get_editor_property('bVisible')}")
        # root_component.set_editor_property('bVisible', False)


if __name__ == '__main__':
    # select_static_actors_by_type()
    log_actors()

# log_actors():
# LogPython: actor label:Cube
# LogPython: actor name:StaticMeshActor_1
# LogPython: actor instance name: StaticMeshActor_1
# LogPython: actor path name:/Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel.StaticMeshActor_1
# LogPython: actor full name: StaticMeshActor /Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel.StaticMeshActor_1
# LogPython: actor owner:None
# LogPython: actor parent actor:None
# LogPython: actor attach parent actor: <built-in method get_attach_parent_actor of StaticMeshActor object at 0x00000188F80283B0>
# LogPython: actor attached actors: ["/Script/Engine.StaticMeshActor'/Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel.StaticMeshActor_2'"]
# LogPython: actor folder path:None
# LogPython: actor level:<Object '/Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel' (0x00000B926E578400) Class 'Level'>
# LogPython: actor location:<Struct 'Vector' (0x00000188F801B3A0) {x: -1030.000000, y: 1830.000000, z: 0.000000}>
# LogPython: actor rotation: <Struct 'Rotator' (0x00000188F801B3A0) {pitch: 0.000000, yaw: 0.000000, roll: 0.000000}>
# LogPython: ----------------------------------------------------------------------------------------------------
# LogPython: actor label:Cube2
# LogPython: actor name:StaticMeshActor_2
# LogPython: actor instance name: StaticMeshActor_2
# LogPython: actor path name:/Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel.StaticMeshActor_2
# LogPython: actor full name: StaticMeshActor /Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel.StaticMeshActor_2
# LogPython: actor owner:None
# LogPython: actor parent actor:None
# LogPython: actor attach parent actor: <built-in method get_attach_parent_actor of StaticMeshActor object at 0x00000188F8028110>
# LogPython: actor attached actors: []
# LogPython: actor folder path:None
# LogPython: actor level:<Object '/Game/StarterContent/Maps/StarterMap.StarterMap:PersistentLevel' (0x00000B926E578400) Class 'Level'>
# LogPython: actor location:<Struct 'Vector' (0x00000188F801B3A0) {x: -1020.000000, y: 1840.000000, z: 0.000000}>
# LogPython: actor rotation: <Struct 'Rotator' (0x00000188F801B3A0) {pitch: 0.000000, yaw: 0.000000, roll: 0.000000}>
