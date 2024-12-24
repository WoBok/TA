import unreal

editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def get_actors_by_type(actor_type):
    world = editor_subsystem.get_editor_world()
    actor = unreal.GameplayStatics.get_all_actors_of_class(world, actor_type)
    return actor


def select_static_actors_by_type():
    actors = get_actors_by_type(unreal.StaticMeshActor)  # 通过父类unreal.Actor可以找到所有Actor
    editor_actor_subsystem.set_selected_level_actors(actors)


if __name__ == '__main__':
    select_static_actors_by_type()
