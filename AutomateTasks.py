import bpy

class MyProperties(bpy.types.PropertyGroup):
    # Rename Object Properties
    old_name: bpy.props.StringProperty(default="Old Name")  # type: ignore
    new_name: bpy.props.StringProperty(default="New Name")  # type: ignore
    # Rename UV Map
    uvmap_new: bpy.props.StringProperty(default="UVMap")  # type: ignore
    # Test Buttons
    transfere_normals : bpy.props.BoolProperty(default=True) # type: ignore
    transfere_edge_normals : bpy.props.BoolProperty(default=True) # type: ignore
    test : bpy.props.BoolProperty(default=True) # type: ignore
    add_weighted_normals : bpy.props.BoolProperty(default=True) # type: ignore

class AT_OT_find_replace(bpy.types.Operator):
    """ Finds and replaces text in the file """
    bl_idname = "at.find_replace"
    bl_label = "Find Replace"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene.my_properties_props

        old_name = scene.old_name
        new_name = scene.new_name

        for obj in bpy.context.selected_objects:
            # Update the object name
            obj.name = obj.name.replace(old_name, new_name)
            # Update the mesh name
            if obj.type == 'MESH':
                obj.data.name = obj.name

        return {'FINISHED'}
    
class AT_OT_uv_replace(bpy.types.Operator):
    """ Finds and replaces old UV Map with new one """
    bl_idname = "at.uv_replace"
    bl_label = "UV Replace"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene.my_properties_props

        uvmap_new = scene.uvmap_new

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                for uvmap in obj.data.uv_layers:
                    uvmap.name = uvmap_new
                    
        return {'FINISHED'}

class AT_PT_batch_rename_panel(bpy.types.Panel):
    """ Batch Rename main panel """
    bl_label = "Batch Rename"
    bl_idname = "AT_PT_batch_rename_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automate Tasks"

    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT":
            return True
        
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='CURRENT_FILE')    

    def draw(self, context):
        layout = self.layout
        scene = context.scene.my_properties_props

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

        layout.operator("at.find_replace", text="Object Rename")

        box = layout.box()
        row = box.row()
        split = row.split(factor=0.3)
        split.label(text="UV Map:")
        split.prop(scene, "uvmap_new", text="")

        layout.operator("at.uv_replace", text="Uv Map Rename")

        row = layout.row()
        row.label(text="Transfere Normals:")
        row = layout.row(align=True)
        row.prop(scene, "transfere_normals", text="New", toggle=True)
        row.prop(scene, "transfere_edge_normals", text="Prefix", toggle=True)
        
        row = layout.row()
        row.prop(scene, "add_weighted_normals", text="Weighted Normals")
        row = layout.row()
        row.prop(scene, "test", text="Test")

classes = (
    MyProperties,
    AT_PT_batch_rename_panel,
    AT_OT_find_replace,
    AT_OT_uv_replace,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_properties_props = bpy.props.PointerProperty(type=MyProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_properties_props

if __name__ == "__main__":
    register()
if __name__ == "__main__":

    register()
