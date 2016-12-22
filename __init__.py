# BEGIN GPL BLOCK    
#    Blender Renderwatch monitors the status of the Render operation
#    Copyright (C) 2016  Mark Fitzgibbon
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
	"version":(1,0),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Render",
	"author":"ibbolia"
}
import bpy
import math
import mathutils
from math import radians

class Orbital:
	'''Orbital class contains variables and functions for positioning and rotating camera around a model
		'''
	def __init__(self):
		self.TT_FILEPATH_ROOT = "/tmp\\"
		self.TT_FILEPATH_ITERATOR = "1"
		self.TT_FILEPATH_EXT  =".png"
		self.TT_ANGLE_INCREMENTS = 90
		self.TT_POSITION = (0.0, -5.0, 0.0)	#Camera should be in front (Neg-Y) of model
		self.TT_TARGET_VIEW = (0.0, 0.0, 0.0)	#Default viewpoint to origin
		self.TT_ROTATION_X = 90.0
		self.TT_ROTATION_Y = 0.0
		self.TT_ROTATION_Z = 0.0
		self.TT_RADIUS = 0.0
		self.tt_origin = (0.0, 0.0, 0.0)

	def calculateRadius(self):
		rdSquared = math.pow((self.TT_POSITION[0] - self.tt_origin[0]), 2) + math.pow((self.TT_POSITION[1] - self.tt_origin[1]), 2)+ math.pow((self.TT_POSITION[2] - self.tt_origin[2]), 2)
		self.TT_RADIUS = math.sqrt(rdSquared)

	def setToFrontview(self, camera):
		'''sets camera of choice to a directly front view position (assuming "Front" is negative Y)
			camera -- Camera object to be positioned
			'''
		#Move camera front and center
		camera.location = self.TT_POSITION
		camera.rotation_euler = (radians(self.TT_ROTATION_X), 0.0, 0.0)
		#reposition camera to fit selected items
		bpy.ops.view3d.camera_to_view_selected()
		self.TT_POSITION = camera.location
		self.TT_RADIUS = camera.location[1]	#currently, Y coordinate == radius

	def renderOrbit(self, camera):
		'''Iterate tghrough radial steps and render at position
			camera -- Camera object to perform on
			'''
		while(self.TT_ROTATION_Z < 270):
			#Take render
			print("Camera at (" +str(self.TT_POSITION[0]) +"," + str(self.TT_POSITION[1]) +"," + str(self.TT_POSITION[2])  +")" )
			print("Camera heading: " + str(self.TT_ROTATION_Z))
			bpy.data.scenes['Scene'].render.filepath = self.TT_FILEPATH_ROOT + self.TT_FILEPATH_ITERATOR + self.TT_FILEPATH_EXT
			bpy.ops.render.render( write_still=True ) 
			self.TT_FILEPATH_ITERATOR = str(int(self.TT_FILEPATH_ITERATOR)+1)
			self.TT_ROTATION_Z = self.TT_ROTATION_Z + self.TT_ANGLE_INCREMENTS
			camera.rotation_euler = (radians(self.TT_ROTATION_X), 0.0, radians(self.TT_ROTATION_Z))
			#Set position
			self.TT_POSITION[0] = (self.TT_RADIUS * math.cos(radians(self.TT_ROTATION_Z+self.TT_ANGLE_INCREMENTS)))
			self.TT_POSITION[1] =  (self.TT_RADIUS * math.sin(radians(self.TT_ROTATION_Z+self.TT_ANGLE_INCREMENTS)))
			camera.location= mathutils.Vector(self.TT_POSITION)
			#bpy.ops.mesh.primitive_cube_add(location=self.TT_POSITION) 

class OrbitalOperator(bpy.types.Operator):
	'''Class to interface with blender python
		'''	
	bl_idname = "object.automatic_turntable"    #id name
	bl_label = "Orbit selected object and render"        #Display Label
	bl_options = {"REGISTER"}       #Possible operations

	def execute(self, context):
		obj_cam = bpy.data.objects["Camera"]
		orbit = Orbital()
		orbit.setToFrontview(obj_cam)
		orbit.renderOrbit(obj_cam)
		return {"FINISHED"}

def register():
	bpy.utils.register_class(OrbitalOperator)

def unregister():
	bpy.utils.unregister_class(OrbitalOperator)

if __name__ == "__main__":
	register()