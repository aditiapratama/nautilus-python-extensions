import os
from subprocess import call

from gi import require_version
from gi.repository import GObject, Nautilus

require_version("Gtk", "3.0")
require_version("Nautilus", "3.0")
# path to blender
context_menus = [
    ("/opt/blender/2.93/blender", "Blender 2.93"),
    ("/opt/blender/3.6/blender", "Blender 3.6"),
    ("/opt/blender/4.1.1/blender", "Blender 4.1.1"),
    ("/opt/blender/4.2/blender", "Blender 4.2"),
]
CMD = "alacritty -e "

# always create new window?
NEWWINDOW = True


class BlenderExtension(GObject.GObject, Nautilus.MenuProvider):
    def launch_blender(self, menu, path, file):
        command = f"{CMD} {path} '{file.get_location().get_path()}' &"
        print(command)
        call(command, shell=True)

    def get_file_items(self, window, files):
        if not files:
            return
        if ".blend" not in files[0].get_name():
            return
        file = files[0]
        menu_items = []
        for path, name in context_menus:
            item = Nautilus.MenuItem(
                name=f"BlenderMenuProvider::OpenWith{name}",
                label=f"Open with {name}",
                tip=f"Open {file.get_name()} with {name}",
            )
            item.connect("activate", self.launch_blender, path, file)
            menu_items.append(item)

        return menu_items
