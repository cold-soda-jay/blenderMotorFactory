import bpy
import math
import mathutils
import random
from math import radians


# Fixed value

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

#SMALL_GEAR_LENGTH = 2.5
#LARGE_GEAR_LENGTH = 1.8

orient_dict = {
    'mf_West':((radians(0),"Z"), BOTTOM_DIA,True),
    'mf_South':((radians(-90),"Z"),BOTTOM_HEIGHT,True),
    'mf_East':((radians(0),"Z"), BOTTOM_DIA,False),
    'mf_North':((radians(-90),"Z"),BOTTOM_HEIGHT,False)
}


# Definiert welchel operation gibt es

def combine_all_obj(main_obj,object_list):
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


def create_Bottom(factory):

    # TODO: Real size of the component

    init_x = factory.init_x
    init_y = factory.init_y
    init_z = factory.init_z

    size = 1
    main_hight = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_radius = SUB_BOTTOM_DIA * size
    sub_long = SUB_BOTTOM_LENGTH * size

    inner_radius = factory.mf_Sub_Bottom_Inner_Dia * size
    inner_long = SUB_BOTTOM_INNER_DEPTH * size

    # Add parts

    # Add main cylinder
    cylinder_r = main_width/2
    cylinder_d = main_long
    cylinder_x = init_x
    cylinder_y = init_y
    cylinder_z = init_z + cylinder_d/2 + sub_long    

    cyl = create_motor_main((cylinder_x, cylinder_y, cylinder_z),main_hight,main_width,main_long)
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


def create_middle(factory):

    # Hight: x achse
    # Width: y achse
    # Length/Long: z achse

    size = 1
    thickness = BOARD_THICKNESS
    bolt_orient = factory.mf_Bolt_Orientation

    main_hight = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_radius = SUB_BOTTOM_DIA * size
    sub_long = SUB_BOTTOM_LENGTH * size

    inner_radius = factory.mf_Sub_Bottom_Inner_Dia * size
    inner_long = SUB_BOTTOM_INNER_DEPTH * size

    bit_type = factory.mf_Bit_Type

    init_x = factory.init_x 
    init_y = factory.init_y
    init_z = factory.init_z 

    cuboid_long = thickness *size + BOLT_LENGTH
    ub_lx = init_x 
    ub_ly = init_y
    ub_lz = init_z+ sub_long+ main_long - thickness *size/2 + BOLT_LENGTH/2

    cube_1 = create_motor_main((ub_lx,ub_ly,ub_lz),main_hight,main_width,cuboid_long)

    cube_1.name = 'cube1'


    ##Part 2
    height = BOARD_THICKNESS
    width = 0.9 * main_width/2
    p2_length = BOLT_LENGTH/2

    x = init_x - main_hight/2 + height
    y = init_y - 0.2
    z = init_z + main_long + sub_long + p2_length

    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
    bpy.ops.transform.resize(value=(height, width, p2_length))

    cube_2 = bpy.context.object

    ##Part 3
    height = BOARD_THICKNESS
    width = 0.9 * main_width/2
    p3_length = BOLT_LENGTH/2

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
    bolt_x = init_x + main_hight/2 - BOLT_DIA
    bolt_y = init_y + main_width/2
    bolt_z = init_z+ sub_long+ main_long + BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
    rota=(radians(180), 'X')
    bolt_1 = create_bolt((bolt_x, bolt_y, bolt_z),rota,bit_type,orientation=bolt_orient)

    #Cereate  Bolt 2
    bolt_x = init_x - main_hight/2 + BOLT_DIA
    bolt_y = init_y - main_width/2
    bolt_z = init_z+ sub_long+ main_long + BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
    bolt_2 = create_bolt((bolt_x, bolt_y, bolt_z),rota,bit_type,orientation=bolt_orient)

    en_part = combine_all_obj(cube_1,[cube_2,cube_3,en_1,en_2,en_3,en_4,en_5,en_6,bolt_1,bolt_2])
    en_part.name = 'Energy Part'

   # bpy.context.view_layer.objects.active = en_part
    
    #bpy.ops.transform.rotate(value=radians(180),orient_axis="Z") 


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


def create_motor_main(position, height, width, length):

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


