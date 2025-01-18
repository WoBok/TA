import unreal
from enum import Enum

Category = "Position Distributor"
editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


class DistributionType(Enum):
    AlongX = 'AlongX'
    AlongY = 'AlongY'
    XYCircle = 'XYCircle'


@unreal.uclass()
class EditorPositionDistributor(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(static=True, ret=unreal.Array(unreal.Actor), meta=dict(Category=Category))
    def load_selected_actors():
        actors = editor_actor_subsystem.get_selected_level_actors()
        return actors

    @unreal.ufunction(static=True, params=[unreal.ComboBoxString], meta=dict(Category=Category))
    def set_cbs_options(cbs):
        cbs.clear_options()
        distribution_types = [item.value for item in DistributionType]
        for distribution_type in distribution_types:
            cbs.add_option(distribution_type)

    @unreal.ufunction(static=True, params=[unreal.Array(unreal.Actor), str, float], meta=dict(Category=Category))
    def distribute_actors(actors, distribution_type, distance_between_actors):
        print(distribution_type)
        match distribution_type:
            case DistributionType.AlongX.value:
                EditorPositionDistributor.distribution_along_x(actors, distance_between_actors)
            case DistributionType.AlongY.value:
                EditorPositionDistributor.distribution_along_y(actors, distance_between_actors)
            case DistributionType.XYCircle.value:
                EditorPositionDistributor.x_y_circle(actors, distance_between_actors)

    @staticmethod
    def distribution_along_x(actors, distance_between_actors):
        print("distribution_along_x")
        for i in range(0, len(actors)):
            if i == 0:
                continue
            last_actor_bounds = actors[i - 1].get_actor_bounds(False, True)
            print(distance_between_actors)
            print(type(distance_between_actors))
            x_location = last_actor_bounds[1].x / 2 + distance_between_actors
            print()
            target_location = last_actor_bounds[0] + unreal.Vector(x_location, 0, 0)
            actors[i].set_actor_location(target_location, False, True)

    @staticmethod
    def distribution_along_y(actors, distance_between_actors):
        print("distribution_along_y")
        for i in range(0, len(actors)):
            if i == 0:
                continue
            last_actor_bounds = actors[i - 1].get_actor_bounds(False, True)

            y_location = last_actor_bounds[1].y / 2 + distance_between_actors
            target_location = last_actor_bounds[0] + unreal.Vector(0, y_location, 0)
            actors[i].set_actor_location(target_location, False, True)

    @staticmethod
    def x_y_circle(actors, distance_between_actors):
        print("x_y_circle")
        for actor in actors:
            print(actor.get_name())
