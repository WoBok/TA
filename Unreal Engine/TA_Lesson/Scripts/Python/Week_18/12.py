import math
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
        for i in range(0, len(actors)):
            if i == 0:
                continue
            last_actor_scale = actors[i - 1].get_actor_scale3d()
            last_actor_bounds = actors[i - 1].get_actor_bounds(True, True)
            last_actor_bound_x = last_actor_bounds[1].x * last_actor_scale.x

            current_actor_scale = actors[i].get_actor_scale3d()
            current_actor_bounds = actors[i].get_actor_bounds(True, True)
            current_actor_bound_x = current_actor_bounds[1].x * current_actor_scale.x
            x_location = last_actor_bound_x / 2 + current_actor_bound_x / 2 + distance_between_actors

            last_actor_location = actors[i - 1].get_actor_location()

            target_location = last_actor_location + unreal.Vector(x_location, 0, 0)
            actors[i].set_actor_location(target_location, False, True)

    @staticmethod
    def distribution_along_y(actors, distance_between_actors):
        for i in range(0, len(actors)):
            if i == 0:
                continue
            last_actor_scale = actors[i - 1].get_actor_scale3d()
            last_actor_bounds = actors[i - 1].get_actor_bounds(True, True)
            last_actor_bound_y = last_actor_bounds[1].y * last_actor_scale.y

            current_actor_scale = actors[i].get_actor_scale3d()
            current_actor_bounds = actors[i].get_actor_bounds(True, True)
            current_actor_bound_y = current_actor_bounds[1].y * current_actor_scale.y
            y_location = last_actor_bound_y / 2 + current_actor_bound_y / 2 + distance_between_actors

            last_actor_location = actors[i - 1].get_actor_location()

            target_location = last_actor_location + unreal.Vector(0, y_location, 0)
            actors[i].set_actor_location(target_location, False, True)

    @staticmethod
    def x_y_circle(actors, distance_between_actors):
        origin_location = actors[0].get_actor_location()
        circumference = 0
        for actor in actors:
            actor_bounds = actor.get_actor_bounds(True, True)
            actor_scale = actor.get_actor_scale3d()
            circumference += actor_bounds[1].y * actor_scale.y + distance_between_actors
        radius = circumference / (2 * math.pi)
        radian = 0
        for actor in actors:
            actor_bounds = actor.get_actor_bounds(True, True)
            actor_scale = actor.get_actor_scale3d()
            radian += (actor_bounds[1].y * actor_scale.y + distance_between_actors) / radius
            x_location = radius * math.cos(radian)
            y_location = radius * math.sin(radian)
            target_location = origin_location + unreal.Vector(x_location, y_location, 0)
            actor.set_actor_location(target_location, False, True)
