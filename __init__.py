

bl_info = {
    "name": "Auto Reference Image Adder",
    "author": "Jere Tolonen",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Add > Image > Custom Submenu",
    "description": "Adds a reference image to specific locations using a file popup browser via a submenu",
    "category": "Object",
}

from .AutoReference import *