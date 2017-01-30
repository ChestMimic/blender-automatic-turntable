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
	"version":(0,2,2),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Render",
	"author":"Mark Fitzgibbon"
}
import bpy
import mathutils
from math import radians

from bpy.props import IntProperty, FloatProperty, StringProperty

from . import BoundingBox, Orbital
from . import RadialPoints

addons_keymap = []

class Turntable:

	def __init__(self, iterations=1, increments=90, camera="", filepath="", position, cam_rot=(90, 0, 0)):
		self.iterations=iterations
		self.increments=increments
		self.camera=camera	#Object of camera (eg bpy.data.objects)
		self.filepath=filepath
		self.position=position
		self.camera_rotation = cam_rot
		pass

	def initializeCamera(self):
		#Activate requested camera
		if self.camera is not bpy.context.scene.camera.name:
			bpy.context.scene.camera = self.camera

	def renderCurrentPosition(self):
		bpy.data.scenes['Scene'].render.filepath = self.filepath
		bpy.ops.render.render( write_still=True )




class AutomaticTurntableOperator(bpy.types.Operator):
	"""docstring for AutomaticTurntableOperator"""
	bl_idname = "render.automatic_turntable"
	bl_label = "Automatic Turntable Renders"
	bl_options = {"REGISTER"}

	#Number of renders to take
	iterations = IntProperty(
		name= "Iterations",
		min = 1,
		default = 1)
	#Angle between iterations
	increments = FloatProperty(
		name ="Increments",
		min = 0,
		max = 360,
		default = 90
		)
	camera = StringProperty(
		name="Camera")
	filepath = StringProperty(
		name="File Path")

	def invoke(self, context, iterations, increments, camera):
		self.iterations = iterations
		self.increments = increments
		self.camera = camera
		return self.execute(context)

	def execute(self, context):
		
		box = BoundingBox.BoundingBox(bpy.context.selected_objects)
		ttb=Turntable(self.iterations, self.increments, bpy.data.objects[self.camera], self.filepath, box.midpoint)
		return {'FINISHED'}


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

class RenderMenu(bpy.types.Menu):
	bl_idname="Object_MT_automatic_turntable"
	bl_label="Automatic Turntable"

	def draw(self, context):
		layout = self.layout

		layout.operator("render.automatic_turntable", text = "Automatic Turntable")

def register():
	#bpy.utils.register_class(OrbitalOperator)
	bpy.utils.register_class(AutomaticTurntableOperator)
	bpy.utils.register_class(RenderMenu)

def unregister():
	#bpy.utils.unregister_class(OrbitalOperator)
	bpy.utils.unregister_class(AutomaticTurntableOperator)
	bpy.utils.unregister_class(RenderMenu)

if __name__ == "__main__":
	register()