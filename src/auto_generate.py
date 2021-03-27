import bpy
import random

def generate_param():
    MotorParameters = {
            "mf_Top_Type" : random.choice(["mf_Top_Type_A","mf_Top_Type_B"]),
            "mf_Extension_Type_A" : random.choice(["mf_Extension_Type_1","mf_Extension_Type_2", "mf_None"]),
            "mf_Extension_Type_B" : random.choice(["mf_Extension_Type_1","mf_None"]),
            "mf_Gear_Orientation_1" : random.choice(['r0','r90', 'r180','r270']),
            "mf_Gear_Orientation_2" : random.choice(['r90', 'r180','r270']),
            "mf_Flip" : random.choice([True,False]),
            "mf_Color_Render" : False,
            "mf_Bottom_Length" : random.uniform(4, 8),
            "mf_Sub_Bottom_Length" : random.uniform(0.6, 2),

            "mf_Lower_Gear_Dia": random.uniform(3.5, 4.5),
            "mf_Lower_Gear_Position": random.uniform( 3.6, 4.2),
            "mf_Lower_Gear_Bolt_Random" : False,
            "mf_Lower_Gear_Bolt_Position_1": random.uniform(190,230),
            "mf_Lower_Gear_Bolt_Position_2": random.uniform(320,350),            
            
            "mf_Gear_Bolt_Random_B": True,
            "mf_Gear_Bolt_Nummber_B" : str(random.randrange(2, 3)),
            "mf_Type_B_Height_1" : random.uniform(6.3, 8),
            "mf_Type_B_Height_2" : random.uniform(2, 6),
            "mf_Gear_Bolt_Right_B" : random.uniform(1.7,4),
                        
            "mf_Upper_Gear_Dia": random.uniform(5, 6.5),
            "mf_Upper_Bolt_Nummber": str(random.randrange(1, 3)),
            "mf_Upper_Gear_Bolt_Random" : True,

            "mf_Bit_Type" : random.choice(['mf_Bit_Torx','mf_Bit_Slot','mf_Bit_Cross']),
            "mf_Bolt_Orientation": "mf_all_random",
            }
    return MotorParameters

def create_motor(number: int, **data):
    for i in range(number):
        param = generate_param()
        for key, value in data.items():
            param[key] = value
        motor = bpy.ops.mesh.add_motor(**param)
            
        
            
if __name__ == "__main__":
    # Change this value to set how many models should be generated 
    num = 15
    data = {}
    # Set parameter that should be manuelly modified
    data['save_path']="D:/blender_tests/" # Add other param like this
    create_motor(num, **data)   
               
        
