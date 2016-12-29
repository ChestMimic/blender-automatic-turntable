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
	"version":(0,2),
	"blender":(2,78,0),
	"support":"TESTING",
	"category":"Render",
	"author":"ibbolia"
}
import bpy
import math
import mathutils
from mathutils import Vector
from math import radians

from . import RadialPoints


class BoundingBox:
	def __init__(self, lst=[]):
		self.xMin = None
		self.xMax = None
		self.yMin = None
		self.yMax = None
		self.zMin = None
		self.zMax = None

		print("RUN")
		#Obtain bounding box in an object's local space
		for ob in lst:
			loc = ob.location
			for b in ob.bound_box:
				if self.xMax is None or ((Vector(b)[0] + ob.location[0]) > self.xMax):
					self.xMax = Vector(b)[0] + ob.location[0]
				if self.xMin is None or ((Vector(b)[0] + ob.location[0]) < self.xMin):
					self.xMin = Vector(b)[0] + ob.location[0]

				if self.yMax is None or ((Vector(b)[1] + ob.location[1]) > self.yMax) :
					self.yMax = Vector(b)[1] + ob.location[1]
				if self.yMin is None or ((Vector(b)[1] + ob.location[1]) < self.yMin):
					self.yMin = Vector(b)[1] + ob.location[1]

				if self.zMax is None or ((Vector(b)[2] + ob.location[2]) > self.zMax):
					self.zMax = Vector(b)[2] + ob.location[2]
				if self.zMin is None or ((Vector(b)[2] + ob.location[2]) < self.zMin):
					self.zMin = Vector(b)[2] + ob.location[2]

		self.xMid = (self.xMin + self.xMax)/2
		self.yMid = (self.yMin + self.yMax)/2
		self.zMid = (self.zMin + self.zMax)/2

		self.minimum = (self.xMin, self.yMin, self.zMin)
		self.maximum = (self.xMax, self.yMax, self.zMax)
		self.midpoint = (self.xMid, self.yMid, self.zMid)


class Orbital:
	'''Orbital class contains variables and functions for positioning and rotating camera around a model
		'''
	def __init__(self, box = None):
		self.TT_FILEPATH_ROOT = "/tmp\\"
		self.TT_FILEPATH_ITERATOR = "1"
		self.TT_FILEPATH_EXT  =".png"

		self.TT_ANGLE_INCREMENTS = 90
		self.TT_POSITION = (0.0, -5.0, 0.0)	#Camera should be in front (Neg-Y) of model

		self.TT_ROTATION_X = 90.0
		self.TT_ROTATION_Y = 0.0
		self.TT_ROTATION_Z = 0.0

		self.tt_orbit = RadialPoints.CircularPositioning()
		if box is not None:
			self.tt_orbit.tt_origin = box.midpoint 
		self.tt_iterations = 3

	def setToFrontview(self, camera):
		'''sets camera of choice to a directly front view position (assuming "Front" is theta=270 degrees)
			camera -- Camera object to be positioned
			'''
		#Move camera front and center
		camera.location = self.TT_POSITION
		camera.rotation_euler = (radians(self.TT_ROTATION_X), 0.0, 0.0)

		#reposition camera to fit selected items
		bpy.ops.view3d.camera_to_view_selected()
		camera.location = (camera.location[0], camera.location[1]+ (camera.location[1]*.1), camera.location[2])
		rads = self.tt_orbit.radiusToPoint(camera.location)
		self.tt_orbit.tt_circular_coords = [rads, 270]
		print("Orbiting around: " + str(self.tt_orbit.tt_origin) )

	def renderOrbit(self, camera):
		'''Iterate tghrough radial steps and render at position
			camera -- Camera object to perform on
			'''
		#Removes first render jitter
		sampPos = self.tt_orbit.getPointXYZ()
		camera.location= mathutils.Vector(sampPos)

		while(self.tt_iterations >0):
			#Take render
			#print("Iteration #" + str(self.tt_iterations))
			bpy.data.scenes['Scene'].render.filepath = self.TT_FILEPATH_ROOT + self.TT_FILEPATH_ITERATOR + self.TT_FILEPATH_EXT
			bpy.ops.render.render( write_still=True ) 

			#Rotate camera
			self.TT_FILEPATH_ITERATOR = str(int(self.TT_FILEPATH_ITERATOR)+1)
			self.TT_ROTATION_Z = self.TT_ROTATION_Z + self.TT_ANGLE_INCREMENTS
			camera.rotation_euler = (radians(self.TT_ROTATION_X), 0.0, radians(self.TT_ROTATION_Z))
			
			#Set camera position
			self.tt_orbit.addToAngle(self.TT_ANGLE_INCREMENTS)
			sampPos = self.tt_orbit.getPointXYZ()
			camera.location= mathutils.Vector(sampPos)
			self.tt_iterations -= 1
		

class OrbitalOperator(bpy.types.Operator):
	'''Class to interface with blender python
		'''	
	bl_idname = "render.automatic_turntable"    #id name
	bl_label = "Orbit selected object and render"        #Display Label
	bl_options = {"REGISTER"}       #Possible operations

	def execute(self, context):
		print("Execute Script: Automatic Turntable")
		obj_cam = bpy.data.objects["Camera"]
		box = BoundingBox(bpy.context.selected_objects)
		print("Box centered at: " + str(box.midpoint))
		orbit = Orbital(box)
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