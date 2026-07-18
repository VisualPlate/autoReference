# Auto reference  
Blender extension that inserts reference images automatically into scene collection of choosen axis and positions them into their correct positions in the workspace to safe time on adding references of objects

## Installation  
1. Download .ZIP file of this project on github (main branch)
2. Open Blender (version 4.2.0 or above),  
go to "Edit"-> "Preferences" -> "Get Extensions" -> "Install From Disk" -> Choose the .Zip File (autoReference-main.zip)

#### Notes
Do not unzip the .Zip, it wont work otherwise. Blender Extensions need .Zip file to attach them correctly into them

## Usage

1. Install the Extension and make sure you have version 4.2.0 or later
2. Click on "Add" -> "Image" -> "Add reference Image -> location" -> Select the position you want the image to be in. 

## Features
Automatise and safe time on adding reference images  
Free to use and edit  

## License
This project is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) License


# For Developers
If the scale, offset (or even rotation) isnt't correct, you can edit them at the start of AutoReference.py file

```python
reference_offset # Distance between World Origin and Reference Image
## Note that changing this will automatically change size (uniform scale) of the object

## To remove automatic scaling Remove this line of the code in row 70
empty.empty_display_size = reference_offset #auto size
```
```python
reference_scale # Uniform scale of the object. Has x, y and z axis
# Called like this
reference_scale['x']
reference_scale['y']
reference_scale['z']
```

## For Developers on linux
In cases you need to edit this script for your own purposes you can unzip the autoReference-main.zip file, edit the needed files and test a specific python file inside blender by running command like this
```bash
blender --python "file-path/Autoreference.py"
```