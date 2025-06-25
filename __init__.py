bl_info = {
    "name": "Flatten Selected Meshes",
    "author": "erendl",
    "version": (1, 4),
    "blender": (2, 93, 0),
    "location": "3D View > Sidebar > Flatten",
    "description": "Joins selected mesh objects into model_x and removes related empty parents & collections",
    "category": "Object",
}

import bpy, re

def get_next_model_name():x
    existing = [o.name for o in bpy.data.objects if re.match(r"model_\d+", o.name)]
    idx = 1
    while f"model_{idx}" in existing:
        idx += 1
    return f"model_{idx}"

def collect_parents(objects):
    """Collect all parents of the given objects"""
    parents = set()
    for obj in objects:
        current = obj.parent
        while current:
            parents.add(current)
            current = current.parent
    return parents

class FLATTEN_OT_selected_clean(bpy.types.Operator):
    bl_idname = "object.flatten_selected_clean"
    bl_label = "Flatten Selected Meshes (Clean)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_meshes = [o for o in context.selected_objects if o.type == 'MESH']
        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}

        # Collect parent objects 
        parent_objs = collect_parents(selected_meshes)

        # Clear parents
        for obj in selected_meshes:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            obj.select_set(False)

        # Join objects
        for obj in selected_meshes:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = selected_meshes[0]
        bpy.ops.object.join()
        joined_obj = context.active_object
        joined_obj.name = get_next_model_name()

        # Remove parent objects from the scene
        for parent in parent_objs:
            if parent.name in bpy.data.objects:
                bpy.data.objects.remove(parent, do_unlink=True)

        # Clean up empty collections
        for col in bpy.data.collections:
            if not col.objects:
                bpy.data.collections.remove(col)

        self.report({'INFO'}, f"Flatten complete: {joined_obj.name}")
        return {'FINISHED'}

class FLATTEN_PT_panel(bpy.types.Panel):
    bl_label = "Flatten"
    bl_idname = "FLATTEN_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Flatten'

    def draw(self, context):
        self.layout.operator("object.flatten_selected_clean")

def register():
    bpy.utils.register_class(FLATTEN_OT_selected_clean)
    bpy.utils.register_class(FLATTEN_PT_panel)

def unregister():
    bpy.utils.unregister_class(FLATTEN_OT_selected_clean)
    bpy.utils.unregister_class(FLATTEN_PT_panel)

if __name__ == "__main__":
    register()
