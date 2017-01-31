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

	def __init__(self, camera, filepath="//render_out",iterations=1, increments=90,  position=(0,0, 0), cam_rot=(90, 0, 0)):
		self.iterations=iterations
		self.increments=increments
		self.camera=camera	#Object of camera (eg bpy.data.objects)
		self.filepath=filepath
		self.position=position	#Camera XYZ position
		self.camera_rotation = cam_rot

		#Set target center
		box = BoundingBox.BoundingBox(bpy.context.selected_objects)
		self.orbit = RadialPoints.CircularPositioning(box.midpoint)

		#Set target radius
		radius = max(box.maximum[0] - box.midpoint[0], box.maximum[1]-box.midpoint[1]) #Largest of either X or Y value
		self.orbit.tt_circular_coords = [radius, 270]	#Angle 270 should translate to a Front view

		#List of all camera position/rotation comos in order
		self.camera_atlas = []
		flag = self.iterations
		while(flag > 0):
			posit = self.orbit.getPointXYZ()	#Location of camera
			rotat = (radians(self.camera_rotation[0]), radians(self.camera_rotation[1]), radians(self.camera_rotation[2]))
			self.camera_atlas.append([posit, rotat])
			self.orbit.addToAngle(self.increments)
			self.camera_rotation = (self.camera_rotation[0], self.camera_rotation[1], self.camera_rotation[2] + increments)
			flag -= 1

	def initializeCamera(self):
		#Activate requested camera if it isn't
		if self.camera is not bpy.context.scene.camera:
			bpy.context.scene.camera = self.camera

	def renderCurrentPosition(self):
		bpy.data.scenes['Scene'].render.filepath = self.filepath
		bpy.ops.render.render( write_still=True )

	def setToIndexAndRender(self, index = 0):
		#Set position and rotation of camera to position on list at index
		self.camera.location = mathutils.Vector(self.camera_atlas[index][0])
		self.camera.rotation_euler = self.camera_atlas[index][1]

		self.renderCurrentPosition()

	def renderAllPositions(self):
		self.initializeCamera()
		index = 0
		for cpos in self.camera_atlas:
			self.setToIndexAndRender(index)
			index += 1



class AutomaticTurntableOperator(bpy.types.Operator):
	"""docstring for AutomaticTurntableOperator"""
	bl_idname = "render.automatic_turntable"
	bl_label = "Automatic Turntable Renders"
	bl_options = {'REGISTER', 'UNDO'}

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

	def invoke(self, context, event):
		#self.iterations = iterations
		#self.increments = increments
		#self.camera = camera
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		
		box = BoundingBox.BoundingBox(bpy.context.selected_objects)
		ttb=Turntable(bpy.data.objects[self.camera], self.filepath, self.iterations, self.increments,  box.midpoint)
		ttb.renderAllPositions()
		return {'FINISHED'}


class OrbitalOperator(bpy.types.Operator):
	'''Class to interface with blender python
		'''	
	bl_idname = "render.automatic_turntable"    #id name
	bl_label = "Orbit selected object and render"        #Display Label
	bl_options = {'REGISTER', 'UNDO'}       #Possible operations

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