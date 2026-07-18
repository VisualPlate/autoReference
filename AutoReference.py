
bl_info = {
    "name": "Auto Reference Image Adder",
    "author": "Jere Tolonen",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Add > Image > Custom Submenu",
    "description": "Adds a reference image to specific locations using a file popup browser via a submenu",
    "category": "Object",
}

import bpy
import os
import math
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

#BASE SETTINGS
OFFSET_DIST = 15.0
SCALE_AMOUNT = {
    'x': 1.0,
    'y': 1.0,
    'z': 1.0
}
AXIS_CONFIG = {
    'FRONT':  ((math.radians(90), 0, 0),               (0, -OFFSET_DIST, 0)),
    'BACK':   ((math.radians(90), 0, math.radians(180)), (0, OFFSET_DIST, 0)),
    'LEFT':   ((math.radians(90), 0, math.radians(-90)), (-OFFSET_DIST, 0, 0)),
    'RIGHT':  ((math.radians(90), 0, math.radians(90)),  (OFFSET_DIST, 0, 0)),
    'TOP':    ((0, 0, 0),                                (0, 0, OFFSET_DIST)),
    'BOTTOM': ((math.radians(180), 0, 0),                (0, 0, -OFFSET_DIST)),
}

#---------- REFERENCE IMAGE CREATION ----------

def create_reference_image_empty(context, filepath, axis='BOTTOM'):
    """Manually build an Empty (type='IMAGE') pointing at filepath, no reliance
    on the internal load_reference_image operator."""

    #Load the image into Blender's data (if not already loaded). 
    #This doesnt cause memory duplication if the image is already loaded, it will just return the existing image datablock.
    img = bpy.data.images.load(filepath, check_existing=True)

    #Create empty and assign data onto it
    name = f"Ref_{axis.title()}"
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'IMAGE'
    empty.data = img 

    #Add the empty (reference image) to the scene collection
    context.scene.collection.objects.link(empty)

    # Setting transforms -> rotation, location, scale etc. based on the axis chosen
    rot, loc = AXIS_CONFIG.get(axis.upper(), ((0, 0, 0), (0, 0, 0)))
    empty.rotation_euler = rot
    empty.location = loc
    empty.empty_display_size = OFFSET_DIST #auto size
    empty.scale = (SCALE_AMOUNT['x'], SCALE_AMOUNT['y'], SCALE_AMOUNT['z'])


    return empty


def add_reference_image_popup(self, context, axis='BOTTOM'):
    bpy.ops.object.reference_image_file_browser('INVOKE_DEFAULT', axis=axis)


class OBJECT_OT_reference_image_file_browser(bpy.types.Operator, ImportHelper):
    """Popup file browser -> load image -> position as reference plane"""
    bl_idname = "object.reference_image_file_browser"
    bl_label = "Select Reference Image"
    bl_options = {'REGISTER', 'UNDO'}

    #allowed image files types
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.exr',
        options={'HIDDEN'},
    )
    axis: StringProperty(default='BOTTOM', options={'HIDDEN'})

    def execute(self, context):
        if not self.filepath or not os.path.exists(self.filepath):
            self.report({'WARNING'}, "No valid image selected")
            return {'CANCELLED'}

        ref_obj = create_reference_image_empty(context, self.filepath, axis=self.axis)

        #Deselect all and select the newly created reference image empty, set it as active
        bpy.ops.object.select_all(action='DESELECT')
        ref_obj.select_set(True)
        context.view_layer.objects.active = ref_obj

        self.report({'INFO'}, f"Loaded reference image for {self.axis}")
        return {'FINISHED'}

#---------- REFERENCE IMAGE CREATION END----------


#---------- ADD SUBMENU ----------
# FRONT
class OBJECT_OT_add_reference_Front(bpy.types.Operator):
    bl_idname = "object.add_reference_front"
    bl_label = "-> Front (add to +Y)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='FRONT')
        return {'FINISHED'}

# BACK
class OBJECT_OT_add_reference_Back(bpy.types.Operator):
    bl_idname = "object.add_reference_back"
    bl_label = "-> Back (add to -Y)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='BACK')
        return {'FINISHED'}

# LEFT
class OBJECT_OT_add_reference_Left(bpy.types.Operator):
    bl_idname = "object.add_reference_left"
    bl_label = "-> Left (add to +X)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='LEFT')
        return {'FINISHED'}

# RIGHT
class OBJECT_OT_add_reference_Right(bpy.types.Operator):
    bl_idname = "object.add_reference_right"
    bl_label = "-> Right (add to -X)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='RIGHT')
        return {'FINISHED'}

# TOP
class OBJECT_OT_add_reference_Top(bpy.types.Operator):
    bl_idname = "object.add_reference_top"
    bl_label = "-> Top (add to -Z)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='TOP')
        return {'FINISHED'}

# BOTTOM
class OBJECT_OT_add_reference_Bottom(bpy.types.Operator):
    bl_idname = "object.add_reference_bottom"
    bl_label = "-> Bottom (add to +Z)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_reference_image_popup(self, context, axis='BOTTOM')
        return {'FINISHED'}
#---------- ADD SUBMENU END ----------


#---------- ADD SUBMENU CLASS ----------
class VIEW3D_MT_custom_image_submenu(bpy.types.Menu):
    bl_label = "Add Reference Image -> Location"
    bl_idname = "VIEW3D_MT_custom_image_submenu"

    def draw(self, context):
        layout = self.layout
        # These must match the bl_idname of each operator exactly
        layout.operator("object.add_reference_front", icon='IMAGE_DATA')
        layout.operator("object.add_reference_back", icon='IMAGE_DATA')
        layout.operator("object.add_reference_left", icon='IMAGE_DATA')
        layout.operator("object.add_reference_right", icon='IMAGE_DATA')
        layout.operator("object.add_reference_top", icon='IMAGE_DATA')
        layout.operator("object.add_reference_bottom", icon='IMAGE_DATA')

#---------- ADD SUBMENU CLASS END ----------

#---------- ADD REFERENCE IMAGE POPUP AND ADD ----------

# Draw function that injects the submenu into Blender's existing menu
def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_custom_image_submenu", icon='FILE_NEW')


# Register and Unregister everything properly
classes = (
    OBJECT_OT_reference_image_file_browser,
    OBJECT_OT_add_reference_Front,
    OBJECT_OT_add_reference_Back,
    OBJECT_OT_add_reference_Left,
    OBJECT_OT_add_reference_Right,
    OBJECT_OT_add_reference_Top,
    OBJECT_OT_add_reference_Bottom,
    VIEW3D_MT_custom_image_submenu,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_image_add.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_image_add.remove(menu_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()