def create_4_convex_cyl(factory):

    #Four convex cylinder and side board

    init_x = factory.init_x
    init_y = factory.init_y 
    init_z = factory.init_z

    size = 1
    main_hight = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_long = SUB_BOTTOM_LENGTH * size


    #four_cyl_dia = 1.4/2
    step = 0.1

    four_cyl_z = main_long + sub_long
    

    cy1_z = C1_LENGTH/2
    cy2_z = (C1_LENGTH+C2_LENGTH)/2
    cy3_z = (C1_LENGTH+C2_LENGTH+C3_LENGTH)/2
    cy4_z = (C1_LENGTH+C2_LENGTH+C3_LENGTH+C4_LENGTH)/2
    #Create 4 Covex cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=FOUR_CYL_DIA, depth=C1_LENGTH, location=(0,0,four_cyl_z+cy1_z))
    cyl_1 = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(radius=FOUR_CYL_DIA - step, depth=C1_LENGTH+C2_LENGTH, location=(0,0,four_cyl_z+cy2_z))
    cyl_2 = bpy.context.object

    bpy.ops.mesh.primitive_cylinder_add(radius=FOUR_CYL_DIA- step *2, depth= C1_LENGTH+C2_LENGTH+C3_LENGTH, location=(0,0,four_cyl_z+cy3_z))
    cyl_3 = bpy.context.object

    bpy.ops.mesh.primitive_cylinder_add(radius=FOUR_CYL_DIA - step *3, depth=C1_LENGTH+C2_LENGTH+C3_LENGTH+C4_LENGTH, location=(0,0,four_cyl_z+cy4_z))
    cyl_4 = bpy.context.object
    
    

    up = combine_all_obj(cyl_1,[cyl_2,cyl_3,cyl_4])

    return up


def create_upper_part(factory):
    rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]
    up1 = create_up1(factory,length_relativ)
    up2 = create_up2(factory,length_relativ)
    board = create_side_board(factory)
    upper_part = combine_all_obj(up1,[up2,board])
    #bpy.ops.transform.translate(value=(0,-0.5,0))
    x,y,z = upper_part.location
    bpy.context.view_layer.objects.active = upper_part

    if factory.mf_Gear_Orientation == 'mf_West' :
        bpy.ops.transform.translate(value=(0,-2*y,0))
        #bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, mirror, False))
    elif factory.mf_Gear_Orientation == 'mf_North' :
        nx,ny = rotate_around_point((0,0),-90,(x,y))

        #upper_part.location = (n_x,n_y,z)
        bpy.ops.transform.translate(value=(-1.25,ny-y,0))
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, True, False))
    elif factory.mf_Gear_Orientation == 'mf_South' :
        nx,ny = rotate_around_point((0,0),90,(x,y))
        #upper_part.location = (n_x,n_y,z)
        bpy.ops.transform.translate(value=(-2.75,-y-ny,0))

        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1])
        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))

    
        #bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(mirror, False, False))

    
    return upper_part


def create_up1(factory,length_relativ):
    
    init_x = factory.init_x
    init_y = factory.init_y
    init_z = factory.init_z
    #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]


    size = 1
    main_height = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_long = SUB_BOTTOM_LENGTH * size

    small_gear_dia = factory.mf_Small_Gear_Dia
    small_gear_position = factory.mf_Small_Gear_Position
    large_gear_dia = factory.mf_Large_Gear_Dia

    #Create small gear
    x = init_x + small_gear_dia/2
    y = init_y - main_width/4
    z = main_long + sub_long + small_gear_position

    rotation_s = (radians(-90),"X")

    s_gear = create_gear(factory,(x,y,z),"small",length_relativ)

    #Create board
    width = 2.5
    height = BOARD_THICKNESS
    length = math.sqrt((x-FOUR_CYL_DIA)**2 +small_gear_position**2)

    x_board = FOUR_CYL_DIA + (x - FOUR_CYL_DIA)/2
    y_board = y + 0.5
    z_board = main_long + sub_long + (small_gear_position)/2

    angel = math.atan((x-FOUR_CYL_DIA)/small_gear_position)

   

    bpy.ops.mesh.primitive_cube_add(location=(x_board,y_board,z_board))
    bpy.ops.transform.resize(value=(height/2, width/2, length/2))
    cube_2 = bpy.context.object

    bpy.context.view_layer.objects.active = cube_2
    bpy.ops.transform.rotate(value=-angel,orient_axis='Y') 

    #Create large Gear
    x_large = init_x + small_gear_dia/2 - 0.8
    y_large = init_y - main_width/4 - length_relativ/6
    z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2
    rotation_l = (radians(-90),"X")

    l_gear = create_gear(factory,(x_large,y_large,z_large),"large",length_relativ)


    #extension_zone = create_extension_zone(factory,(x_large,y_large,z_large))
    up1 = combine_all_obj(s_gear,[cube_2,l_gear])
    bpy.context.view_layer.objects.active = up1

    if factory.mf_Gear_Orientation in ['mf_North','mf_South'] :
        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
        bpy.ops.transform.translate(value=(0,-length_relativ/3,0))


    return up1


