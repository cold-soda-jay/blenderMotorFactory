import bpy
import math
import mathutils
import random
from math import radians

class Motor_Creator:



    #######################################################################################################################
    ##################### Constants #######################################################################################
    
    #Bottom

    BOTTOM_DIA = 4
    BOTTOM_HEIGHT = 3
    SUB_BOTTOM_LENGTH = 1.2
    SUB_BOTTOM_DIA = 1
    SUB_BOTTOM_INNER_DEPTH = 0.5
    ##Bolt
    BOLT_DIA = 0.4
    BOLT_LENGTH = 1.4
    BOLT_BIT_DIA = 0.2
    BOARD_THICKNESS = 0.1
    FOUR_CYL_DIA = 0.7
    #4 covex cyl
    C1_LENGTH = 1.9
    C2_LENGTH = 2.7
    C3_LENGTH = 1.1
    C4_LENGTH = 0.8


    #######################################################################################################################
    ####################### Variable ######################################################################################
    
    #Position of Motor
    init_x = 0
    init_y = 0
    init_z = 0

    #Size of bottom part
    bottom_length = 6.4
    inner_radius = 1

    #Bolts
    bolt_ortientation = False
    bit_type = "Torx"

    #Gear
    gear_orientation = "mf_East"
    small_gear_dia = 0
    small_gear_position = None
    large_gear_dia = 0

    samll_gear_angel = 0
    samll_gear_bolt_position_angel = 0
    large_gear_angel = 0
    large_gear_bolt_position_angel = 0

    orient_dict = {
        'mf_West':((radians(0),"Z"), BOTTOM_DIA,True),
        'mf_South':((radians(-90),"Z"),BOTTOM_HEIGHT,True),
        'mf_East':((radians(0),"Z"), BOTTOM_DIA,False),
        'mf_North':((radians(-90),"Z"),BOTTOM_HEIGHT,False)
    }

    #Extention Zone
    ex_type = None

    #Color Render
    color_render = False
    gear_Flip = False



    def __init__(self,factory):
        self.init_x = factory.init_x
        self.init_y = factory.init_y
        self.init_z = factory.init_z
        self.bottom_length = factory.mf_Bottom_Length
        self.inner_radius = factory.mf_Sub_Bottom_Inner_Dia
        self.bolt_ortientation = factory.mf_Bolt_Orientation
        self.bit_type = factory.mf_Bit_Type
        self.gear_orientation = factory.mf_Gear_Orientation
        self.small_gear_dia = factory.mf_Small_Gear_Dia
        self.small_gear_position = factory.mf_Small_Gear_Position
        self.large_gear_dia = factory.mf_Large_Gear_Dia
        self.ex_type = factory.mf_Type
        self.gear_Flip = factory.mf_Flip
        self.color_render = factory.mf_Color_Render
        self.samll_gear_angel = factory.mf_Small_Gear_Bolt_Angel
        self.samll_gear_bolt_position_angel = factory.mf_Small_Gear_Bolt_Rotation        
        self.large_gear_angel = factory.mf_Large_Gear_Bolt_Angel
        self.large_gear_bolt_position_angel = factory.mf_Large_Gear_Bolt_Rotation


    ##############################################################################################################################
    ########################## Utility ###########################################################################################
    

    def combine_all_obj(self, main_obj, object_list):
        bpy.ops.object.select_all(action='DESELECT')
        #bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = main_obj
        for obj in object_list:
            try:
                main_obj.select_set(True)        
                obj.select_set(True)
                bpy.ops.object.join()
            except ReferenceError:
                bpy.context.view_layer.objects.active = None
                return main_obj
        bpy.context.view_layer.objects.active = None
        return main_obj

    def rotate_around_point(self, origin, angel, obj_position):
        rot = radians(angel)   
        relativ_point = [obj_position[0]-origin[0], obj_position[1]-origin[1]]
        x = relativ_point[0] * math.cos(rot) - relativ_point[1] * math.sin(rot) 
        y = relativ_point[0] * math.sin(rot)  + relativ_point[1] * math.cos(rot)
        return x+origin[0],y+origin[1]

    def create_ring(self, position,height,radius,thickness,rotation=None):
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=position)
        cly_out = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(radius=radius-thickness, depth=height+1, location=position)
        cly_in = bpy.context.object

        bool_in = cly_out.modifiers.new('bool_in', 'BOOLEAN')
        bool_in.operation = 'DIFFERENCE'
        bool_in.object = cly_in
        bpy.context.view_layer.objects.active = cly_out
        res = bpy.ops.object.modifier_apply(modifier='bool_in')
        # Delete the cylinder.x
        cly_in.select_set(True)
        bpy.ops.object.delete() 
        #if rotation is not None:
        #    bpy.context.view_layer.objects.active = cly_out
        #    bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        return cly_out

    def create_triangle(self, position,thickness,length,towards=None):
        h=length
        t=thickness
        x=position[0]
        y=position[1]
        z=position[2]
        verts=[
            (x,y+t/2,z+h),
            (x,y+t/2,z),
            (x+h,y+t/2,z),
            (x,y-t/2,z+h),
            (x,y-t/2,z),
            (x+h,y-t/2,z),
        ]
        faces = [
            [0, 1, 2],
            [3, 4, 5],
            [0,3,4,1],
            [1,4,5,2],
            [0,3,5,2],
        ]

        obj = self.add_mesh("triangle", verts, faces)
        return obj

    def add_mesh(self, name, verts, faces, edges=None, col_name="Collection"):    
        if edges is None:
            edges = []
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get(col_name)
        col.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        mesh.from_pydata(verts, edges, faces)
        return obj

    def add_torx(self,position,size,depth):
        x = position[0]
        y = position[1]
        z = position[2] + 0.2
        depth += 0.1

        v1 = [0, 0.5 * size,0]
        v2 = [- 0.1443 * size, 0.25 * size,0]
        v3 = [- 0.433 * size, 0.25 * size, 0]
        v4 = [-0.2887 * size, 0, 0]
        v5 = [- 0.433 * size,  -0.25 * size, 0]
        v6 = [-0.1443 * size, -0.25 * size, 0]

        verts = [
            self.add_vector(position, v1),
            self.add_vector(position, v2),
            self.add_vector(position, v3),
            self.add_vector(position, v4),
            self.add_vector(position, v5),
            self.add_vector(position, v6),
            self.add_vector(position, v1,minus=1),
            self.add_vector(position, v2,minus=1),
            self.add_vector(position, v3,minus=1),
            self.add_vector(position, v4,minus=1),
            self.add_vector(position, v5,minus=1),
            self.add_vector(position, v6,minus=1),

            self.add_vector(position, v1, height=depth),
            self.add_vector(position, v2, height=depth),
            self.add_vector(position, v3, height=depth),
            self.add_vector(position, v4, height=depth),
            self.add_vector(position, v5, height=depth),
            self.add_vector(position, v6, height=depth),
            self.add_vector(position, v1,minus=1, height=depth),
            self.add_vector(position, v2,minus=1, height=depth),
            self.add_vector(position, v3,minus=1, height=depth),
            self.add_vector(position, v4,minus=1, height=depth),
            self.add_vector(position, v5,minus=1, height=depth),
            self.add_vector(position, v6,minus=1, height=depth),
            [x,y,z-depth*2],
        ]
        
        up = [0,1,2,3,4,5,6,7,8,9,10,11]
        bott = [12,13,14,15,16,17,18,19,20,21,22,23]
        faces = [up]
        for i in range(12):
            if i < 11:
                faces.append([up[i],up[i+1],bott[i+1],bott[i]])
                faces.append([bott[i+1],bott[i],24])
            else:
                faces.append([up[11],up[0],bott[0],bott[11]])
                faces.append([bott[11],bott[0],24])
        
        obj = self.add_mesh("torx", verts, faces)
        return obj

    def diff_obj(self, main, slave):
        boolean = main.modifiers.new('boolean', 'BOOLEAN')
        boolean.operation = 'DIFFERENCE'
        boolean.object = slave
        bpy.context.view_layer.objects.active = main
        res = bpy.ops.object.modifier_apply(modifier='boolean')
        return res

    def add_vector(self,v1,v2,minus=0,height=0):
        out = []
        for i in range(len(v1)):
            if minus == 1:
                out.append(v1[i]-v2[i])
            else:
                out.append(v1[i]+v2[i])
        if height != 0:
            out[-1] -= height
        return out

    def create_motor_main(self, position, height, width, length):

        # Add main cylinder
        cylinder_r = width/2
        cylinder_d = length

        bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_r, depth=cylinder_d, location=position)
        cyl = bpy.context.object
        cyl.name = 'Motor_main_part'


        # Add cube 1
        cuboid_lx = position[0] - width- height/2
        cuboid_ly = position[1]
        cuboid_lz = position[2]
        bpy.ops.mesh.primitive_cube_add(location=(cuboid_lx,cuboid_ly,cuboid_lz))
        bpy.ops.transform.resize(value=(width, width, length))

        cube_1 = bpy.context.object
        cube_1.name = 'cube1'

        # Add cube 2
        cuboid_lx = position[0] + width + height/2
        cuboid_ly = position[1]
        cuboid_lz = position[2]
        bpy.ops.mesh.primitive_cube_add(location=(cuboid_lx,cuboid_ly,cuboid_lz))
        bpy.ops.transform.resize(value=(width, width, length))

        cube_2 = bpy.context.object
        cube_2.name = 'cube2'


        # Boolean Operation for Cube 1
        bool_1 = cyl.modifiers.new('bool_1', 'BOOLEAN')
        bool_1.operation = 'DIFFERENCE'
        bool_1.object = cube_1
        bpy.context.view_layer.objects.active = cyl
        res = bpy.ops.object.modifier_apply(modifier='bool_1')

        # Boolean Operation for Cube 2
        bool_2 = cyl.modifiers.new('bool_2', 'BOOLEAN')
        bool_2.operation = 'DIFFERENCE'
        bool_2.object = cube_2
        bpy.context.view_layer.objects.active = cyl
        res = bpy.ops.object.modifier_apply(modifier='bool_2')

        cube_2.select_set(True)
        bpy.ops.object.delete()

        cube_1.select_set(True)
        bpy.ops.object.delete()

        return cyl

    def create_bolt(self, position,rotation=None,bit_type=None,orientation='mf_all_same',only_body=None):
        """[summary]
        create_bolt((0,0,0),(radians(45),'X'))
        """    
        out_dia = self.BOLT_DIA
        if only_body :
            out_length = only_body
            z_in = position[2] + out_length/2 - 0.15

            part = self.create_ring((position[0],position[1],z_in),out_length,self.BOLT_DIA,0.2*self.BOLT_DIA)
            part.name = 'Bolt'

        else:
            out_length = self.BOLT_LENGTH

            in_dia = 0.8 * self.BOLT_DIA
            
            z_in = position[2] + out_length/2
            bpy.ops.mesh.primitive_cylinder_add(radius=in_dia, depth=in_dia, location=(position[0],position[1],z_in))
            in_cyl = bpy.context.object
            in_cyl.name = 'in_cylinder'

            z_sphe = z_in + in_dia/2

            bpy.ops.mesh.primitive_cylinder_add(radius=out_dia, depth=out_length, location=position)
            out_cyl = bpy.context.object
            out_cyl.name = 'out_cylinder'

            bpy.ops.mesh.primitive_uv_sphere_add(radius=in_dia, location=(position[0],position[1],z_sphe))
            sphere = bpy.context.object
            sphere.name = 'sphere'
            z_cut = z_sphe + in_dia/2 + in_dia/3
            bpy.ops.mesh.primitive_cylinder_add(radius=in_dia, depth=in_dia, location=(position[0],position[1],z_cut))
            cut_cyl = bpy.context.object
            cut_cyl.name = 'cut_cylinder'

            bool_in = sphere.modifiers.new('bool_in', 'BOOLEAN')
            bool_in.operation = 'DIFFERENCE'
            bool_in.object = cut_cyl
            bpy.context.view_layer.objects.active = sphere
            res = bpy.ops.object.modifier_apply(modifier='bool_in')
            # Delete the cylinder.x
            cut_cyl.select_set(True)
            bpy.ops.object.delete() 

            if bit_type == 'mf_Bit_Slot':
                bpy.ops.mesh.primitive_cube_add(location=(position[0],position[1],z_sphe+ in_dia/3))
                bpy.ops.transform.resize(value=(in_dia*1.5, 0.05, 0.2))
                bit = bpy.context.object
            elif bit_type == 'mf_Bit_Torx':
                bit = self.add_torx((position[0],position[1],z_sphe+ in_dia),in_dia*1.5,0.2)
            elif bit_type == 'mf_Bit_Cross':
                bpy.ops.mesh.primitive_cube_add(location=(position[0],position[1],z_sphe+ in_dia/3))
                bpy.ops.transform.resize(value=(0.05, in_dia, 0.2))
                bit_1 = bpy.context.object
                bool_bit = sphere.modifiers.new('bool_bit', 'BOOLEAN')
                bool_bit.operation = 'DIFFERENCE'
                bool_bit.object = bit_1
                bpy.context.view_layer.objects.active = sphere
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit')

                bool_bit_2 = in_cyl.modifiers.new('bool_bit_2', 'BOOLEAN')
                bool_bit_2.operation = 'DIFFERENCE'
                bool_bit_2.object = bit_1
                bpy.context.view_layer.objects.active = in_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_2')

                bool_bit_3 = out_cyl.modifiers.new('bool_bit_3', 'BOOLEAN')
                bool_bit_3.operation = 'DIFFERENCE'
                bool_bit_3.object = bit_1
                bpy.context.view_layer.objects.active = out_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_3')

                bit_1.select_set(True)
                bpy.ops.object.delete() 
                #bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 

                bpy.ops.mesh.primitive_cube_add(location=(position[0],position[1],z_sphe+ in_dia/3))
                bpy.ops.transform.resize(value=(in_dia, 0.05, 0.2))
                bit_2 = bpy.context.object   
                bool_bit = sphere.modifiers.new('bool_bit', 'BOOLEAN')
                bool_bit.operation = 'DIFFERENCE'
                bool_bit.object = bit_2
                bpy.context.view_layer.objects.active = sphere
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit')

                bool_bit_2 = in_cyl.modifiers.new('bool_bit_2', 'BOOLEAN')
                bool_bit_2.operation = 'DIFFERENCE'
                bool_bit_2.object = bit_2
                bpy.context.view_layer.objects.active = in_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_2')

                bool_bit_3 = out_cyl.modifiers.new('bool_bit_3', 'BOOLEAN')
                bool_bit_3.operation = 'DIFFERENCE'
                bool_bit_3.object = bit_2
                bpy.context.view_layer.objects.active = out_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_3')

                bit_2.select_set(True)
                bpy.ops.object.delete()          

            if bit_type == 'mf_Bit_Cross':
                pass
            
            else:
                bool_bit = sphere.modifiers.new('bool_bit', 'BOOLEAN')
                bool_bit.operation = 'DIFFERENCE'
                bool_bit.object = bit
                bpy.context.view_layer.objects.active = sphere
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit')

                bool_bit_2 = in_cyl.modifiers.new('bool_bit_2', 'BOOLEAN')
                bool_bit_2.operation = 'DIFFERENCE'
                bool_bit_2.object = bit
                bpy.context.view_layer.objects.active = in_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_2')

                bool_bit_3 = out_cyl.modifiers.new('bool_bit_3', 'BOOLEAN')
                bool_bit_3.operation = 'DIFFERENCE'
                bool_bit_3.object = bit
                bpy.context.view_layer.objects.active = out_cyl
                res_2 = bpy.ops.object.modifier_apply(modifier='bool_bit_3')

                bit.select_set(True)
                bpy.ops.object.delete() 


            part = self.combine_all_obj(out_cyl,[sphere,in_cyl])
            part.name = 'Bolt'

        if orientation == 'mf_all_random':
            angel = random.randrange(0, 360, 10)     
            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=radians(angel),orient_axis='Z') 
        if rotation:
            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        if self.color_render:
            pass

        return part


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
        sub_long = self.SUB_BOTTOM_LENGTH * size

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
        sub_long = self.SUB_BOTTOM_LENGTH * size

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

        ##Diverse Part 1
        en_height_5 = thickness/2
        en_width_5 = en_width_4/3
        en_long_5 = en_long_3/3

        en_x_5 = energy_x
        en_y_5 = en_y_3 - en_width_3 - en_width_5
        en_z_5 = init_z+ sub_long+ main_long + 1.4 - en_long_5 - thickness

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_5,en_z_5))
        bpy.ops.transform.resize(value=(en_height_5, en_width_5, en_long_5))
        en_5 = bpy.context.object
        en_5.name = 'cube6'

        ##Diverse Part 2
        en_height_6 = thickness/2
        en_width_6 = en_width_4/6
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_6 = bpy.context.object
        en_6.name = 'cube7'


        #Cereate  Bolt 1
        bolt_x = init_x + main_hight/2 - self.BOLT_DIA
        bolt_y = init_y + main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        rota=(radians(180), 'X')
        bolt_1 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota,bit_type,orientation=bolt_orient)

        #Cereate  Bolt 2
        bolt_x = init_x - main_hight/2 + self.BOLT_DIA
        bolt_y = init_y - main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        bolt_2 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota,bit_type,orientation=bolt_orient)

        en_part = self.combine_all_obj(cube_1,[cube_2,cube_3,en_1,en_2,en_3,en_4,en_5,en_6,bolt_1,bolt_2])
        en_part.name = 'Energy Part'

        
        ##Cut parts
        cut_height_3 = main_hight/20
        cut_width_3 = 4.5 * thickness
        cut_long_3 = main_hight/4

        cut_x_3 = init_x 
        cut_y_3 = main_width + cut_width_3/2
        cut_z_3 = init_z+ sub_long+ main_long

        #bpy.ops.mesh.primitive_cube_add(location=(cut_x_3,cut_y_3,cut_z_3))
        #bpy.ops.transform.resize(value=(cut_height_3, cut_width_3, cut_long_3))

        #cut_3 = create_triangle((cut_x_3,cut_y_3,cut_z_3),cut_width_3,cut_long_3)
        #cut_3.name = 'cube4'

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

        sub_long = self.SUB_BOTTOM_LENGTH * size


        #four_cyl_dia = 1.4/2
        step = 0.1

        four_cyl_z = main_long + sub_long


        cy1_z = self.C1_LENGTH/2
        cy2_z = (self.C1_LENGTH + self.C2_LENGTH)/2
        cy3_z = (self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH)/2
        cy4_z = (self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH + self.C4_LENGTH)/2
        #Create 4 Covex cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA, depth=self.C1_LENGTH, location=(0,0,four_cyl_z+cy1_z))
        cyl_1 = bpy.context.object
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step, depth=self.C1_LENGTH + self.C2_LENGTH, location=(0,0,four_cyl_z+cy2_z))
        cyl_2 = bpy.context.object

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA- step *2, depth= self.C1_LENGTH + self.C2_LENGTH 
                                            + self.C3_LENGTH, location=(0,0,four_cyl_z+cy3_z))
        cyl_3 = bpy.context.object

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *3, depth=self.C1_LENGTH + self.C2_LENGTH 
                                            + self.C3_LENGTH + self.C4_LENGTH, location=(0,0,four_cyl_z+cy4_z))
        cyl_4 = bpy.context.object

        up = self.combine_all_obj(cyl_1,[cyl_2,cyl_3,cyl_4])

        return up


    ##############################################################################################################################
    ######################## Upper Part ###################################################################################

    def create_up1(self, length_relativ):
        
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z
        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]


        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.SUB_BOTTOM_LENGTH * size

        small_gear_dia = self.small_gear_dia
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia

        #Create small gear
        x = init_x + small_gear_dia/2
        y = init_y - main_width/4
        z = main_long + sub_long + small_gear_position

        rotation_s = (radians(-90),"X")

        s_gear = self.create_gear((x,y,z),"small",length_relativ)

        #Create board
        #width = 2.5
        #height = self.BOARD_THICKNESS
        #length = math.sqrt((x-self.FOUR_CYL_DIA)**2 +small_gear_position**2)

        #x_board = self.FOUR_CYL_DIA + (x - self.FOUR_CYL_DIA)/2
        #y_board = y + 0.5
        #z_board = main_long + sub_long + (small_gear_position)/2

        #angel = math.atan((x-self.FOUR_CYL_DIA)/small_gear_position)

    
        #bpy.ops.mesh.primitive_cube_add(location=(x_board,y_board,z_board))
        #bpy.ops.transform.resize(value=(height/2, width/2, length/2))
        #board = bpy.context.object

        #bpy.context.view_layer.objects.active = board
        #bpy.ops.transform.rotate(value=-angel,orient_axis='Y') 

        #Create large Gear
        x_large = init_x + small_gear_dia/2 - 0.8
        y_large = init_y - main_width/4 - length_relativ/6
        z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2
        rotation_l = (radians(-90),"X")

        l_gear = self.create_gear((x_large,y_large,z_large),"large",length_relativ)


        #extension_zone = create_extension_zone(factory,(x_large,y_large,z_large))
        up1 = self.combine_all_obj(s_gear,[l_gear])
        bpy.context.view_layer.objects.active = up1

        if self.gear_orientation in ['mf_North','mf_South'] :
            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
            bpy.ops.transform.translate(value=(0,-length_relativ/3,0))

        return up1

    def create_gear(self,position,gear_type,info,extension_zone = False):
        bit_type = self.bit_type
        bolt_orient = self.bolt_ortientation
        rotation = (radians(-90),"X")
        length_relativ = info
        if gear_type == 'small':
            radius = self.small_gear_dia/2
            if extension_zone:
                length = 0.3
            else:
                length = length_relativ*2/3
            inner_radius = 1/2
            inner_length = 1.4 * length +1
            angel = self.samll_gear_angel  * 10
            bolt_position_angel = self.samll_gear_bolt_position_angel * 10
            if self.gear_orientation in ['mf_East','mf_West'] and self.ex_type == 'mf_Type_B':
                bolt_position_angel -= 25

            #Create out
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=position)
            out_cyl = bpy.context.object
            out_cyl.name = 'out_cylinder'

            #Create inner
            bpy.ops.mesh.primitive_cylinder_add(radius=inner_radius, depth=inner_length, location=position)
            in_cyl = bpy.context.object
            in_cyl.name = 'in_cylinder'
            
            #Crete Bolts
            if extension_zone:
                body = length
                z_bolt_init = position[2]
            else:
                body = None
                z_bolt_init = position[2] + length/2 - self.BOLT_LENGTH/2 + 0.3

            #Init position
            x_bolt_init = position[0]+ radius + 0.9*self.BOLT_DIA
            y_bolt_init = position[1] 

            #Calculate the rotation
            x_bolt_1,y_bolt_1 = self.rotate_around_point((position[0],position[1]),bolt_position_angel,(x_bolt_init,y_bolt_init))
            x_bolt_2,y_bolt_2 = self.rotate_around_point((position[0],position[1]),bolt_position_angel+angel,(x_bolt_init,y_bolt_init))       
            bolt_1 = self.create_bolt((x_bolt_1,y_bolt_1,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_2,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)       
            part = self.combine_all_obj(out_cyl,[in_cyl,bolt_1,bolt_2])
            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        
            return part
        elif gear_type == 'large':

            radius = self.large_gear_dia/2
            if extension_zone:
                length = 0.3
            else:
                length = length_relativ/3
            inner_radius_1 = 1.6/2
            inner_radius_2 = 1.3/2
            inner_radius_3 = 2.9/2
            

            inner_length = length + 1
            angel = self.large_gear_angel * 10
            bolt_position_angel = self.large_gear_bolt_position_angel * 10
            
            #Ring 1
            thickness_1 = radius - inner_radius_1
            cly_1 = self.create_ring(position,length,radius,thickness_1)

            #Ring 2
            x = position[0]
            y = position[1]
            z = position[2] - 0.3
            position_in = (x,y,z)

            thickness_2 = inner_radius_1 - inner_radius_2
            cly_2 = self.create_ring(position_in,inner_length,inner_radius_1,thickness_2)

            #Ring 3
            x = position[0]
            y = position[1]
            z = position[2] + 0.1
            position_3 = (x,y,z)

            thickness_3 = 0.2
            cly_3 = self.create_ring(position_3,length+0.3,inner_radius_3,thickness_3)

            if extension_zone:
                body = length
                z_bolt_init = position[2]
            else:
                body = None
                z_bolt_init = position[2] + length/2 - self.BOLT_LENGTH/2 + 0.3

            #Init position
            x_bolt_init = position[0]+ radius + 0.9*self.BOLT_DIA
            y_bolt_init = position[1] 

            #Calculate the rotation
            x_bolt_1,y_bolt_1 = self.rotate_around_point((position[0],position[1]),bolt_position_angel,(x_bolt_init,y_bolt_init))
            x_bolt_2,y_bolt_2 = self.rotate_around_point((position[0],position[1]),bolt_position_angel+angel,(x_bolt_init,y_bolt_init))       
            bolt_1 = self.create_bolt((x_bolt_1,y_bolt_1,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_2,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)       
            part = self.combine_all_obj(cly_1,[cly_2,cly_3,bolt_1,bolt_2])
            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        
            return part

    def create_extension_zone(self, large_gear_position, gear_length):

        small_gear_dia = self.small_gear_dia
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia
        s_length_1 = 2.9/2
        s_length_2 = 5.5
        s_length_3 = 1.5
        s_length_4 = 4.5
        s_length_6 = 3

        if self.ex_type == 'mf_Type_B':
            angle_1 = 15
            angle_2 = 0
            s_length_5 = 3.5
        elif self.ex_type == 'mf_Type_A':
            angle_1 = 30
            s_length_5 = 5
            angle_2 = 25

        angle_3 = 35

        x = large_gear_position[0]
        y = large_gear_position[1] - gear_length/2 + 0.4
        z = large_gear_position[2]

        x_thickness = math.cos(radians(angle_3)) * 0.2

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
            (p1x- x_thickness + (large_gear_dia/6)* math.cos(radians(30)), y, p1z-(large_gear_dia/6)* math.sin(radians(30))), #0
            (p1x- x_thickness + (large_gear_dia/6)* math.cos(radians(30)), y - thickness_bottom, p1z-(large_gear_dia/6* math.sin(radians(30)))), #1
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
            #[12, 4, 6, 8],
            [13, 15, 16, 14],       

        ]
        bottom_board = self.add_mesh("bottom board", verts_bottom, faces_bottom)


        #Create end cylinder
        if self.ex_type == 'mf_Type_B':
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

            board = self.combine_all_obj(bottom_board,[board_1, board_2,end_cly_1,end_cly_2])

            bevel = board.modifiers.new(name='bevel', type='BEVEL')
            
            bevel.affect = 'EDGES'
            bevel.angle_limit = 100
            bevel.offset_type = 'WIDTH'
            bevel.width = 1000000
            bpy.context.view_layer.objects.active = board
            res = bpy.ops.object.modifier_apply(modifier='bevel')

        elif self.ex_type == 'mf_Type_A':

            dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)
            x_cyl = p5x - (p5x - p6x)/2 
            y_cyl = (y - 0.8)
            z_cyl = p6z - (p6z -p5z)/2 
            end_cly = self.create_ring((x_cyl,y_cyl,z_cyl), 1.6, dia/2, 0.5)
            end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly.name = 'End_cylinder'
            board = self.combine_all_obj(bottom_board,[board_1, board_2,end_cly])

            bevel = board.modifiers.new(name='bevel', type='BEVEL')
            
            bevel.affect = 'EDGES'
            bevel.angle_limit = 100
            bevel.offset_type = 'WIDTH'
            bevel.width = 1000000
            bpy.context.view_layer.objects.active = board
            res = bpy.ops.object.modifier_apply(modifier='bevel')

        #bpy.ops.mesh.bevel(offset_type='OFFSET', offset=10.0, affect ='EDGES')

        return board

    def create_up2(self,length_relativ):

        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]

        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.SUB_BOTTOM_LENGTH * size

        small_gear_dia = self.small_gear_dia
        small_gear_position = self.small_gear_position
        large_gear_dia = self.large_gear_dia

        #Create small gear
        x = init_x + small_gear_dia/2
        y = init_y - main_width/4 - length_relativ/3 - 0.15
        z = main_long + sub_long + small_gear_position

        rotation_s = (radians(-90),"X")

        s_gear = self.create_gear((x,y,z),"small",length_relativ,extension_zone=True)


        #Create large Gear
        x_large = init_x + small_gear_dia/2 - 0.8
        y_large = init_y - main_width/4 - length_relativ/6 - length_relativ/6 - 0.15
        z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2
        rotation_l = (radians(-90),"X")

        l_gear = self.create_gear((x_large,y_large,z_large),"large",length_relativ,extension_zone=True)

        gears = self.combine_all_obj(s_gear,[l_gear])

        if self.gear_orientation in ['mf_North','mf_South'] :
            bpy.context.view_layer.objects.active = gears

            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
            bpy.ops.transform.translate(value=(0,1.25,0))

            
        extension_zone = self.create_extension_zone((x_large,y_large,z_large),0.3)
        if self.gear_orientation in ['mf_North','mf_South'] :
            bpy.context.view_layer.objects.active = extension_zone
            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, True, False))
            bpy.ops.transform.translate(value=(5.5/2-0.65+0.3, -length_relativ+0.05,0))

        up2 = self.combine_all_obj(gears,[extension_zone])
        return up2

    def create_side_board(self):
            #Create Side board
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.SUB_BOTTOM_LENGTH * size


        ##Part 1
        if self.gear_orientation in ['mf_West', 'mf_East'] :
            width = 0.9 * self.BOTTOM_DIA/2
        elif self.gear_orientation in ['mf_North', 'mf_South'] :
            width = 0.9 * self.BOTTOM_HEIGHT/2
        height = self.BOARD_THICKNESS
        p1_length = 2.4/2

        if self.gear_orientation in ['mf_West', 'mf_East'] :
            x = init_x - self.BOTTOM_HEIGHT/2 + self.BOARD_THICKNESS
            y = init_y - 2 * self.BOARD_THICKNESS
            z = init_z + main_long + sub_long + self.BOLT_LENGTH + p1_length - self.BOLT_LENGTH/2
            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(height, width, p1_length - self.BOLT_LENGTH/2 ))

        elif self.gear_orientation in ['mf_North', 'mf_South'] :
            x = init_x + 2 * self.BOARD_THICKNESS
            y = init_y + self.BOTTOM_HEIGHT/2 - self.BOARD_THICKNESS
            z = init_z + main_long + sub_long + self.BOLT_LENGTH + p1_length - self.BOLT_LENGTH/2

            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(width, height, p1_length - self.BOLT_LENGTH/2 ))
        

        board_1 = bpy.context.object

        ##Part 2

        z = init_z + main_long + sub_long + p1_length*2 + (
                        self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH - p1_length*2 )/2

        if self.gear_orientation in ['mf_West', 'mf_East'] :
            x = init_x - self.BOTTOM_HEIGHT/4 + self.BOARD_THICKNESS
            p2_length = math.sqrt((self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH-p1_length*2)**2 
                                    + (main_height/2)**2 )/2
            angel = math.atan((main_height/2)/(self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH -
                                     p1_length*2))
            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(height, width, p2_length))
            board_2 = bpy.context.object
            bpy.context.view_layer.objects.active = board_2
            bpy.ops.transform.rotate(value=-angel,orient_axis='Y') 
        elif self.gear_orientation in ['mf_North', 'mf_South'] :
            y = init_y + self.BOTTOM_HEIGHT/4 - self.BOARD_THICKNESS
            p2_length = math.sqrt((self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH-p1_length*2)**2 +
                                 (main_height/2)**2 )/2
            angel = math.atan((main_height/2)/(self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH - p1_length*2))

            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(width, height, p2_length))

            board_2 = bpy.context.object

            bpy.context.view_layer.objects.active = board_2
            bpy.ops.transform.rotate(value=-angel,orient_axis='X') 
        #cube_2.matrix_world @= Matrix.Rotation(radians(angel),4,'Y') 


        #Create board

        x = self.small_gear_dia/2
        y = - main_width/4
        z = main_long + sub_long + self.small_gear_position

        width = 2.5
        height = self.BOARD_THICKNESS
        length = math.sqrt((x-self.FOUR_CYL_DIA)**2 +  self.small_gear_position**2)

        if self.gear_orientation in ['mf_East','mf_West'] :
            x_board = self.FOUR_CYL_DIA + (x - self.FOUR_CYL_DIA)/2
            y_board = y + 0.5
            z_board = main_long + sub_long + ( self.small_gear_position)/2
            just_rotate = False
        elif self.gear_orientation in ['mf_North', 'mf_South'] :
            x_board = 0.1
            y_board = -1.5
            z_board = main_long + sub_long + ( self.small_gear_position)/2
            just_rotate = True


        angel = math.atan((x-self.FOUR_CYL_DIA)/ self.small_gear_position)

    
        bpy.ops.mesh.primitive_cube_add(location=(x_board,y_board,z_board))
        bpy.ops.transform.resize(value=(height/2, width/2, length/2))
        board_3 = bpy.context.object

        bpy.context.view_layer.objects.active = board_3
        

        if just_rotate:
            bpy.ops.transform.rotate(value=angel,orient_axis='Y') 
            bpy.ops.transform.rotate(value=radians(-90),orient_axis='Z') 
        else:
            bpy.ops.transform.rotate(value=-angel,orient_axis='Y') 




        board = self.combine_all_obj(board_1,[board_2,board_3])

        return board

    def create_upper_part(self):
        rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]
        up1 = self.create_up1(length_relativ)
        up2 = self.create_up2(length_relativ)
        board = self.create_side_board()
        upper_part = self.combine_all_obj(up1,[up2])
        #bpy.ops.transform.translate(value=(0,-0.5,0))
        x,y,z = upper_part.location
        #x1,y1,z1 = board_side.location
        bpy.context.view_layer.objects.active = upper_part

        if self.gear_orientation == 'mf_West' :
            bpy.ops.transform.translate(value=(0,-2*y,0))
            #bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, mirror, False))


        elif self.gear_orientation == 'mf_North' :
            nx,ny = self.rotate_around_point((0,0),-90,(x,y))

            #upper_part.location = (n_x,n_y,z)
            bpy.ops.transform.translate(value=(-1.25,ny-y,0))
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, True, False))


        elif self.gear_orientation == 'mf_South' :
            nx,ny = self.rotate_around_point((0,0),90,(x,y))
            #upper_part.location = (n_x,n_y,z)
            bpy.ops.transform.translate(value=(-2.75,-y-ny,0))
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
            bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
            

        if self.gear_Flip: 
            if self.gear_orientation in ['mf_East','mf_West']:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, False, False))
            else:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))


            #bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(mirror, False, False))

        upper = self.combine_all_obj(upper_part,[board])

        return upper
