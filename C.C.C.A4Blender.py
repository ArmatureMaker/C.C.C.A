bl_info = {
    "name": "Clean Cutters Collection",
    "blender": (4, 2, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "ArmatureMaker.com",
    "description": "Addon to clean up unused objects from Boxcutter's Cutters collection. Ctrl+Alt+X to call it.",
}

import bpy

# Function to clean the cutters collection
def clean_cutters_collection():
    cutters_collection_name = "Cutters"
    unused_collection_name = "Unused Cutters"

    cutters_collection = bpy.data.collections.get(cutters_collection_name)
    if not cutters_collection:
        print(f"Collection named '{cutters_collection_name}' not found")
        return

    if unused_collection_name not in bpy.data.collections:
        unused_collection = bpy.data.collections.new(unused_collection_name)
        bpy.context.scene.collection.children.link(unused_collection)
    else:
        unused_collection = bpy.data.collections[unused_collection_name]

    # Assign red color to the "Unused Cutters" collection
    unused_collection.color_tag = 'COLOR_01'  # COLOR_01 corresponds to red in Blender's palette

    used_objects = set()

    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if modifier.type == 'BOOLEAN':
                used_objects.add(modifier.object)

    for obj in cutters_collection.objects:
        if obj not in used_objects:
            cutters_collection.objects.unlink(obj)
            unused_collection.objects.link(obj)
            print(f"{obj.name} was moved to the 'Unused Cutters' collection")

# Operator for the functionality
class OBJECT_OT_clean_cutters(bpy.types.Operator):
    bl_idname = "object.clean_cutters"
    bl_label = "Clean Cutters"
    bl_description = "Move unused cutter objects to a separate collection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        clean_cutters_collection()
        return {'FINISHED'}

# Pie Menu to access the functionality
class VIEW3D_PIE_MT_clean_cutters(bpy.types.Menu):
    bl_label = "Clean Cutters Pie Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.clean_cutters", text="Clean Cutters", icon='MOD_BOOLEAN')

# Registration and keyboard shortcut assignment
addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_clean_cutters)
    bpy.utils.register_class(VIEW3D_PIE_MT_clean_cutters)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu_pie", type='X', value='PRESS', ctrl=True, alt=True)
    kmi.properties.name = "VIEW3D_PIE_MT_clean_cutters"

    addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(OBJECT_OT_clean_cutters)
    bpy.utils.unregister_class(VIEW3D_PIE_MT_clean_cutters)


if __name__ == "__main__":
    register()