def create_side_board(factory):
        #Create Side board
    init_x = factory.init_x
    init_y = factory.init_y
    init_z = factory.init_z
    #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]


    size = 1
    main_height = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_long = SUB_BOTTOM_LENGTH * size


    ##Part 1
    if factory.mf_Gear_Orientation in ['mf_West', 'mf_East'] :
        width = 0.9 * BOTTOM_DIA/2
    elif factory.mf_Gear_Orientation in ['mf_North', 'mf_South'] :
        width = 0.9 *BOTTOM_HEIGHT/2
    height = BOARD_THICKNESS
    p1_length = 2.4/2

    if factory.mf_Gear_Orientation in ['mf_West', 'mf_East'] :
        x = init_x - BOTTOM_HEIGHT/2 + BOARD_THICKNESS
        y = init_y - 2*BOARD_THICKNESS
        z = init_z + main_long + sub_long + BOLT_LENGTH + p1_length - BOLT_LENGTH/2
        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p1_length - BOLT_LENGTH/2 ))

    elif factory.mf_Gear_Orientation in ['mf_North', 'mf_South'] :
        x = init_x + 2*BOARD_THICKNESS
        y = init_y + BOTTOM_HEIGHT/2 - BOARD_THICKNESS
        z = init_z + main_long + sub_long + BOLT_LENGTH + p1_length - BOLT_LENGTH/2

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(width, height, p1_length - BOLT_LENGTH/2 ))
       

   

    board_1 = bpy.context.object

    ##Part 2

    z = init_z + main_long + sub_long + p1_length*2 + (C1_LENGTH+C2_LENGTH+C3_LENGTH - p1_length*2 )/2

    if factory.mf_Gear_Orientation in ['mf_West', 'mf_East'] :
        x = init_x - BOTTOM_HEIGHT/4 + BOARD_THICKNESS
        p2_length = math.sqrt((C1_LENGTH+C2_LENGTH+C3_LENGTH-p1_length*2)**2 + (main_height/2)**2 )/2
        angel = math.atan((main_height/2)/(C1_LENGTH+C2_LENGTH+C3_LENGTH - p1_length*2))
        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p2_length))
        board_2 = bpy.context.object
        bpy.context.view_layer.objects.active = board_2
        bpy.ops.transform.rotate(value=-angel,orient_axis='Y') 
    elif factory.mf_Gear_Orientation in ['mf_North', 'mf_South'] :
        y = init_y + BOTTOM_HEIGHT/4 - BOARD_THICKNESS
        p2_length = math.sqrt((C1_LENGTH+C2_LENGTH+C3_LENGTH-p1_length*2)**2 + (main_height/2)**2 )/2
        angel = math.atan((main_height/2)/(C1_LENGTH+C2_LENGTH+C3_LENGTH - p1_length*2))

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(width, height, p2_length))

        board_2 = bpy.context.object

        bpy.context.view_layer.objects.active = board_2
        bpy.ops.transform.rotate(value=-angel,orient_axis='X') 
    #cube_2.matrix_world @= Matrix.Rotation(radians(angel),4,'Y') 

    board = combine_all_obj(board_1,[board_2])

    return board


