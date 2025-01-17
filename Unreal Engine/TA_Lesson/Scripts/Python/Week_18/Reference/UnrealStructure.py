# coding=utf-8
import unreal


@unreal.ustruct()
class WidgetAMStructure(unreal.StructBase):
    successful = unreal.uproperty(bool)
    scalar_values = unreal.uproperty(unreal.Array(float))
    switch_values = unreal.uproperty(unreal.Array(bool))
    color_values = unreal.uproperty(unreal.Array(unreal.Color))
