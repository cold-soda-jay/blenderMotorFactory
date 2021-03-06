import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from . import motor as mt
from bpy_extras.object_utils import AddObjectHelper




#from math import *


class Motor_Factory_Operator(bpy.types.Operator,AddObjectHelper):
    
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
    id_Nr = 0

    MotorParameters = [
        "mf_Top_Type",
        "mf_Extension_Type_A",
        "mf_Extension_Type_B",
        "mf_Gear_Orientation_1",
        "mf_Gear_Orientation_2",
        "mf_Flip",
        "mf_Color_Render",
        "mf_Bottom_Length",
        "mf_Sub_Bottom_Length",
        "mf_Lower_Gear_Dia",
        "mf_Lower_Gear_Position",
        "mf_Upper_Gear_Dia",

        
        "mf_Bit_Type",
        "mf_Bolt_Orientation",
        "mf_Lower_Gear_Bolt_Random",
        "mf_Lower_Gear_Bolt_Position_1",
        "mf_Lower_Gear_Bolt_Position_2", 
        
        "mf_Upper_Bolt_Nummber",
        "mf_Upper_Gear_Bolt_Random",
        "mf_Upper_Gear_Bolt_Position_1_1",
        "mf_Upper_Gear_Bolt_Position_1_2",
        "mf_Upper_Gear_Bolt_Position_1_3",
        #"mf_Upper_Gear_Bolt_Position_1",
        "mf_Upper_Gear_Bolt_Position_2_1",
        "mf_Upper_Gear_Bolt_Position_2_2",
        "mf_Upper_Gear_Bolt_Position_3",
              
        "mf_Type_B_Height_1",
        "mf_Type_B_Height_2", 
        "mf_Gear_Bolt_Random_B",
        "mf_Gear_Bolt_Nummber_B",
        "mf_Gear_Bolt_Position_B_1",
        "mf_Gear_Bolt_Position_B_2",
        "mf_Gear_Bolt_Position_B_3",
        "mf_Gear_Bolt_Right_B",
        "temp_save",
        "save_path",

        ]
    
    CsvParameters = [
        "mf_Top_Type",
        "mf_Extension_Type_A",
        "mf_Extension_Type_B",
        "mf_Gear_Orientation_1",
        "mf_Gear_Orientation_2",
        "mf_Flip",
        "mf_Color_Render",
        "mf_Bottom_Length",
        "mf_Sub_Bottom_Length",
        "mf_Lower_Gear_Dia",
        "mf_Lower_Gear_Position",
        "mf_Upper_Gear_Dia",
        "mf_Bit_Type",
        "mf_Bolt_Orientation",
        "mf_Lower_Gear_Bolt_Random",
        "mf_Lower_Gear_Bolt_Position_1",
        "mf_Lower_Gear_Bolt_Position_2", 
        "mf_Upper_Bolt_Nummber",
        "mf_Upper_Gear_Bolt_Random",
        "mf_Upper_Gear_Bolt_Position_1",
        "mf_Upper_Gear_Bolt_Position_2",
        "mf_Upper_Gear_Bolt_Position_3",
        "mf_Type_B_Height_1",
        "mf_Type_B_Height_2", 
        "mf_Gear_Bolt_Random_B",
        "mf_Gear_Bolt_Nummber_B",
        "mf_Gear_Bolt_Position_B_1",
        "mf_Gear_Bolt_Position_B_2",
        "mf_Gear_Bolt_Position_B_3",
        "mf_Gear_Bolt_Right_B",
        ]
    #Create genera types and Variables

    ################### General ##################################
    #Head Types 
    Head_Type_List = [('mf_Top_Type_A','Type A (Two gears)','Type A'),
                        ('mf_Top_Type_B','Type B (One gears)','Type B')]
    mf_Top_Type = EnumProperty( attr='mf_Top_Type',
            name='Type',
            description='Choose the type of Motor you would like',
            items = Head_Type_List, default = 'mf_Top_Type_A')
    
    #Extension zone Types
    
    Extention_Type_List_A = [('mf_Extension_Type_1','Type 1','Type 1'),
                 ('mf_Extension_Type_2','Type 2','Type 2'),                 
                 ('mf_None','None','None') 
                 ]
    mf_Extension_Type_A = EnumProperty( attr='mf_Extension_Type',
            name='Extension Area Type',
            description='Choose the type of extension area you would like',
            items = Extention_Type_List_A, default = 'mf_Extension_Type_1')
    
    Extention_Type_List_B = [('mf_Extension_Type_1','Type 1','Type 1'),                                 
                 ('mf_None','None','None') 
                 ]
    mf_Extension_Type_B = EnumProperty( attr='mf_Extension_Type',
            name='Extension Area Type',
            description='Choose the type of extension area you would like',
            items = Extention_Type_List_B, default = 'mf_Extension_Type_1')


   
    # Gear Orientation
    Orientation_List_Type_2 = [
                ('r90','90','90'),             
                ('r180','180','180'),
                ('r270','270','270')
        ]

    Orientation_List_Type_1 = [
                ('r0','0','0'),
                ('r90','90','90'),             
                ('r180','180','180'),
                ('r270','270','270')
        ]

    mf_Gear_Orientation_1 = EnumProperty( attr='mf_Gear_Orientation',
            name='Gear Rotation',
            description='Rotation of gears and extension zone',
            items = Orientation_List_Type_1, default = 'r0')   

    mf_Gear_Orientation_2 = EnumProperty( attr='mf_Gear_Orientation',
            name='Gear Rotation',
            description='Rotation of gears and extension zone',
            items = Orientation_List_Type_2, default = 'r270')

    mf_Flip : BoolProperty(name = "Flip",
                default = False,
                description = "Flip the gears")

    # Set color rendering option
    mf_Color_Render : BoolProperty(name = "Color Render",
                default = False,
                description = "Render clor or not")

    ################## Bottom ########################################
    #Bottom Length      
    mf_Bottom_Length = FloatProperty(attr='mf_Bottom_Length',
            name='Bottom Length', default = 6.4,
            min = 4, soft_min = 0, max = 8, 
            description='Length of the Bottom')

    #Sub Bottom length      
    mf_Sub_Bottom_Length = FloatProperty(attr='mf_Sub_Bottom_Length',
            name='Sub Bottom Length', default = 1.2,
            min =0.6, soft_min = 0.1, max = 2, 
            description='Length of the Sub Bottom')
                    
    

    ###################### Lower Gears for type A and B ########################################
    mf_Lower_Gear_Dia = FloatProperty(attr='mf_Lower_Gear_Dia',
        name='Lower Gear Dia', default = 4,
        min = 3.5, soft_min = 0, max = 4.5, 
        description='Diameter of lower Gear')

    mf_Lower_Gear_Position = FloatProperty(attr='mf_Lower_Gear_Position',
        name='Lower Gear Position', default = 3.6,
        min = 3.6, soft_min = 0, max = 4.2, 
        description='Position of lower Gear in middel axe respect to the top of bottom part(mf_Sub_Bottom_Length + mf_Bottom_Length)')


    mf_Lower_Gear_Bolt_Random : BoolProperty(name = "Random Bolt Position of lower gear", 
                default = False,
                description = "Random Bolt Rotation")

    mf_Lower_Gear_Bolt_Position_1 = IntProperty(attr='mf_Lower_Gear_Bolt_Position',
        name='Position of bolt 1 on lower gear', default = 200,
        min = 190, max = 230, step=5,
        description='Position of bolts on lower gear')

    mf_Lower_Gear_Bolt_Position_2 = IntProperty(attr='mf_Lower_Gear_Bolt_Position',
        name='Position of bolts on lower gear', default = 320,
        min = 320, max = 350,  step=5,
        description='Position of bolt 2 on lower gear')
    
    #################################### Gear option for Type B ###########################################
    mf_Gear_Bolt_Random_B : BoolProperty(name = "Random Bolt Position ", 
                default = False,
                description = "Random Bolt Rotation")


    upper_Gear_Bolt_Random = [('2','2','2'),
                    ('3','3','3')]
    mf_Gear_Bolt_Nummber_B = EnumProperty( attr='mf_Gear_Bolt_Nummber_B',
            name='Number of Bolts',
            description='Number of Bolts around Gear',
            items = upper_Gear_Bolt_Random, default = '2')

    mf_Gear_Bolt_Position_B_1 = IntProperty(attr='mf_Gear_Bolt_Position_B_1',
        name='Position of bolts on gear', default = 215,
        min = 210, max = 225, step=1,
        description='Position of bolt 1 on gear')

    mf_Gear_Bolt_Position_B_2 = IntProperty(attr='mf_Gear_Bolt_Position_B_2',
        name='Position of bolts on gear', default = 90,
        min = 70, max =110,  
        description='Position of bolt 2 on gear')
    
    mf_Gear_Bolt_Position_B_3 = IntProperty(attr='mf_Gear_Bolt_Position_B_3',
        name='Position of bolts on gear', default = 180,
        min = 130, max = 190,  step=1,
        description='Position of bolt 2 on gear')
    
    mf_Type_B_Height_1 =   FloatProperty(attr='mf_Type_B_Height_1',
        name='Height of Extension left', default = 7,
        min = 6.3, soft_min = 0, max = 7.5, 
        description='Height of Extension left relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length)') 
    
    
    mf_Type_B_Height_2 =   FloatProperty(attr='mf_Type_B_Height_2',
        name='Height of Extension right', default =3.5,
        min = 3, soft_min = 0, max = 6, 
        description='Height of Extension right relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length)') 
    
    mf_Gear_Bolt_Right_B =   FloatProperty(attr='mf_Gear_Bolt_Right_B',
        name='Position of bolt at right', default =2.5,
        min = 1.7, soft_min = 0, max = 4, 
        description='Position of bolt at right relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length) ')

    ########################## Upper part Type A ###############################

    mf_Upper_Gear_Dia = FloatProperty(attr='mf_Upper_Gear_Dia',
        name='Upper Gear Dia', default = 5.5,
        min = 5, soft_min = 0, max = 6.5, 
        description='Diameter of upper Gear')

    #Bolt on large gear
    
    upper_Gear_Bolt_Random = [('1','1','1'),
                    ('2','2','2'),
                    ('3','3','3')]
    mf_Upper_Bolt_Nummber = EnumProperty( attr='mf_Upper_Bolt_Nummber',
            name='Number of Bolts',
            description='Number of Bolts around upper Gear',
            items = upper_Gear_Bolt_Random, default = '2')


    mf_Upper_Gear_Bolt_Random : BoolProperty(name = "Random Bolt Position of upper gear",
                default = False,
                description = "Random Bolt Rotation")


    #TODO: Change range
    
    #mf_Upper_Gear_Bolt_Position_1 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
    # #   name='Position of bolts on large gear', default = 13,
    #    min = 0, max = uppp, step=1,
     #   description='Position of bolts on large gear')
    
    mf_Upper_Gear_Bolt_Position_1_1 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 210, step=1,
        description='Position of bolts on large gear')
    
    mf_Upper_Gear_Bolt_Position_1_2 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 100, step=1,
        description='Position of bolts on large gear')
    
    mf_Upper_Gear_Bolt_Position_1_3 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 65, step=1,
        description='Position of bolts on large gear')
    

    mf_Upper_Gear_Bolt_Position_2_1 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_2',
        name='Position of bolts on large gear', default = 100,
        min = 110, max = 210, step=1,
        description='Position of bolts on large gear')    
    mf_Upper_Gear_Bolt_Position_2_2 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_2',
        name='Position of bolts on large gear', default = 100,
        min = 75, max = 135, step=1,
        description='Position of bolts on large gear')
    

    mf_Upper_Gear_Bolt_Position_3 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_3',
        name='Position of bolts on large gear', default =200,
        min = 145, max = 210, step=1,
        description='Position of bolts on large gear')


    ###################### Bolts ############################################

    bolt_orientation_list = [('mf_all_same', 'All Same','All Same'),
                            ('mf_all_random', 'All Random', 'All Random')]
    mf_Bolt_Orientation = EnumProperty( attr='mf_Bolt_Orientation',
            name='Bolt Ortientation',
            description='Orientation of bolts',
            items = bolt_orientation_list, default = 'mf_all_same')
    
    
    #Bit Types
    Bit_Type_List = [('mf_Bit_Torx','Torx','Torx Bit Type'),
                    ('mf_Bit_Slot','Slot','Slot Bit Type'),
                    ('mf_Bit_Cross','Cross','Cross Bit Type'),
                    ('mf_Bit_Allen','Allen','Allen Bit Type')]
    mf_Bit_Type = EnumProperty( attr='mf_Bit_Type',
            name='Bit Type',
            description='Choose the type of bit to you would like',
            items = Bit_Type_List, default = 'mf_Bit_Torx')
    
    ##################### Svae path #####################
    temp_save : BoolProperty(name = "Save the module ", 
                default = False,
                description = "Save the module")
    
    save_path = StringProperty(name = "Save Path",
                default = "None", maxlen=4096,
                description = "Save the modell")        
    
    mf_Upper_Gear_Bolt_Position_1 = 0

    mf_Upper_Gear_Bolt_Position_2 = 0

    def draw(self, context):
        """
        Define the contex menu

        """
        layout = self.layout
        col = layout.column()
        
        col.label(text="General")
        col.prop(self, 'mf_Top_Type')
        if self.mf_Top_Type == "mf_Top_Type_A":  
            col.prop(self, 'mf_Extension_Type_A')
            if self.mf_Extension_Type_A == 'mf_Extension_Type_1':
                col.prop(self, 'mf_Gear_Orientation_1')        
            elif self.mf_Extension_Type_A == 'mf_Extension_Type_2':
                col.prop(self, 'mf_Gear_Orientation_2') 
            else:
                col.prop(self, 'mf_Gear_Orientation_1')      
        elif self.mf_Top_Type == "mf_Top_Type_B":
            col.prop(self, 'mf_Extension_Type_B')
            col.prop(self, 'mf_Gear_Orientation_1')
        
      
        col.prop(self, 'mf_Flip')

        col.prop(self, 'mf_Color_Render')

        col.label(text="Bottom")
        col.prop(self, 'mf_Bottom_Length') 
        col.prop(self, 'mf_Sub_Bottom_Length')

        col.label(text="Gears")
        col.prop(self, 'mf_Lower_Gear_Dia') 
        col.prop(self, 'mf_Lower_Gear_Position')
        if self.mf_Top_Type == "mf_Top_Type_A":  
            col.prop(self, 'mf_Upper_Gear_Dia')    
        elif  self.mf_Top_Type == "mf_Top_Type_B":  
            col.prop(self, 'mf_Type_B_Height_1')
            col.prop(self, 'mf_Type_B_Height_2')

        col.label(text="Bolts Type")
        col.prop(self, 'mf_Bit_Type')
        col.prop(self, 'mf_Bolt_Orientation')      

        if self.mf_Top_Type == "mf_Top_Type_A":    

            col.label(text="Bolts Position around lower gear")

            col.prop(self, 'mf_Lower_Gear_Bolt_Random')    
            if not self.mf_Lower_Gear_Bolt_Random: 
                col.prop(self, 'mf_Lower_Gear_Bolt_Position_1')
                col.prop(self, 'mf_Lower_Gear_Bolt_Position_2')
            col.label(text="Bolts Position around upper gear")

            col.prop(self, 'mf_Upper_Bolt_Nummber')
            col.prop(self, 'mf_Upper_Gear_Bolt_Random')
            if not self.mf_Upper_Gear_Bolt_Random:
                if self.mf_Upper_Bolt_Nummber == '1':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_1') 
                elif self.mf_Upper_Bolt_Nummber == '2':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_2') 
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_2_1') 

                elif self.mf_Upper_Bolt_Nummber == '3':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_3') 
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_2_2')
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_3')

        elif self.mf_Top_Type == "mf_Top_Type_B":
            col.label(text="Bolts Position around gear B")
            col.prop(self, 'mf_Gear_Bolt_Right_B')

            if self.mf_Extension_Type_B == "mf_None":
                col.prop(self, 'mf_Gear_Bolt_Nummber_B')                        
            col.prop(self, 'mf_Gear_Bolt_Random_B')
            if not self.mf_Gear_Bolt_Random_B:
                col.prop(self, 'mf_Gear_Bolt_Position_B_1')
                col.prop(self, 'mf_Gear_Bolt_Position_B_2')
                if self.mf_Extension_Type_B == "mf_None" and self.mf_Gear_Bolt_Nummber_B == '3':
                    col.prop(self, 'mf_Gear_Bolt_Position_B_3')
        col.prop(self, 'temp_save')
        if self.temp_save:
            col.prop(self, 'save_path')
        col.separator()


    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        if  context.selected_objects != [] and context.active_object and \
            ('Motor' in context.active_object.data.name) :
            obj = context.active_object
            oldmesh = obj.data
            oldmeshname = obj.data.name
            obj = self.create_motor()
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
        """Create motor

        Returns:
            Motor Object
        """

        # Check if the model should be svaed
        if self.save_path == "None":
            pass
        else:  
            self.save_path = self.save_path.replace("\\","/")
            if not self.save_path.endswith('/'):
                self.save_path += '/'  
            # Make dir when not exist   
            try:
                os.mkdir(self.save_path)
            except:
                pass        
                  
            self.id_Nr = len([x for x in os.listdir(self.save_path) if "Motor_" in x])+1
            path_of_folder = self.save_path + "Motor_%04d/"%self.id_Nr
            try:
                os.mkdir(path_of_folder)
            except:
                pass
        # different headtype instance different object
        if self.mf_Top_Type == "mf_Top_Type_A":
            creator = mt.Type_A(self)
            if self.mf_Upper_Bolt_Nummber == '1':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_1
            elif self.mf_Upper_Bolt_Nummber == '2':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_2
                self.mf_Upper_Gear_Bolt_Position_2 = self.mf_Upper_Gear_Bolt_Position_2_1
            elif self.mf_Upper_Bolt_Nummber == '3':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_3
                self.mf_Upper_Gear_Bolt_Position_2 = self.mf_Upper_Gear_Bolt_Position_2_2

               

        elif self.mf_Top_Type == "mf_Top_Type_B":
            creator = mt.Type_B(self) 
        
        #Create bottom part
        bottom = creator.create_Bottom()
        #Create energy part (Electric socket)
        en_part = creator.create_en_part()
        #Create Upper part
        upper_part = creator.create_upper_part()
        obj_list=[upper_part,en_part]
        
        # Combine all created parts
        motor = creator.combine_all_obj(bottom,obj_list)     
        motor.name = "Motor"
        motor.data.name = "Motor"
        
        # Check if color should be rendered
        for area in bpy.context.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':               
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D':
                        if self.mf_Color_Render:
                            space.shading.type = 'MATERIAL'
                        elif space.shading.type == 'MATERIAL' and len(bpy.data.materials) >0:
                            for material in bpy.data.materials:
                                material.user_clear()
                                bpy.data.materials.remove(material) #delete it
                            space.shading.type = 'SOLID' # set the viewport shading to rendered
                        else:
                            space.shading.type = 'SOLID' # set the viewport shading to rendered
        motor["category_id"] = 9
        creator.save_modell(motor)
        creator.write_back(self)
        creator.save_csv(self)  
        if self.temp_save and self.save_path != "None":
           bpy.context.window_manager.popup_menu(self.success_save, title="Info", icon='PLUGIN')    

           self.temp_save = False   
           self.save_path = "None"  
        creator.clear_bolt()
        self.test(creator)    
        return motor

    def success_save(self,okay,context):
        text = "Module saved under " + str(self.save_path)+ "Motor_%04d/"%self.id_Nr#"Motor_"+str(self.id_Nr)+'/'
        okay.layout.label(text=text)
    
    def test(self,creator):
        #creator.create_internal_gear((0,0,20), 0.5, 2)
        pass


   

    



