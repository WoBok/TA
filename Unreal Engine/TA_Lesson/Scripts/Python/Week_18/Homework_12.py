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
    """
    获得Level中选中的Actor
    """

    @unreal.ufunction(static=True, ret=unreal.Array(unreal.Actor), meta=dict(Category=Category))
    def load_selected_actors():
        actors = editor_actor_subsystem.get_selected_level_actors()
        return actors

    """
    对Combo Box String设置选项
    """

    @unreal.ufunction(static=True, params=[unreal.ComboBoxString], meta=dict(Category=Category))
    def set_cbs_options(cbs):
        cbs.clear_options()
        distribution_types = [item.value for item in DistributionType]
        for distribution_type in distribution_types:
            cbs.add_option(distribution_type)

    """
    对选中的Actor进行排列
    """

    @unreal.ufunction(static=True, params=[unreal.Array(unreal.Actor), str, float], meta=dict(Category=Category))
    def distribute_actors(actors, distribution_type, distance_between_actors):
        print(distribution_type)
        match distribution_type:
            case DistributionType.AlongX.value:
                EditorPositionDistributor.distribution_along_axis(actors, distance_between_actors, 'x')
            case DistributionType.AlongY.value:
                EditorPositionDistributor.distribution_along_axis(actors, distance_between_actors, 'y')
            case DistributionType.XYCircle.value:
                EditorPositionDistributor.x_y_circle(actors, distance_between_actors)

    """
    根据轴向排列，排列起点为当前选择的Actor中的第一个的位置
    """

    @staticmethod
    def distribution_along_axis(actors, distance_between_actors, axis):
        for i in range(0, len(actors)):
            if i == 0:  # 若为选中的第一个Actor，则只设置旋转
                target_rotation = unreal.Rotator(0, 0, 0)
                match axis:
                    case 'x':
                        target_rotation = unreal.MathLibrary.make_rot_from_x(unreal.Vector(1, 0, 0))
                    case 'y':
                        target_rotation = unreal.MathLibrary.make_rot_from_x(unreal.Vector(0, 1, 0))
                actors[i].set_actor_rotation(target_rotation, True)
                continue
            # 当前Actor和上一个Actor的宽度各取一半与设置的间隔距离（distance_between_actors）相加
            # 计算出当前Actor位置与上一个Actor位置的偏移
            last_actor_width = EditorPositionDistributor.get_actor_width(actors[i - 1], axis)
            current_actor_width = EditorPositionDistributor.get_actor_width(actors[i], axis)
            last_actor_location = actors[i - 1].get_actor_location()
            interval = last_actor_width / 2 + current_actor_width / 2 + distance_between_actors
            location_offset = unreal.Vector(0, 0, 0)
            match axis:
                case 'x':
                    location_offset = unreal.Vector(interval, 0, 0)
                case 'y':
                    location_offset = unreal.Vector(0, interval, 0)
            target_location = last_actor_location + location_offset  # 上一个Actor的位置加上偏移值计算出当前Actor的位置
            target_rotation = unreal.MathLibrary.make_rot_from_x(location_offset)
            actors[i].set_actor_location_and_rotation(target_location, target_rotation, False, True)

    """
    计算Actor在某个轴向上的宽度
    """

    @staticmethod
    def get_actor_width(actor, axis):
        actor_static_mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
        actor_bounds = actor_static_mesh_comp.get_local_bounds()  # 获取Static Mesh的Bound
        actor_width = 0
        match axis:
            case 'x':
                actor_width = actor_bounds[1].x - actor_bounds[0].x  # 根据Bound计算出Actor的宽度
                actor_scale = actor.get_actor_scale3d().x  # 获得Actor的缩放
                actor_width *= actor_scale  # 将Actor的缩放施加到宽度上
            case 'y':
                actor_width = actor_bounds[1].y - actor_bounds[0].y
                actor_scale = actor.get_actor_scale3d().y
                actor_width *= actor_scale
        return actor_width

    @staticmethod
    def x_y_circle(actors, distance_between_actors):
        origin_location = actors[0].get_actor_location()
        circumference = 0
        for actor in actors:  # 根据每个Actor的宽度和间隔距离计算出圆周长
            actor_width = EditorPositionDistributor.get_actor_width(actor, 'y')
            circumference += actor_width + distance_between_actors
        radius = circumference / (2 * math.pi)  # 根据圆周长计算出圆的半径
        radian = 0
        for actor in actors:
            actor_width = EditorPositionDistributor.get_actor_width(actor, 'y')
            radian += (actor_width / 2 + distance_between_actors) / radius  # 根据Actor的宽度和间隔距离计算出弧度偏移值
            x_location = radius * math.cos(radian)
            y_location = radius * math.sin(radian)  # 使用弧度与半径计算出位置
            radian += actor_width / 2 / radius
            location_offset = unreal.Vector(x_location, y_location, 0)
            target_location = origin_location + location_offset
            target_rotation = unreal.MathLibrary.make_rot_from_x(-location_offset)
            actor.set_actor_location_and_rotation(target_location, target_rotation, False, True)
