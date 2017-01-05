# BEGIN GPL BLOCK    
#    Batch renders around selection to create turntable frames
#    Copyright (C) 2017  Mark Fitzgibbon
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# END GPL BLOCK
bl_info = {
	"name":"Automatic Turntable",
	"description":"Automatically focus camera to rotate around a selected object in a scene",
	"version":(0,2),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Render",
	"author":"Mark Fitzgibbon"
}
import bpy

from . import BoundingBox, Orbital

class OrbitalOperator(bpy.types.Operator):
	'''Class to interface with blender python
		'''	
	bl_idname = "render.automatic_turntable"    #id name
	bl_label = "Orbit selected object and render"        #Display Label
	bl_options = {"REGISTER"}       #Possible operations

	def execute(self, context):
		print("Execute Script: Automatic Turntable")
		obj_cam = bpy.data.objects["Camera"]
		box = BoundingBox.BoundingBox(bpy.context.selected_objects)
		print("Box centered at: " + str(box.midpoint))
		orbit = Orbital.Orbital(box)
		orbit.setToFrontview(obj_cam)
		print("camera starting at: " + str(obj_cam.location))
		orbit.renderOrbit(obj_cam)
		print("End Script: Automatic Turntable")
		return {"FINISHED"}

def register():
	bpy.utils.register_class(OrbitalOperator)

def unregister():
	bpy.utils.unregister_class(OrbitalOperator)

if __name__ == "__main__":
	register()