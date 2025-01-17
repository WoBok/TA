# coding=utf-8
import os
import re
from functools import reduce
import unreal

from UnrealUtils import (
    editor_utility_subsystem,
    editor_actor_subsystem
)
from EditorAssetUtils import open_assets_in_editor
from UnrealStructure import WidgetAMStructure

Category = 'Actor Manager Editor BP Function Library'


@unreal.uclass()
class AMEditorBPFLibrary(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(static=True, params=[unreal.Actor], meta=dict(Category=Category))
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
                    new_label += f'%0{len(text)}i' % (index + 1)
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
