bl_info = {
    "name": "Romaines Skin Importer",
    "category": "render",
}

import bpy
import urllib.request
import json
import base64

class SkinImporter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""

    bl_label = "Minecraft Skin Panel"
    bl_idname = "MATERIAL_PT_minecraft_skin"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    
    
    def get_skin(self, user):
        uuid_api = "https://api.mojang.com/users/profiles/minecraft/"
        with urllib.request.urlopen(uuid_api + user) as response:
            content = response.read().decode('utf-8')
        data = json.loads(content)
        uuid = data["id"]
        print(content)
        print(uuid)
        session_api = "https://sessionserver.mojang.com/session/minecraft/profile/"
        with urllib.request.urlopen(session_api + uuid) as response:
            content = response.read().decode('utf-8')
        data = json.loads(content)
        print(content)
        b64value = data["properties"][0]["value"]
        newdict = base64.decodebytes(b64value.encode('ascii')).decode('utf-8')
        decodedvalue = json.loads(newdict)
        print(decodedvalue)
        skin_url = decodedvalue["textures"]["SKIN"]["url"]
        print(skin_url)
        testfile = urllib.request
        testfile.urlretrieve(skin_url, user + "_skin.png" )
        bpy.data.images.load(user + "_skin.png")
        return skin_url

    def draw(self, context):
        props = context.scene.skin_props
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Player username:", icon='WORLD_DATA')

        row = layout.row()
        row.prop(props, "user", icon="VIEWZOOM", text="")

        row = layout.row()
        row.label(props.skin_url)
        
def user_update(self, context):
        sk = SkinImporter
        self.skin_url = sk.get_skin(self, self.user)

def register():
    global SkinProps
    sk = SkinImporter
    
    class SkinProps(bpy.types.PropertyGroup):
        user = bpy.props.StringProperty(name="Username",
            description="Type the name of the player whose skin you want",
            default="",
            update=user_update)
        skin_url = bpy.props.StringProperty(name="Skin Url",
            description="URL of the player's skin",
            default="")
    #bpy.utils.register_module(__name__)
    bpy.utils.register_class(SkinImporter)
    bpy.utils.register_class(SkinProps)
    bpy.types.Scene.skin_props = bpy.props.PointerProperty(type=SkinProps)

        


def unregister():
    bpy.utils.unregister_class(SkinImporter)


if __name__ == "__main__":
    register()