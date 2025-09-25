import bpy


class AT_OT_find_replace(bpy.types.Operator):
    """ Finds and replaces text in the file """
    bl_idname = "at.find_replace"
    bl_label = "Find Replace"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        old = scene.old_name
        new = scene.new_name
        mode = scene.preset_type_enum

        for obj in bpy.context.selected_objects:
            if mode == 'REPLACE':
                # Update the object name
                obj.name = obj.name.replace(old, new)
                # Update the mesh name
                if obj.type == 'MESH':
                    obj.data.name = obj.name
            elif mode == 'SET':
                pass
            elif mode == 'STRIP':
                pass
            elif mode == 'CASE':
                pass
        return {'FINISHED'}


class AT_PT_batch_rename_panel(bpy.types.Panel):
    """ Batch Rename main panel """
    bl_label = "Batch Rename"
    bl_idname = "AT_PT_batch_rename_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automate Tasks"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "preset_type_enum", text="Mode")

        # Rename Assets
        box = layout.box()

        row = box.row()
        split = row.split(factor=0.3)
        split.label(text="Find:")
        split.prop(scene, "old_name", text="")

        row = box.row()
        split = row.split(factor=0.3)
        split.label(text="Replace:")
        split.prop(scene, "new_name", text="")

        layout.operator("at.find_replace", text="Rename")


def register():
    bpy.utils.register_class(AT_PT_batch_rename_panel)
    bpy.utils.register_class(AT_OT_find_replace)

    # Rename Object Properties
    bpy.types.Scene.old_name = bpy.props.StringProperty(
        name="Old Name",
        description="Old object name",
        default="Old Name"
    )
    bpy.types.Scene.new_name = bpy.props.StringProperty(
        name="New Name",
        description="New object name",
        default="New Name"
    )

    bpy.types.Scene.preset_type_enum : bpy.props.EnumProperty(
        name= "mode",
        description= "Select an option",
        items= [
            ('REPLACE', "Find/Replace", "Replace text in the name"),
            ('SET', "Set Name", "Set a new name or prefix/suffix existing one"),
            ('STRIP', "Strip Characters", "Strip text from the name"),
            ('CASE', "Change Case", "Change case of each name"),
        ]
) # pyright: ignore[reportInvalidTypeForm]

def unregister():
    bpy.utils.unregister_class(AT_PT_batch_rename_panel)
    bpy.utils.unregister_class(AT_OT_find_replace)

if __name__ == "__main__":
    register()