# Blender Motor Factory

This is an blender addon which can create motor. We parameterized many features of a motor and so user can generate various model in same type but different parameters.

This addon only support [blender version 2.90.1](https://download.blender.org/release/Blender2.90/). Other version may cause unpredictable falier.

## 1. Installation

1. Download the project via ``git clone https://github.com/cold-soda-jay/blenderMotorFactory.git`` or download zip file from realese.
2. In Blender, go *Edit > Preference > Install* and find the file **Add Motor.zip**. Make sure it is activated.
3. Now you can find it in *Add >Mesh*

## 2. Advanced

### 2.1 Save model

This Addon allow user generate various model and save the parameter as well as model as .stl file. To save the model, you can run the command in blender Console (**Shift + F4** to open it): 
``bpy.ops.mesh.add_motor(save_path="Path of folder")``

The model will be saved as a whole entity and seperate parts

<div align="left"><img src="pic\saved_file.png" alt="Image" style="zoom:0%;" /></div>

<div align="center"><img src="pic\parts_model.png" alt="Image" style="zoom:80%;" /></div>

#### Save Model in Blender

When you modified some motor manuelly and want to save the model and property value part by part, you can choose **Save the model** and then give the loaction where you want to save the model. Then the model you created will be saved.

<div align="center"><img src="pic/save.png" alt="Image" style="zoom:0%;" /></div>

### 2.2 CSV data

The parameters of generated model will be saved into a csv file when ``save_path`` setted. Every model will be saved in a separate folder with a number as name. This number represent the Id of the model. The parameters of this model can be found in csv file. 

 

#### Bolt Positions

The position of all bolts will also be saved as a list in the file. The order of bolt position is from bottom to top.

<div align="center"><img src="pic/bolts.png" alt="Image" style="zoom:80%;" /></div>

Every bolt will have a vector to store its position and orientation. In CSV the last colum stores all bolts positions. The result is a [3\*2\*n] list. Each bolt position will be represented as a vector [
    Top_position(x,y,z), 
    Bottom_position(x,y,z)
].
>      E.g.: [
>            #Bolt 1
>            [
>                [x1,y1,z1],
>                [x2,y2,z2]
>            ],
>            #Bolt 2
>            [
>                [x3,y3,z3],
>                [x4,y4,z4] 
>            ],
>            .....           
>        ] 


### 2.3 Auto generation


To generate more models at once, you can use script ``./src/auto_generate.py``. In the script you can set the number of generated models and define several parameters when generating. Here are all parameters:

```python

[
"mf_Head_Type", 
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

"mf_Gear_Bolt_Random_B",
"mf_Gear_Bolt_Nummber_B",
"mf_Gear_Bolt_Position_B_1",
"mf_Gear_Bolt_Position_B_2",
"mf_Gear_Bolt_Position_B_3",
"mf_Gear_Bolt_Right_B",

"mf_Upper_Bolt_Nummber",
"mf_Upper_Gear_Bolt_Random",
"mf_Upper_Gear_Bolt_Position_1",
"mf_Upper_Gear_Bolt_Position_2",
"mf_Upper_Gear_Bolt_Position_3",

"mf_Type_B_Height_1",
"mf_Type_B_Height_2",

"save_path",

]
```

After setting the parameters, you can runthe script in command line with following command:

```
path/of/blender -b -P path/of/auto_generate.py 1> nul
```

See more details in `auto_generate.py`