def create_up2(factory,length_relativ):

    #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]

    init_x = factory.init_x
    init_y = factory.init_y
    init_z = factory.init_z

    size = 1
    main_height = BOTTOM_HEIGHT * size
    main_width = BOTTOM_DIA * size
    main_long = factory.mf_Bottom_Length * size

    sub_long = SUB_BOTTOM_LENGTH * size

    small_gear_dia = factory.mf_Small_Gear_Dia
    small_gear_position = factory.mf_Small_Gear_Position
    large_gear_dia = factory.mf_Large_Gear_Dia

    #Create small gear
    x = init_x + small_gear_dia/2
    y = init_y - main_width/4 - length_relativ/3 - 0.15
    z = main_long + sub_long + small_gear_position

    rotation_s = (radians(-90),"X")

    s_gear = create_gear(factory,(x,y,z),"small",length_relativ,extension_zone=True)


    #Create large Gear
    x_large = init_x + small_gear_dia/2 - 0.8
    y_large = init_y - main_width/4 - length_relativ/6 - length_relativ/6 - 0.15
    z_large = main_long + sub_long + small_gear_position + large_gear_dia/2 + 0.2
    rotation_l = (radians(-90),"X")

    l_gear = create_gear(factory,(x_large,y_large,z_large),"large",length_relativ,extension_zone=True)

    gears = combine_all_obj(s_gear,[l_gear])

    if factory.mf_Gear_Orientation in ['mf_North','mf_South'] :
        bpy.context.view_layer.objects.active = gears

        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
        bpy.ops.transform.translate(value=(0,1.25,0))

        
    extension_zone = create_extension_zone(factory,(x_large,y_large,z_large),0.3)
    if factory.mf_Gear_Orientation in ['mf_North','mf_South'] :
        bpy.context.view_layer.objects.active = extension_zone
        bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, True, False))
        bpy.ops.transform.translate(value=(5.5/2-0.65+0.3, -length_relativ+0.05,0))
       # bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))

    #else:
     #   extension_zone = create_extension_zone(factory,(x_large,y_large,z_large),0.3)


    up2 = combine_all_obj(gears,[extension_zone])
    return up2


def create_extension_zone(factory,large_gear_position,gear_length):

    small_gear_dia = factory.mf_Small_Gear_Dia
    small_gear_position = factory.mf_Small_Gear_Position
    large_gear_dia = factory.mf_Large_Gear_Dia
    s_length_1 = 2.9/2
    s_length_2 = 5.5
    s_length_3 = 1.5
    s_length_4 = 4.5
    s_length_6 = 3

    if factory.mf_Type == 'mf_Type_B':
        angle_1 = 15
        angle_2 = 0
        s_length_5 = 3.5
    elif factory.mf_Type == 'mf_Type_A':
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

    board_1 = add_mesh("board_1", verts_b1, faces_b1)

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
    board_2 = add_mesh("board_2", verts_b2, faces_b2)

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
    bottom_board = add_mesh("bottom board", verts_bottom, faces_bottom)


    #Create end cylinder
    if factory.mf_Type == 'mf_Type_B':
        dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)/3
        x_cyl_1 = p5x - (p5x - p6x)*5/6
        y_cyl_1 = (y - 0.8)
        z_cyl_1 = p6z - (p6z -p5z)/3 
        end_cly_1 = create_ring((x_cyl_1,y_cyl_1 - 0.5,z_cyl_1), 2.6, dia/2, 0.5)
        end_cly_1.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        end_cly_1.name = 'End_cylinder'
        
        x_cyl_2 = p5x - (p5x - p6x)/6
        y_cyl_2 = (y - 0.8)
        z_cyl_2 = p6z - (p6z -p5z)*2/3 
        end_cly_2 = create_ring((x_cyl_2,y_cyl_2 - 0.5,z_cyl_2), 2.6, dia/2, 0.5)
        end_cly_2.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        end_cly_2.name = 'End_cylinder'

        board = combine_all_obj(bottom_board,[board_1, board_2,end_cly_1,end_cly_2])

        bevel = board.modifiers.new(name='bevel', type='BEVEL')
        
        bevel.affect = 'EDGES'
        bevel.angle_limit = 100
        bevel.offset_type = 'WIDTH'
        bevel.width = 1000000
        bpy.context.view_layer.objects.active = board
        res = bpy.ops.object.modifier_apply(modifier='bevel')

    elif factory.mf_Type == 'mf_Type_A':

        dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)
        x_cyl = p5x - (p5x - p6x)/2 
        y_cyl = (y - 0.8)
        z_cyl = p6z - (p6z -p5z)/2 
        end_cly = create_ring((x_cyl,y_cyl,z_cyl), 1.6, dia/2, 0.5)
        end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        end_cly.name = 'End_cylinder'
        board = combine_all_obj(bottom_board,[board_1, board_2,end_cly])

        bevel = board.modifiers.new(name='bevel', type='BEVEL')
        
        bevel.affect = 'EDGES'
        bevel.angle_limit = 100
        bevel.offset_type = 'WIDTH'
        bevel.width = 1000000
        bpy.context.view_layer.objects.active = board
        res = bpy.ops.object.modifier_apply(modifier='bevel')

    #bpy.ops.mesh.bevel(offset_type='OFFSET', offset=10.0, affect ='EDGES')

    return board


