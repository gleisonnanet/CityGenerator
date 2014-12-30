import bpy
import os

def load_all(scene):
    """Load all the needed resources."""
    load_texture("vert_road")
    load_texture("hor_road")
    load_texture("crossroads")
    load_texture("pavement_regular")
    load_texture("pavement_nrm")
    load_object("traffic_lights", scene)


def load_texture(oname):
    """Append a texture."""
    
    # load texture iff not already existant
    if oname not in bpy.data.textures.keys():
        load("Texture", oname)


def load_object(oname, scene):
    """Append an object."""
    
    # load object iff not already existant
    if oname not in bpy.data.objects.keys():
        load("Object", oname)
        bpy.context.scene.objects.unlink(bpy.data.objects[oname])


def load(ofolder, oname):
    """Append an element based on a resource in blender ;
    ofolder is the subfolder in the blender file, oname is the
    object name"""
    
    # append the resource
    s = os.sep
    opath = "//resources.blend\\{}\\{}".format(ofolder, oname)
    dpath = bpy.utils.script_paths()[1] + \
        ("{0}addons{0}city_generator{0}resources{0}resources.blend" + 
        "\\{1}\\").format(s, ofolder)
    
    bpy.ops.wm.link_append(filepath=opath,
                           filename=oname,
                           directory=dpath,
                           filemode=1,
                           link=False,
                           relative_path=True,
                           active_layer=True)