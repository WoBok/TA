import os
import unreal


class Toolbox:
    def __init__(self):
        self.menus = unreal.ToolMenus.get()

        self.main_menu = self.menus.find_menu("LevelEditor.MainMenu")
        if not self.main_menu:
            unreal.log_warning("Failed to find the 'Main' menu. Something is wrong in the force!")

    def add_sub_menu(self, menu_name, label, parent, section, tip='placeholder', force_recreate=False):
        submenu_full_name = f'{parent.menu_name}.{menu_name}'
        if force_recreate:
            self.menus.remove_menu(submenu_full_name)
        if not self.menus.is_menu_registered(submenu_full_name):
            self.menus.register_menu(
                name=menu_name,
                parent=parent.menu_name
            )
        sub_menu = self.menus.find_menu(submenu_full_name)
        if not sub_menu:  # Avoid adding duplicated menus
            unreal.log('Creating Menu %s "%s"!' % (submenu_full_name, label))
            sub_menu = parent.add_sub_menu(
                owner=parent.get_name(),
                section_name=section,
                name=menu_name,
                label=label
                # tool_tip=tip
            )
        return sub_menu

    def add_menu_item(self, name, label, parent, command, tip='', insert_after='', section='Scripts'):
        if insert_after:
            # Insert after another menu item
            entry_position = unreal.ToolMenuInsert(insert_after, unreal.ToolMenuInsertType.AFTER)
        else:
            # Insert as first item in menu
            entry_position = unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST)
        new_entry = unreal.ToolMenuEntry(
            name=name,
            # If you pass a type that is not supported Unreal will let you know,
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=entry_position
        )
        new_entry.set_label(label)
        new_entry.set_tool_tip(tip)
        # this is what gets executed on click
        new_entry.set_string_command(
            type=unreal.ToolMenuStringCommandType.COMMAND,
            custom_type="Command",
            string=command
        )
        parent.add_menu_entry(
            section_name=section,
            args=new_entry
        )

        return new_entry

    def create_menu_items(self):
        #######################################################################
        # add a menu in the main menu bar
        #######################################################################
        toolbox_menu = self.add_sub_menu(
            menu_name='PythonTools',
            label='Python Tools',
            parent=self.main_menu,
            section='PythonTools',
            tip='this is a collection of python tool'
        )

        #######################################################################
        # add sections for all the menu and sub menu items
        #######################################################################
        toolbox_menu.add_section(
            section_name='ActorToolsSection',
            label='Actor Tools',
            insert_type=unreal.ToolMenuInsertType.DEFAULT
        )

        toolbox_menu.add_section(
            section_name='AssetToolsSection',
            label='Asset Tools',
            insert_type=unreal.ToolMenuInsertType.DEFAULT
        )

        toolbox_menu.add_section(
            section_name='MiscToolsSection',
            label='Misc',
            insert_type=unreal.ToolMenuInsertType.DEFAULT
        )

        #######################################################################
        # add items for actors section
        #######################################################################
        self.add_menu_item(
            name='LogSelectedActors',
            label='Log Selected Actors',
            parent=toolbox_menu,
            command='py LevelActorUtils.py --log_selected_actors ()',
            tip='Log information for selected actors in level editor',
            section='ActorToolsSection'
        )

        self.add_menu_item(
            name='SelectActorsBySM',
            label='Select Actors By SM_*',
            parent=toolbox_menu,
            command='py LevelActorUtils.py --select_actors_by_label (SM_)',
            tip='Select all actors with label startswith SM_',
            section='ActorToolsSection'
        )

        #######################################################################
        # add items for assets section
        #######################################################################
        asset_menu = self.add_sub_menu(
            menu_name='AssetImportTools',
            label='Asset Import Tools',
            parent=toolbox_menu,
            section='AssetToolsSection',
            tip='this is a collection of python tools for assets'
        )
        self.add_menu_item(
            name='ImportTexture',
            label='Import Example Texture',
            parent=asset_menu,
            command='py EditorAssetUtils.py --example_import_texture_asset ()'
        )
        self.add_menu_item(
            name='ImportStaticMesh',
            label='Import Example Static Mesh',
            parent=asset_menu,
            command='py EditorAssetUtils.py --example_import_sm_asset ()'
        )
        self.add_menu_item(
            name='ImportSkeletonMesh',
            label='Import Example Skeletal Mesh',
            parent=asset_menu,
            command='py EditorAssetUtils.py --example_import_skm_asset ()'
        )

        #######################################################################
        # add items for Misc section
        #######################################################################
        self.add_menu_item(
            name='CBShowCurrentLevel',
            label='Show Current Level in CB',
            parent=toolbox_menu,
            command='py EditorAssetUtils.py --show_current_level_in_cb ()',
            section='MiscToolsSection',
            tip='Show current level in content browser'
        )
        self.add_menu_item(
            name='RawFileBrowser',
            label='Raw File Browser',
            parent=toolbox_menu,
            command='py UnrealContentBrowser.py',
            section='MiscToolsSection',
            tip='Open Raw File Content Browser Standalone'
        )
        self.add_menu_item(
            name='LaunchAMTool',
            label='Launch Actor Manager',
            parent=toolbox_menu,
            command='py ToolLaunchers.py --launch_actor_manager_tool ()',
            section='MiscToolsSection',
            tip='Launch the Actor Manager Tool from BP_UWidget_ActorManager'
        )

        self.menus.refresh_all_widgets()


if __name__ == '__main__':
    tb = Toolbox()
    tb.create_menu_items()