def create_bolt(position,rotation=None,bit_type=None,orientation='mf_all_same',only_body=None):
    """[summary]
    create_bolt((0,0,0),(radians(45),'X'))
    """    
    out_dia = BOLT_DIA
    if only_body :
        out_length = only_body
        z_in = position[2] + out_length/2 - 0.15

        part = create_ring((position[0],position[1],z_in),out_length,BOLT_DIA,0.2*BOLT_DIA)
        part.name = 'Bolt'

    else:
        out_length = BOLT_LENGTH

        in_dia = 0.8 * BOLT_DIA
        
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
            bit = add_torx((position[0],position[1],z_sphe+ in_dia),in_dia*1.5,0.2)
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


        part = combine_all_obj(out_cyl,[sphere,in_cyl])
        part.name = 'Bolt'

    if orientation == 'mf_all_random':
        angel = random.randrange(0, 360, 10)     
        bpy.context.view_layer.objects.active = part
        bpy.ops.transform.rotate(value=radians(angel),orient_axis='Z') 
    if rotation:
        bpy.context.view_layer.objects.active = part
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 

    return part


def create_gear(factory,position,gear_type,info,extension_zone = False):
    bit_type = factory.mf_Bit_Type
    bolt_orient = factory.mf_Bolt_Orientation
    rotation = (radians(-90),"X")
    length_relativ = info
    #orient_dict[factory.mf_Gear_Orientation]
    if gear_type == 'small':
        radius = factory.mf_Small_Gear_Dia/2
        if extension_zone:
            length = 0.3
        else:
            length = length_relativ*2/3
        inner_radius = 1/2
        inner_length = 1.4 * length +1
        angel = factory.mf_Small_Gear_Bolt_Angel  * 10
        bolt_position_angel = factory.mf_Small_Gear_Bolt_Rotation * 10
        if factory.mf_Gear_Orientation in ['mf_East','mf_West'] and factory.mf_Type == 'mf_Type_B':
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
            z_bolt_init = position[2] + length/2 - BOLT_LENGTH/2 + 0.3
        #Init position
        x_bolt_init = position[0]+ radius + 0.9*BOLT_DIA
        y_bolt_init = position[1] 
        #z_bolt_init = position[2] + length/2 - BOLT_LENGTH/2
        #Calculate the rotation
        x_bolt_1,y_bolt_1 = rotate_around_point((position[0],position[1]),bolt_position_angel,(x_bolt_init,y_bolt_init))
        x_bolt_2,y_bolt_2 = rotate_around_point((position[0],position[1]),bolt_position_angel+angel,(x_bolt_init,y_bolt_init))       
        bolt_1 = create_bolt((x_bolt_1,y_bolt_1,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)
        bolt_2 = create_bolt((x_bolt_2, y_bolt_2,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)       
        part = combine_all_obj(out_cyl,[in_cyl,bolt_1,bolt_2])
        bpy.context.view_layer.objects.active = part
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
    
        return part
    elif gear_type == 'large':

        radius = factory.mf_Large_Gear_Dia/2
        if extension_zone:
            length = 0.3
        else:
            length = length_relativ/3
        inner_radius_1 = 1.6/2
        inner_radius_2 = 1.3/2
        inner_radius_3 = 2.9/2
        

        inner_length = length + 1
        angel = factory.mf_Large_Gear_Bolt_Angel * 10
        bolt_position_angel = factory.mf_Large_Gear_Bolt_Rotation * 10
        
        #Ring 1

        thickness_1 = radius - inner_radius_1
        cly_1 = create_ring(position,length,radius,thickness_1)

        #Ring 2
        x = position[0]
        y = position[1]
        z = position[2] - 0.3
        position_in = (x,y,z)

        thickness_2 = inner_radius_1 - inner_radius_2
        cly_2 = create_ring(position_in,inner_length,inner_radius_1,thickness_2)

        #Ring 3
        x = position[0]
        y = position[1]
        z = position[2] + 0.1
        position_3 = (x,y,z)

        thickness_3 = 0.2
        cly_3 = create_ring(position_3,length+0.3,inner_radius_3,thickness_3)

        if extension_zone:
            body = length
            z_bolt_init = position[2]
        else:
            body = None
            z_bolt_init = position[2] + length/2 - BOLT_LENGTH/2 + 0.3
        #Init position
        x_bolt_init = position[0]+ radius + 0.9*BOLT_DIA
        y_bolt_init = position[1] 
        #z_bolt_init = position[2] + length/2 - BOLT_LENGTH/2
        #Calculate the rotation
        x_bolt_1,y_bolt_1 = rotate_around_point((position[0],position[1]),bolt_position_angel,(x_bolt_init,y_bolt_init))
        x_bolt_2,y_bolt_2 = rotate_around_point((position[0],position[1]),bolt_position_angel+angel,(x_bolt_init,y_bolt_init))       
        bolt_1 = create_bolt((x_bolt_1,y_bolt_1,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)
        bolt_2 = create_bolt((x_bolt_2, y_bolt_2,z_bolt_init),bit_type=bit_type,orientation=bolt_orient,only_body=body)       
        part = combine_all_obj(cly_1,[cly_2,cly_3,bolt_1,bolt_2])
        bpy.context.view_layer.objects.active = part
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
    
        return part


def rotate_around_point(origin,angel,obj_position):
    rot = radians(angel)   
    relativ_point = [obj_position[0]-origin[0], obj_position[1]-origin[1]]
    x = relativ_point[0] * math.cos(rot) - relativ_point[1] * math.sin(rot) 
    y = relativ_point[0] * math.sin(rot)  + relativ_point[1] * math.cos(rot)
    return x+origin[0],y+origin[1]


def create_ring(position,height,radius,thickness,rotation=None):

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


def create_triangle(position,thickness,length,towards=None):
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

    obj = add_mesh("triangle", verts, faces)
    return obj


def add_mesh(name, verts, faces, edges=None, col_name="Collection"):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)
    return obj


def add_torx(position,size,depth):
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
        add_vector(position, v1),
        add_vector(position, v2),
        add_vector(position, v3),
        add_vector(position, v4),
        add_vector(position, v5),
        add_vector(position, v6),
        add_vector(position, v1,minus=1),
        add_vector(position, v2,minus=1),
        add_vector(position, v3,minus=1),
        add_vector(position, v4,minus=1),
        add_vector(position, v5,minus=1),
        add_vector(position, v6,minus=1),

        add_vector(position, v1, height=depth),
        add_vector(position, v2, height=depth),
        add_vector(position, v3, height=depth),
        add_vector(position, v4, height=depth),
        add_vector(position, v5, height=depth),
        add_vector(position, v6, height=depth),
        add_vector(position, v1,minus=1, height=depth),
        add_vector(position, v2,minus=1, height=depth),
        add_vector(position, v3,minus=1, height=depth),
        add_vector(position, v4,minus=1, height=depth),
        add_vector(position, v5,minus=1, height=depth),
        add_vector(position, v6,minus=1, height=depth),
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
    
    obj = add_mesh("torx", verts, faces)
    return obj


def sub_obj(domain, slave):
    boolean = domain.modifiers.new('boolean', 'BOOLEAN')
    boolean.operation = 'DIFFERENCE'
    boolean.object = slave
    bpy.context.view_layer.objects.active = domain
    res = bpy.ops.object.modifier_apply(modifier='boolean')
    return res


def add_vector(v1,v2,minus=0,height=0):
    out = []
    for i in range(len(v1)):
        if minus == 1:
            out.append(v1[i]-v2[i])
        else:
            out.append(v1[i]+v2[i])
    if height != 0:
        out[-1] -= height
    return out
    