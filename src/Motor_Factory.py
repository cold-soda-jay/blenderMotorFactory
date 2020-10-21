import bpy
from bpy.props import *
from bpy_extras import object_utils
from . import motor as mt



#from math import *


class Motor_Factory_Operator(bpy.types.Operator):
    #Set Genera information
    bl_idname = "mesh.add_motor"
    bl_label = "Motor Property"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "Add new motor"
    MAX_INPUT_NUMBER = 10

    motor : BoolProperty(name = "Motor",
                default = True,
                description = "New motor")

    change : BoolProperty(name = "Change",
                default = False,
                description = "Change motor")
    init_x = 0
    init_y = 0
    init_z = 0

    MotorParameters = [
        "mf_Type",
        "mf_Bottom_Length",
        "mf_Bit_Type",
        "mf_Sub_Bottom_Inner_Dia",
        "mf_Small_Gear_Dia",
        "mf_Small_Gear_Position",
        "mf_Small_Gear_Bolt_Angle",
        "mf_Small_Gear_Bolt_Rotation",
        "mf_Large_Gear_Dia",
        "mf_Large_Gear_Bolt_Angle",
        "mf_Large_Gear_Bolt_Rotation",
        "mf_Gear_Orientation",
        "mf_Color_Render",
        "mf_Flip",
        ]
    #Create genera types

    #Bottom Types
    Extention_Type_List = [('mf_Type_A','Type 1','Type 1'),
                 ('mf_Type_B','Type 2','Type 2')  ]
    mf_Type = EnumProperty( attr='mf_Type',
            name='Extention Area Type',
            description='Choose the type of Bottom you would like',
            items = Extention_Type_List, default = 'mf_Type_A')


    mf_Color_Render : BoolProperty(name = "Color Render",
                default = False,
                description = "Render clor or not")

    mf_Bottom_Size = FloatProperty(attr='mf_Bottom_Size',
            name='Bottom Size', default = 20,
            min = 0, soft_min = 0, max = 50, 
            description='Size of the Bottom in percent')

    #Bit Types
    Bit_Type_List = [('mf_Bit_Torx','Torx','Torx Bit Type'),
                    ('mf_Bit_Slot','Slot','Slot Bit Type'),
                    ('mf_Bit_Cross','Cross','Cross Bit Type')]
    mf_Bit_Type = EnumProperty( attr='mf_Bit_Type',
            name='Bit Type',
            description='Choose the type of bit to you would like',
            items = Bit_Type_List, default = 'mf_Bit_Torx')


    #Head Types 
    Head_Type_List = [('mf_Head_Type_A','Type A','Type A')]
    mf_Head_Type = EnumProperty( attr='mf_Head_Type',
            name='Type',
            description='Choose the type of Motor you would like',
            items = Head_Type_List, default = 'mf_Head_Type_A')

    #Bottom size      
    mf_Bottom_Length = FloatProperty(attr='mf_Bottom_Length',
            name='Bottom Length', default = 6.4,
            min = 0, soft_min = 0, max = MAX_INPUT_NUMBER, 
            description='Length of the Bottom')
            

    mf_Sub_Bottom_Inner_Dia = FloatProperty(attr='mf_Sub_Bottom_Inner_Dia',
        name='Sub Bottom Inner Dia', default = 0.5,
        min = 0, soft_min = 0, max = 0.9, 
        description='Length of the sub Bottom inner dia')

    mf_Small_Gear_Dia = FloatProperty(attr='mf_Small_Gear_Dia',
        name='Small Gear Dia', default = 4,
        min = 3.5, soft_min = 0, max = 4.5, 
        description='Diameter of small Gear')

    mf_Small_Gear_Position = FloatProperty(attr='mf_Small_Gear_Position',
        name='Small Gear Position', default = 3.6,
        min = 3.6, soft_min = 0, max = 4.2, 
        description='Position of small Gear in middel axe')

    mf_Small_Gear_Bolt_Angle = FloatProperty(attr='mf_Small_Gear_Bolt_Angle',
        name='Angle between bolts on small gear', default = 12,
        min = 6, soft_min = 0, max = 18, 
        description='Angle between bolts on small gear')

    mf_Small_Gear_Bolt_Rotation = FloatProperty(attr='mf_Small_Gear_Bolt_Rotation',
        name='Position of bolts on small gear', default = 20,
        min = 0, soft_min = 0, max = 36, 
        description='Position of bolts on small gear')

    mf_Large_Gear_Dia = FloatProperty(attr='mf_Large_Gear_Dia',
        name='Large Gear Dia', default = 5.5,
        min = 5, soft_min = 0, max = 6.5, 
        description='Diameter of large Gear')

    mf_Large_Gear_Bolt_Angle = FloatProperty(attr='mf_Large_Gear_Bolt_Angle',
        name='Angle between bolts on large gear', default = 17,
        min = 6, soft_min = 0, max = 18, 
        description='Angle between bolts on large gear')

    mf_Large_Gear_Bolt_Rotation = FloatProperty(attr='mf_Large_Gear_Bolt_Rotation',
        name='Position of bolts on large gear', default = 1.3,
        min = 0, soft_min = 0, max = 36, 
        description='Position of bolts on large gear')

    Orientation_List = [
                ('mf_East','0','0'),
                ('mf_South','90','90'),             
                ('mf_West','180','180'),
                ('mf_North','270','270')
 ]

    mf_Gear_Orientation = EnumProperty( attr='mf_Gear_Orientation',
            name='Gear Ortientation',
            description='Orientation of gears and extension zone',
            items = Orientation_List, default = 'mf_East')

    mf_Flip : BoolProperty(name = "Flip",
                default = False,
                description = "Flip the gears")

    bolt_orientation_list = [('mf_all_same', 'All Same','All Same'),
                            ('mf_all_random', 'All Random', 'All Random')]
    mf_Bolt_Orientation = EnumProperty( attr='mf_Gear_Orientation',
            name='Bolt Ortientation',
            description='Orientation of bolts',
            items = bolt_orientation_list, default = 'mf_all_same')

            
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        #ENUMS
        col.prop(self, 'mf_Head_Type')
        col.prop(self, 'mf_Type')
        col.prop(self, 'mf_Bit_Type')
        col.prop(self, 'mf_Color_Render')
        col.prop(self, 'mf_Gear_Orientation')        
        col.prop(self, 'mf_Flip')
        col.prop(self, 'mf_Bolt_Orientation')       
        col.prop(self, 'mf_Bottom_Length') 
        col.prop(self, 'mf_Sub_Bottom_Inner_Dia')
        col.prop(self, 'mf_Small_Gear_Dia') 
        col.prop(self, 'mf_Small_Gear_Position')         
        col.prop(self, 'mf_Small_Gear_Bolt_Angle')     
        col.prop(self, 'mf_Small_Gear_Bolt_Rotation')
        col.prop(self, 'mf_Large_Gear_Dia')     
        col.prop(self, 'mf_Large_Gear_Bolt_Angle') 
        col.prop(self, 'mf_Large_Gear_Bolt_Rotation')
     
           
        #col.prop(self, 'bf_presets')
        col.separator()


    def execute(self, context):
        if  context.active_object and \
            ('Motor' in context.active_object.name_full) and (self.change == True):
            obj = context.active_object
            oldmesh = obj.data
            oldmeshname = obj.data.name
            obj = self.create_motor()
            #obj.data = mesh
            try:
                bpy.ops.object.vertex_group_remove(all=True)
            except:
                pass

            for material in oldmesh.materials:
                obj.data.materials.append(material)

            bpy.data.meshes.remove(oldmesh)
            obj.data.name = oldmeshname
        else:
            obj = self.create_motor()

        obj.data["Motor"] = True
        obj.data["change"] = False
        for prm in self.MotorParameters:
            obj.data[prm] = getattr(self, prm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}


    def create_motor(self):

        creator = mt.Motor_Creator(self)
        bottom = creator.create_Bottom()
        middle = creator.create_middle()
        #if self.mf_Type == 'mf_Type_A':
        convex = creator.create_4_convex_cyl()
        up = creator.create_upper_part()
            #up1 =ut.create_up1(self)
            #up2 = ut.create_up2(self)
        obj_list=[convex,middle,up]
        for area in bpy.context.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D':
                        if self.mf_Color_Render:
                            space.shading.type = 'MATERIAL'
                        else:
                            space.shading.type = 'SOLID' # set the viewport shading to rendered
    
        motor = creator.combine_all_obj(bottom,obj_list)     
            
        return motor

    

   

    



