# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "MotorFactory",
    "author" : "Cold-Soda-Joe",
    "description" : "Motor Factory",
    "blender" : (2, 90, 1),
    "version" : (1, 1, 0),
    "location" : "View3D > Add > Mesh",
    "warning" : "",
    "category" : "Add Mesh"
}

import bpy

from .Motor_Factory import Motor_Factory_Operator


def add_mesh_motor_button(self, context):
    self.layout.operator(Motor_Factory_Operator.bl_idname, text="Motor", icon="PLUGIN")


def Motor_contex_menu(self, context):
    bl_label = 'Change'

    obj = context.object
    layout = self.layout
    if 'Motor' in obj.name_full:
        props = layout.operator(Motor_Factory_Operator.bl_idname, text="Change Motor")
        props.change = True
        for prm in Motor_Factory_Operator.MotorParameters:
            setattr(props, prm, obj.data[prm])
        layout.separator()

def register():
    bpy.utils.register_class(Motor_Factory_Operator)

    bpy.types.VIEW3D_MT_mesh_add.append(add_mesh_motor_button)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(Motor_contex_menu)


def unregister():
    
    bpy.types.VIEW3D_MT_object_context_menu.remove(Motor_contex_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_mesh_motor_button)
    bpy.utils.unregister_class(Motor_Factory_Operator)

