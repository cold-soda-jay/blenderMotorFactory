import bpy
import os
import math
import mathutils
import random
from math import radians
import bmesh
import random
import csv
import re




class Factory: 
    """Basic Class for creating motor. Contains several basic methods and variables.
    

        To use this the defined motor operator should be created and given when initiationg:
        
        e.g.: creator = Factory(operator)
    """
    
    #######################################################################################################################
    ##################### Constants #######################################################################################
    
    #Bottom

    BOTTOM_DIA = 4
    BOTTOM_HEIGHT = 3
    SUB_BOTTOM_DIA = 1
    SUB_BOTTOM_INNER_DEPTH = 0.5
    ##Bolt
    BOLT_RAD = 0.4
    BOLT_LENGTH = 1.4
    BOLT_BIT_DIA = 0.2
    BOLT_THREAD_LENGTH = 1.3
    BOLT_THREAD_DIA = 0.2
    
    # Board
    BOARD_THICKNESS = 0.1
    FOUR_CYL_DIA = 0.7

    # 4 convex part
    
    C1_LENGTH = 0
    C2_LENGTH = 0
    C3_LENGTH = 0
    C4_LENGTH = 0
    C5_LENGTH = 0

    EXTENSION_THICKNESS = 0.2
    


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
    bolt_num = 0
    gear_orientation = "r0"

    
    # Define the behavior of rotation and flip
    orient_dict = {
        'r0':((radians(0),"Z"), BOTTOM_DIA, -BOTTOM_HEIGHT-0.1),
        'r90':((radians(-90),"Z"), BOTTOM_HEIGHT, BOTTOM_HEIGHT),
        'r180':((radians(-180),"Z"), BOTTOM_DIA, BOTTOM_DIA),
        'r270':((radians(-270),"Z"), BOTTOM_HEIGHT, -BOTTOM_DIA)
    }

    #Extention Zone
    head_Type = None
    ex_type = None

    #Color Render
    color_render = False
    gear_Flip = False

    #Define the parameter that should be svaed in csv file
    motor_param = [
        
    ]
    key_list = []
    save_path = "None"
    id_Nr = 0
    s_bolt_list = []
    l_bolt_list = []
    bolt_position = []
    
    out_bolt_position = []
    temp_save = False
    bolt_roate_angle_list = []
    general_Bolt = None

    def __init__(self,factory):
        """initiate variables.

        Args:
            factory ([bpy.types.Operator]): [Operator]
        """
        
        self.head_Type = factory.mf_Top_Type
        self.init_x = factory.init_x
        self.init_y = factory.init_y
        self.init_z = factory.init_z
        self.bottom_length = factory.mf_Bottom_Length
        self.inner_radius = 0.5
        self.sub_bottom_length = factory.mf_Sub_Bottom_Length
        self.bolt_ortientation = factory.mf_Bolt_Orientation

        self.bit_type = factory.mf_Bit_Type
        self.bolt_position = []
        
        self.out_bolt_position = []
        self.bolt_roate_angle_list = []

        self.gear_Flip = factory.mf_Flip

        self.lower_gear_dia = factory.mf_Lower_Gear_Dia
        self.lower_gear_position = factory.mf_Lower_Gear_Position
        
        self.color_render = factory.mf_Color_Render

        self.motor_param += [
            "mf_Top_Type",
            "mf_Flip",
            "mf_Color_Render",
            "mf_Bottom_Length",
            "mf_Sub_Bottom_Length",
            "mf_Bit_Type",
            "mf_Bolt_Orientation",
            
        ]
        self.save_path = factory.save_path
        self.temp_save = factory.temp_save
        self.id_Nr = factory.id_Nr     
        self.init_modify(factory)
        self.general_Bolt = self.create_general_bolt()
    
    def init_modify(self,factory):
        """Init other variables by demand

        Args:
            factory (bpy.types.Operator): [Operator]
        """
        pass

    ##############################################################################################################################
    ########################## Genera Utility ####################################################################################
    

    def combine_all_obj(self, main_obj, object_list):
        """Combine objects. Joint all opjects in object_list into main_obj

        Args:
            main_obj ([bpy.types.Object]): [main object]
            object_list ([list]): [List of objects that shold be joined into main object]

        Returns:
            [bpy.types.Object]: [Combined object. Should have same attribute as main_obj]
        """
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = main_obj
        for obj in object_list:
            try:
                if obj is None:
                    continue
                main_obj.select_set(True)        
                obj.select_set(True)
                bpy.ops.object.join()
            except ReferenceError:
                bpy.context.view_layer.objects.active = None
                return main_obj
        bpy.context.view_layer.objects.active = None
        return main_obj

    def rotate_around_point(self, origin, Angle, obj_position):
        """Caculate rotation for 2D case.

        Args:
            origin (tuple): Original point which object should rotate around it. Size: 1*2
            Angle (float): Rotate angle
            obj_position (tuple): Object position. Size: 1*2

        Returns:
            tuple: Rotated object position
        """
        if type(Angle) == int or float:
            rot = radians(Angle)   
        else:
            rot = Angle
        relativ_point = [obj_position[0]-origin[0], obj_position[1]-origin[1]]
        x = relativ_point[0] * math.cos(rot) - relativ_point[1] * math.sin(rot) 
        y = relativ_point[0] * math.sin(rot)  + relativ_point[1] * math.cos(rot)
        return x+origin[0],y+origin[1]

    def create_ring(self, position,height,radius,thickness):
        """Create ring object

        Args:
            position (tuple): position of ring. Size: 1*3
            height (float): height of ring
            radius (float): raius of ring
            thickness (float): Thickness of ring

        Returns:
            bpy.type.Object: Created ring
        """
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

        return cly_out

    def add_mesh(self, name, verts, faces, edges=None, col_name="Collection"):  
        """Create mesh using verts and faces

        Args:
            name (str): 
            verts (tuple): List of verts
            faces (tuple): List of faces
            edges (Tuple, optional): [description]. Defaults to None.
            col_name (str, optional): [description]. Defaults to "Collection".

        Returns:
            [bpy.type.objects]:
        """
          
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
        """Create torx model

        Args:
            position (tuple): 
            size (float): [description]
            depth (float): [description]

        Returns:
            bpy.type.Object: Torx object
        """
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
        """Boolean oeration for two object. 

        Args:
            main (bpy.type.objects): Main object that should be cutted
            slave (bpy.type.objects): Slave object that cuts main object

        """
        boolean = main.modifiers.new('bool_in', 'BOOLEAN')
        boolean.operation = 'DIFFERENCE'
        boolean.object = slave
        bpy.context.view_layer.objects.active = main
        res = bpy.ops.object.modifier_apply(modifier='bool_in')
        
        return res

    def add_vector(self,v1,v2,minus=0,height=0):
        """Add each element in two vectors

        Args:
            v1 (list): [description]
            v2 (list): [description]
            minus (int, optional): Set to 1, then v1 - v2. Set to 0, then v1 + v2. Defaults to 0.
            height (int, optional): Set to 1, add height. Defaults to 0.

        Returns:
            list: result vector
        """
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
        """Create motor botom main part(a cutted cylinder)

        Args:
            position ([type]): [description]
            height ([type]): [description]
            width ([type]): [description]
            length ([type]): [description]

        """

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

    def create_general_bolt(self):
        local = (0,0,0)
        bit_type = self.bit_type
        shank_length = 0
        shank_dia = 6
        cap_height = 3
        cap_dia = 7
        thread_length = 14
        major = 3
        minor = 4
        pitch = 1
        crest = 41
        root = 1
        div = 60
        if bit_type == 'mf_Bit_Slot':
            bpy.ops.mesh.bolt_add(align='VIEW', location=local, 
                                    bf_Model_Type='bf_Model_Bolt', 
                                    bf_Head_Type='bf_Head_Cap', bf_Bit_Type='bf_Bit_None', 
                                    bf_Shank_Length=shank_length, 
                                    bf_Shank_Dia=shank_dia,  
                                    bf_Cap_Head_Height=cap_height, bf_Cap_Head_Dia=cap_dia, 
                                    bf_Thread_Length=thread_length, 
                                    bf_Major_Dia=major, bf_Pitch=pitch, bf_Minor_Dia=minor, 
                                bf_Crest_Percent=crest, bf_Root_Percent=root,  bf_Div_Count=div,)
            bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            bolt = bpy.context.object
            bolt.location = local  
            
            bpy.ops.mesh.primitive_cube_add(location=(position[0],position[1],position[2]+out_length/2+0.2))
            bpy.ops.transform.resize(value=(5, 0.05, 0.2))
            bit = bpy.context.object
            
            bool_bit = bolt.modifiers.new('bool_bit', 'BOOLEAN')
            bool_bit.operation = 'DIFFERENCE'
            bool_bit.object = bit
            bpy.context.view_layer.objects.active = bolt
            res = bpy.ops.object.modifier_apply(modifier='bool_bit')
            bit.select_set(True)
            bpy.ops.object.delete() 
            
        elif bit_type == 'mf_Bit_Torx':
            #Torx
            
            bpy.ops.mesh.bolt_add(align='CURSOR', #location=local,  
                                bf_Model_Type='bf_Model_Bolt', bf_Head_Type='bf_Head_Cap', 
                                bf_Bit_Type='bf_Bit_Torx', bf_Shank_Length=shank_length, 
                                bf_Shank_Dia=shank_dia, bf_Torx_Size_Type='bf_Torx_T20', bf_Torx_Bit_Depth=2, 
                                bf_Cap_Head_Height=cap_height+1, bf_Cap_Head_Dia=cap_dia, 
                                bf_Thread_Length=thread_length, bf_Major_Dia=major, bf_Pitch=pitch, bf_Minor_Dia=minor, 
                                bf_Crest_Percent=crest, bf_Root_Percent=root,  bf_Div_Count=div,)
            bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            bolt = bpy.context.object
            bolt.location = local
            
        elif bit_type == 'mf_Bit_Cross':
            # Cross
            bpy.ops.mesh.bolt_add(align='WORLD', location=local,
                                    bf_Model_Type='bf_Model_Bolt',
                                    bf_Head_Type='bf_Head_Cap', bf_Bit_Type='bf_Bit_Philips', 
                                    bf_Shank_Length=shank_length, bf_Shank_Dia=shank_dia, 
                                    bf_Phillips_Bit_Depth=2.23269, bf_Cap_Head_Height=cap_height, bf_Cap_Head_Dia=cap_dia, 
                                    bf_Philips_Bit_Dia=3, bf_Thread_Length=thread_length, 
                                    bf_Major_Dia=major, bf_Pitch=pitch, bf_Minor_Dia=minor, 
                                bf_Crest_Percent=crest, bf_Root_Percent=root,  bf_Div_Count=div)
            bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            bolt = bpy.context.object
            bolt.location = local
            
        elif bit_type == 'mf_Bit_Allen':
            #Allen
            bpy.ops.mesh.bolt_add(align='WORLD', location=local, 
                                bf_Model_Type='bf_Model_Bolt', bf_Head_Type='bf_Head_Cap', bf_Bit_Type='bf_Bit_Allen', 
                                bf_Shank_Length=shank_length, bf_Shank_Dia=shank_dia, 
                                bf_Allen_Bit_Depth=2, bf_Allen_Bit_Flat_Distance=3, bf_Cap_Head_Height=cap_height, bf_Cap_Head_Dia=cap_dia, 
                                bf_Thread_Length=thread_length, 
                                bf_Major_Dia=major, bf_Pitch=pitch, bf_Minor_Dia=minor, 
                                bf_Crest_Percent=crest, bf_Root_Percent=root,  bf_Div_Count=div)
            bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
            bolt = bpy.context.object
            bolt.location = local
        return bolt

    def create_bolt(self, position,rotation=None,only_body=False):
        """[summary]
        create_bolt((0,0,0),(radians(45),'X'))
        """   
        bit_type = self.bit_type
        orientation = self.bolt_ortientation
        out_dia = self.BOLT_RAD



        # Check if only body should be created
        if only_body :
            out_length = 0.3
            z_in = position[2] + out_length/2 - 0.15

            part = self.create_ring((position[0],position[1],z_in),out_length, out_dia,0.2*out_dia)
            part.name = 'Bolt'

            if rotation:
                bpy.ops.object.select_all(action='DESELECT')
                part.select_set(True)
                bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
            return [part, None]

        else:
            self.bolt_position.append(position)
            out_length = self.BOLT_LENGTH

            in_dia = 0.8 * self.BOLT_RAD
            
            #Create Shell for Bolt
            
            cyl_shell = self.create_ring((position[0],position[1],position[2]-0.15), out_length, out_dia, 0.2)
            bpy.ops.mesh.primitive_cylinder_add(radius=self.BOLT_THREAD_DIA, depth=0.1, location=(position[0],position[1],position[2]-0.8))
            cyl_deck = bpy.context.object
            out_cyl = self.combine_all_obj(cyl_shell, [cyl_deck])
            out_cyl.name = 'out_cylinder'
            bpy.ops.object.select_all(action='DESELECT')
            ##################################### Bolt ######################################################################################################
            local = (position[0],position[1],position[2]+0.15)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.context.view_layer.objects.active = self.general_Bolt
            self.general_Bolt.select_set(True)  
            
            bpy.ops.object.duplicate(linked=0,mode='TRANSLATION') 
            bolt = bpy.context.object
            #bolt = self.general_Bolt.copy()
            #bolt.data = self.general_Bolt.data.copy()
            bolt.location = local
            #bolt = self.create_ring((0,0,0), 0.01, 0.01, 0.005)
            bolt.name = 'Bolt_'+str(self.bolt_num)
            self.bolt_num+=1
                       
            if self.color_render:
                self.rend_color(out_cyl,"Plastic")
                self.rend_color(bolt,"Bit")
                #self.rend_color(in_cyl,"Bit")
                #self.rend_color(thread,"Bit")


        # rotate the bit
        Angle = 0
        if orientation == 'mf_all_random':
            Angle = random.randrange(0, 360, 1) 
            bpy.ops.object.select_all(action='DESELECT')
            bolt.select_set(True)    
            bpy.ops.transform.rotate(value=radians(Angle),orient_axis='Z') 
        #rotate Bolt
        if rotation:
            bpy.ops.object.select_all(action='DESELECT')
            out_cyl.select_set(True)
            bolt.select_set(True)
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
            
            #bpy.ops.object.select_all(action='DESELECT')
            #out_cyl.select_set(True)
            #bolt.select_set(True)
            #bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1],orient_type='LOCAL')
            
        #print(Angle)
        if bit_type == 'mf_Bit_Slot':
            self.bolt_roate_angle_list.append(Angle%180)
        elif bit_type == 'mf_Bit_Torx':
            self.bolt_roate_angle_list.append(Angle%60)
        elif bit_type == 'mf_Bit_Cross':
            self.bolt_roate_angle_list.append(Angle%90)
        elif bit_type == 'mf_Bit_Allen':
            self.bolt_roate_angle_list.append(Angle%60)
        bolt["category_id"] = 4
        return [out_cyl,bolt]

    def rend_color(self, obj, part):
        """Rend color option. 

        Args:
            obj (bpy.type.Objects): Object to be colored
            part (str): Keyword for color rendering
        """

        mat = bpy.data.materials.new(name="Material")
        
        if part == "Metall":
            mat.metallic = 0.8
            mat.roughness = 0.4
            mat.diffuse_color = (0.3, 0.3, 0.3, 1)
            mat.specular_intensity = 0.9
        
        elif part == "Energy":
            mat.diffuse_color = (0.781, 0.775, 0.308, 1)
        
        elif part == "Plastic":
            mat.diffuse_color = (0, 0, 0, 1)
            mat.metallic = 0.4
            mat.specular_intensity = 0.5
            mat.roughness = 0.7

        elif part == "Bit":           
            mat.diffuse_color = (0.9, 0.9, 0.9, 1)
            mat.metallic = 0.9
            mat.specular_intensity = 0.7
            mat.roughness = 0.1

        # Assign it to object
        if obj.data.materials:
            # assign to 1st material slot
            obj.data.materials[0] = mat
        else:
            # no slots
            obj.data.materials.append(mat)
        bpy.context.view_layer.objects.active = None

    def rotate_object(self, object_rotate):
        """Rotate object after creation. Rotation will set by user

        Args:
            object_rotate (bpy.type.Objects): Object to be rotated
        """
        rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]
        if object_rotate is None:
            return
        x,y,z = object_rotate.location
        bpy.ops.object.select_all(action='DESELECT')
        object_rotate.select_set(True)
        #bpy.context.view_layer.objects.active = object_rotate
        if self.gear_orientation == 'r180' :
            nx,ny = self.rotate_around_point((0,0),180,(x,y))
            bpy.ops.transform.translate(value=(nx-x,ny-y,0))
            bpy.ops.transform.rotate(value=-radians(180),orient_axis=rotation[1])

        elif self.gear_orientation == 'r270' :
            nx,ny = self.rotate_around_point((0,0),-270,(x,y))
            bpy.ops.transform.translate(value=(nx-x,ny-y,0))
            bpy.ops.transform.rotate(value=-rotation[0],orient_axis=rotation[1])

        elif self.gear_orientation == 'r90' :
            nx,ny = self.rotate_around_point((0,0),-90,(x,y))
            bpy.ops.transform.translate(value=(nx-x,ny-y,0))
            bpy.ops.transform.rotate(value=-rotation[0],orient_axis=rotation[1])
            
        else:
            pass
        bpy.ops.object.select_all(action='DESELECT')
        self.flip_object(object_rotate)

    def flip_object(self, object_rotate):
        x,y,z = object_rotate.location
        bpy.ops.object.select_all(action='DESELECT')
        object_rotate.select_set(True)
        if self.gear_Flip : 
            if self.gear_orientation in ['r0','r180']:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, False, False))
                bpy.ops.transform.translate(value=(-2*x,0,0))
      
            else:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
                bpy.ops.transform.translate(value=(0,-2*y,0))
        bpy.ops.object.select_all(action='DESELECT')

    def init_key_list(self,factory):
        """Initiate key list for saving to csv

        Args:
            factory (bpy.types.Operator): Operator
        """
        #key_list = ["Nr."]
        motor_params = getattr(factory, "CsvParameters")
        key_list = ["Nr."] + motor_params + ["Bolts_Positions", "Bolt Angles", "Number of Bolts"]       
        self.key_list=key_list

    def init_csv(self,path, factory):
        """initiate csv file

        Args:
            path (str): 
            factory (bpy.types.Operator):
        """
        self.init_key_list(factory)
        with open(path, "a+", encoding='utf-8') as log:
            writer = csv.writer(log)
            writer.writerow(self.key_list)

    def write_data(self, path, data):
        """Write data into csv

        Args:
            path (str): 
            data (dict): 
            factory (bpy.types.Operator): 
        """

        csvdict = csv.DictReader(open(path, 'rt', encoding='utf-8', newline=''))
        dictrow = [row for row in csvdict if len(row) > 0 ]
        dictrow.append(data)
        with open(path, "w+", encoding='utf-8', newline='') as lloo:
            # lloo.write(new_a_buf.getvalue())
            wrier = csv.DictWriter(lloo, self.key_list)
            wrier.writeheader()
            for wowow in dictrow:
                wrier.writerow(wowow)

    def save_csv(self, factory):
        """Save csv file

        Args:
            factory (bpy.types.Operator): 
        """
        if self.save_path == "None":
            pass
        else:
            self.init_key_list(factory)

            csv_path= self.save_path + 'data.csv'
            if not os.path.isfile(csv_path):
                self.init_csv(csv_path, factory)                             
            data = self.create_data_list(factory)
            self.write_data(csv_path,data)

    def create_data_list(self, factory):
        """Create data list `

        Args:
            factory (bpy.types.Operator): 

        Returns:
            dict: Dictionary of parameter
        """
        data_list=['%04d'%self.id_Nr]
        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')

        for name in self.key_list[1:-3]:            
            if name in self.motor_param:
                value = str(getattr(factory,name))
                if pattern.match(value):
                    data_list.append('%.03f'%float(value))
                else:
                    data_list.append(value)

            else:
                data_list.append('-')
        data_list.append(self.out_bolt_position)
        data_list.append(self.bolt_roate_angle_list)
        data_list.append(len(self.out_bolt_position))
        data = dict(zip(self.key_list,data_list))
        return data

    def save_modell(self,modell, addtional = None):
        """Save model

        Args:
            modell (bpy.types.Objects): 
            addtional (bpy.types.Objects, optional): If other model should be saved in the same file. Defaults to None.
        """
        if self.save_path == "None":
            pass
        else:
            if modell is None:
                return  
            modell.data.name = modell.data.name[-3:]
            path_of_folder = self.save_path + "Motor_%04d/"%self.id_Nr
            bpy.ops.object.select_all(action='DESELECT')
            modell.select_set(True)
            if addtional:
                addtional.select_set(True)
            name = modell.name
            if self.color_render:
                if name == "Bolt" and os.path.isfile(path_of_folder+name+'.obj'):
                    return
                try:
                    bpy.ops.export_scene.obj(filepath=path_of_folder+name+'.obj', check_existing=True, use_selection=True, filter_glob='*.obj',)
                except:
                    print("Error!")
            else:
                if name == "Bolt" and os.path.isfile(path_of_folder+name+'.stl'):
                    return
                try:
                    bpy.ops.export_mesh.stl(filepath=path_of_folder+name+'.stl', check_existing=True, use_selection=True, filter_glob='*.stl',)
                except:
                    print("Error!")
            bpy.ops.object.select_all(action='DESELECT')

    def write_back(self,factory):
        pass
        
    def calculate_bolt_position(self):
        
        """Caculate bolts positions. The result form is a [3*2*n] list. Each bolt position will be represented as a vector [Top_position(x,y,z), Bottom_position(x,y,z)].
        E.g.: [
            #Bolt 1
            [
                [x1,y1,z1],
                [x2,y2,z2]
            ],
            #Bolt 2
            [
                [x3,y3,z3],
                [x4,y4,z4] 
            ],
            .....           
        ]

        Args:
            root_position (tuple): Position of oringin  which bolt shoud rotate around
        """

        x ,y, z = 0,0,0
        out_position=[]
        top_z =  1#self.BOLT_LENGTH/2 + 0.4 * self.BOLT_RAD + 0.8 * self.BOLT_RAD/3 + 0.2
        bottom_z = 0.7#self.BOLT_LENGTH/2

        # Bolts on "Bottom part"
        for position in  self.bolt_position[0:2]:
            top = [
                '%.03f'%round(position[0],3),
                '%.03f'%round(position[1],3),
                '%.03f'%round(position[2] - top_z,3)
            ]
            bottom = [
                '%.03f'%round(position[0],3),
                '%.03f'%round(position[1],3),
                '%.03f'%round(position[2] + bottom_z,3)
            ]
            out_position.append([top, bottom])
        
        for b_position in self.bolt_position[2:]:         
            x ,y, z = b_position
            
            # Calculate rotation
            if self.gear_orientation == 'r180' :
                x_new, y_new = self.rotate_around_point((0,0),180,(x ,y))
                if self.head_Type == "mf_Top_Type_A":
                    x_top = -x_new
                    x_bottom = -x_new
                    y_top =  -y_new  - top_z
                    y_bottom = -y_new + bottom_z
                elif self.head_Type == "mf_Top_Type_B":
                    x_top = -(x_new - top_z)
                    x_bottom = -(x_new + bottom_z)
                    y_top =  -y_new
                    y_bottom = -y_new
                                
            elif self.gear_orientation == 'r270' :
                x_new, y_new = self.rotate_around_point((0,0),-270,(x ,y))
                if self.head_Type == "mf_Top_Type_A":
                    x_top = x_new+ top_z
                    x_bottom = x_new- bottom_z
                    y_top =  y_new 
                    y_bottom = y_new 
                elif self.head_Type == "mf_Top_Type_B":
                    x_top = -x_new
                    x_bottom = -x_new
                    y_top =  -(y_new + top_z)
                    y_bottom = -(y_new - bottom_z )   

            elif self.gear_orientation == 'r90' :
                x_new, y_new = self.rotate_around_point((0,0),-90,(x ,y))
                if self.head_Type == "mf_Top_Type_A":
                    x_top = x_new - top_z
                    x_bottom = x_new + bottom_z
                    y_top =  y_new
                    y_bottom = y_new
                elif self.head_Type == "mf_Top_Type_B":
                    x_new, y_new = x, y
                    x_top = -x_new
                    x_bottom = -x_new
                    y_top =  -(y_new - top_z)
                    y_bottom = -(y_new + bottom_z)
                       
            elif self.gear_orientation == 'r0' :
                x_new, y_new = x, y
                if self.head_Type == "mf_Top_Type_A":    
                    x_top = x_new
                    x_bottom = x_new
                    y_top =  y_new - top_z
                    y_bottom = y_new + bottom_z
                elif self.head_Type == "mf_Top_Type_B":
                    x_top = x_new + top_z
                    x_bottom = x_new - bottom_z
                    y_top =  y_new 
                    y_bottom = y_new
                    
            # Caculate Flip                   
            if self.gear_Flip:
                if self.head_Type == "mf_Top_Type_A":
                    if self.gear_orientation in ['r0','r180']:
                        x_top = -x_top
                        x_bottom = -x_bottom
                    else:
                        y_top = -y_top
                        y_bottom = -y_bottom
                elif self.head_Type == "mf_Top_Type_B":
                    if self.gear_orientation in ['r0','r180']:
                        y_top = y_top
                        y_bottom = y_bottom
                    else: 
                        x_top = -x_top
                        x_bottom = -x_bottom  
                                                              
            top = ['%.03f'%x_top,
                    '%.03f'%y_top,
                    '%.03f'%z]
            bottom = ['%.03f'%x_bottom,
                        '%.03f'%y_bottom,
                        '%.03f'%z]  
     
            out_position.append([top, bottom])
        self.out_bolt_position = out_position

    def normal_gear(self,number,thickness):
        position = (0,0,0)
        ring_main =self.create_ring(position=position,height=1,radius=1.1, thickness=thickness)
        angle = 2*math.pi/number
        len_base = math.sin(angle/2)
        posi_x = math.cos(angle/2)
        teeth_list = []
        position_teeth = [position[0]-posi_x, position[1],position[2]]
        for i in range(number):
            teeth = self.create_teeth_mesh(position_teeth, 1, len_base)
            rotation_angle = i*angle
            r_x, r_y = self.rotate_around_point(position[:2], rotation_angle, teeth.location[:2])
            teeth.location.x = r_x
            teeth.location.y = r_y
            teeth.select_set(True)
            bpy.ops.transform.rotate(value=rotation_angle,orient_axis="Z")
            teeth_list.append(teeth)
            bpy.ops.object.select_all(action='DESELECT')
        internal_gear = self.combine_all_obj(ring_main, teeth_list)
        return internal_gear   

    def create_internal_gear(self, position, height, radius, number, thickness=0.5):
        internal_gear = self.normal_gear(number, thickness)
        bpy.ops.object.select_all(action='DESELECT')
        internal_gear.select_set(True)
        bpy.ops.transform.resize(value=(radius, radius, height))
        internal_gear.location = position
        return internal_gear   
    
    def create_teeth_mesh(self, position,height,len_base):
        x = position[0] 
        y = position[1]
        z = position[2] + height/2
        t_len = 2.3 *len_base
        len_up = len_base * 0.4
        p1x = x
        p1y = y + len_base
        p2x = x - t_len
        p2y = y + len_up
        p3x = x - t_len
        p3y = y - len_up
        p4x = x
        p4y = y - len_base
        
        verts =[
            [p1x, p1y, z],
            [p1x, p1y + len_base, z - height],
            [p2x, p2y, z],
            [p2x, p2y + len_base, z - height],
            [p3x, p3y,z],
            [p3x, p3y + len_base, z - height],
            [p4x, p4y, z],
            [p4x, p4y + len_base, z - height],
        ]
        
        faces = [
            [0,1,3,2],
            [2,3,5,4],
            [4,5,7,6],
            [6,7,1,0],
            [0,2,4,6],
            [1,3,5,7]
        ]
        
        obj = self.add_mesh('Teeth',verts, faces)
        return obj      

    def clear_bolt(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        bpy.context.view_layer.objects.active = self.general_Bolt
        self.general_Bolt.select_set(True)  
        bpy.ops.object.delete()
