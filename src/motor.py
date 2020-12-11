import bpy
import os
import math
import mathutils
import random
from .utility import Factory
from math import radians
import bmesh
import random
import csv


class Motor_Creator(Factory):

    def __init__(self,factory):
            self.head_Type = factory.mf_Head_Type
            self.init_x = factory.init_x
            self.init_y = factory.init_y
            self.init_z = factory.init_z
            self.bottom_length = factory.mf_Bottom_Length
            self.inner_radius = 0.5
            self.sub_bottom_length = factory.mf_Sub_Bottom_Length
            self.bolt_ortientation = factory.mf_Bolt_Orientation

            self.bit_type = factory.mf_Bit_Type
            self.ex_type = factory.mf_Extension_Type
            
            if self.ex_type == 'mf_Extension_Type_1':
                self.gear_orientation = factory.mf_Gear_Orientation_1
                #self.gear_Flip = factory.mf_Flip_1


            elif self.ex_type == 'mf_Extension_Type_2':
                self.gear_orientation = factory.mf_Gear_Orientation_2
                #self.gear_Flip = factory.mf_Flip_2
            else:
                self.gear_orientation = factory.mf_Gear_Orientation_1


            self.gear_Flip = factory.mf_Flip_1

            self.lower_gear_dia = factory.mf_Lower_Gear_Dia
            self.small_gear_position = factory.mf_Small_Gear_Position
            self.large_gear_dia = factory.mf_Large_Gear_Dia
            self.color_render = factory.mf_Color_Render

            self.small_gear_bolt_random = factory.mf_Small_Gear_Bolt_Random

            self.samll_gear_bolt_rotation_1 = factory.mf_Small_Gear_Bolt_Rotation_1
            self.samll_gear_bolt_rotation_2 = factory.mf_Small_Gear_Bolt_Rotation_2

            self.l_bolt_num = factory.mf_Bolt_Nummber
            
            self.large_Gear_Bolt_Random = factory.mf_Large_Gear_Bolt_Random
            #large_gear_Angle = 0
            self.large_Gear_Bolt_Rotation_1 = factory.mf_Large_Gear_Bolt_Rotation_1
            self.large_Gear_Bolt_Rotation_2 = factory.mf_Large_Gear_Bolt_Rotation_2
            self.large_Gear_Bolt_Rotation_3 = factory.mf_Large_Gear_Bolt_Rotation_3
            if  self.l_bolt_num == 1:
                self.large_Gear_Bolt_Rotation_2 = -999
                self.large_Gear_Bolt_Rotation_3 = -999
            elif self.l_bolt_num == 2:
                self.large_Gear_Bolt_Rotation_3 = -999
            self.l_bolt_lsit = []
            self.s_bolt_lsit = []
            #self.large_gear_Angle = factory.mf_Large_Gear_Bolt_Angle
            #self.large_gear_bolt_position_Angle = factory.mf_Large_Gear_Bolt_Rotation
            self.save_path = factory.mf_Save_Path
            self.id_Nr = factory.id_Nr    
            
    ##############################################################################################################################
    ######################## Bottom Part #########################################################################################
    

    def create_Bottom(self):
        """Create Bottom Part

        Returns:
            
        """
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_radius = self.SUB_BOTTOM_DIA * size
        sub_long = self.sub_bottom_length * size

        inner_radius = self.inner_radius * size
        inner_long = self.SUB_BOTTOM_INNER_DEPTH * size

        # Add parts

        # Add main cylinder
        cylinder_d = main_long
        cylinder_x = init_x
        cylinder_y = init_y
        cylinder_z = init_z + cylinder_d/2 + sub_long    

        cyl = self.create_motor_main((cylinder_x, cylinder_y, cylinder_z),main_hight,main_width,main_long)
        cyl.name = 'Motor'

        # Add sub cylinder
        sub_cylinder_r = sub_radius/2
        sub_cylinder_d = sub_long
        sub_cylinder_x = init_x
        sub_cylinder_y = init_y
        sub_cylinder_z = init_z  + sub_long/2
        bpy.ops.mesh.primitive_cylinder_add(radius=sub_cylinder_r, depth=sub_cylinder_d, location=(sub_cylinder_x, sub_cylinder_y, sub_cylinder_z))
        sub_cyl = bpy.context.object
        sub_cyl.name = 'sub_cylinder'

        # Add inner cylinder
        inner_cylinder_r = inner_radius/2
        inner_cylinder_d = inner_long *2
        inner_cylinder_x = init_x
        inner_cylinder_y = init_y
        inner_cylinder_z = init_z 
        bpy.ops.mesh.primitive_cylinder_add(radius=inner_cylinder_r, depth=inner_cylinder_d, location=(inner_cylinder_x, inner_cylinder_y, inner_cylinder_z))
        inner_cyl = bpy.context.object
        inner_cyl.name = 'inner_cylinder'


        # Boolean Operation for inner cylinder
        bool_3 = sub_cyl.modifiers.new('bool_3', 'BOOLEAN')
        bool_3.operation = 'DIFFERENCE'
        bool_3.object = inner_cyl
        bpy.context.view_layer.objects.active = sub_cyl
        res = bpy.ops.object.modifier_apply(modifier='bool_3')

        # Delete the cylinder.x
        inner_cyl.select_set(True)
        bpy.ops.object.delete()

        #Combine the Objects
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.context.view_layer.objects.active = cyl
        cyl.select_set(True)        
        sub_cyl.select_set(True)
        bpy.ops.object.join()

        if self.color_render:
            self.rend_color(cyl, "Metall")
        cyl.name = "Bottom_part"
        self.save_modell(cyl)
        return cyl


    ##############################################################################################################################
    ######################## Middle Part #########################################################################################

    def create_middle(self):

        # Hight: x achse
        # Width: y achse
        # Length/Long: z achse

        size = 1
        thickness = self.BOARD_THICKNESS
        bolt_orient = self.bolt_ortientation

        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_radius = self.SUB_BOTTOM_DIA * size
        sub_long = self.sub_bottom_length * size

        inner_radius = self.inner_radius * size
        inner_long = self.SUB_BOTTOM_INNER_DEPTH * size

        bit_type = self.bit_type

        init_x = self.init_x 
        init_y = self.init_y
        init_z = self.init_z 

        cuboid_long = thickness *size + self.BOLT_LENGTH
        ub_lx = init_x 
        ub_ly = init_y
        ub_lz = init_z+ sub_long+ main_long - thickness *size/2 + self.BOLT_LENGTH/2

        cube_1 = self.create_motor_main((ub_lx,ub_ly,ub_lz),main_hight,main_width,cuboid_long)

        cube_1.name = 'cube1'


        ##Part 2
        height = self.BOARD_THICKNESS
        width = 0.9 * main_width/2
        p2_length = self.BOLT_LENGTH/2

        x = init_x - main_hight/2 + height
        y = init_y - 0.2
        z = init_z + main_long + sub_long + p2_length

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p2_length))

        cube_2 = bpy.context.object

        ##Part 3
        height = self.BOARD_THICKNESS
        width = 0.9 * main_width/2
        p3_length = self.BOLT_LENGTH/2

        x = init_x + main_hight/2 - height
        y = init_y - 0.2
        z = init_z + main_long + sub_long + p3_length

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p3_length))

        cube_3 = bpy.context.object

        #Create Engergy part
        convex = self.create_4_convex_cyl()

        #Cereate  Bolt 1
        bolt_x = init_x + main_hight/2 - self.BOLT_RAD
        bolt_y = init_y + main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        rota=(radians(180), 'X')
        bolt_1 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota)

        #Cereate  Bolt 2
        bolt_x = init_x - main_hight/2 + self.BOLT_RAD
        bolt_y = init_y - main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        bolt_2 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota)

        mid_1 = self.combine_all_obj(cube_1,[cube_2,cube_3])
        mid_1.name = 'Middle_Part'

        if self.color_render:
            self.rend_color(mid_1, "Plastic")

        mid = self.combine_all_obj(mid_1,[bolt_1[0],bolt_2[0],convex])
        mid.name = 'Middle_Part'

        return mid, [bolt_1[1], bolt_2[1]]

    def create_en_part(self):

        size = 1
        thickness = self.BOARD_THICKNESS

        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size
        sub_long = self.sub_bottom_length * size

        init_x = self.init_x 
        init_y = self.init_y
        init_z = self.init_z 


        height_en = 1.4/2
        length_en = 3/2

        en_z = init_z+ sub_long+ main_long - 0.1
        en_width_1 = thickness * size
        en_long_1 = length_en

        energy_x = init_x + main_hight/4
        en_y_1 = init_y - main_width/2

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_1,en_z))
        bpy.ops.transform.resize(value=(height_en, en_width_1, en_long_1))
        en_1 = bpy.context.object
        en_1.name = 'cube2'

        ##Middle Part
        en_height_2 = height_en/2
        en_width_2 = 2* thickness * size
        en_long_2 = length_en

        en_y_2 = en_y_1 - en_width_1 - en_width_2

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_2,en_z))
        bpy.ops.transform.resize(value=(en_height_2, en_width_2, en_long_2))
        en_2 = bpy.context.object
        en_2.name = 'cube3'

        ##Outer Part
        en_height_3 = height_en
        en_width_3 = thickness/2 * size
        en_long_3 = length_en

        en_y_3 = en_y_2 - en_width_2 - en_width_3

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_3,en_z))
        bpy.ops.transform.resize(value=(en_height_3, en_width_3, en_long_3))
        en_3 = bpy.context.object
        en_3.name = 'cube4'

        ##Up Part
        en_height_4 = height_en
        en_width_4 = 1.5/2
        en_long_4 = 0.5 * thickness * size

        en_y_4 = en_y_1 - en_width_4 + en_width_1
        en_z_4 = en_z + length_en

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_4,en_z_4))
        bpy.ops.transform.resize(value=(en_height_4, en_width_4, en_long_4))
        en_4 = bpy.context.object
        en_4.name = 'cube5'

        en_part_1 = self.combine_all_obj(en_1,[en_2,en_3,en_4])

        if self.color_render:
            self.rend_color(en_part_1, "Energy")

        bpy.context.view_layer.objects.active = None

        ##Diverse Part 1
        en_height_5 = thickness
        en_width_5 = en_width_4/3
        en_long_5 = en_long_3/3

        en_y_5 = en_y_3 - en_width_3 - en_width_5
        en_z_5 = init_z+ sub_long+ main_long + 1.4 - en_long_5 - thickness

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_5,en_z_5))
        bpy.ops.transform.resize(value=(en_height_5, en_width_5, en_long_5))
        en_5 = bpy.context.object
        en_5.name = 'cube6'

        ##Diverse Part 2
        en_height_6 = thickness
        en_width_6 = en_width_4/6
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_6 = bpy.context.object
        en_6.name = 'cube7'


        ##Diverse Part 3
        en_height_6 = thickness
        en_width_6 = en_width_4/4
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6 + 0.5

        bpy.ops.mesh.primitive_cube_add(location=(energy_x-0.5,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_7 = bpy.context.object


        ##Diverse Part 4
        en_height_6 = thickness
        en_width_6 = en_width_4/4
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6 + 0.5

        bpy.ops.mesh.primitive_cube_add(location=(energy_x+0.5,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_8 = bpy.context.object
        en_part_2 = self.combine_all_obj(en_5,[en_6, en_7,en_8])
        if self.color_render:
            self.rend_color(en_part_2, "Bit")
        bpy.context.view_layer.objects.active = None
        en_part = self.combine_all_obj(en_part_1,[en_part_2])

        en_part.name = "Charger"
        self.save_modell(en_part)

        return en_part

    ##############################################################################################################################
    ######################## 4 Convex Cylinder Part ##############################################################################

    def create_4_convex_cyl(self):
        #Four convex cylinder and side board

        init_x = self.init_x
        init_y = self.init_y 
        init_z = self.init_z

        size = 1
        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size


        #four_cyl_dia = 1.4/2
        step = 0.1

        four_cyl_z = main_long + sub_long
        if self.head_Type == "mf_Head_Type_A":
            length_1 = self.C1_LENGTH_A
            length_2 = self.C1_LENGTH_A + self.C2_LENGTH_A
            length_3 = self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A
            length_4 = self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A + self.C4_LENGTH_A
            length_5 = 0.1
        elif self.head_Type == "mf_Head_Type_B":
            length_1 = self.C1_LENGTH_B
            length_2 = self.C1_LENGTH_B + self.C2_LENGTH_B
            length_3 = self.C1_LENGTH_B + self.C2_LENGTH_B + self.C3_LENGTH_B
            length_4 = self.C1_LENGTH_B + self.C2_LENGTH_B + self.C3_LENGTH_B + self.C4_LENGTH_B
            length_5 = self.C1_LENGTH_B + self.C2_LENGTH_B + self.C3_LENGTH_B + self.C4_LENGTH_B + self.C5_LENGTH_B

        cy1_z = length_1/2
        cy2_z = length_2/2
        cy3_z = length_3/2
        cy4_z = length_4/2
        cy5_z = length_5/2
        #Create 4 Covex cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA, depth=length_1, location=(0,0,four_cyl_z+cy1_z))
        cyl_1 = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step, depth=length_2, location=(0,0,four_cyl_z+cy2_z))
        cyl_2 = bpy.context.object

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA- step *2, depth= length_3, location=(0,0,four_cyl_z+cy3_z))
        cyl_3 = bpy.context.object

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *3, depth=length_4, location=(0,0,four_cyl_z+cy4_z))
        cyl_4 = bpy.context.object

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *4, depth=length_5, location=(0,0,four_cyl_z+cy5_z))
        cyl_5 = bpy.context.object


        up = self.combine_all_obj(cyl_1,[cyl_2,cyl_3,cyl_4,cyl_5])

        if self.color_render:
            self.rend_color(up, "Plastic")

        return up


    ##############################################################################################################################
    ######################## Upper Part Type A ###################################################################################

    def create_up(self, length_relativ, extension=False):
        
        init_x = self.init_x
        init_y = self.init_y
        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]


        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        lower_gear_dia = self.lower_gear_dia
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia
        if extension:
            x = init_x + lower_gear_dia/2
            y = init_y - main_width/4 - length_relativ/3 - 0.15
            z = main_long + sub_long + small_gear_position

            x_large = init_x + lower_gear_dia/2 - 0.8
            y_large = init_y - main_width/4 - length_relativ/6 - length_relativ/6 - 0.15
            z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2
        else:
            x = init_x + lower_gear_dia/2
            y = init_y - main_width/4
            z = main_long + sub_long + small_gear_position

            x_large = init_x + lower_gear_dia/2 - 0.8
            y_large = init_y - main_width/4 - length_relativ/6
            z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2

        #Create small gear
        rotation_s = (radians(-90),"X")
        extension_zone = None
        bottom_board =None
        if extension:
            extension_zone, bottom_board = self.create_extension_zone((x_large,y_large,z_large),0.3)
            s_gear = self.create_gear((x,y,z),self.lower_gear_dia/2,"stick",length_relativ,extension_zone=bottom_board)
            y_bolt_init = y

        else:
            s_gear = self.create_gear((x,y,z),self.lower_gear_dia/2,"stick",length_relativ)
            y_bolt_init = y - length_relativ/2 + self.BOLT_LENGTH/2 + self.EXTENSION_THICKNESS + 0.1


        # Create Bolt for small gear

        x_bolt_init = x+ lower_gear_dia/2 + 0.9*self.BOLT_RAD
        z_bolt_init = z 
        # Calculate the rotate (x,z axis)
        bolt_rotation_1 = self.samll_gear_bolt_rotation_1
        bolt_rotation_2 = self.samll_gear_bolt_rotation_2
        if self.small_gear_bolt_random:  
            if extension:
                bolt_rotation_1,bolt_rotation_2 =  self.s_bolt_lsit     
            bolt_rotation_1 = random.uniform(190,230)
            self.samll_gear_bolt_rotation_1 = bolt_rotation_1
            bolt_rotation_2 =  random.uniform(310,350)
            self.samll_gear_bolt_rotation_2 = bolt_rotation_2
            self.s_bolt_lsit = [bolt_rotation_1,bolt_rotation_2]

        x_bolt_1, z_bolt_1 = self.rotate_around_point((x,z),bolt_rotation_1,(x_bolt_init,z_bolt_init))
        x_bolt_2, z_bolt_2 = self.rotate_around_point((x,z),bolt_rotation_2,(x_bolt_init,z_bolt_init))       
        bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init,z_bolt_1), rotation = rotation_s, only_body = extension)
        bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init,z_bolt_2), rotation = rotation_s, only_body = extension) 

        bolt_shell_list = [bolt_1[0], bolt_2[0]]
        bolt_bit_list = [bolt_1[1], bolt_2[1]]

        #Create large Gear
        if extension:
            l_gear = self.create_gear((x_large,y_large,z_large),self.large_gear_dia/2, "hollow",length_relativ,extension_zone=bottom_board)
            y_bolt_init = y_large

        else:
            l_gear = self.create_gear((x_large,y_large,z_large),self.large_gear_dia/2, "hollow",length_relativ)
            y_bolt_init = y_large - length_relativ/3 + self.BOLT_LENGTH/2 + 0.3


        #Create bolts for large gear
        x_bolt_init = x_large+ large_gear_dia/2 + 0.9*self.BOLT_RAD
        z_bolt_init = z_large 

        #Calculate the rotation
        single_bolt_area = 210/self.l_bolt_num
        bolt_position_angle_1 = self.large_Gear_Bolt_Rotation_1
        bolt_position_angle_2 = self.large_Gear_Bolt_Rotation_2+single_bolt_area
        bolt_position_angle_3 = self.large_Gear_Bolt_Rotation_3+single_bolt_area+single_bolt_area

        if self.l_bolt_num == 1:
            if self.large_Gear_Bolt_Random:                    
                if extension:
                    bolt_position_angle_1 = self.l_bolt_lsit[0]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area)
                    self.large_Gear_Bolt_Rotation_1 = bolt_position_angle_1
                    self.l_bolt_lsit=[bolt_position_angle_1]

            x_bolt, z_bolt = self.rotate_around_point((x_large, z_large),bolt_position_angle_1,(x_bolt_init,z_bolt_init))
            bolt = self.create_bolt((x_bolt,y_bolt_init,z_bolt), rotation = rotation_s, only_body=extension)
            bolt_shell_list.append(bolt[0])
            bolt_bit_list.append(bolt[1])
        elif self.l_bolt_num == 2:
            if self.large_Gear_Bolt_Random:
                if extension:
                    bolt_position_angle_1 = self.l_bolt_lsit[0]
                    bolt_position_angle_2 = self.l_bolt_lsit[1]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area) 
                    bolt_position_angle_2 = random.uniform(bolt_position_angle_1 + 0.5*single_bolt_area, 2*single_bolt_area)
                    self.large_Gear_Bolt_Rotation_1 = bolt_position_angle_1
                    self.large_Gear_Bolt_Rotation_2 = bolt_position_angle_2
                    self.l_bolt_lsit=[bolt_position_angle_1, bolt_position_angle_2]

            x_bolt_1, z_bolt_1 = self.rotate_around_point((x_large,z_large),bolt_position_angle_1,(x_bolt_init,z_bolt_init))
            x_bolt_2, z_bolt_2 = self.rotate_around_point((x_large,z_large),bolt_position_angle_2,(x_bolt_init,z_bolt_init))
            bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init,z_bolt_1), rotation = rotation_s, only_body=extension)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init,z_bolt_2), rotation = rotation_s, only_body=extension)

            bolt_shell_list.append(bolt_1[0])
            bolt_bit_list.append(bolt_1[1])

            bolt_shell_list.append(bolt_2[0])
            bolt_bit_list.append(bolt_2[1])           


        elif self.l_bolt_num == 3:
            if self.large_Gear_Bolt_Random:

                if extension:
                    bolt_position_angle_1 = self.l_bolt_lsit[0]
                    bolt_position_angle_2 = self.l_bolt_lsit[1]
                    bolt_position_angle_3 = self.l_bolt_lsit[2]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area) 
                    bolt_position_angle_2 = random.uniform(bolt_position_angle_1 + 0.5*single_bolt_area, 2*single_bolt_area)
                    bolt_position_angle_3 = random.uniform(bolt_position_angle_2 + 0.5*single_bolt_area, 3*single_bolt_area)
                    self.large_Gear_Bolt_Rotation_1 = bolt_position_angle_1
                    self.large_Gear_Bolt_Rotation_2 = bolt_position_angle_2
                    self.large_Gear_Bolt_Rotation_3 = bolt_position_angle_3
                    self.l_bolt_lsit=[bolt_position_angle_1, bolt_position_angle_2, bolt_position_angle_3]
                
            x_bolt_1, z_bolt_1 = self.rotate_around_point((x_large,z_large),bolt_position_angle_1,(x_bolt_init,z_bolt_init))
            x_bolt_2, z_bolt_2 = self.rotate_around_point((x_large,z_large),bolt_position_angle_2,(x_bolt_init,z_bolt_init))
            x_bolt_3, z_bolt_3 = self.rotate_around_point((x_large,z_large),bolt_position_angle_3,(x_bolt_init,z_bolt_init))
            bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init, z_bolt_1), rotation = rotation_s, only_body=extension)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init, z_bolt_2), rotation = rotation_s, only_body=extension)
            bolt_3 = self.create_bolt((x_bolt_3, y_bolt_init, z_bolt_3), rotation = rotation_s, only_body=extension)

            bolt_shell_list.append(bolt_1[0])
            bolt_bit_list.append(bolt_1[1])
            
            bolt_shell_list.append(bolt_2[0])
            bolt_bit_list.append(bolt_2[1]) 

            bolt_shell_list.append(bolt_3[0])
            bolt_bit_list.append(bolt_3[1])


        #extension_zone = create_extension_zone(factory,(x_large,y_large,z_large))

        if extension: 
            up = self.combine_all_obj(s_gear,[l_gear,extension_zone,bottom_board] + bolt_shell_list)

        else:
            gear_board = self.create_gear_board()
            up = self.combine_all_obj(s_gear,[l_gear,gear_board] + bolt_shell_list)
        if self.color_render:
            self.rend_color(up, "Plastic")

        return up, bolt_bit_list

    def create_gear(self,position, radius, gear_type,info,extension_zone = None):
        rotation = (radians(-90),"X")
        length_relativ = info
        if gear_type == 'stick':
            if extension_zone:
                length = 0.5
            else:
                length = length_relativ*2/3
            inner_radius = 1/2
            inner_length = 1.4 * length +1

            #Create out
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=position)
            out_cyl = bpy.context.object
            out_cyl.name = 'out_cylinder'

            #Create inner
            bpy.ops.mesh.primitive_cylinder_add(radius=inner_radius, depth=inner_length, location=position)
            in_cyl = bpy.context.object
            in_cyl.name = 'in_cylinder'
            
            if extension_zone:
                cly_1 = self.create_ring((position[0],position[1],position[2]+0.1),0.4,radius-0.5, 0.7)
                self.diff_obj(out_cyl, cly_1)

                cly_1.select_set(True)
                bpy.ops.object.delete() 
               
            part = self.combine_all_obj(out_cyl,[in_cyl])

            if self.color_render:
                self.rend_color(part, "Plastic")

            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 

            if extension_zone:
                bpy.ops.mesh.primitive_cylinder_add(radius=radius-0.5, depth=length+10, location=position)
                cly_2 = bpy.context.object

                bpy.context.view_layer.objects.active = part
                bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
                self.diff_obj(extension_zone, cly_2)
                cly_2.select_set(True)
                bpy.ops.object.delete()
        
            return part
        elif gear_type == 'hollow':

            if extension_zone:
                length = 0.5
            else:
                length = length_relativ/3
            inner_radius_1 = 1.6/2
            inner_radius_2 = 1.3/2
            inner_radius_3 = 2.9/2
            inner_length = length + 0.3          
            
            #Ring 1
            thickness_1 = radius - inner_radius_1
            cly_1 = self.create_ring(position,length,radius,thickness_1)

            #Ring 2
            x = position[0]
            y = position[1]
            z = position[2] - 0.3
            position_in = (x,y,z)

            thickness_2 = inner_radius_1 - inner_radius_2
            cly_2 = self.create_ring(position,inner_length,inner_radius_1,thickness_2)

            #Ring 3
            x = position[0]
            y = position[1]
            z = position[2] + 0.1
            position_3 = (x,y,z)

            thickness_3 = 0.2
            cly_3 = self.create_ring(position_3,length+0.3,inner_radius_3,thickness_3)


            part = self.combine_all_obj(cly_1,[cly_2,cly_3])
            if self.color_render:
                self.rend_color(part, "Plastic")

            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        
            return part
        
    def create_extension_zone(self, large_gear_position, gear_length):

        lower_gear_dia = self.lower_gear_dia
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia


        s_length_1 = 2.9/2
        s_length_2 = 5.5
        s_length_3 = 1.5
        s_length_4 = 4.5
        s_length_6 = 3

        if self.ex_type == 'mf_Extension_Type_2':
            angle_1 = 15
            angle_2 = 0
            s_length_5 = 3.5
        elif self.ex_type == 'mf_Extension_Type_1':
            angle_1 = 30
            s_length_5 = 5
            angle_2 = 25

        angle_3 = 35

        x = large_gear_position[0]
        y = large_gear_position[1] - gear_length/2 + 0.4
        z = large_gear_position[2]

        x_thickness = math.cos(radians(angle_3)) * self.EXTENSION_THICKNESS

        p1x = x + s_length_1 * math.cos(radians(angle_1))
        p1z = z + s_length_1 * math.sin(radians(angle_1))

        p2x = x - s_length_1 * math.cos(radians(angle_1))
        p2z = z - s_length_1 * math.sin(radians(angle_1))

        p3x = p1x + s_length_2 * math.sin(radians(angle_1))
        p3z = p1z - s_length_2 * math.cos(radians(angle_1))

        p3hx = p3x - s_length_3 * math.sin(radians(angle_2))
        p3hz = p3z - s_length_3 * math.cos(radians(angle_2))

        p4x = p2x + s_length_4 * math.sin(radians(angle_2))
        p4z = p2z - s_length_4 * math.cos(radians(angle_2))

        p5x = p3x - s_length_5 * math.sin(radians(angle_2))
        p5z = p3z - s_length_5 * math.cos(radians(angle_2))

        p6x = p4x
        p6z = p4z - s_length_6

        y_of = 0

        #Create side board 1
        verts_b1 = [
            (p1x, y, p1z),
            (p1x - x_thickness, y, p1z),
            (p1x, y - 0.5 +y_of, p1z),
            (p1x - x_thickness, y - 0.5 +y_of, p1z),
            (p3x, y , p3z),
            (p3x - x_thickness, y, p3z),
            (p3x, y - 1.1 +y_of, p3z),
            (p3x - x_thickness, y - 1.1 +y_of, p3z),
            (p5x, y, p5z),
            (p5x - x_thickness, y, p5z),
            (p5x, y - 1.5 +y_of, p5z),
            (p5x - x_thickness, y - 1.5 +y_of, p5z),
        ]
        faces_b1 = [
            [0, 1, 3, 2],
            [1,5,7,3],
            [5,9,11,7],
            [9,8,10,11],
            [8,10,6,4],
            [4,6,2,0],
            [0,1,5,9,8,4],
            [2,3,7,11,10,6],
        ]

        board_1 = self.add_mesh("board_1", verts_b1, faces_b1)

        #Create side board 2
        verts_b2 = [
            (p2x, y, p2z),
            (p2x + x_thickness, y, p2z),
            (p2x, y - 0.5 +y_of, p2z),
            (p2x + x_thickness, y - 0.5 +y_of, p2z),
            (p4x, y, p4z),
            (p4x + x_thickness, y, p4z),
            (p4x, y - 1.1 +y_of, p4z),
            (p4x + x_thickness, y - 1.1 +y_of, p4z),
            (p6x, y, p6z),
            (p6x + x_thickness, y, p6z),
            (p6x, y - 1.5 +y_of, p6z),
            (p6x + x_thickness, y - 1.5 +y_of, p6z),
        ]
        faces_b2 = [
            [0,1,3,2],
            [1,5,7,3],
            [5,9,11,7],
            [9,8,10,11],
            [8,10,6,4],
            [4,6,2,0],
            [0,1,5,9,8,4],
            [2,3,7,11,10,6],
        ]
        board_2 = self.add_mesh("board_2", verts_b2, faces_b2)

        #Create bottom board
        thickness_bottom = 0.3
        verts_bottom = [
            (p1x- x_thickness , y, p1z-(large_gear_dia/6)* math.sin(radians(angle_1))), #0
            (p1x- x_thickness , y - thickness_bottom, p1z-(large_gear_dia/6* math.sin(radians(angle_1)))), #1
            (p3x- x_thickness, y, p3z), #2
            (p3x- x_thickness, y - thickness_bottom, p3z), #3
            (p5x- x_thickness, y, p5z), #4
            (p5x- x_thickness, y - thickness_bottom, p5z), #5
            (p6x , y, p6z), #6
            (p6x, y - thickness_bottom, p6z), #7
            (p4x , y, p4z), #8
            (p4x, y - thickness_bottom, p4z), #9
            (p2x, y, p2z-large_gear_dia/6), #10
            (p2x , y - thickness_bottom, p2z-large_gear_dia/6), #11
            (p3hx- x_thickness, y, p3hz), #12
            (p3hx- x_thickness, y - 1.1 +y_of, p3hz), #13
            (p4x , y - 1.1 +y_of, p4z), #14
            (p5x- x_thickness, y - 1.5 +y_of, p5z), #15
            (p6x , y - 1.5 +y_of, p6z), #16
        ]

        faces_bottom = [
            [0,1,3,2],
            [2,3,5,4],
            [4,5,7,6],
            [6,7,9,8],
            [8,9,11,10],
            [10,11,1,0],
            [9,2,4,6,8,10],
            [1,3,5,7,9,11],
            [12,13,14,8],
            [13, 15, 16, 14],       

        ]
        bottom_board = self.add_mesh("bottom board", verts_bottom, faces_bottom)

        #Create end cylinder
        if self.ex_type == 'mf_Extension_Type_2':
            dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)/3
            x_cyl_1 = p5x - (p5x - p6x)*5/6
            y_cyl_1 = (y - 0.8)
            z_cyl_1 = p6z - (p6z -p5z)/3 
            end_cly_1 = self.create_ring((x_cyl_1,y_cyl_1 - 0.5,z_cyl_1), 2.6, dia/2, 0.5)
            end_cly_1.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly_1.name = 'End_cylinder'
            
            x_cyl_2 = p5x - (p5x - p6x)/6
            y_cyl_2 = (y - 0.8)
            z_cyl_2 = p6z - (p6z -p5z)*2/3 
            end_cly_2 = self.create_ring((x_cyl_2,y_cyl_2 - 0.5,z_cyl_2), 2.6, dia/2, 0.5)
            end_cly_2.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly_2.name = 'End_cylinder'

            board = self.combine_all_obj(board_1,[board_2,end_cly_1,end_cly_2])

            bevel = board.modifiers.new(name='bevel', type='BEVEL')
            
            bevel.affect = 'EDGES'
            bevel.angle_limit = 100
            bevel.offset_type = 'WIDTH'
            bevel.width = 1000000
            bpy.context.view_layer.objects.active = board
            res = bpy.ops.object.modifier_apply(modifier='bevel')

        elif self.ex_type == 'mf_Extension_Type_1':

            dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)
            x_cyl = p5x - (p5x - p6x)/2 
            y_cyl = (y - 0.8)
            z_cyl = p6z - (p6z -p5z)/2 
            end_cly = self.create_ring((x_cyl,y_cyl,z_cyl), 1.6, dia/2, 0.5)
            end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly.name = 'End_cylinder'
            board = self.combine_all_obj(board_1,[board_1, board_2,end_cly])

        if self.ex_type == 'mf_Extension_Type_2':
            bpy.ops.transform.mirror(orient_type='LOCAL',constraint_axis=(True, False, False))
            bpy.ops.transform.translate(value=(2.9/2*1.6,0,0))
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.context.view_layer.objects.active = bottom_board
            bottom_board.select_set(True)
            bpy.ops.transform.mirror(orient_type='LOCAL',constraint_axis=(True, False, False))
            bpy.ops.transform.translate(value=(2.9/2*1.6,0,0))


        if self.color_render:
            self.rend_color(board, "Plastic")

        return board, bottom_board

    def create_outer_board(self):
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        height = self.BOARD_THICKNESS
        p1_length = 2.4/2
        ##Part 1
        if self.gear_orientation in ['mf_HundredEighteen', 'mf_zero'] :
            width = 0.9 * self.BOTTOM_DIA/2
        elif self.gear_orientation in ['mf_TwoHundredSeven', 'mf_Ninety'] :
            width = 0.9 * self.BOTTOM_HEIGHT/2
        

        x1 = init_x - self.BOTTOM_HEIGHT/2 + self.BOARD_THICKNESS
        y1 = init_y - 2 * self.BOARD_THICKNESS
        z1 = init_z + main_long + sub_long + self.BOLT_LENGTH + p1_length - self.BOLT_LENGTH/2
        bpy.ops.mesh.primitive_cube_add(location=(x1,y1,z1))
        bpy.ops.transform.resize(value=(height, width, p1_length - self.BOLT_LENGTH/2 ))

        board_1 = bpy.context.object

        z2 = init_z + main_long + sub_long + p1_length*2 + (
                        self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A - p1_length*2 )/2

        x2 = init_x - self.BOTTOM_HEIGHT/4 + self.BOARD_THICKNESS
        p2_length = math.sqrt((self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A-p1_length*2)**2 
                                + (main_height/2)**2 )/2
        Angle = math.atan((main_height/2)/(self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A -
                                    p1_length*2))
        bpy.ops.mesh.primitive_cube_add(location=(x2,y1,z2))
        bpy.ops.transform.resize(value=(height, width, p2_length))
        board_2 = bpy.context.object
        bpy.context.view_layer.objects.active = board_2
        bpy.ops.transform.rotate(value=-Angle,orient_axis='Y') 

        board_out = self.combine_all_obj(board_1,[board_2])

        x,y,z = board_out.location

        board_in = self.create_middle_board_mesh()
        outer_board = self.combine_all_obj(board_out,[board_in])

        

        return outer_board

    def create_gear_board(self):

        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        height = self.BOARD_THICKNESS

        length = self.small_gear_position /2

        x = main_height/4
        y = -0.2
        z = init_z + main_long + sub_long + self.BOLT_LENGTH
        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(main_height*0.15, self.BOARD_THICKNESS/2, length))

        if self.gear_orientation in ['mf_TwoHundredSeven111', 'mf_Ninety111'] :
            x = 0
            y = - main_width/2
            z = init_z + main_long + sub_long + self.BOLT_LENGTH
            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(self.BOARD_THICKNESS/2, main_width*0.09, length))

        board_5 = bpy.context.object

        #Create board
        x = self.lower_gear_dia/2
        y = - main_width/4 +0.25
        z = main_long + sub_long + self.small_gear_position

        width = 2.25
        height = self.BOARD_THICKNESS
        length = math.sqrt((x-self.FOUR_CYL_DIA)**2 +  self.small_gear_position**2)

        x_board = self.FOUR_CYL_DIA + (x - self.FOUR_CYL_DIA)/2
        y_board = y + 0.5
        z_board = main_long + sub_long + ( self.small_gear_position)/2


        Angle = math.atan((x-self.FOUR_CYL_DIA)/ self.small_gear_position)

    
        bpy.ops.mesh.primitive_cube_add(location=(x_board,y_board,z_board))
        bpy.ops.transform.resize(value=(height/2, width/2, length/2))
        board_3 = bpy.context.object

        bpy.context.view_layer.objects.active = board_3        

        bpy.ops.transform.rotate(value=-Angle,orient_axis='Y') 

        board_gear= self.combine_all_obj(board_5,[board_3])

        return board_gear

    def create_middle_board_mesh(self):
        main_long = self.bottom_length 

        sub_long = self.sub_bottom_length
        l1 = 2.4
        l2 = self.C1_LENGTH_A + self.C2_LENGTH_A + self.C3_LENGTH_A

        east = self.BOTTOM_HEIGHT/2 - 0.1
        north = self.BOTTOM_HEIGHT/2 - 0.1

        thickness = self.BOARD_THICKNESS/2

        z_offset = main_long + sub_long

        #if self.gear_orientation in ['mf_zero','mf_HundredEighteen'] :
        p1 = [0, thickness, z_offset]
        p2 = [0, thickness, z_offset+l2]
        p3 = [-east, thickness ,z_offset+l1]
        p4 = [-east, thickness, z_offset]
        p_thick = [0, -2* thickness, 0]

        verts = []
        
        for n in [p1,p2,p3,p4]:
            verts.append(n)
            verts.append(self.add_vector(n,p_thick))

        faces = [
            [0, 1, 3, 2],
            [2, 3 ,5, 4],
            [4, 5, 7, 6],
            [6, 7, 1, 0],
            [0, 2, 4, 6],
            [1, 3, 5, 7]
        ]

        board = self.add_mesh("board", verts, faces)
        return board

    def create_upper_part_Type_A(self):
        rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]
        #self.rotate_object(up1)
        if self.ex_type == "mf_None":
            extension_zone = None
            bolt_list_2 = []
            ex_list=[]
        else:
            extension_zone, bolt_list_2 = self.create_up(length_relativ, extension=True)
            extension_zone.name = "Up2"
            self.save_modell(extension_zone)
            for bolt in bolt_list_2:
                self.save_modell(bolt)
            extension_zone_1 = self.combine_all_obj(extension_zone,bolt_list_2)
            self.rotate_object(extension_zone_1)      
            ex_list=[extension_zone_1]
 

        up1, bolt_list_1 = self.create_up(length_relativ)
        board = self.create_outer_board()  
        middle, bolt_list_middle = self. create_middle()

        for bolt in bolt_list_1:
            self.save_modell(bolt)

        for bolt in bolt_list_middle:
            self.save_modell(bolt)

        gear_1 = self.combine_all_obj(board,[up1])
        gear_1.name = "Up1"
        self.save_modell(gear_1,middle)

        gear_2 = self.combine_all_obj(gear_1,bolt_list_1)
        self.rotate_object(gear_2)



        upper = self.combine_all_obj(gear_2, ex_list)
        x,y,z = upper.location
        self.calculate_bolt_position((x,y,z))

        if self.gear_Flip : 
            if self.gear_orientation in ['mf_zero','mf_HundredEighteen']:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, False, False))
                bpy.ops.transform.translate(value=(-2*x,0,0))
      
            else:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
                bpy.ops.transform.translate(value=(0,-2*y,0))

        gear = self.combine_all_obj(upper, [middle] + bolt_list_middle)

        return upper
    
    ##############################################################################################################################
    ######################## Upper Part Type B ###################################################################################
    
    def create_type_b_gear(self, extension=None):
        init_x = self.init_x
        init_y = self.init_y
        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]
        #length_relativ = 1
        #rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]
        length_relativ = 4.5

        rotation_s = (radians(-90),"Y")
        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        lower_gear_radius = self.lower_gear_dia/2
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia

   
        x = init_x
        y = init_y - lower_gear_radius
        z = main_long + sub_long + small_gear_position

        #Create gear

        ring_1 = self.create_ring((x,y,z),length_relativ/3,lower_gear_radius, 1.6)
        ring_2 = self.create_ring((x,y,z),length_relativ/3 +0.5, 0.9, 0.4)
        s_gear = self.combine_all_obj(ring_1, [ring_2])
        #s_gear = self.create_gear((x,y,z),lower_gear_radius,"hollow",length_relativ)
        s_gear.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 


        exte = self.create_gear_extension((x,y,z),length_relativ)


        # Create Bolts

        x_bolt_init = x + length_relativ/6 - self.BOLT_LENGTH/2 + self.EXTENSION_THICKNESS + 0.1
        y_bolt_init = y - lower_gear_radius - 0.9*self.BOLT_RAD
        z_bolt_init = z 
        # Calculate the rotate (x,z axis)
        bolt_rotation_1 = 45#self.samll_gear_bolt_rotation_1
        bolt_rotation_2 = -90#self.samll_gear_bolt_rotation_2
        #if self.small_gear_bolt_random:  
            #if extension:
            #    bolt_rotation_1,bolt_rotation_2 =  self.s_bolt_lsit     
           # bolt_rotation_1 = random.uniform(190,230)
            #self.samll_gear_bolt_rotation_1 = bolt_rotation_1
            #bolt_rotation_2 =  random.uniform(310,350)
            #self.samll_gear_bolt_rotation_2 = bolt_rotation_2
            #self.s_bolt_lsit = [bolt_rotation_1,bolt_rotation_2]
        
        y_bolt_1, z_bolt_1 = self.rotate_around_point((y,z),bolt_rotation_1,(y_bolt_init,z_bolt_init))
        y_bolt_2, z_bolt_2 = self.rotate_around_point((y,z),bolt_rotation_2,(y_bolt_init,z_bolt_init))       
        bolt_1 = self.create_bolt((x_bolt_init, y_bolt_1,z_bolt_1), rotation = rotation_s, only_body = extension)
        bolt_2 = self.create_bolt((x_bolt_init, y_bolt_2,z_bolt_2), rotation = rotation_s, only_body = extension) 

        y_bolt_3 = self.FOUR_CYL_DIA + self.BOLT_RAD

        bolt_3 = self.create_bolt((x_bolt_init, y_bolt_3,z_bolt_1), rotation = rotation_s, only_body = extension)

        bolt_shell_list = [bolt_1[0], bolt_2[0],bolt_3[0]]
        bolt_bit_list = [bolt_1[1], bolt_2[1],bolt_3[1]]



        upper_1 = self.combine_all_obj(s_gear, [exte]+bolt_shell_list)
        return upper_1, bolt_bit_list
    

    def create_gear_extension(self, position, length_relative):
        main_long = self.bottom_length 
        sub_long = self.sub_bottom_length
        radius = self.lower_gear_dia/2
        thickness = length_relative/6

        x_up = position[0]
        y_up = position[1] - radius
        z_up = position[2] + 3.1

        x_mid = x_up
        y_mid = position[1] + 0.1
        z_mid = position[2] + radius + self.BOLT_RAD*2

        x_low = position[0]
        y_low = 2.4
        z_low = main_long + sub_long + 3.5


        verts = [
            (x_up, y_up, z_up), #0
            (x_up + thickness, y_up, z_up), #1
            (x_up, y_up, position[2]-radius + 0.1), #2
            (x_up + thickness, y_up, position[2]-radius +0.1), #3
            (x_up, self.FOUR_CYL_DIA+0.3, main_long+sub_long+0.8), #4
            (x_up + thickness, self.FOUR_CYL_DIA+0.3, main_long+sub_long+0.8), #5
            (x_low, y_low, z_low), #6
            (x_low + thickness, y_low, z_low), #7
            (x_mid, y_mid, z_mid), #8
            (x_mid + thickness, y_mid, z_mid), #9
        ] 

        faces = [
            [0,1,3,2],
            [2,4,5,3],
            [4,5,7,6],
            [8,6,7,9],
            [0,8,9,1],
            [0,8,6,4,2],
            [1,9,7,5,3],
            

        ]
        board_bottom = self.add_mesh("bottom board", verts, faces)

        bpy.ops.mesh.primitive_cylinder_add(radius=radius/2, depth=5, location=position)
        cly_cut = bpy.context.object

        bpy.ops.object.select_all(action='DESELECT')
        cly_cut.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 

        self.diff_obj(board_bottom, cly_cut)
        cly_cut.select_set(True)
        bpy.ops.object.delete()

        #Create end cylinder
        cyl_dia = 0.6
        x_cyl = x_up + thickness/2
        y_cyl = y_up + cyl_dia/2
        z_cyl = z_up - cyl_dia/2
        end_cly = self.create_ring((x_cyl,y_cyl,z_cyl), thickness, cyl_dia, 0.4)
        #end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
        #end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'Z')
        end_cly.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        end_cly.name = 'End_cylinder'

        bpy.ops.mesh.primitive_cylinder_add(radius=cyl_dia, depth=thickness+1, location=(x_cyl,y_cyl,z_cyl))
        tmp = bpy.context.object
        tmp.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        self.diff_obj(board_bottom, tmp)
        tmp.select_set(True)
        bpy.ops.object.delete()


        #Create end cylinder
        x_cyl_2 = x_low + thickness/2
        y_cyl_2 = y_low - cyl_dia/2
        z_cyl_2 = z_low - cyl_dia/2
        end_cly_2 = self.create_ring((x_cyl_2,y_cyl_2,z_cyl_2), thickness, cyl_dia, 0.4)
        end_cly_2.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z')  
        end_cly.name = 'End_cylinder'

        bpy.ops.mesh.primitive_cylinder_add(radius=cyl_dia, depth=thickness+1, location=(x_cyl_2,y_cyl_2,z_cyl_2))
        tmp = bpy.context.object  
        tmp.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        self.diff_obj(board_bottom, tmp)
        tmp.select_set(True)
        bpy.ops.object.delete()

        extension = self.combine_all_obj(board_bottom,[end_cly,end_cly_2])
        if self.color_render:
            self.rend_color(extension, "Plastic")

        return extension

    def create_upper_part_Type_B(self):
        rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]

        upper_1, bolt_list = self.create_type_b_gear()

        middle, bolt_list_middle = self. create_middle()
        gear = self.combine_all_obj(upper_1, [middle] + bolt_list_middle+bolt_list)

        return gear

    def create_upper_part(self):
        if self.head_Type == "mf_Head_Type_A":
            return self.create_upper_part_Type_A()
        elif self.head_Type == "mf_Head_Type_B":
            return self.create_upper_part_Type_B()